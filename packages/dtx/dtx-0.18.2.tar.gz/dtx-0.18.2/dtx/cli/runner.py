# result_collector.py
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field

from dtx.config import globals
from dtx.core.engine.evaluator import EvaluatorRouter
from dtx.core.engine.scanner import EngineConfig, MultiTurnScanner
from dtx.core.models.analysis import RedTeamPlan
from dtx.core.models.results import EvalReport
from dtx.core.models.tactic import PromptMutationTactic
from dtx.plugins.providers.base.agent import BaseAgent

from .console_output import BaseResultCollector


class TestRunInput(BaseModel):
    agent_type: str
    url: Optional[str] = ""
    max_prompts: int = 1000000
    override_tactics: List[str] = Field(default_factory=list)


class RedTeamTestRunner:
    def __init__(self, config: TestRunInput):
        self.config = config
        self.report: Optional[EvalReport] = None

    def run(
        self, plan: RedTeamPlan, agent: BaseAgent, collector: BaseResultCollector
    ) -> EvalReport:
        scope = plan.scope

        tactics = [
            PromptMutationTactic(name=t) for t in self.config.override_tactics
        ] or scope.redteam.tactics

        # Get the global evaluator from red team plan
        if scope.redteam.global_evaluator:
            global_evaluator = scope.redteam.global_evaluator.evaluation_method
        else:
            preferred_evaluator = agent.get_preferred_evaluator()
            if preferred_evaluator:
                global_evaluator = preferred_evaluator.evaluation_method
            else:
                global_evaluator = None

        config = EngineConfig(
            evaluator_router=EvaluatorRouter(
                model_eval_factory=globals.get_eval_factory()
            ),
            test_suites=plan.test_suites,
            tactics_repo=globals.get_tactics_repo(),
            tactics=tactics,
            global_evaluator=global_evaluator,
            max_per_tactic=scope.redteam.max_prompts_per_tactic,
        )

        scanner = MultiTurnScanner(config)

        for result in scanner.scan(agent, max_prompts=self.config.max_prompts):
            collector.add_result(result)

        collector.finalize()

        self.report = EvalReport(
            scope=plan.scope,
            eval_results=collector.results if hasattr(collector, "results") else [],
        )
        return self.report

    def save_yaml(self, path: str):
        if not self.report:
            raise ValueError("Run must be called before saving.")
        yaml_data = yaml.dump(self.report.model_dump(), default_flow_style=False)
        with open(path, "w") as file:
            file.write(yaml_data)

    def save_json(self, path: str):
        if not self.report:
            raise ValueError("Run must be called before saving.")
        json_data = self.report.model_dump_json(indent=2)
        with open(path, "w") as file:
            file.write(json_data)

from typing import Optional

import yaml
from pydantic import BaseModel

from dtx.config import globals
from dtx.core.models.analysis import PromptDataset, RedTeamPlan, TestSuitePrompts
from dtx.core.models.scope import RedTeamScope
from dtx.plugins.redteam.dataset.hf.analysis import AppRiskAnalysis_HF
from dtx.plugins.redteam.dataset.hf.generator import HFDataset_PromptsGenerator
from dtx.plugins.redteam.dataset.stargazer.generator import (
    Stargazer_PromptsGenerator,
)
from dtx.plugins.redteam.dataset.stingray.generator import (
    Stringray_PromptsGenerator,
)
from dtx.threat_model.analysis import AppRiskAnalysis, AppRiskAnalysisModelChain
from dtx.threat_model.analysis_sr import (
    AppRiskAnalysis_SR,
)


class PlanInput(BaseModel):
    dataset: PromptDataset
    max_prompts: int = 20
    prompts_per_risk: int = 5


class RedTeamPlanGenerator:
    def __init__(self, scope: RedTeamScope, config: PlanInput):
        self.scope = scope
        self.config = config
        self.plan: Optional[RedTeamPlan] = None

    def run(self) -> RedTeamPlan:
        if self.config.dataset == PromptDataset.STRINGRAY:
            self.plan = self._generate_with_stringray()
        elif self.config.dataset == PromptDataset.STARGAZER:
            self.plan = self._generate_with_stargazer()
        elif self.config.dataset.derived_from_hf():
            self.plan = self._generate_with_hf()
        else:
            raise ValueError("Unsupported dataset type")
        return self.plan

    def save_yaml(self, path: str):
        if not self.plan:
            raise ValueError("No plan is provided to save")
        yaml_data = yaml.dump(self.plan.model_dump(), default_flow_style=False)
        with open(path, "w") as file:
            file.write(yaml_data)

    @staticmethod
    def load_yaml(path: str) -> RedTeamPlan:
        with open(path, "r") as file:
            data = yaml.safe_load(file)
        return RedTeamPlan(**data)

    def _generate_with_stargazer(self) -> RedTeamPlan:
        analyzer = AppRiskAnalysis(
            llm=AppRiskAnalysisModelChain(model_name="gpt-4o", temperature=0.5)
        )
        analysis_result = analyzer.analyze(self.scope)
        generator = Stargazer_PromptsGenerator(model="gpt-4o", temperature=0.7)
        test_suite = self._build_test_suite(
            generator, analysis_result, PromptDataset.STARGAZER
        )
        return RedTeamPlan(
            scope=self.scope, threat_model=analysis_result, test_suites=[test_suite]
        )

    def _generate_with_stringray(self) -> RedTeamPlan:
        analyzer = AppRiskAnalysis_SR()
        # llm=AppRiskAnalysisModelChain_SR(model_name="gpt-4o-mini", temperature=0.0)
        analysis_result = analyzer.analyze(self.scope)
        generator = Stringray_PromptsGenerator()
        test_suite = self._build_test_suite(
            generator, analysis_result, PromptDataset.STRINGRAY
        )
        return RedTeamPlan(
            scope=self.scope, threat_model=analysis_result, test_suites=[test_suite]
        )

    def _generate_with_hf(self) -> RedTeamPlan:
        hf_prompt_gen = globals.get_deps_factory().hf_prompt_generator
        analyzer = AppRiskAnalysis_HF(hf_prompts_gen=hf_prompt_gen)
        analysis_result = analyzer.analyze(self.scope, dataset=self.config.dataset)

        generator = HFDataset_PromptsGenerator(hf_prompts_gen=hf_prompt_gen)
        test_suite = TestSuitePrompts(dataset=self.config.dataset)
        for prompts in generator.generate(
            dataset=self.config.dataset,
            app_name=analysis_result.threat_analysis.target.name,
            threat_desc=analysis_result.threat_analysis.analysis,
            risks=analysis_result.threats.risks,
            max_prompts=self.config.max_prompts,
            prompts_per_risk=self.config.prompts_per_risk,
        ):
            test_suite.risk_prompts.append(prompts)

        return RedTeamPlan(
            scope=self.scope, threat_model=analysis_result, test_suites=[test_suite]
        )

    def _build_test_suite(
        self, generator, analysis_result, dataset
    ) -> TestSuitePrompts:
        test_suite = TestSuitePrompts(dataset=dataset)
        for prompts in generator.generate(
            app_name=analysis_result.threat_analysis.target.name,
            threat_desc=analysis_result.threat_analysis.analysis,
            risks=analysis_result.threats.risks,
            max_prompts=self.config.max_prompts,
            prompts_per_risk=self.config.prompts_per_risk,
        ):
            test_suite.risk_prompts.append(prompts)
        return test_suite

from typing import Optional

from dtx.core.models.evaluator import EvaluatorInScope
from dtx.core.models.prompts import (
    BaseMultiTurnConversation,
    BaseMultiTurnResponse,
)


class BaseAgent:
    def generate(self, prompt: str) -> str:
        raise ValueError("Not Implemented Error")

    def converse(self, prompt: BaseMultiTurnConversation) -> BaseMultiTurnResponse:
        """
        Perform Multi turn conversation with the agent
        """
        raise ValueError("Not Implemented Error")

    def get_preferred_evaluator(self) -> Optional[EvaluatorInScope]:
        """
        Return Preferred Evaluator if exists
        """
        return None

from dtx.core.models.evaluator import (
    BasePromptEvaluation,
    EvaluationModelName,
    EvaluationModelType,
)
from dtx.core.models.prompts import BaseMultiTurnResponse
from dtx.core.models.results import EvaluationStatus


class BaseEvaluator:
    ## Define below to provide name and type of the evaluator
    EVAL_TYPE: EvaluationModelType = None
    EVAL_NAME: EvaluationModelName = None

    def evaluate(
        self,
        conversation: BaseMultiTurnResponse,
        evaluation_method: BasePromptEvaluation,
    ) -> EvaluationStatus:
        """
        This method is used to invoke the chain and evaluate the given text against the provided evaluation criteria.

        :param text: The response text from the AI system that needs evaluation.
        :param evaluation_criteria: The criteria against which the response is evaluated.
        :return: An EvaluationStatus object containing the result and description of the evaluation.
        """
        raise ValueError("Method Not Implemented")

    def get_name(self) -> EvaluationModelName:
        return self.EVAL_NAME

    def get_type(self) -> EvaluationModelType:
        return self.EVAL_TYPE

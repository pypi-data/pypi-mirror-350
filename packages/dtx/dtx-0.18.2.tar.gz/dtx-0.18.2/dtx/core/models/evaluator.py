from enum import Enum
from typing import List

from pydantic import BaseModel, Field, field_serializer


class EvaluatorScope(str, Enum):
    SCORES = "scores"  # Scope evaluator is labels
    RESPONSE = "response"  # Scope of evaluator is whole response

    def __str__(self):
        return self.value  # Ensures correct YAML serialization

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class EvaluationModelType(str, Enum):
    TOXICITY = "TOXICITY"
    STRING_SEARCH = "STRING_SEARCH"
    JSON_EXPRESSION = "JSON_EXPRESSION"
    POLICY = "POLICY"

    def __str__(self):
        return self.value  # Ensures correct YAML serialization

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class EvaluationModelName(str, Enum):
    ANY = "ANY"  # Any model of the choice, it is default
    OLLAMA_LLAMA_GUARD = "OLLAMA_LLAMA_GUARD"
    ANY_KEYWORD_MATCH = "ANY_KEYWORD_MATCH"
    ANY_JSONPATH_EXP = "ANY_JSONPATH_EXP"
    IBM_GRANITE_TOXICITY_HAP_38M = "IBM_GRANITE_TOXICITY_HAP_38M"
    IBM_GRANITE_TOXICITY_HAP_125M = "IBM_GRANITE_TOXICITY_HAP_125M"
    POLICY_BASED_EVALUATION_OPENAI = "POLICY_BASED_EVALUATION_OPENAI"

    def __str__(self):
        return self.value  # Ensures correct YAML serialization

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class BasePromptEvaluation(BaseModel):
    scope: EvaluatorScope = Field(
        default=EvaluatorScope.RESPONSE, description="Scope of Evaluator"
    )

    @field_serializer("scope")
    def serialize_scope(self, scope: EvaluatorScope) -> str:
        """Serialize the scope enum to a string."""
        return str(scope)


# --------------------
# Model Eval based Test Prompts
# -----------------------


class TypeAndNameBasedEvaluator(BasePromptEvaluation):
    eval_model_type: EvaluationModelType
    eval_model_name: EvaluationModelName

    @field_serializer("eval_model_type")
    def serialize_eval_model_type(self, eval_model_type: EvaluationModelType) -> str:
        return str(eval_model_type)

    @field_serializer("eval_model_name")
    def serialize_eval_model_name(self, eval_model_name: EvaluationModelName) -> str:
        return str(eval_model_name)


### Model based evaluators
class ModelBasedPromptEvaluation(TypeAndNameBasedEvaluator):
    pass


class IBMGraniteHAP38M(ModelBasedPromptEvaluation):
    eval_model_type: EvaluationModelType = EvaluationModelType.TOXICITY
    eval_model_name: EvaluationModelName = (
        EvaluationModelName.IBM_GRANITE_TOXICITY_HAP_38M
    )


class IBMGraniteHAP125M(ModelBasedPromptEvaluation):
    eval_model_type: EvaluationModelType = EvaluationModelType.TOXICITY
    eval_model_name: EvaluationModelName = (
        EvaluationModelName.IBM_GRANITE_TOXICITY_HAP_125M
    )


###


class AnyKeywordBasedPromptEvaluation(TypeAndNameBasedEvaluator):
    eval_model_type: EvaluationModelType = EvaluationModelType.STRING_SEARCH
    eval_model_name: EvaluationModelName = EvaluationModelName.ANY_KEYWORD_MATCH

    keywords: List[str] = Field(
        default_factory=list, description="Match the presence of any of the keyword"
    )


class AnyJsonPathExpBasedPromptEvaluation(TypeAndNameBasedEvaluator):
    """
    Evaluate success if any of the json expression is matched to be true.
    Note, success means no vulnerability. Failed means evaluation failed
    """

    eval_model_type: EvaluationModelType = EvaluationModelType.JSON_EXPRESSION
    eval_model_name: EvaluationModelName = EvaluationModelName.ANY_JSONPATH_EXP

    expressions: List[str] = Field(
        default_factory=list, description="Evaluate any of the json path expressions"
    )


#
# Evaluators Combined
#


class EvaluatorInScope(BaseModel):
    evaluation_method: (
        ModelBasedPromptEvaluation
        | AnyJsonPathExpBasedPromptEvaluation
        | AnyKeywordBasedPromptEvaluation
    )

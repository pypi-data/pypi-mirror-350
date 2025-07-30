from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_serializer


class BaseTactic(BaseModel):
    name: str = Field(description="Name of the Tactic")


class BaseTacticConfig(BaseModel):
    pass


class TacticModule(Enum):
    FLIP_ATTACK = "flip_attack"

    def __str__(self):
        return self.value  # Ensures correct YAML serialization

    @classmethod
    def values(cls):
        return [mode.value for mode in cls]


class TacticWithModesConfig(BaseTacticConfig):
    modes: Optional[List[str]] = Field(
        default_factory=list, description="Jailbreak Mode Config"
    )


class TacticWithLanguagesConfig(BaseTacticConfig):
    languages: Optional[List[str]] = Field(
        default_factory=list, description="Languages to perform transformation"
    )


class PromptMutationTactic(BaseTactic):
    name: TacticModule = Field(description="Name of the Tactic")
    config: Optional[TacticWithModesConfig | TacticWithLanguagesConfig] = Field(
        default=None,
        description="Configuration specific to the jailbreak Tactic",
    )

    @field_serializer("name")
    def serialize_eval_model_type(self, name: TacticModule) -> str:
        return name.value

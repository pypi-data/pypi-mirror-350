from abc import ABC, abstractmethod
from typing import Iterator

from dtx.core.models.prompts import MultiTurnTestPrompt
from dtx.core.models.tactic import BaseTacticConfig


class BaseTactic(ABC):
    NAME = ".."
    DESCRIPTION = ".."

    def __init__(self):
        pass

    @abstractmethod
    def generate(
        self,
        prompt: MultiTurnTestPrompt,
        config: BaseTacticConfig,
    ) -> Iterator[MultiTurnTestPrompt]:
        pass

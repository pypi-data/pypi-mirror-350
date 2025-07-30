from typing import Literal, Optional

from pydantic import BaseModel, Field

from dtx.core.models.providers.openai import BaseProviderConfig


class GroqProviderConfig(BaseProviderConfig):
    endpoint: Optional[str] = Field(
        default="https://api.groq.com/v1",
        description="Base URL of the Groq server or proxy endpoint.",
    )


class GroqProvider(BaseModel):
    """Wrapper for Groq provider configuration."""

    provider: Literal["groq"] = Field(
        "groq", description="Provider ID, always set to 'groq'."
    )
    config: GroqProviderConfig

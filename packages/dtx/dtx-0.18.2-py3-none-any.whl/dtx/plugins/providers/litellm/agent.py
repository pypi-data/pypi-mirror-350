import os
from typing import Any

import litellm

from dtx.core.models.providers.litellm import LitellmProvider
from dtx.core.models.template.prompts.base import BasePromptTemplateRepo

from ..base.exceptions import InvalidInputException
from ..openai.base import BaseChatAgent

""" 
id: litellm
config:
  model: groq/llama3-70b-8192
"""

""" 
id: litellm
config:
  model: groq/llama3-70b-8192
  task: generation
  endpoint: https://api.groq.com/openai/v1
  params:
    temperature: 0.7
    top_k: 40
    top_p: 0.9
    repeat_penalty: 1.1
    max_tokens: 512
    num_return_sequences: 1
    extra_params:
      stop: ["###", "User:"]

"""


class BaseLiteLLMCompatibleAgent(BaseChatAgent):
    def __init__(
        self,
        provider: LitellmProvider,
        prompt_template: BasePromptTemplateRepo = None,
    ):
        if not provider.config.model:
            raise InvalidInputException("Model name must be provided for the Agent.")

        self._model = provider.config.model
        self._provider = provider
        self._available = False
        self.set_prompt_template(prompt_template)
        self._init_client()

    def _init_client(self):
        try:
            endpoint = self._provider.config.endpoint
            if endpoint:
                os.environ["LITELLM_API_BASE"] = endpoint

            # Test availability
            litellm.completion(
                model=self._model,
                messages=[{"role": "user", "content": "ping"}],
                temperature=0.0,
                max_tokens=1,
            )
            self._available = True

        except Exception as e:
            self.logger.error(f"Failed to initialize LiteLLM client: {e}")
            self._available = False

    def _chat_completion(self, messages: list) -> Any:
        return litellm.completion(
            model=self._model,
            messages=messages,
            num_retries=2,
            **self._build_options(),
        )

    def _extract_response_content(self, response: Any) -> str:
        return response["choices"][0]["message"]["content"]


class LitellmAgent(BaseLiteLLMCompatibleAgent):
    def __init__(
        self,
        provider: LitellmProvider,
        prompt_template: BasePromptTemplateRepo = None,
    ):
        super().__init__(provider=provider, prompt_template=prompt_template)

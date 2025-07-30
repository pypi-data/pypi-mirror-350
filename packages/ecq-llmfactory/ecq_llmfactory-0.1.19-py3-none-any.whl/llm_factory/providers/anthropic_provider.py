from langchain.base_language import BaseLanguageModel
from langchain_anthropic import ChatAnthropic

from llm_factory.factory_llm import AbstractLLMFactory

class AnthropicFactory(AbstractLLMFactory):
    """Factory for Anthropic models"""

    def create_model(self) -> BaseLanguageModel:
        return ChatAnthropic(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries
        )
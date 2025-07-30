from langchain.base_language import BaseLanguageModel
from langchain_fireworks import ChatFireworks

from llm_factory.factory_llm import AbstractLLMFactory

class FireworksFactory(AbstractLLMFactory):
    """Factory for Fireworks models"""

    def create_model(self) -> BaseLanguageModel:
        return ChatFireworks(
            model=self.config.model_name,
            temperature=self.config.temperature,
            model_kwargs={"top_p": self.config.top_p},
            max_tokens=self.config.max_tokens,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries
        )
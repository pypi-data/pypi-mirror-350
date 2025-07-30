from langchain.base_language import BaseLanguageModel
from langchain_openai import ChatOpenAI

from llm_factory.factory_llm import AbstractLLMFactory

class DeepSeekFactory(AbstractLLMFactory):
    """Factory for OpenAI models"""

    def create_model(self) -> BaseLanguageModel:
        return ChatOpenAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            openai_api_key=self.config.api_key,
            openai_api_base='https://api.deepseek.com'
        )
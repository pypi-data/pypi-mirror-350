from langchain.base_language import BaseLanguageModel
from langchain_ollama import OllamaLLM

from llm_factory.factory_llm import AbstractLLMFactory

class OllamaFactory(AbstractLLMFactory):
    """Factory for Ollama models"""

    def create_model(self) -> BaseLanguageModel:
        return OllamaLLM(
            model=self.config.model_name,
            temperature=self.config.temperature,
            num_ctx=self.config.num_ctx,
            num_predict=-1
        )
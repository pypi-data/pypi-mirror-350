from langchain_huggingface.llms import HuggingFacePipeline

from transformers import pipeline
from llm_factory.factory_llm import AbstractLLMFactory

class HuggingFaceFactory(AbstractLLMFactory):
    """Factory for HuggingFace models"""

    def create_model(self):
        pipe = pipeline(
            "text-generation",
            model=self.config.model_name,
            device=self.config.device,
            max_length=self.config.max_length
        )

        return HuggingFacePipeline(pipeline=pipe)
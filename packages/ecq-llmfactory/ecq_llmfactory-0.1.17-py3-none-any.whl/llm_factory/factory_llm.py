from abc import ABC, abstractmethod
from pathlib import Path
import importlib
from typing import Any, Optional, List, Mapping
import functools
from dataclasses import dataclass

import httpx
from pydantic import Field
from langchain.base_language import BaseLanguageModel
from inspect import signature

@dataclass
class ModelConfig:
    """Configuration class for model initialization parameters"""

    provider_name: str
    model_name: str
    temperature: float
    api_key: Optional[str] = None
    max_tokens: Optional[int] = None
    top_p: float = 0.9
    timeout: Optional[int] = None
    max_retries: int = 2
    api_base: Optional[str] = None
    device: Optional[str] | Optional[List[str]] = None
    max_length: Optional[int] = None
    tensor_parallel_size: Optional[int] = None
    max_tokens: Optional[int] = None
    gpu_memory_utilization: Optional[float] = None  # aka number GPU
    max_model_len: Optional[int] = None
    num_ctx: Optional[int] = None
    http_client: Optional[httpx.Client] = None
    http_async_client: Optional[httpx.AsyncClient] = None
    model_kwargs: Optional[dict] = None
    extra_body: Optional[dict] = None

class AbstractLLMFactory(ABC):
    """Abstract base class for LLM initialization"""

    def __init__(self, config: ModelConfig) -> None:
        self.config = config
        self._model: Optional[BaseLanguageModel] = None

    @abstractmethod
    def create_model(self) -> BaseLanguageModel:
        """Create and return a specific LLM instance"""
        pass

    def get_model(self) -> BaseLanguageModel:
        """Get or create LLM instance"""
        if self._model is None:
            self._model = self.create_model()
        return self._model
    
    

class LLMFactoryProvider:
    """Provider class to get appropriate LLM factory"""

    PROVIDERS_DIR = Path(__file__).parent / "providers"

    @staticmethod
    def get_factory(config: ModelConfig) -> AbstractLLMFactory:
        module_path = f"llm_factory.providers.{config.provider_name.lower()}_provider"

        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ImportError(
                f"Could not import module {module_path}: {str(e)}.Please ensure the provider is supported by doing ProviderFactory.get_supported_providers()"
            )
        provider_class = getattr(module, f"{config.provider_name}Factory")
        return provider_class(config)

    @classmethod
    @functools.cache
    def get_supported_providers(cls):
        """List all supported provider names based on files present in the providers directory."""
        provider_files = Path(cls.PROVIDERS_DIR).glob("*_provider.py")
        return {file.stem.replace("_provider", "") for file in provider_files}

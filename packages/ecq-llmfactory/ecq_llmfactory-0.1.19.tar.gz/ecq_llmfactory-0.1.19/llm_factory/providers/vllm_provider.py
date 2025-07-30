from langchain_community.llms import VLLM
from langchain_openai import ChatOpenAI
from llm_factory.factory_llm import AbstractLLMFactory

class vLLMFactory(AbstractLLMFactory):
    """Factory for HuggingFace models"""
    def filter_none_args(self, config):
        config_dict = config.__dict__  # or config.__dict__
        filtered = {
            k: v for k, v in config_dict.items()
            if v is not None and k != "provider_name"
        }
        return filtered
    
    def create_model(self, client_server_mode=True):
        if client_server_mode:
            return ChatOpenAI(
                **self.filter_none_args(self.config)
            )
        llm = VLLM(
            model=self.config.model_name,
            # trust_remote_code=True,  # mandatory for hf models
            tensor_parallel_size=self.config.tensor_parallel_size,
            max_tokens=self.config.max_tokens,
            top_p=self.config.top_p,
            temperature=self.config.temperature,
            vllm_kwargs={'gpu_memory_utilization':self.config.gpu_memory_utilization,
                        'max_model_len': self.config.max_model_len},
        )

        return llm
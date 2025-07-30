from langchain_community.llms import VLLM
from langchain_openai import ChatOpenAI
from llm_factory.factory_llm import AbstractLLMFactory
from inspect import signature

class vLLMFactory(AbstractLLMFactory):
    """Factory for HuggingFace models"""
    def get_chat_openai_args(self, config):
        sig = signature(ChatOpenAI.__init__)
        valid_keys = sig.parameters.keys()

        config_dict = config.__dict__  # or use `vars(config)` if it's a dataclass
        filtered = {k: v for k, v in config_dict.items() if k in valid_keys and v is not None}
        return filtered
    
    def create_model(self, client_server_mode=True):
        if client_server_mode:
            return ChatOpenAI(
                **self.get_chat_openai_args(self.config)
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
# LLMFactory

`LLMFactory` is a modular and extensible framework built on top of the `LangChain` library, designed for streamlined integration and management of Large Language Models (LLMs). By leveraging LangChain's powerful abstractions and tools, `LLMFactory` provides a factory-based approach to initialize and manage LLMs from multiple providers, offering flexibility, maintainability, and scalability.

## Key Features

### 1. **LangChain Foundation**

- LLMFactory utilizes **LangChain** as its core, ensuring compatibility with its powerful tools, chains, and agents.
- It is well-suited for applications requiring complex workflows and advanced LLM capabilities.

### 2. **Abstract Factory Pattern**

- The framework employs the abstract factory design pattern through the `AbstractLLMFactory` base class.
- This ensures a standardized interface for initializing and managing diverse LLMs.

### 3. **Support for Multiple LLM Providers**

- Pre-configured factories for leading LLM providers, including:
  - **OpenAI (ChatOpenAI)**: Supporting models like GPT-3.5 and GPT-4.
  - **DeepSeek**: Extended functionality for OpenAI APIs.
  - **Fireworks (ChatFireworks)**: Tailored models for specific workflows with additional parameters like `top_p` and retries.
  - **Ollama (OllamaLLM)**: Lightweight models with customizable context size.
  - **Anthropic (ChatAnthropic)**: Human-aligned conversational models (e.g., Claude).

### 5. **Model Configuration**

- The `ModelConfig` dataclass encapsulates essential initialization parameters, such as:
  - Model name
  - Temperature for response diversity
  - API keys and base URLs
  - Advanced parameters like `top_p`, `max_tokens`, timeouts, and retries

## Installation

You can install just the base `llmfactory` package, or install a provider's package along with `llmfactory`.

This installs just the base package without installing any provider's SDK.

```shell
pip install ecq-llmfactory
```

## Set up

To get started, you will need API Keys for the providers you intend to use. You'll need to
install the provider-specific library either separately or when installing aisuite.

The API Keys can be set as environment variables, or can be passed as config to the aisuite Client constructor.
You can use tools like [`python-dotenv`](https://pypi.org/project/python-dotenv/) or [`direnv`](https://direnv.net/) to set the environment variables manually.

Set the API keys.

```shell
export DEEPSEEK_API_KEY="your-deepseek-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

Use the python client: <https://python.langchain.com/v0.2/docs/tutorials/>

```python
import os
import dotenv

from llm_factory import LLMFactoryProvider, ModelConfig
from langchain.prompts import ChatPromptTemplate

dotenv.load_dotenv()

ANTHROPIC_KEY = os.environ['ANTHROPIC_API_KEY']
model_config = ModelConfig(
    provider_name='Anthropic',
    model_name="claude-3-opus-20240229",
    api_key=ANTHROPIC_KEY,
    temperature=0.0,
)

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

factory = LLMFactoryProvider.get_factory(model_config)
model = factory.get_model()

chain = prompt_template | model
result = chain.invoke({"language": "italian", "text": "hi"})
# result = 'ciao'
```

List supported providers

```python
# list supported providers
print(LLMFactoryProvider.get_supported_providers())
```

For a list of provider values, you can look at the directory - `/providers/`. The list of supported providers are of the format - `<provider>_provider.py` in that directory. We welcome  providers adding support to this library by adding an implementation file in this directory. Please see section below for how to contribute.

## Adding support for a provider

We have made easy for a provider or volunteer to add support for a new platform.

### Naming Convention for Provider Modules

We follow a convention-based approach for loading providers, which relies on strict naming conventions for both the module name and the class name.

- The provider's module file must be named in the format `<provider>_provider.py`.
- The class inside this module must follow the format: the provider name with the first letter capitalized, followed by the suffix `Provider`.

#### Examples

- **Hugging Face**:
  The provider class should be defined as:

  ```python
  class HuggingfaceProvider(AbstractLLMFactory)
  ```

  in providers/huggingface_provider.py.
  
- **OpenAI**:
  The provider class should be defined as:

  ```python
  class OpenaiProvider(AbstractLLMFactory)
  ```

  in providers/openai_provider.py

This convention simplifies the addition of new providers and ensures consistency across provider implementations.

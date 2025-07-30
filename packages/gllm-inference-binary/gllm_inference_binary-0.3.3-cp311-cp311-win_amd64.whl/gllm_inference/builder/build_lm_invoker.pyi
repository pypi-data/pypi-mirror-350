from _typeshed import Incomplete
from gllm_inference.builder.model_id import ModelId as ModelId, ModelProvider as ModelProvider
from gllm_inference.lm_invoker import AnthropicLMInvoker as AnthropicLMInvoker, AzureOpenAILMInvoker as AzureOpenAILMInvoker, GoogleLMInvoker as GoogleLMInvoker, OpenAICompatibleLMInvoker as OpenAICompatibleLMInvoker, OpenAILMInvoker as OpenAILMInvoker
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from typing import Any

PROVIDER_TO_LM_INVOKER_MAP: dict[str, type[BaseLMInvoker]]
logger: Incomplete

class _Key:
    """Defines valid keys in the config."""
    API_KEY: str
    AZURE_DEPLOYMENT: str
    AZURE_ENDPOINT: str
    BASE_URL: str
    CREDENTIALS_PATH: str
    MODEL_NAME: str

def build_lm_invoker(model_id: str | ModelId, credentials: str, config: dict[str, Any] | None = None) -> BaseLMInvoker:
    '''Build a language model invoker based on the provided configurations.

    Args:
        model_id (str | ModelId): The model id, can either be a ModelId instance or a string in the following format:
            1. For `azure-openai` provider: `azure-openai/azure-endpoint:azure-deployment`.
            2. For `openai-compatible` provider: `openai-compatible/base-url:model-name`.
            3. For other providers: `provider/model-name`.
        credentials (str): The credentials for the language model. Can either be an API key or a path to a credentials
            JSON file.
        config (dict[str, Any] | None, optional): Additional configuration for the language model. Defaults to None.

    Returns:
        BaseLMInvoker: The initialized language model invoker.

    Raises:
        ValueError: If the provided configuration is invalid.

    Usage examples:
        # Using Anthropic
        ```python
        lm_invoker = build_lm_invoker(
            model_id="anthropic/claude-3-5-sonnet-latest",
            credentials="sk-ant-api03-..."
        )
        ```

        # Using Google Gen AI (via API key)
        ```python
        lm_invoker = build_lm_invoker(
            model_id="google/gemini-1.5-flash-latest",
            credentials="AIzaSyD..."
        )
        ```

        # Using Google Vertex AI (via service account)
        ```python
        lm_invoker = build_lm_invoker(
            model_id="google/gemini-1.5-flash",
            credentials="/path/to/google-credentials.json"
        )
        ```

        # Using OpenAI
        ```python
        lm_invoker = build_lm_invoker(
            model_id="openai/gpt-4o-mini",
            credentials="sk-..."
        )
        ```

        # Using Azure OpenAI
        ```python
        lm_invoker = build_lm_invoker(
            model_id="azure-openai/https://my-resource.openai.azure.com:my-deployment",
            credentials="azure-api-key"
        )
        ```

        # Using OpenAI Compatible endpoint (e.g. Groq)
        ```python
        lm_invoker = build_lm_invoker(
            model_id="openai-compatible/https://api.groq.com/openai/v1:llama3-8b-8192",
            credentials="gsk_..."
        )
        ```

    Security warning:
        Please provide the LM invoker credentials ONLY to the `credentials` parameter. Do not put any kind of
        credentials in the `config` parameter as the content of the `config` parameter will be logged.
    '''

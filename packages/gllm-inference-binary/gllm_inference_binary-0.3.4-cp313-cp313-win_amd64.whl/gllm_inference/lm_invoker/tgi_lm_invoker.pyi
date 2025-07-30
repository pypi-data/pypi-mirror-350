from gllm_inference.lm_invoker.openai_compatible_lm_invoker import OpenAICompatibleLMInvoker as OpenAICompatibleLMInvoker
from typing import Any

DEPRECATION_MESSAGE: str

class TGILMInvoker(OpenAICompatibleLMInvoker):
    '''A language model invoker to interact with language models hosted in Text Generation Inference (TGI).

    This class has been deprecated as Text Generation Inference is now supported through `OpenAICompatibleLMInvoker`.
    This class is maintained for backward compatibility and will be removed in version 0.4.0.

    Attributes:
        client (AsyncOpenAI): The OpenAI client instance.
        model_name (str): The name of the language model.
        default_hyperparameters (dict[str, Any]): Default hyperparameters for invoking the model.
        valid_extensions_map (dict[str, set[str]]): A dictionary mapping for validating the content type of the
            multimodal inputs. The keys are the mime types (e.g. "image") and the values are the set of valid
            file extensions (e.g. {".png", ".jpg", ".jpeg"}) for the corresponding mime type.
        valid_extensions (set[str]): A set of valid file extensions for the multimodal inputs.
        tools (list[Any]): The list of tools provided to the model to enable tool calling.
        response_schema (ResponseSchema | None): The schema of the response. If provided, the model will output a
            structured response as defined by the schema. Supports both Pydantic BaseModel and JSON schema dictionary.
        output_analytics (bool): Whether to output the invocation analytics.
    '''
    def __init__(self, url: str, username: str = '', password: str = '', api_key: str = '', default_hyperparameters: dict[str, Any] | None = None) -> None:
        """Initializes a new instance of the TGILMInvoker class.

        Args:
            url (str): The URL of the TGI service.
            username (str, optional): The username for Basic Authentication. Defaults to an empty string.
            password (str, optional): The password for Basic Authentication. Defaults to an empty string.
            api_key (str, optional): The API key for authenticating with the TGI service. Defaults to an empty string.
            default_hyperparameters (dict[str, Any] | None, optional): Default hyperparameters for invoking the model.
                Defaults to None.
        """

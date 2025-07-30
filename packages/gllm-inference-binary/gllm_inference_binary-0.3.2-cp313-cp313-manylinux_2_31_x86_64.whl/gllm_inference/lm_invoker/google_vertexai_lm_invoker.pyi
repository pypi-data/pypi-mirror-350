from gllm_inference.lm_invoker.google_lm_invoker import GoogleLMInvoker as GoogleLMInvoker
from gllm_inference.schema import ResponseSchema as ResponseSchema
from langchain_core.tools import Tool as Tool
from typing import Any

DEPRECATION_MESSAGE: str

class GoogleVertexAILMInvoker(GoogleLMInvoker):
    '''A language model invoker to interact with Google Vertex AI language models.

    This class has been deprecated as Google Vertex AI is now supported through `GoogleLMInvoker`.
    This class is maintained for backward compatibility and will be removed in version 0.4.0.

    Attributes:
        client (Client): The Google client instance.
        model_name (str): The name of the Google language model.
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
    def __init__(self, model_name: str, credentials_path: str, project_id: str | None = None, location: str = 'us-central1', model_kwargs: dict[str, Any] | None = None, default_hyperparameters: dict[str, Any] | None = None, tools: list[Tool] | None = None, response_schema: ResponseSchema | None = None, output_analytics: bool = False, bind_tools_params: dict[str, Any] | None = None, with_structured_output_params: dict[str, Any] | None = None) -> None:
        '''Initializes a new instance of the GoogleVertexAILMInvoker class.

        Args:
            model_name (str): The name of the multimodal language model to be used.
            credentials_path (str): The path to the Google Cloud service account credentials JSON file.
            project_id (str | None, optional): The Google Cloud project ID. Defaults to None, in which case the
                project ID will be loaded from the credentials file.
            location (str, optional): The location of the Google Cloud project. Defaults to "us-central1".
            model_kwargs (dict[str, Any] | None, optional): Additional keyword arguments for the Google Vertex AI
                client.
            default_hyperparameters (dict[str, Any] | None, optional): Default hyperparameters for invoking the model.
                Defaults to None.
            tools (list[Tool] | None, optional): Tools provided to the language model to enable tool calling.
                Defaults to None.
            response_schema (ResponseSchema | None, optional): The schema of the response. If provided, the model will
                output a structured response as defined by the schema. Supports both Pydantic BaseModel and JSON schema
                dictionary. Defaults to None.
            output_analytics (bool, optional): Whether to output the invocation analytics. Defaults to False.
            bind_tools_params (dict[str, Any] | None, optional): Deprecated parameter to add tool calling capability.
                If provided, must at least include the `tools` key that is equivalent to the `tools` parameter.
                Retained for backward compatibility. Defaults to None.
            with_structured_output_params (dict[str, Any] | None, optional): Deprecated parameter to instruct the
                model to produce output with a certain schema. If provided, must at least include the `schema` key that
                is equivalent to the `response_schema` parameter. Retained for backward compatibility. Defaults to None.
        '''

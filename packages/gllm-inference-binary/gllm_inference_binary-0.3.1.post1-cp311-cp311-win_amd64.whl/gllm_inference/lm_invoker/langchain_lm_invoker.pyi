from _typeshed import Incomplete
from gllm_core.event import EventEmitter as EventEmitter
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_inference.schema import ANY_EXTENSION as ANY_EXTENSION, LMOutput as LMOutput, MimeType as MimeType, MultimodalContent as MultimodalContent, MultimodalOutput as MultimodalOutput, MultimodalPrompt as MultimodalPrompt, PromptRole as PromptRole, ResponseSchema as ResponseSchema, TokenUsage as TokenUsage, ToolCall as ToolCall, ToolResult as ToolResult
from gllm_inference.utils import get_mime_type as get_mime_type
from langchain_core.language_models import BaseChatModel as BaseChatModel
from langchain_core.messages import BaseMessage as BaseMessage
from langchain_core.tools import Tool as Tool
from typing import Any

VALID_EXTENSIONS_MAP: Incomplete
MESSAGE_CLASS_MAP: Incomplete

class _Key:
    """Defines valid keys in LangChain."""
    ARGS: str
    FINISH_REASON: str
    ID: str
    IMAGE_URL: str
    INPUT_TOKENS: str
    NAME: str
    OUTPUT_TOKENS: str
    PARSED: str
    RAW: str
    TEXT: str
    TYPE: str
    URL: str

class _InputType:
    """Defines valid input types in LangChain."""
    IMAGE_URL: str
    TEXT: str
    TOOL_CALL: str

class LangChainLMInvoker(BaseLMInvoker):
    '''A language model invoker to interact with LangChain\'s BaseChatModel.

    Attributes:
        model (BaseChatModel): The LangChain\'s BaseChatModel instance.
        default_hyperparameters (dict[str, Any]): Default hyperparameters for invoking the model.
        valid_extensions_map (dict[str, set[str]]): A dictionary mapping for validating the content type of the
            multimodal inputs. The keys are the mime types (e.g. "image") and the values are the set of valid
            file extensions (e.g. {".png", ".jpg", ".jpeg"}) for the corresponding mime type.
        valid_extensions (set[str]): A set of valid file extensions for the multimodal inputs.
        tools (list[Any]): The list of tools provided to the model to enable tool calling.
        response_schema (ResponseSchema | None): The schema of the response. If provided, the model will output a
            structured response as defined by the schema. Supports both Pydantic BaseModel and JSON schema dictionary.
        output_analytics (bool): Whether to output the invocation analytics.

    Input types:
        1. Text.
        2. Image, with extensions depending on the language model\'s capabilities.

        Non-text inputs must be of valid file extensions and can be passed as either:
        1. Base64 encoded bytes.
        2. Remote URLs, with a valid `http` or `https` scheme.
        3. Existing local file paths.

        Usage example:
        ```python
        text = "What animal is in this image?"
        image = "path/to/local/image.png"

        prompt = [(PromptRole.USER, [text, image])]
        result = await lm_invoker.invoke(prompt)
        ```

    Tool calling:
        Tool calling is a feature that allows the language model to call tools to perform tasks.
        Tools can be passed to the via the `tools` parameter as a list of LangChain\'s `Tool` objects.
        When tools are provided and the model decides to call a tool, the tool calls are stored in the
        `tool_calls` attribute in the output.

        Usage example:
        ```python
        lm_invoker = LangChainLMInvoker(..., tools=[tool_1, tool_2])
        ```

        Output example:
        ```python
        LMOutput(
            response="Let me call the tools...",
            tool_calls=[
                ToolCall(id="123", name="tool_1", args={"key": "value"}),
                ToolCall(id="456", name="tool_2", args={"key": "value"}),
            ]
        )
        ```

    Structured output:
        Structured output is a feature that allows the language model to output a structured response.
        This feature can be enabled by providing a schema to the `response_schema` parameter.
        The schema must be either a JSON schema dictionary or a Pydantic BaseModel class.

        Structured output is not compatible with tool calling. The language model also doesn\'t need to stream
        anything when structured output is enabled. Thus, standard invocation will be performed regardless of
        whether the `event_emitter` parameter is provided or not.

        When enabled, the structured output is stored in the `structured_output` attribute in the output.
        1. If the schema is a JSON schema dictionary, the structured output is a dictionary.
        2. If the schema is a Pydantic BaseModel class, the structured output is a Pydantic model.

        # Example 1: Using a JSON schema dictionary
        Usage example:
        ```python
        schema = {
            "title": "Animal",
            "description": "A description of an animal.",
            "properties": {
                "color": {"title": "Color", "type": "string"},
                "name": {"title": "Name", "type": "string"},
            },
            "required": ["name", "color"],
            "type": "object",
        }
        lm_invoker = LangChainLMInvoker(..., response_schema=schema)
        ```
        Output example:
        ```python
        LMOutput(structured_output={"name": "Golden retriever", "color": "Golden"})
        ```

        # Example 2: Using a Pydantic BaseModel class
        Usage example:
        ```python
        class Animal(BaseModel):
            name: str
            color: str

        lm_invoker = LangChainLMInvoker(..., response_schema=Animal)
        ```
        Output example:
        ```python
        LMOutput(structured_output=Animal(name="Golden retriever", color="Golden"))
        ```

    Analytics tracking:
        Analytics tracking is a feature that allows the module to output additional information about the invocation.
        This feature can be enabled by setting the `output_analytics` parameter to `True`.
        When enabled, the following attributes will be stored in the output:
        1. `token_usage`: The token usage.
        2. `duration`: The duration in seconds.
        3. `finish_details`: The details about how the generation finished.

        Output example:
        ```python
        LMOutput(
            response="Golden retriever is a good dog breed.",
            token_usage=TokenUsage(input_tokens=100, output_tokens=50),
            duration=0.729,
            finish_details={"finish_reason": "stop"},
        )
        ```

    Output types:
        The output of the `LangChainLMInvoker` is of type `MultimodalOutput`, which is a type alias that can represent:
        1. `str`: The text response if no additional output is needed.
        2. `LMOutput`: A Pydantic model with the following attributes if any additional output is needed:
            2.1. response (str): The text response.
            2.2. tool_calls (list[ToolCall]): The tool calls, if the `tools` parameter is defined and the language
                model decides to invoke tools. Defaults to an empty list.
            2.3. structured_output (StructuredOutput | None): The structured output, if the `response_schema` parameter
                is defined. Defaults to None.
            2.4. token_usage (TokenUsage | None): The token usage analytics, if the `output_analytics` parameter is
                set to `True`. Defaults to None.
            2.5. duration (float | None): The duration of the invocation in seconds, if the `output_analytics`
                parameter is set to `True`. Defaults to None.
            2.6. finish_details (dict[str, Any] | None): The details about how the generation finished, if the
                `output_analytics` parameter is set to `True`. Defaults to None.
            2.7. reasoning (list[Reasoning]): The reasoning objects. Currently not supported. Defaults to an empty list.
    '''
    model: Incomplete
    response_schema: Incomplete
    output_analytics: Incomplete
    def __init__(self, model: BaseChatModel | None = None, default_hyperparameters: dict[str, Any] | None = None, tools: list[Tool] | None = None, response_schema: ResponseSchema | None = None, output_analytics: bool = False, llm: BaseChatModel | None = None, bind_tools_params: dict[str, Any] | None = None, with_structured_output_params: dict[str, Any] | None = None) -> None:
        """Initializes a new instance of the LangChainLMInvoker class.

        Args:
            model (BaseChatModel | None, optional): The LangChain's BaseChatModel instance. Will be made required in
                v0.3.0 once the `llm` parameter is removed. Defaults to None.
            default_hyperparameters (dict[str, Any] | None, optional): Default hyperparameters for invoking the model.
                Defaults to None.
            tools (list[Tool] | None, optional): Tools provided to the model to enable tool calling. Defaults to None.
            response_schema (ResponseSchema | None, optional): The schema of the response. If provided, the model will
                output a structured response as defined by the schema. Supports both Pydantic BaseModel and JSON schema
                dictionary. Defaults to None.
            output_analytics (bool, optional): Whether to output the invocation analytics. Defaults to False.
            llm (BaseChatModel | None, optional): Deprecated parameter to pass the LangChain's BaseChatModel instance.
                Equivalent to the `model` parameter. Retained for backward compatibility. Defaults to None.
            bind_tools_params (dict[str, Any] | None, optional): Deprecated parameter to add tool calling capability.
                If provided, must at least include the `tools` key that is equivalent to the `tools` parameter.
                Retained for backward compatibility. Defaults to None.
            with_structured_output_params (dict[str, Any] | None, optional): Deprecated parameter to instruct the
                model to produce output with a certain schema. If provided, must at least include the `schema` key that
                is equivalent to the `response_schema` parameter. Retained for backward compatibility. Defaults to None.

        Raises:
            ValueError: If `response_schema` is provided, but `tools` are also provided.
        """

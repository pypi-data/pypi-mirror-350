from _typeshed import Incomplete
from gllm_core.event import EventEmitter as EventEmitter
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_inference.schema import LMOutput as LMOutput, MimeType as MimeType, MultimodalContent as MultimodalContent, MultimodalOutput as MultimodalOutput, MultimodalPrompt as MultimodalPrompt, Reasoning as Reasoning, ResponseSchema as ResponseSchema, TokenUsage as TokenUsage, ToolCall as ToolCall, ToolResult as ToolResult
from gllm_inference.utils import get_mime_type as get_mime_type
from langchain_core.tools import Tool as Tool
from typing import Any

VALID_EXTENSIONS_MAP: Incomplete
DEFAULT_MAX_TOKENS: int
DEFAULT_THINKING_BUDGET: int

class _Key:
    """Defines valid keys in Anthropic."""
    CONTENT: str
    DATA: str
    ID: str
    INPUT: str
    MEDIA_TYPE: str
    NAME: str
    SIGNATURE: str
    SOURCE: str
    STOP_REASON: str
    THINKING: str
    TOOL_USE_ID: str
    TEXT: str
    TYPE: str

class _InputType:
    """Defines valid input types in Anthropic."""
    IMAGE: str
    REDACTED_THINKING: str
    TEXT: str
    THINKING: str
    TOOL_RESULT: str
    TOOL_USE: str

class _OutputType:
    """Defines valid output types in Anthropic."""
    CONTENT_BLOCK_DELTA: str
    CONTENT_BLOCK_STOP: str
    MESSAGE_STOP: str
    REDACTED_THINKING: str
    TEXT: str
    TEXT_DELTA: str
    THINKING: str
    THINKING_DELTA: str
    TOOL_USE: str

class AnthropicLMInvoker(BaseLMInvoker):
    '''A language model invoker to interact with Anthropic language models.

    Attributes:
        client (AsyncAnthropic): The Anthropic client instance.
        model_name (str): The name of the Anthropic language model.
        default_hyperparameters (dict[str, Any]): Default hyperparameters for invoking the model.
        valid_extensions_map (dict[str, set[str]]): A dictionary mapping for validating the content type of the
            multimodal inputs. The keys are the mime types (e.g. "image") and the values are the set of valid
            file extensions (e.g. {".png", ".jpg", ".jpeg"}) for the corresponding mime type.
        valid_extensions (set[str]): A set of valid file extensions for the multimodal inputs.
        tools (list[Tool]): Tools provided to the model to enable tool calling.
        response_schema (ResponseSchema | None): The schema of the response. If provided, the model will output a
            structured response as defined by the schema. Supports both Pydantic BaseModel and JSON schema dictionary.
        output_analytics (bool): Whether to output the invocation analytics.
        use_thinking (bool): Whether to enable thinking.
        thinking_budget (int): The tokens allocated for the thinking process. Ignored if `use_thinking = False`.
        output_thinking (bool): Whether to output the thinking token. Ignored if `use_thinking = False`.

    Input types:
        The `AnthropicLMInvoker` supports the following input types:
        1. Text.
        2. Image: ".jpg", ".jpeg", ".png", ".gif", and ".webp".

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
        lm_invoker = AnthropicLMInvoker(..., tools=[tool_1, tool_2])
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

        Structured output is achieved by providing the schema name in the `tool_choice` parameter. This forces
        the model to call the provided schema as a tool. Thus, structured output is not compatible with:
        1. Tool calling, since the tool calling is reserved to force the model to call the provided schema as a tool.
        2. Thinking, since thinking is not allowed when a tool use is forced through the `tool_choice` parameter.
        The language model also doesn\'t need to stream anything when structured output is enabled. Thus, standard
        invocation will be performed regardless of whether the `event_emitter` parameter is provided or not.

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
        lm_invoker = AnthropicLMInvoker(..., response_schema=schema)
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

        lm_invoker = AnthropicLMInvoker(..., response_schema=Animal)
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
            finish_details={"stop_reason": "end_turn"},
        )
        ```

    Thinking:
        Thinking is a feature that allows the language model to have enhanced reasoning capabilities for complex tasks,
        while also providing transparency into its step-by-step thought process before it delivers its final answer.
        This feature is only available for certain models (As of March 2025, only Claude 3.7 Sonnet) and can be enabled
        by setting the `use_thinking` parameter to `True`.

        When thinking is enabled, the amount of tokens allocated for the thinking process can be set via the
        `thinking_budget` parameter. The `thinking_budget`:
        1. Must be greater than or equal to 1024.
        2. Must be less than the `max_tokens` hyperparameter, as the `thinking_budget` is allocated from the
           `max_tokens`. For example, if `max_tokens=2048` and `thinking_budget=1024`, the language model will
           allocate at most 1024 tokens for thinking and the remaining 1024 tokens for generating the response.

        When enabled, the `output_thinking` parameter can be set to `True` to store the thinking in the `reasoning`
        attribute in the output.

        Output example:
        ```python
        LMOutput(
            response="Golden retriever is a good dog breed.",
            reasoning=[Reasoning(type="thinking", reasoning="Let me think about it...", signature="x")],
        )
        ```

        When streaming is enabled along with thinking, the thinking token will be streamed with the `EventType.DATA`
        event type.

        Streaming output example:
        ```python
        {"type": "data", "value": "Let me think ", ...}  # Thinking token
        {"type": "data", "value": "about it...", ...}  # Thinking token
        {"type": "response", "value": "Golden retriever ", ...}  # Response token
        {"type": "response", "value": "is a good dog breed.", ...}  # Response token
        ```

        When both thinking and tool calling are enabled, the `output_thinking` parameter is required to be `True`.
        Otherwise, feeding back the tool results to the model after the tool calls are executed would throw an error,
        as it\'s required by Anthropic.

    Output types:
        The output of the `AnthropicLMInvoker` is of type `MultimodalOutput`, which is a type alias that can represent:
        1. `str`: The text response if no additional output is needed.
        2. `LMOutput`: A Pydantic model with the following attributes if any additional output is needed:
            2.1. response (str): The text response.
            2.2. tool_calls (list[ToolCall]): The tool calls, if the `tools` parameter is defined and the language
                model decides to invoke tools. Defaults to an empty list.
            2.3. structured_output (StructuredOutput | None): The structured output, if the `response_schema` parameter
                is defined. Defaults to None.
            2.4. token_usage (TokenUsage | None): The token usage information, if the `output_analytics` parameter is
                set to `True`. Defaults to None.
            2.5. duration (float | None): The duration of the invocation in seconds, if the `output_analytics`
                parameter is set to `True`. Defaults to None.
            2.6. finish_details (dict[str, Any]): The details about how the generation finished, if the
                `output_analytics` parameter is set to `True`. Defaults to an empty dictionary.
            2.7. reasoning (list[Reasoning]): The reasoning objects, if the `use_thinking` and `output_thinking`
                parameters are set to `True`. Defaults to an empty list.
    '''
    client: Incomplete
    model_name: Incomplete
    response_schema: Incomplete
    output_analytics: Incomplete
    use_thinking: Incomplete
    thinking_budget: Incomplete
    output_thinking: Incomplete
    def __init__(self, model_name: str, api_key: str, model_kwargs: dict[str, Any] | None = None, default_hyperparameters: dict[str, Any] | None = None, tools: list[Tool] | None = None, response_schema: ResponseSchema | None = None, output_analytics: bool = False, use_thinking: bool = False, thinking_budget: int = ..., output_thinking: bool = False, bind_tools_params: dict[str, Any] | None = None, with_structured_output_params: dict[str, Any] | None = None) -> None:
        """Initializes the AnthropicLmInvoker instance.

        Args:
            model_name (str): The name of the Anthropic language model.
            api_key (str): The Anthropic API key.
            model_kwargs (dict[str, Any] | None, optional): Additional keyword arguments for the Anthropic client.
            default_hyperparameters (dict[str, Any] | None, optional): Default hyperparameters for invoking the model.
                Defaults to None.
            tools (list[Tool] | None, optional): Tools provided to the model to enable tool calling. Defaults to None.
            response_schema (ResponseSchema | None, optional): The schema of the response. If provided, the model will
                output a structured response as defined by the schema. Supports both Pydantic BaseModel and JSON schema
                dictionary. Defaults to None.
            output_analytics (bool, optional): Whether to output the invocation analytics. Defaults to False.
            use_thinking (bool, optional): Whether to enable thinking. Defaults to False.
            thinking_budget (int, optional): The tokens allocated for the thinking process. Must be greater than or
                equal to 1024. Ignored if `use_thinking=False`. Defaults to DEFAULT_THINKING_BUDGET.
            output_thinking (bool, optional): Whether to output the thinking token. Ignored if `use_thinking=False`.
                Defaults to False.
            bind_tools_params (dict[str, Any] | None, optional): Deprecated parameter to add tool calling capability.
                If provided, must at least include the `tools` key that is equivalent to the `tools` parameter.
                Retained for backward compatibility. Defaults to None.
            with_structured_output_params (dict[str, Any] | None, optional): Deprecated parameter to instruct the
                model to produce output with a certain schema. If provided, must at least include the `schema` key that
                is equivalent to the `response_schema` parameter. Retained for backward compatibility. Defaults to None.

        Raises:
            ValueError:
            1. `use_thinking` is True, but the `thinking_budget` is less than 1024.
            2. `use_thinking` is True and `tools` are provided, but `output_thinking` is False.
            3. `response_schema` is provided, but `tools` or `use_thinking` are also provided.
        """

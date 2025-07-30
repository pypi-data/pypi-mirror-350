from _typeshed import Incomplete
from gllm_core.event import EventEmitter as EventEmitter
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_inference.multimodal_lm_invoker.multimodal_lm_invoker import BaseMultimodalLMInvoker as BaseMultimodalLMInvoker
from gllm_inference.multimodal_prompt_builder import MultimodalPromptBuilder as MultimodalPromptBuilder
from gllm_inference.output_parser.output_parser import BaseOutputParser as BaseOutputParser
from gllm_inference.prompt_builder.prompt_builder import BasePromptBuilder as BasePromptBuilder
from gllm_inference.schema import LMOutput as LMOutput, MultimodalContent as MultimodalContent, MultimodalOutput as MultimodalOutput, MultimodalPrompt as MultimodalPrompt, PromptRole as PromptRole, ToolCall as ToolCall, ToolResult as ToolResult
from typing import Any

class LMRequestProcessor:
    """A request processor to perform language models inference.

    The `LMRequestProcessor` class handles the process of building a prompt, invoking a language model, and optionally
    parsing the output. It combines a prompt builder, language model invoker, and an optional output parser to manage
    the inference process in Gen AI applications.

    Attributes:
        prompt_builder (BasePromptBuilder | MultimodalPromptBuilder): The prompt builder used to format the prompt.
        lm_invoker (BaseLMInvoker | BaseMultimodalLMInvoker): The language model invoker that handles the model
            inference.
        output_parser (BaseOutputParser | None): The optional parser to process the model's output, if any.
        tool_dict (dict[str, Tool]): A dictionary of tools provided to the language model to enable tool calling,
            if any. The dictionary maps the tool name to the tools themselves.
    """
    prompt_builder: Incomplete
    lm_invoker: Incomplete
    output_parser: Incomplete
    tool_dict: Incomplete
    def __init__(self, prompt_builder: BasePromptBuilder | MultimodalPromptBuilder, lm_invoker: BaseLMInvoker | BaseMultimodalLMInvoker, output_parser: BaseOutputParser | None = None) -> None:
        """Initializes a new instance of the LMRequestProcessor class.

        Args:
            prompt_builder (BasePromptBuilder | MultimodalPromptBuilder): The prompt builder used to format the prompt.
            lm_invoker (BaseLMInvoker | BaseMultimodalLMInvoker): The language model invoker that handles the model
                inference.
            output_parser (BaseOutputParser, optional): An optional parser to process the model's output.
                Defaults to None.

        WARNING: Support for MultimodalPromptBuilder is deprecated and will be removed in version 0.4.0.
        """
    async def process(self, prompt_kwargs: dict[str, Any], history: list[tuple[str, str]] | None = None, hyperparameters: dict[str, Any] | None = None, event_emitter: EventEmitter | None = None, system_multimodal_contents: list[Any] | None = None, user_multimodal_contents: list[Any] | None = None, auto_execute_tools: bool = True, max_lm_calls: int = 5) -> Any:
        """Processes a language model inference request.

        This method processes the language model inference request as follows:
        1. Assembling the prompt using the provided keyword arguments.
        2. Invoking the language model with the assembled prompt and optional hyperparameters.
        3. If `auto_execute_tools` is True, the method will automatically execute tools if the LM output includes
           tool calls.
        4. Optionally parsing the model's output using the output parser if provided.

        Args:
            prompt_kwargs (dict[str, Any]): A dictionary of arguments used to format the prompt.
            history (list[tuple[str, str]] | None, optional): A list of tuples representing the conversation history.
                Defaults to None.
            hyperparameters (dict[str, Any] | None, optional): A dictionary of hyperparameters for the model invocation.
                Defaults to None.
            event_emitter (EventEmitter | None, optional): An event emitter for streaming model outputs.
                Defaults to None.
            system_multimodal_contents (list[Any] | None, optional): A list of multimodal contents for the system
                message. Defaults to None.
            user_multimodal_contents (list[Any] | None, optional): A list of multimodal contents for the user message.
                Defaults to None.
            auto_execute_tools (bool, optional): Whether to automatically execute tools if the LM invokes output
                tool calls. Defaults to True.
            max_lm_calls (int, optional): The maximum number of times the language model can be invoked
                when `auto_execute_tools` is True. Defaults to 5.

        Returns:
            Any: The result of the language model invocation, optionally parsed by the output parser.
        """

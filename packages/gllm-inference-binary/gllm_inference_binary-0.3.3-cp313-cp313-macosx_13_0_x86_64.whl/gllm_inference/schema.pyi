from enum import StrEnum
from pydantic import BaseModel
from typing import Any

ResponseSchema = dict[str, Any] | type[BaseModel]
StructuredOutput = dict[str, Any] | BaseModel

class ToolCall(BaseModel):
    """Defines a tool call request when a language model decides to invoke a tool.

    Attributes:
        id (str): The ID of the tool call.
        name (str): The name of the tool.
        args (dict[str, Any]): The arguments of the tool call.
    """
    id: str
    name: str
    args: dict[str, Any]

class ToolResult(BaseModel):
    """Defines a tool result to be sent back to the language model.

    Attributes:
        id (str): The ID of the tool call.
        output (str): The output of the tool call.
    """
    id: str
    output: str

class Reasoning(BaseModel):
    """Defines a reasoning output when a language model is configured to use reasoning.

    Attributes:
        id (str): The ID of the reasoning output. Defaults to an empty string.
        reasoning (str): The reasoning text. Defaults to an empty string.
        type (str): The type of the reasoning output. Defaults to an empty string.
        data (str): The additional data of the reasoning output. Defaults to an empty string.
    """
    id: str
    reasoning: str
    type: str
    data: str

class TokenUsage(BaseModel):
    """Defines the token usage data structure of a language model.

    Attributes:
        input_tokens (int): The number of input tokens.
        output_tokens (int): The number of output tokens.
    """
    input_tokens: int
    output_tokens: int

class LMOutput(BaseModel):
    """Defines the output of a language model.

    Attributes:
        response (str): The text response. Defaults to an empty string.
        tool_calls (list[ToolCall]): The tool calls, if the language model decides to invoke tools.
            Defaults to an empty list.
        structured_output (StructuredOutput | None): The structured output, if a response schema is defined
            for the language model. Defaults to None.
        token_usage (TokenUsage | None): The token usage analytics, if requested. Defaults to None.
        duration (float | None): The duration of the invocation in seconds, if requested. Defaults to None.
        finish_details (dict[str, Any]): The details about how the generation finished, if requested.
            Defaults to an empty dictionary.
        reasoning (list[Reasoning]): The reasoning, if the language model is configured to output reasoning.
            Defaults to an empty list.
    """
    response: str
    tool_calls: list[ToolCall]
    structured_output: StructuredOutput | None
    token_usage: TokenUsage | None
    duration: float | None
    finish_details: dict[str, Any]
    reasoning: list[Reasoning]

class PromptRole(StrEnum):
    """Defines valid prompt roles."""
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'

class MimeType(StrEnum):
    """Defines valid mime types."""
    AUDIO = 'audio'
    DOCUMENT = 'document'
    IMAGE = 'image'
    VIDEO = 'video'

ANY_EXTENSION: str
UnimodalContent = str | list[str | ToolCall] | list[ToolResult]
UnimodalPrompt = list[tuple[PromptRole, UnimodalContent]]
MultimodalContent = str | bytes | ToolCall | ToolResult | Reasoning
MultimodalPrompt = list[tuple[PromptRole, list[MultimodalContent]]]
MultimodalOutput = str | LMOutput

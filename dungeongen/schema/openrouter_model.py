from typing import Optional, Union
from pydantic import BaseModel


class FunctionCall(BaseModel):
    name: str
    arguments: str  # JSON format arguments


class ToolCall(BaseModel):
    id: str
    type: str  # 'function'
    function: FunctionCall


class NonChatChoice(BaseModel):
    finish_reason: Optional[str] = None
    text: str


class Message(BaseModel):
    content: Optional[str] = None
    role: str
    tool_calls: Optional[list[ToolCall]] = None
    function_call: Optional[FunctionCall] = None


class NonStreamingChoice(BaseModel):
    finish_reason: Optional[str] = None
    message: Message


class Delta(BaseModel):
    content: Optional[str] = None
    role: Optional[str] = None
    tool_calls: Optional[list[ToolCall]] = None
    function_call: Optional[FunctionCall] = None


class StreamingChoice(BaseModel):
    finish_reason: Optional[str] = None
    delta: Delta


class Error(BaseModel):
    code: int
    message: str


class OpenRouterResponse(BaseModel):
    id: str
    choices: list[dict[str, str]]
    created: int
    model: str
    object: str
    usage: Optional[dict[str, int]] = None


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    total_cost: float


class Response(BaseModel):
    id: str
    choices: list[Union[NonStreamingChoice, StreamingChoice, NonChatChoice, Error]]
    created: int  # Unix timestamp
    model: str
    object: str  # 'chat.completion' or 'chat.completion.chunk'
    usage: Optional[Usage] = None

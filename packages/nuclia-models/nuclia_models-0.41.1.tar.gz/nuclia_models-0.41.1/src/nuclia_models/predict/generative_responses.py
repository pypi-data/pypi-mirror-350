from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field

GenerativeResponseType = Literal["text", "object", "meta", "citations", "status"]


class TextGenerativeResponse(BaseModel):
    type: Literal["text"] = "text"
    text: str


class JSONGenerativeResponse(BaseModel):
    type: Literal["object"] = "object"
    object: dict[str, Any]


class MetaGenerativeResponse(BaseModel):
    type: Literal["meta"] = "meta"
    input_tokens: int
    output_tokens: int
    timings: dict[str, float]
    input_nuclia_tokens: Optional[float] = None
    output_nuclia_tokens: Optional[float] = None


class CitationsGenerativeResponse(BaseModel):
    type: Literal["citations"] = "citations"
    citations: dict[str, Any]


class RerankGenerativeResponse(BaseModel):
    type: Literal["rerank"] = "rerank"
    context_scores: dict[str, float]


class StatusGenerativeResponse(BaseModel):
    type: Literal["status"] = "status"
    code: str
    details: Optional[str] = None


class CallArguments(BaseModel):
    name: Optional[str]
    arguments: dict[str, Any]


class ToolCall(BaseModel):
    function: CallArguments
    id: Optional[str] = None


class ToolsGenerativeResponse(BaseModel):
    type: Literal["tools"] = "tools"
    tools: dict[str, list[ToolCall]]


GenerativeResponse = Union[
    TextGenerativeResponse,
    JSONGenerativeResponse,
    MetaGenerativeResponse,
    CitationsGenerativeResponse,
    StatusGenerativeResponse,
    RerankGenerativeResponse,
    ToolsGenerativeResponse,
]


class GenerativeChunk(BaseModel):
    chunk: GenerativeResponse = Field(..., discriminator="type")


class GenerativeFullResponse(BaseModel):
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    timings: Optional[dict[str, float]] = None
    citations: Optional[dict[str, Any]] = None
    code: Optional[str] = None
    details: Optional[str] = None
    answer: str
    object: Optional[dict[str, Any]] = None
    input_nuclia_tokens: Optional[float] = None
    output_nuclia_tokens: Optional[float] = None
    tools: Optional[dict[str, list[ToolCall]]] = None

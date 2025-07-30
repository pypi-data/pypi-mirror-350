# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ChatCreateCompletionParams", "Message", "ResponseFormat"]


class ChatCreateCompletionParams(TypedDict, total=False):
    frequency_penalty: Required[float]

    max_completion_tokens: Required[Optional[int]]

    messages: Required[Iterable[Message]]

    model: Required[str]

    presence_penalty: Required[float]

    stream: Required[bool]

    temperature: Required[Optional[float]]

    top_p: Required[Optional[float]]

    response_format: ResponseFormat

    seed: int

    stop: Union[str, List[str]]


class Message(TypedDict, total=False):
    role: Required[Literal["system", "user", "assistant", "tool"]]

    content: None


class ResponseFormat(TypedDict, total=False):
    json_schema: Required[Dict[str, object]]

    type: Required[Literal["text", "json_schema"]]

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .chat import (
    ChatResource,
    AsyncChatResource,
    ChatResourceWithRawResponse,
    AsyncChatResourceWithRawResponse,
    ChatResourceWithStreamingResponse,
    AsyncChatResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["InternalResource", "AsyncInternalResource"]


class InternalResource(SyncAPIResource):
    @cached_property
    def chat(self) -> ChatResource:
        return ChatResource(self._client)

    @cached_property
    def with_raw_response(self) -> InternalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/premAI-io/prem-py-sdk#accessing-raw-response-data-eg-headers
        """
        return InternalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InternalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/premAI-io/prem-py-sdk#with_streaming_response
        """
        return InternalResourceWithStreamingResponse(self)


class AsyncInternalResource(AsyncAPIResource):
    @cached_property
    def chat(self) -> AsyncChatResource:
        return AsyncChatResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncInternalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/premAI-io/prem-py-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncInternalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInternalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/premAI-io/prem-py-sdk#with_streaming_response
        """
        return AsyncInternalResourceWithStreamingResponse(self)


class InternalResourceWithRawResponse:
    def __init__(self, internal: InternalResource) -> None:
        self._internal = internal

    @cached_property
    def chat(self) -> ChatResourceWithRawResponse:
        return ChatResourceWithRawResponse(self._internal.chat)


class AsyncInternalResourceWithRawResponse:
    def __init__(self, internal: AsyncInternalResource) -> None:
        self._internal = internal

    @cached_property
    def chat(self) -> AsyncChatResourceWithRawResponse:
        return AsyncChatResourceWithRawResponse(self._internal.chat)


class InternalResourceWithStreamingResponse:
    def __init__(self, internal: InternalResource) -> None:
        self._internal = internal

    @cached_property
    def chat(self) -> ChatResourceWithStreamingResponse:
        return ChatResourceWithStreamingResponse(self._internal.chat)


class AsyncInternalResourceWithStreamingResponse:
    def __init__(self, internal: AsyncInternalResource) -> None:
        self._internal = internal

    @cached_property
    def chat(self) -> AsyncChatResourceWithStreamingResponse:
        return AsyncChatResourceWithStreamingResponse(self._internal.chat)

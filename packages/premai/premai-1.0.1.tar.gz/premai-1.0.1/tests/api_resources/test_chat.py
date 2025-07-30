# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from premai import Premai, AsyncPremai
from tests.utils import assert_matches_type
from premai.types import ChatRetrieveModelsResponse, ChatCreateCompletionResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChat:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_completion(self, client: Premai) -> None:
        chat = client.chat.create_completion(
            frequency_penalty=-2,
            max_completion_tokens=1,
            messages=[{"role": "system"}],
            model="model",
            presence_penalty=-2,
            stream=True,
            temperature=0,
            top_p=0,
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_completion_with_all_params(self, client: Premai) -> None:
        chat = client.chat.create_completion(
            frequency_penalty=-2,
            max_completion_tokens=1,
            messages=[
                {
                    "role": "system",
                    "content": None,
                }
            ],
            model="model",
            presence_penalty=-2,
            stream=True,
            temperature=0,
            top_p=0,
            response_format={
                "json_schema": {"foo": "bar"},
                "type": "text",
            },
            seed=0,
            stop="string",
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_completion(self, client: Premai) -> None:
        response = client.chat.with_raw_response.create_completion(
            frequency_penalty=-2,
            max_completion_tokens=1,
            messages=[{"role": "system"}],
            model="model",
            presence_penalty=-2,
            stream=True,
            temperature=0,
            top_p=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_completion(self, client: Premai) -> None:
        with client.chat.with_streaming_response.create_completion(
            frequency_penalty=-2,
            max_completion_tokens=1,
            messages=[{"role": "system"}],
            model="model",
            presence_penalty=-2,
            stream=True,
            temperature=0,
            top_p=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_internal_models(self, client: Premai) -> None:
        chat = client.chat.retrieve_internal_models()
        assert_matches_type(object, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_internal_models(self, client: Premai) -> None:
        response = client.chat.with_raw_response.retrieve_internal_models()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(object, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_internal_models(self, client: Premai) -> None:
        with client.chat.with_streaming_response.retrieve_internal_models() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(object, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_models(self, client: Premai) -> None:
        chat = client.chat.retrieve_models()
        assert_matches_type(ChatRetrieveModelsResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_models(self, client: Premai) -> None:
        response = client.chat.with_raw_response.retrieve_models()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatRetrieveModelsResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_models(self, client: Premai) -> None:
        with client.chat.with_streaming_response.retrieve_models() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatRetrieveModelsResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChat:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_completion(self, async_client: AsyncPremai) -> None:
        chat = await async_client.chat.create_completion(
            frequency_penalty=-2,
            max_completion_tokens=1,
            messages=[{"role": "system"}],
            model="model",
            presence_penalty=-2,
            stream=True,
            temperature=0,
            top_p=0,
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_completion_with_all_params(self, async_client: AsyncPremai) -> None:
        chat = await async_client.chat.create_completion(
            frequency_penalty=-2,
            max_completion_tokens=1,
            messages=[
                {
                    "role": "system",
                    "content": None,
                }
            ],
            model="model",
            presence_penalty=-2,
            stream=True,
            temperature=0,
            top_p=0,
            response_format={
                "json_schema": {"foo": "bar"},
                "type": "text",
            },
            seed=0,
            stop="string",
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_completion(self, async_client: AsyncPremai) -> None:
        response = await async_client.chat.with_raw_response.create_completion(
            frequency_penalty=-2,
            max_completion_tokens=1,
            messages=[{"role": "system"}],
            model="model",
            presence_penalty=-2,
            stream=True,
            temperature=0,
            top_p=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_completion(self, async_client: AsyncPremai) -> None:
        async with async_client.chat.with_streaming_response.create_completion(
            frequency_penalty=-2,
            max_completion_tokens=1,
            messages=[{"role": "system"}],
            model="model",
            presence_penalty=-2,
            stream=True,
            temperature=0,
            top_p=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_internal_models(self, async_client: AsyncPremai) -> None:
        chat = await async_client.chat.retrieve_internal_models()
        assert_matches_type(object, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_internal_models(self, async_client: AsyncPremai) -> None:
        response = await async_client.chat.with_raw_response.retrieve_internal_models()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(object, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_internal_models(self, async_client: AsyncPremai) -> None:
        async with async_client.chat.with_streaming_response.retrieve_internal_models() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(object, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_models(self, async_client: AsyncPremai) -> None:
        chat = await async_client.chat.retrieve_models()
        assert_matches_type(ChatRetrieveModelsResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_models(self, async_client: AsyncPremai) -> None:
        response = await async_client.chat.with_raw_response.retrieve_models()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatRetrieveModelsResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_models(self, async_client: AsyncPremai) -> None:
        async with async_client.chat.with_streaming_response.retrieve_models() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatRetrieveModelsResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

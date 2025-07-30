# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import (
    APIKeyListResponse,
    APIKeyCreateResponse,
    APIKeyUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAPIKeys:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: FlowAISDK) -> None:
        api_key = client.api_keys.create(
            key_name="x",
        )
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: FlowAISDK) -> None:
        response = client.api_keys.with_raw_response.create(
            key_name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: FlowAISDK) -> None:
        with client.api_keys.with_streaming_response.create(
            key_name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: FlowAISDK) -> None:
        api_key = client.api_keys.update(
            key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(APIKeyUpdateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: FlowAISDK) -> None:
        api_key = client.api_keys.update(
            key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            is_active=True,
            key_name="key_name",
        )
        assert_matches_type(APIKeyUpdateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: FlowAISDK) -> None:
        response = client.api_keys.with_raw_response.update(
            key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyUpdateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: FlowAISDK) -> None:
        with client.api_keys.with_streaming_response.update(
            key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyUpdateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key_id` but received ''"):
            client.api_keys.with_raw_response.update(
                key_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: FlowAISDK) -> None:
        api_key = client.api_keys.list()
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: FlowAISDK) -> None:
        api_key = client.api_keys.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: FlowAISDK) -> None:
        response = client.api_keys.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: FlowAISDK) -> None:
        with client.api_keys.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyListResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: FlowAISDK) -> None:
        api_key = client.api_keys.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert api_key is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: FlowAISDK) -> None:
        response = client.api_keys.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert api_key is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: FlowAISDK) -> None:
        with client.api_keys.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert api_key is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key_id` but received ''"):
            client.api_keys.with_raw_response.delete(
                "",
            )


class TestAsyncAPIKeys:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncFlowAISDK) -> None:
        api_key = await async_client.api_keys.create(
            key_name="x",
        )
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api_keys.with_raw_response.create(
            key_name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api_keys.with_streaming_response.create(
            key_name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyCreateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncFlowAISDK) -> None:
        api_key = await async_client.api_keys.update(
            key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(APIKeyUpdateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        api_key = await async_client.api_keys.update(
            key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            is_active=True,
            key_name="key_name",
        )
        assert_matches_type(APIKeyUpdateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api_keys.with_raw_response.update(
            key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyUpdateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api_keys.with_streaming_response.update(
            key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyUpdateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key_id` but received ''"):
            await async_client.api_keys.with_raw_response.update(
                key_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncFlowAISDK) -> None:
        api_key = await async_client.api_keys.list()
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        api_key = await async_client.api_keys.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api_keys.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyListResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api_keys.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyListResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncFlowAISDK) -> None:
        api_key = await async_client.api_keys.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert api_key is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api_keys.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert api_key is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api_keys.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert api_key is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key_id` but received ''"):
            await async_client.api_keys.with_raw_response.delete(
                "",
            )

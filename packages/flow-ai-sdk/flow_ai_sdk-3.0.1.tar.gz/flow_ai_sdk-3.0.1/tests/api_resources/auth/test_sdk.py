# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types.auth import SDKLoginResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSDK:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_login(self, client: FlowAISDK) -> None:
        sdk = client.auth.sdk.login()
        assert_matches_type(SDKLoginResponse, sdk, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_login(self, client: FlowAISDK) -> None:
        response = client.auth.sdk.with_raw_response.login()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sdk = response.parse()
        assert_matches_type(SDKLoginResponse, sdk, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_login(self, client: FlowAISDK) -> None:
        with client.auth.sdk.with_streaming_response.login() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sdk = response.parse()
            assert_matches_type(SDKLoginResponse, sdk, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSDK:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_login(self, async_client: AsyncFlowAISDK) -> None:
        sdk = await async_client.auth.sdk.login()
        assert_matches_type(SDKLoginResponse, sdk, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_login(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.auth.sdk.with_raw_response.login()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sdk = await response.parse()
        assert_matches_type(SDKLoginResponse, sdk, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_login(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.auth.sdk.with_streaming_response.login() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sdk = await response.parse()
            assert_matches_type(SDKLoginResponse, sdk, path=["response"])

        assert cast(Any, response.is_closed) is True

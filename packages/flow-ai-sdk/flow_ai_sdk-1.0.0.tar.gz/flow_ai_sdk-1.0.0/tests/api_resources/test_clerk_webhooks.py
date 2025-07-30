# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClerkWebhooks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_handle_event(self, client: FlowAISDK) -> None:
        clerk_webhook = client.clerk_webhooks.handle_event()
        assert_matches_type(object, clerk_webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_handle_event_with_all_params(self, client: FlowAISDK) -> None:
        clerk_webhook = client.clerk_webhooks.handle_event(
            svix_id="svix-id",
            svix_signature="svix-signature",
            svix_timestamp="svix-timestamp",
        )
        assert_matches_type(object, clerk_webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_handle_event(self, client: FlowAISDK) -> None:
        response = client.clerk_webhooks.with_raw_response.handle_event()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        clerk_webhook = response.parse()
        assert_matches_type(object, clerk_webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_handle_event(self, client: FlowAISDK) -> None:
        with client.clerk_webhooks.with_streaming_response.handle_event() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            clerk_webhook = response.parse()
            assert_matches_type(object, clerk_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncClerkWebhooks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_handle_event(self, async_client: AsyncFlowAISDK) -> None:
        clerk_webhook = await async_client.clerk_webhooks.handle_event()
        assert_matches_type(object, clerk_webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_handle_event_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        clerk_webhook = await async_client.clerk_webhooks.handle_event(
            svix_id="svix-id",
            svix_signature="svix-signature",
            svix_timestamp="svix-timestamp",
        )
        assert_matches_type(object, clerk_webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_handle_event(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.clerk_webhooks.with_raw_response.handle_event()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        clerk_webhook = await response.parse()
        assert_matches_type(object, clerk_webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_handle_event(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.clerk_webhooks.with_streaming_response.handle_event() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            clerk_webhook = await response.parse()
            assert_matches_type(object, clerk_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

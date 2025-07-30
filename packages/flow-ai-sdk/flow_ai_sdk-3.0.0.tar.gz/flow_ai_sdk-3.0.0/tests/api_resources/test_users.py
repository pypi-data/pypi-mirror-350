# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_role(self, client: FlowAISDK) -> None:
        user = client.users.update_role(
            args={},
            kwargs={},
            role="user",
        )
        assert user is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_role(self, client: FlowAISDK) -> None:
        response = client.users.with_raw_response.update_role(
            args={},
            kwargs={},
            role="user",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert user is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_role(self, client: FlowAISDK) -> None:
        with client.users.with_streaming_response.update_role(
            args={},
            kwargs={},
            role="user",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert user is None

        assert cast(Any, response.is_closed) is True


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_role(self, async_client: AsyncFlowAISDK) -> None:
        user = await async_client.users.update_role(
            args={},
            kwargs={},
            role="user",
        )
        assert user is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_role(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.users.with_raw_response.update_role(
            args={},
            kwargs={},
            role="user",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert user is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_role(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.users.with_streaming_response.update_role(
            args={},
            kwargs={},
            role="user",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert user is None

        assert cast(Any, response.is_closed) is True

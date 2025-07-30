# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPrefect:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_webhook(self, client: FlowAISDK) -> None:
        prefect = client.integrations.prefect.create_webhook(
            flow_run={"prefect_flow_run_id": "prefect_flow_run_id"},
        )
        assert_matches_type(object, prefect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_webhook_with_all_params(self, client: FlowAISDK) -> None:
        prefect = client.integrations.prefect.create_webhook(
            flow_run={
                "prefect_flow_run_id": "prefect_flow_run_id",
                "prefect_flow_run_name": "prefect_flow_run_name",
                "state_message": "state_message",
                "state_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                "state_type": "state_type",
            },
            queue_name="queue_name",
        )
        assert_matches_type(object, prefect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_webhook(self, client: FlowAISDK) -> None:
        response = client.integrations.prefect.with_raw_response.create_webhook(
            flow_run={"prefect_flow_run_id": "prefect_flow_run_id"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prefect = response.parse()
        assert_matches_type(object, prefect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_webhook(self, client: FlowAISDK) -> None:
        with client.integrations.prefect.with_streaming_response.create_webhook(
            flow_run={"prefect_flow_run_id": "prefect_flow_run_id"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prefect = response.parse()
            assert_matches_type(object, prefect, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPrefect:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_webhook(self, async_client: AsyncFlowAISDK) -> None:
        prefect = await async_client.integrations.prefect.create_webhook(
            flow_run={"prefect_flow_run_id": "prefect_flow_run_id"},
        )
        assert_matches_type(object, prefect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_webhook_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        prefect = await async_client.integrations.prefect.create_webhook(
            flow_run={
                "prefect_flow_run_id": "prefect_flow_run_id",
                "prefect_flow_run_name": "prefect_flow_run_name",
                "state_message": "state_message",
                "state_timestamp": parse_datetime("2019-12-27T18:11:19.117Z"),
                "state_type": "state_type",
            },
            queue_name="queue_name",
        )
        assert_matches_type(object, prefect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_webhook(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.integrations.prefect.with_raw_response.create_webhook(
            flow_run={"prefect_flow_run_id": "prefect_flow_run_id"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prefect = await response.parse()
        assert_matches_type(object, prefect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_webhook(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.integrations.prefect.with_streaming_response.create_webhook(
            flow_run={"prefect_flow_run_id": "prefect_flow_run_id"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prefect = await response.parse()
            assert_matches_type(object, prefect, path=["response"])

        assert cast(Any, response.is_closed) is True

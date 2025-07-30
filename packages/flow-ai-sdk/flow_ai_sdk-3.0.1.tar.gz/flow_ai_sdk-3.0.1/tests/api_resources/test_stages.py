# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import io
import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import (
    StageDetails,
    StageListResponse,
    StageCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: FlowAISDK) -> None:
        stage = client.stages.create(
            files=[io.BytesIO(b"raw file contents")],
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            source_type="agent_rules",
        )
        assert_matches_type(StageCreateResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: FlowAISDK) -> None:
        response = client.stages.with_raw_response.create(
            files=[io.BytesIO(b"raw file contents")],
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            source_type="agent_rules",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = response.parse()
        assert_matches_type(StageCreateResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: FlowAISDK) -> None:
        with client.stages.with_streaming_response.create(
            files=[io.BytesIO(b"raw file contents")],
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            source_type="agent_rules",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = response.parse()
            assert_matches_type(StageCreateResponse, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: FlowAISDK) -> None:
        stage = client.stages.retrieve(
            0,
        )
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: FlowAISDK) -> None:
        response = client.stages.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = response.parse()
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: FlowAISDK) -> None:
        with client.stages.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = response.parse()
            assert_matches_type(StageDetails, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: FlowAISDK) -> None:
        stage = client.stages.update(
            stage_id=0,
        )
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: FlowAISDK) -> None:
        stage = client.stages.update(
            stage_id=0,
            original_filename="original_filename",
        )
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: FlowAISDK) -> None:
        response = client.stages.with_raw_response.update(
            stage_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = response.parse()
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: FlowAISDK) -> None:
        with client.stages.with_streaming_response.update(
            stage_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = response.parse()
            assert_matches_type(StageDetails, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: FlowAISDK) -> None:
        stage = client.stages.list()
        assert_matches_type(StageListResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: FlowAISDK) -> None:
        stage = client.stages.list(
            limit=0,
            skip=0,
        )
        assert_matches_type(StageListResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: FlowAISDK) -> None:
        response = client.stages.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = response.parse()
        assert_matches_type(StageListResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: FlowAISDK) -> None:
        with client.stages.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = response.parse()
            assert_matches_type(StageListResponse, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: FlowAISDK) -> None:
        stage = client.stages.delete(
            0,
        )
        assert_matches_type(object, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: FlowAISDK) -> None:
        response = client.stages.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = response.parse()
        assert_matches_type(object, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: FlowAISDK) -> None:
        with client.stages.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = response.parse()
            assert_matches_type(object, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_ping(self, client: FlowAISDK) -> None:
        stage = client.stages.ping()
        assert_matches_type(object, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_ping(self, client: FlowAISDK) -> None:
        response = client.stages.with_raw_response.ping()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = response.parse()
        assert_matches_type(object, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_ping(self, client: FlowAISDK) -> None:
        with client.stages.with_streaming_response.ping() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = response.parse()
            assert_matches_type(object, stage, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncStages:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncFlowAISDK) -> None:
        stage = await async_client.stages.create(
            files=[io.BytesIO(b"raw file contents")],
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            source_type="agent_rules",
        )
        assert_matches_type(StageCreateResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.stages.with_raw_response.create(
            files=[io.BytesIO(b"raw file contents")],
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            source_type="agent_rules",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = await response.parse()
        assert_matches_type(StageCreateResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.stages.with_streaming_response.create(
            files=[io.BytesIO(b"raw file contents")],
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            source_type="agent_rules",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = await response.parse()
            assert_matches_type(StageCreateResponse, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        stage = await async_client.stages.retrieve(
            0,
        )
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.stages.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = await response.parse()
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.stages.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = await response.parse()
            assert_matches_type(StageDetails, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncFlowAISDK) -> None:
        stage = await async_client.stages.update(
            stage_id=0,
        )
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        stage = await async_client.stages.update(
            stage_id=0,
            original_filename="original_filename",
        )
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.stages.with_raw_response.update(
            stage_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = await response.parse()
        assert_matches_type(StageDetails, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.stages.with_streaming_response.update(
            stage_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = await response.parse()
            assert_matches_type(StageDetails, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncFlowAISDK) -> None:
        stage = await async_client.stages.list()
        assert_matches_type(StageListResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        stage = await async_client.stages.list(
            limit=0,
            skip=0,
        )
        assert_matches_type(StageListResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.stages.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = await response.parse()
        assert_matches_type(StageListResponse, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.stages.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = await response.parse()
            assert_matches_type(StageListResponse, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncFlowAISDK) -> None:
        stage = await async_client.stages.delete(
            0,
        )
        assert_matches_type(object, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.stages.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = await response.parse()
        assert_matches_type(object, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.stages.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = await response.parse()
            assert_matches_type(object, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_ping(self, async_client: AsyncFlowAISDK) -> None:
        stage = await async_client.stages.ping()
        assert_matches_type(object, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_ping(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.stages.with_raw_response.ping()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stage = await response.parse()
        assert_matches_type(object, stage, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_ping(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.stages.with_streaming_response.ping() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stage = await response.parse()
            assert_matches_type(object, stage, path=["response"])

        assert cast(Any, response.is_closed) is True

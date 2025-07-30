# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import Job
from flow_ai_sdk.types.projects import JobListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: FlowAISDK) -> None:
        job = client.projects.jobs.create(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
        )
        assert_matches_type(Job, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: FlowAISDK) -> None:
        response = client.projects.jobs.with_raw_response.create(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(Job, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: FlowAISDK) -> None:
        with client.projects.jobs.with_streaming_response.create(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(Job, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.jobs.with_raw_response.create(
                project_id="",
                config={"foo": "bar"},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: FlowAISDK) -> None:
        job = client.projects.jobs.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: FlowAISDK) -> None:
        job = client.projects.jobs.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=1,
            offset=0,
            status="status",
        )
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: FlowAISDK) -> None:
        response = client.projects.jobs.with_raw_response.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: FlowAISDK) -> None:
        with client.projects.jobs.with_streaming_response.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(JobListResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.jobs.with_raw_response.list(
                project_id="",
            )


class TestAsyncJobs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncFlowAISDK) -> None:
        job = await async_client.projects.jobs.create(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
        )
        assert_matches_type(Job, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.jobs.with_raw_response.create(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(Job, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.jobs.with_streaming_response.create(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(Job, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.jobs.with_raw_response.create(
                project_id="",
                config={"foo": "bar"},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncFlowAISDK) -> None:
        job = await async_client.projects.jobs.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        job = await async_client.projects.jobs.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=1,
            offset=0,
            status="status",
        )
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.jobs.with_raw_response.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.jobs.with_streaming_response.list(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(JobListResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.jobs.with_raw_response.list(
                project_id="",
            )

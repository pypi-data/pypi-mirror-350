# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import (
    Project,
    ProjectListResponse,
    ProjectArchiveResponse,
    ProjectGetDatasetResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: FlowAISDK) -> None:
        project = client.projects.create(
            name="x",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: FlowAISDK) -> None:
        project = client.projects.create(
            name="x",
            description="description",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: FlowAISDK) -> None:
        response = client.projects.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: FlowAISDK) -> None:
        with client.projects.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(Project, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: FlowAISDK) -> None:
        project = client.projects.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: FlowAISDK) -> None:
        response = client.projects.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: FlowAISDK) -> None:
        with client.projects.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(Project, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: FlowAISDK) -> None:
        project = client.projects.update(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: FlowAISDK) -> None:
        project = client.projects.update(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            name="x",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: FlowAISDK) -> None:
        response = client.projects.with_raw_response.update(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: FlowAISDK) -> None:
        with client.projects.with_streaming_response.update(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(Project, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.with_raw_response.update(
                project_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: FlowAISDK) -> None:
        project = client.projects.list()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: FlowAISDK) -> None:
        project = client.projects.list(
            limit=1,
            offset=0,
            status="status",
        )
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: FlowAISDK) -> None:
        response = client.projects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: FlowAISDK) -> None:
        with client.projects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(ProjectListResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: FlowAISDK) -> None:
        project = client.projects.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert project is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: FlowAISDK) -> None:
        response = client.projects.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert project is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: FlowAISDK) -> None:
        with client.projects.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert project is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_archive(self, client: FlowAISDK) -> None:
        project = client.projects.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProjectArchiveResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_archive(self, client: FlowAISDK) -> None:
        response = client.projects.with_raw_response.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(ProjectArchiveResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_archive(self, client: FlowAISDK) -> None:
        with client.projects.with_streaming_response.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(ProjectArchiveResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_archive(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.with_raw_response.archive(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_dataset(self, client: FlowAISDK) -> None:
        project = client.projects.get_dataset(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProjectGetDatasetResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_dataset_with_all_params(self, client: FlowAISDK) -> None:
        project = client.projects.get_dataset(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            version="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProjectGetDatasetResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_dataset(self, client: FlowAISDK) -> None:
        response = client.projects.with_raw_response.get_dataset(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(ProjectGetDatasetResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_dataset(self, client: FlowAISDK) -> None:
        with client.projects.with_streaming_response.get_dataset(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(ProjectGetDatasetResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_dataset(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.with_raw_response.get_dataset(
                project_id="",
            )


class TestAsyncProjects:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.create(
            name="x",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.create(
            name="x",
            description="description",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(Project, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(Project, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.update(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.update(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            name="x",
        )
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.with_raw_response.update(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(Project, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.with_streaming_response.update(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(Project, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.with_raw_response.update(
                project_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.list()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.list(
            limit=1,
            offset=0,
            status="status",
        )
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(ProjectListResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert project is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert project is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert project is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_archive(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProjectArchiveResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.with_raw_response.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(ProjectArchiveResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.with_streaming_response.archive(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(ProjectArchiveResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_archive(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.with_raw_response.archive(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_dataset(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.get_dataset(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProjectGetDatasetResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_dataset_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        project = await async_client.projects.get_dataset(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            version="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ProjectGetDatasetResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_dataset(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.with_raw_response.get_dataset(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(ProjectGetDatasetResponse, project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_dataset(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.with_streaming_response.get_dataset(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(ProjectGetDatasetResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_dataset(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.with_raw_response.get_dataset(
                project_id="",
            )

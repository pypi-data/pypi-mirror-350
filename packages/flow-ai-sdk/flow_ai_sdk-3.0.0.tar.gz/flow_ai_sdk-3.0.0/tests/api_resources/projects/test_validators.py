# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types.projects import ProjectValidator, ValidatorListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestValidators:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: FlowAISDK) -> None:
        validator = client.projects.validators.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ValidatorListResponse, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: FlowAISDK) -> None:
        response = client.projects.validators.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = response.parse()
        assert_matches_type(ValidatorListResponse, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: FlowAISDK) -> None:
        with client.projects.validators.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = response.parse()
            assert_matches_type(ValidatorListResponse, validator, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.validators.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_add(self, client: FlowAISDK) -> None:
        validator = client.projects.validators.add(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            email="dev@stainless.com",
        )
        assert_matches_type(ProjectValidator, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_add(self, client: FlowAISDK) -> None:
        response = client.projects.validators.with_raw_response.add(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            email="dev@stainless.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = response.parse()
        assert_matches_type(ProjectValidator, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_add(self, client: FlowAISDK) -> None:
        with client.projects.validators.with_streaming_response.add(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            email="dev@stainless.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = response.parse()
            assert_matches_type(ProjectValidator, validator, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_add(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.validators.with_raw_response.add(
                project_id="",
                email="dev@stainless.com",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_remove(self, client: FlowAISDK) -> None:
        validator = client.projects.validators.remove(
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert validator is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_remove(self, client: FlowAISDK) -> None:
        response = client.projects.validators.with_raw_response.remove(
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = response.parse()
        assert validator is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_remove(self, client: FlowAISDK) -> None:
        with client.projects.validators.with_streaming_response.remove(
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = response.parse()
            assert validator is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_remove(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            client.projects.validators.with_raw_response.remove(
                validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                project_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validator_id` but received ''"):
            client.projects.validators.with_raw_response.remove(
                validator_id="",
                project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )


class TestAsyncValidators:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncFlowAISDK) -> None:
        validator = await async_client.projects.validators.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ValidatorListResponse, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.validators.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = await response.parse()
        assert_matches_type(ValidatorListResponse, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.validators.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = await response.parse()
            assert_matches_type(ValidatorListResponse, validator, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.validators.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_add(self, async_client: AsyncFlowAISDK) -> None:
        validator = await async_client.projects.validators.add(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            email="dev@stainless.com",
        )
        assert_matches_type(ProjectValidator, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_add(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.validators.with_raw_response.add(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            email="dev@stainless.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = await response.parse()
        assert_matches_type(ProjectValidator, validator, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.validators.with_streaming_response.add(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            email="dev@stainless.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = await response.parse()
            assert_matches_type(ProjectValidator, validator, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_add(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.validators.with_raw_response.add(
                project_id="",
                email="dev@stainless.com",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_remove(self, async_client: AsyncFlowAISDK) -> None:
        validator = await async_client.projects.validators.remove(
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert validator is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.projects.validators.with_raw_response.remove(
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validator = await response.parse()
        assert validator is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.projects.validators.with_streaming_response.remove(
            validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validator = await response.parse()
            assert validator is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_remove(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `project_id` but received ''"):
            await async_client.projects.validators.with_raw_response.remove(
                validator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                project_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validator_id` but received ''"):
            await async_client.projects.validators.with_raw_response.remove(
                validator_id="",
                project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

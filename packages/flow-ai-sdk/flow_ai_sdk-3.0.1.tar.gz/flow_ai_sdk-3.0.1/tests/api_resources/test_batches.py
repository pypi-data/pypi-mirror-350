# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import (
    BatchRead,
    BatchListMineResponse,
    BatchListTestcasesResponse,
    BatchRetrieveStatusResponse,
    BatchListValidationsResponse,
    BatchCreateValidationTaskResponse,
    BatchRetrieveValidationTaskResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBatches:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: FlowAISDK) -> None:
        batch = client.batches.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchRead, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: FlowAISDK) -> None:
        response = client.batches.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BatchRead, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: FlowAISDK) -> None:
        with client.batches.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BatchRead, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.batches.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: FlowAISDK) -> None:
        batch = client.batches.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert batch is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: FlowAISDK) -> None:
        response = client.batches.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert batch is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: FlowAISDK) -> None:
        with client.batches.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert batch is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.batches.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_validation_task(self, client: FlowAISDK) -> None:
        batch = client.batches.create_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchCreateValidationTaskResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_validation_task(self, client: FlowAISDK) -> None:
        response = client.batches.with_raw_response.create_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BatchCreateValidationTaskResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_validation_task(self, client: FlowAISDK) -> None:
        with client.batches.with_streaming_response.create_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BatchCreateValidationTaskResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_validation_task(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.batches.with_raw_response.create_validation_task(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list_mine(self, client: FlowAISDK) -> None:
        batch = client.batches.list_mine()
        assert_matches_type(BatchListMineResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_mine(self, client: FlowAISDK) -> None:
        response = client.batches.with_raw_response.list_mine()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BatchListMineResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_mine(self, client: FlowAISDK) -> None:
        with client.batches.with_streaming_response.list_mine() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BatchListMineResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list_testcases(self, client: FlowAISDK) -> None:
        batch = client.batches.list_testcases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchListTestcasesResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_testcases(self, client: FlowAISDK) -> None:
        response = client.batches.with_raw_response.list_testcases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BatchListTestcasesResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_testcases(self, client: FlowAISDK) -> None:
        with client.batches.with_streaming_response.list_testcases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BatchListTestcasesResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list_testcases(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.batches.with_raw_response.list_testcases(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list_validations(self, client: FlowAISDK) -> None:
        batch = client.batches.list_validations(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchListValidationsResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_validations(self, client: FlowAISDK) -> None:
        response = client.batches.with_raw_response.list_validations(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BatchListValidationsResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_validations(self, client: FlowAISDK) -> None:
        with client.batches.with_streaming_response.list_validations(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BatchListValidationsResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list_validations(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.batches.with_raw_response.list_validations(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_status(self, client: FlowAISDK) -> None:
        batch = client.batches.retrieve_status(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchRetrieveStatusResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_status(self, client: FlowAISDK) -> None:
        response = client.batches.with_raw_response.retrieve_status(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BatchRetrieveStatusResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_status(self, client: FlowAISDK) -> None:
        with client.batches.with_streaming_response.retrieve_status(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BatchRetrieveStatusResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_status(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.batches.with_raw_response.retrieve_status(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_validation_task(self, client: FlowAISDK) -> None:
        batch = client.batches.retrieve_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchRetrieveValidationTaskResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_validation_task(self, client: FlowAISDK) -> None:
        response = client.batches.with_raw_response.retrieve_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(BatchRetrieveValidationTaskResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_validation_task(self, client: FlowAISDK) -> None:
        with client.batches.with_streaming_response.retrieve_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(BatchRetrieveValidationTaskResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_validation_task(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.batches.with_raw_response.retrieve_validation_task(
                "",
            )


class TestAsyncBatches:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        batch = await async_client.batches.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchRead, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.batches.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(BatchRead, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.batches.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BatchRead, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.batches.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncFlowAISDK) -> None:
        batch = await async_client.batches.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert batch is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.batches.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert batch is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.batches.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert batch is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.batches.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_validation_task(self, async_client: AsyncFlowAISDK) -> None:
        batch = await async_client.batches.create_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchCreateValidationTaskResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_validation_task(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.batches.with_raw_response.create_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(BatchCreateValidationTaskResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_validation_task(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.batches.with_streaming_response.create_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BatchCreateValidationTaskResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_validation_task(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.batches.with_raw_response.create_validation_task(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_mine(self, async_client: AsyncFlowAISDK) -> None:
        batch = await async_client.batches.list_mine()
        assert_matches_type(BatchListMineResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_mine(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.batches.with_raw_response.list_mine()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(BatchListMineResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_mine(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.batches.with_streaming_response.list_mine() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BatchListMineResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_testcases(self, async_client: AsyncFlowAISDK) -> None:
        batch = await async_client.batches.list_testcases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchListTestcasesResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_testcases(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.batches.with_raw_response.list_testcases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(BatchListTestcasesResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_testcases(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.batches.with_streaming_response.list_testcases(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BatchListTestcasesResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list_testcases(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.batches.with_raw_response.list_testcases(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_validations(self, async_client: AsyncFlowAISDK) -> None:
        batch = await async_client.batches.list_validations(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchListValidationsResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_validations(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.batches.with_raw_response.list_validations(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(BatchListValidationsResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_validations(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.batches.with_streaming_response.list_validations(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BatchListValidationsResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list_validations(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.batches.with_raw_response.list_validations(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_status(self, async_client: AsyncFlowAISDK) -> None:
        batch = await async_client.batches.retrieve_status(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchRetrieveStatusResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_status(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.batches.with_raw_response.retrieve_status(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(BatchRetrieveStatusResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_status(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.batches.with_streaming_response.retrieve_status(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BatchRetrieveStatusResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_status(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.batches.with_raw_response.retrieve_status(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_validation_task(self, async_client: AsyncFlowAISDK) -> None:
        batch = await async_client.batches.retrieve_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchRetrieveValidationTaskResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_validation_task(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.batches.with_raw_response.retrieve_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(BatchRetrieveValidationTaskResponse, batch, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_validation_task(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.batches.with_streaming_response.retrieve_validation_task(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(BatchRetrieveValidationTaskResponse, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_validation_task(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.batches.with_raw_response.retrieve_validation_task(
                "",
            )

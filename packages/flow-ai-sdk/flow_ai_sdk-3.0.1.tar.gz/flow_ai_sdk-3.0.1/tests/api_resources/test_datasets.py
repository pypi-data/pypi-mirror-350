# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import DatasetRetrieveItemsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDatasets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: FlowAISDK) -> None:
        dataset = client.datasets.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert dataset is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: FlowAISDK) -> None:
        response = client.datasets.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert dataset is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: FlowAISDK) -> None:
        with client.datasets.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert dataset is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_items(self, client: FlowAISDK) -> None:
        dataset = client.datasets.retrieve_items(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DatasetRetrieveItemsResponse, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_items_with_all_params(self, client: FlowAISDK) -> None:
        dataset = client.datasets.retrieve_items(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=1,
            offset=0,
        )
        assert_matches_type(DatasetRetrieveItemsResponse, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_items(self, client: FlowAISDK) -> None:
        response = client.datasets.with_raw_response.retrieve_items(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetRetrieveItemsResponse, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_items(self, client: FlowAISDK) -> None:
        with client.datasets.with_streaming_response.retrieve_items(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetRetrieveItemsResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_items(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            client.datasets.with_raw_response.retrieve_items(
                dataset_id="",
            )


class TestAsyncDatasets:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncFlowAISDK) -> None:
        dataset = await async_client.datasets.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert dataset is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.datasets.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert dataset is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.datasets.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert dataset is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_items(self, async_client: AsyncFlowAISDK) -> None:
        dataset = await async_client.datasets.retrieve_items(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DatasetRetrieveItemsResponse, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_items_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        dataset = await async_client.datasets.retrieve_items(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=1,
            offset=0,
        )
        assert_matches_type(DatasetRetrieveItemsResponse, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_items(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.datasets.with_raw_response.retrieve_items(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetRetrieveItemsResponse, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_items(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.datasets.with_streaming_response.retrieve_items(
            dataset_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetRetrieveItemsResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_items(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dataset_id` but received ''"):
            await async_client.datasets.with_raw_response.retrieve_items(
                dataset_id="",
            )

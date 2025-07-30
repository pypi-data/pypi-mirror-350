# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import (
    TestCase,
    TestCaseListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTestCases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: FlowAISDK) -> None:
        test_case = client.test_cases.create(
            expected_output="expected_output",
            status="status",
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: FlowAISDK) -> None:
        test_case = client.test_cases.create(
            expected_output="expected_output",
            status="status",
            api_key_user_id="api_key_user_id",
            description="description",
            is_active=True,
            name="name",
            trajectory=[
                {
                    "content": "content",
                    "order": 0,
                    "role": "role",
                    "type": "message",
                }
            ],
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: FlowAISDK) -> None:
        response = client.test_cases.with_raw_response.create(
            expected_output="expected_output",
            status="status",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: FlowAISDK) -> None:
        with client.test_cases.with_streaming_response.create(
            expected_output="expected_output",
            status="status",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: FlowAISDK) -> None:
        test_case = client.test_cases.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: FlowAISDK) -> None:
        response = client.test_cases.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: FlowAISDK) -> None:
        with client.test_cases.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.test_cases.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: FlowAISDK) -> None:
        test_case = client.test_cases.update(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={"foo": "bar"},
            test_case_in={},
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: FlowAISDK) -> None:
        test_case = client.test_cases.update(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={"foo": "bar"},
            test_case_in={
                "description": "description",
                "expected_output": "expected_output",
                "is_active": True,
                "name": "name",
                "status": "status",
            },
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: FlowAISDK) -> None:
        response = client.test_cases.with_raw_response.update(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={"foo": "bar"},
            test_case_in={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: FlowAISDK) -> None:
        with client.test_cases.with_streaming_response.update(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={"foo": "bar"},
            test_case_in={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.test_cases.with_raw_response.update(
                test_case_id="",
                current_user_payload={"foo": "bar"},
                test_case_in={},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: FlowAISDK) -> None:
        test_case = client.test_cases.list()
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: FlowAISDK) -> None:
        test_case = client.test_cases.list(
            batch_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_after="created_after",
            created_before="created_before",
            limit=1,
            name="name",
            skip=0,
            sort_by="sort_by",
            sort_order="sort_order",
            status="status",
        )
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: FlowAISDK) -> None:
        response = client.test_cases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: FlowAISDK) -> None:
        with client.test_cases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCaseListResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: FlowAISDK) -> None:
        test_case = client.test_cases.delete(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            body={"foo": "bar"},
        )
        assert test_case is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: FlowAISDK) -> None:
        response = client.test_cases.with_raw_response.delete(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            body={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert test_case is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: FlowAISDK) -> None:
        with client.test_cases.with_streaming_response.delete(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            body={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert test_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.test_cases.with_raw_response.delete(
                test_case_id="",
                body={"foo": "bar"},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_validation(self, client: FlowAISDK) -> None:
        test_case = client.test_cases.get_validation(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_validation(self, client: FlowAISDK) -> None:
        response = client.test_cases.with_raw_response.get_validation(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(object, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_validation(self, client: FlowAISDK) -> None:
        with client.test_cases.with_streaming_response.get_validation(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(object, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_validation(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            client.test_cases.with_raw_response.get_validation(
                "",
            )


class TestAsyncTestCases:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncFlowAISDK) -> None:
        test_case = await async_client.test_cases.create(
            expected_output="expected_output",
            status="status",
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        test_case = await async_client.test_cases.create(
            expected_output="expected_output",
            status="status",
            api_key_user_id="api_key_user_id",
            description="description",
            is_active=True,
            name="name",
            trajectory=[
                {
                    "content": "content",
                    "order": 0,
                    "role": "role",
                    "type": "message",
                }
            ],
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.test_cases.with_raw_response.create(
            expected_output="expected_output",
            status="status",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.test_cases.with_streaming_response.create(
            expected_output="expected_output",
            status="status",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        test_case = await async_client.test_cases.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.test_cases.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.test_cases.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.test_cases.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncFlowAISDK) -> None:
        test_case = await async_client.test_cases.update(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={"foo": "bar"},
            test_case_in={},
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        test_case = await async_client.test_cases.update(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={"foo": "bar"},
            test_case_in={
                "description": "description",
                "expected_output": "expected_output",
                "is_active": True,
                "name": "name",
                "status": "status",
            },
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.test_cases.with_raw_response.update(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={"foo": "bar"},
            test_case_in={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.test_cases.with_streaming_response.update(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={"foo": "bar"},
            test_case_in={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.test_cases.with_raw_response.update(
                test_case_id="",
                current_user_payload={"foo": "bar"},
                test_case_in={},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncFlowAISDK) -> None:
        test_case = await async_client.test_cases.list()
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        test_case = await async_client.test_cases.list(
            batch_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            created_after="created_after",
            created_before="created_before",
            limit=1,
            name="name",
            skip=0,
            sort_by="sort_by",
            sort_order="sort_order",
            status="status",
        )
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.test_cases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCaseListResponse, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.test_cases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCaseListResponse, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncFlowAISDK) -> None:
        test_case = await async_client.test_cases.delete(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            body={"foo": "bar"},
        )
        assert test_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.test_cases.with_raw_response.delete(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            body={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert test_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.test_cases.with_streaming_response.delete(
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            body={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert test_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.test_cases.with_raw_response.delete(
                test_case_id="",
                body={"foo": "bar"},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_validation(self, async_client: AsyncFlowAISDK) -> None:
        test_case = await async_client.test_cases.get_validation(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_validation(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.test_cases.with_raw_response.get_validation(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(object, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_validation(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.test_cases.with_streaming_response.get_validation(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(object, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_validation(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `test_case_id` but received ''"):
            await async_client.test_cases.with_raw_response.get_validation(
                "",
            )

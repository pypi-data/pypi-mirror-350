# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types import (
    TestCaseValidation,
    ValidationListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestValidations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: FlowAISDK) -> None:
        validation = client.validations.create(
            current_user_payload={},
            is_accepted=True,
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: FlowAISDK) -> None:
        validation = client.validations.create(
            current_user_payload={},
            is_accepted=True,
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            feedback="feedback",
            item_feedbacks=[
                {
                    "item_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "feedback": "feedback",
                }
            ],
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: FlowAISDK) -> None:
        response = client.validations.with_raw_response.create(
            current_user_payload={},
            is_accepted=True,
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = response.parse()
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: FlowAISDK) -> None:
        with client.validations.with_streaming_response.create(
            current_user_payload={},
            is_accepted=True,
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = response.parse()
            assert_matches_type(TestCaseValidation, validation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: FlowAISDK) -> None:
        validation = client.validations.retrieve(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: FlowAISDK) -> None:
        response = client.validations.with_raw_response.retrieve(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = response.parse()
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: FlowAISDK) -> None:
        with client.validations.with_streaming_response.retrieve(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = response.parse()
            assert_matches_type(TestCaseValidation, validation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_id` but received ''"):
            client.validations.with_raw_response.retrieve(
                validation_id="",
                current_user_payload={},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: FlowAISDK) -> None:
        validation = client.validations.update(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: FlowAISDK) -> None:
        validation = client.validations.update(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
            feedback="feedback",
            is_accepted=True,
            item_feedbacks=[
                {
                    "item_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "feedback": "feedback",
                }
            ],
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: FlowAISDK) -> None:
        response = client.validations.with_raw_response.update(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = response.parse()
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: FlowAISDK) -> None:
        with client.validations.with_streaming_response.update(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = response.parse()
            assert_matches_type(TestCaseValidation, validation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_id` but received ''"):
            client.validations.with_raw_response.update(
                validation_id="",
                current_user_payload={},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: FlowAISDK) -> None:
        validation = client.validations.list(
            current_user_payload={},
        )
        assert_matches_type(ValidationListResponse, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: FlowAISDK) -> None:
        validation = client.validations.list(
            current_user_payload={},
            created_after="created_after",
            created_before="created_before",
            is_accepted=True,
            limit=1,
            skip=0,
            sort_by="sort_by",
            sort_order="sort_order",
            test_case_id="test_case_id",
            validator_id="validator_id",
        )
        assert_matches_type(ValidationListResponse, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: FlowAISDK) -> None:
        response = client.validations.with_raw_response.list(
            current_user_payload={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = response.parse()
        assert_matches_type(ValidationListResponse, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: FlowAISDK) -> None:
        with client.validations.with_streaming_response.list(
            current_user_payload={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = response.parse()
            assert_matches_type(ValidationListResponse, validation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: FlowAISDK) -> None:
        validation = client.validations.delete(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )
        assert validation is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: FlowAISDK) -> None:
        response = client.validations.with_raw_response.delete(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = response.parse()
        assert validation is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: FlowAISDK) -> None:
        with client.validations.with_streaming_response.delete(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = response.parse()
            assert validation is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_id` but received ''"):
            client.validations.with_raw_response.delete(
                validation_id="",
                current_user_payload={},
            )


class TestAsyncValidations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncFlowAISDK) -> None:
        validation = await async_client.validations.create(
            current_user_payload={},
            is_accepted=True,
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        validation = await async_client.validations.create(
            current_user_payload={},
            is_accepted=True,
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            feedback="feedback",
            item_feedbacks=[
                {
                    "item_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "feedback": "feedback",
                }
            ],
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.validations.with_raw_response.create(
            current_user_payload={},
            is_accepted=True,
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = await response.parse()
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.validations.with_streaming_response.create(
            current_user_payload={},
            is_accepted=True,
            test_case_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validation_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            validator_task_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = await response.parse()
            assert_matches_type(TestCaseValidation, validation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        validation = await async_client.validations.retrieve(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.validations.with_raw_response.retrieve(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = await response.parse()
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.validations.with_streaming_response.retrieve(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = await response.parse()
            assert_matches_type(TestCaseValidation, validation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_id` but received ''"):
            await async_client.validations.with_raw_response.retrieve(
                validation_id="",
                current_user_payload={},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncFlowAISDK) -> None:
        validation = await async_client.validations.update(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        validation = await async_client.validations.update(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
            feedback="feedback",
            is_accepted=True,
            item_feedbacks=[
                {
                    "item_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "feedback": "feedback",
                }
            ],
        )
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.validations.with_raw_response.update(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = await response.parse()
        assert_matches_type(TestCaseValidation, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.validations.with_streaming_response.update(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = await response.parse()
            assert_matches_type(TestCaseValidation, validation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_id` but received ''"):
            await async_client.validations.with_raw_response.update(
                validation_id="",
                current_user_payload={},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncFlowAISDK) -> None:
        validation = await async_client.validations.list(
            current_user_payload={},
        )
        assert_matches_type(ValidationListResponse, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        validation = await async_client.validations.list(
            current_user_payload={},
            created_after="created_after",
            created_before="created_before",
            is_accepted=True,
            limit=1,
            skip=0,
            sort_by="sort_by",
            sort_order="sort_order",
            test_case_id="test_case_id",
            validator_id="validator_id",
        )
        assert_matches_type(ValidationListResponse, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.validations.with_raw_response.list(
            current_user_payload={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = await response.parse()
        assert_matches_type(ValidationListResponse, validation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.validations.with_streaming_response.list(
            current_user_payload={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = await response.parse()
            assert_matches_type(ValidationListResponse, validation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncFlowAISDK) -> None:
        validation = await async_client.validations.delete(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )
        assert validation is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.validations.with_raw_response.delete(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validation = await response.parse()
        assert validation is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.validations.with_streaming_response.delete(
            validation_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_payload={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validation = await response.parse()
            assert validation is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_id` but received ''"):
            await async_client.validations.with_raw_response.delete(
                validation_id="",
                current_user_payload={},
            )

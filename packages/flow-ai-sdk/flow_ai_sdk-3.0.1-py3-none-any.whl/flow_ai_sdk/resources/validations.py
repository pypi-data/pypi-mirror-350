# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

import httpx

from ..types import (
    validation_list_params,
    validation_create_params,
    validation_delete_params,
    validation_update_params,
    validation_retrieve_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.test_case_validation import TestCaseValidation
from ..types.validation_list_response import ValidationListResponse
from ..types.validation_item_feedback_param import ValidationItemFeedbackParam

__all__ = ["ValidationsResource", "AsyncValidationsResource"]


class ValidationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ValidationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return ValidationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ValidationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return ValidationsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        current_user_payload: object,
        is_accepted: bool,
        test_case_id: str,
        validation_task_id: str,
        validator_task_id: str,
        feedback: Optional[str] | NotGiven = NOT_GIVEN,
        item_feedbacks: Optional[Iterable[ValidationItemFeedbackParam]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseValidation:
        """
        Create Test Case Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/validations",
            body=maybe_transform(
                {
                    "is_accepted": is_accepted,
                    "test_case_id": test_case_id,
                    "validation_task_id": validation_task_id,
                    "validator_task_id": validator_task_id,
                    "feedback": feedback,
                    "item_feedbacks": item_feedbacks,
                },
                validation_create_params.ValidationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"current_user_payload": current_user_payload}, validation_create_params.ValidationCreateParams
                ),
            ),
            cast_to=TestCaseValidation,
        )

    def retrieve(
        self,
        validation_id: str,
        *,
        current_user_payload: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseValidation:
        """
        Get Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return self._get(
            f"/validations/{validation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"current_user_payload": current_user_payload}, validation_retrieve_params.ValidationRetrieveParams
                ),
            ),
            cast_to=TestCaseValidation,
        )

    def update(
        self,
        validation_id: str,
        *,
        current_user_payload: object,
        feedback: Optional[str] | NotGiven = NOT_GIVEN,
        is_accepted: Optional[bool] | NotGiven = NOT_GIVEN,
        item_feedbacks: Optional[Iterable[ValidationItemFeedbackParam]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseValidation:
        """
        Update Test Case Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return self._put(
            f"/validations/{validation_id}",
            body=maybe_transform(
                {
                    "feedback": feedback,
                    "is_accepted": is_accepted,
                    "item_feedbacks": item_feedbacks,
                },
                validation_update_params.ValidationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"current_user_payload": current_user_payload}, validation_update_params.ValidationUpdateParams
                ),
            ),
            cast_to=TestCaseValidation,
        )

    def list(
        self,
        *,
        current_user_payload: object,
        created_after: Optional[str] | NotGiven = NOT_GIVEN,
        created_before: Optional[str] | NotGiven = NOT_GIVEN,
        is_accepted: Optional[bool] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
        sort_by: Optional[str] | NotGiven = NOT_GIVEN,
        sort_order: str | NotGiven = NOT_GIVEN,
        test_case_id: Optional[str] | NotGiven = NOT_GIVEN,
        validator_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationListResponse:
        """
        List Validations

        Args:
          created_after: Filter by creation date (ISO format)

          created_before: Filter by creation date (ISO format)

          is_accepted: Filter by acceptance status

          sort_by: Field to sort by

          sort_order: Sort direction (asc or desc)

          test_case_id: Filter by test case ID

          validator_id: Filter by validator user ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/validations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "current_user_payload": current_user_payload,
                        "created_after": created_after,
                        "created_before": created_before,
                        "is_accepted": is_accepted,
                        "limit": limit,
                        "skip": skip,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "test_case_id": test_case_id,
                        "validator_id": validator_id,
                    },
                    validation_list_params.ValidationListParams,
                ),
            ),
            cast_to=ValidationListResponse,
        )

    def delete(
        self,
        validation_id: str,
        *,
        current_user_payload: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/validations/{validation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"current_user_payload": current_user_payload}, validation_delete_params.ValidationDeleteParams
                ),
            ),
            cast_to=NoneType,
        )


class AsyncValidationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncValidationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncValidationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncValidationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncValidationsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        current_user_payload: object,
        is_accepted: bool,
        test_case_id: str,
        validation_task_id: str,
        validator_task_id: str,
        feedback: Optional[str] | NotGiven = NOT_GIVEN,
        item_feedbacks: Optional[Iterable[ValidationItemFeedbackParam]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseValidation:
        """
        Create Test Case Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/validations",
            body=await async_maybe_transform(
                {
                    "is_accepted": is_accepted,
                    "test_case_id": test_case_id,
                    "validation_task_id": validation_task_id,
                    "validator_task_id": validator_task_id,
                    "feedback": feedback,
                    "item_feedbacks": item_feedbacks,
                },
                validation_create_params.ValidationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"current_user_payload": current_user_payload}, validation_create_params.ValidationCreateParams
                ),
            ),
            cast_to=TestCaseValidation,
        )

    async def retrieve(
        self,
        validation_id: str,
        *,
        current_user_payload: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseValidation:
        """
        Get Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return await self._get(
            f"/validations/{validation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"current_user_payload": current_user_payload}, validation_retrieve_params.ValidationRetrieveParams
                ),
            ),
            cast_to=TestCaseValidation,
        )

    async def update(
        self,
        validation_id: str,
        *,
        current_user_payload: object,
        feedback: Optional[str] | NotGiven = NOT_GIVEN,
        is_accepted: Optional[bool] | NotGiven = NOT_GIVEN,
        item_feedbacks: Optional[Iterable[ValidationItemFeedbackParam]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseValidation:
        """
        Update Test Case Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return await self._put(
            f"/validations/{validation_id}",
            body=await async_maybe_transform(
                {
                    "feedback": feedback,
                    "is_accepted": is_accepted,
                    "item_feedbacks": item_feedbacks,
                },
                validation_update_params.ValidationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"current_user_payload": current_user_payload}, validation_update_params.ValidationUpdateParams
                ),
            ),
            cast_to=TestCaseValidation,
        )

    async def list(
        self,
        *,
        current_user_payload: object,
        created_after: Optional[str] | NotGiven = NOT_GIVEN,
        created_before: Optional[str] | NotGiven = NOT_GIVEN,
        is_accepted: Optional[bool] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
        sort_by: Optional[str] | NotGiven = NOT_GIVEN,
        sort_order: str | NotGiven = NOT_GIVEN,
        test_case_id: Optional[str] | NotGiven = NOT_GIVEN,
        validator_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationListResponse:
        """
        List Validations

        Args:
          created_after: Filter by creation date (ISO format)

          created_before: Filter by creation date (ISO format)

          is_accepted: Filter by acceptance status

          sort_by: Field to sort by

          sort_order: Sort direction (asc or desc)

          test_case_id: Filter by test case ID

          validator_id: Filter by validator user ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/validations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "current_user_payload": current_user_payload,
                        "created_after": created_after,
                        "created_before": created_before,
                        "is_accepted": is_accepted,
                        "limit": limit,
                        "skip": skip,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "test_case_id": test_case_id,
                        "validator_id": validator_id,
                    },
                    validation_list_params.ValidationListParams,
                ),
            ),
            cast_to=ValidationListResponse,
        )

    async def delete(
        self,
        validation_id: str,
        *,
        current_user_payload: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/validations/{validation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"current_user_payload": current_user_payload}, validation_delete_params.ValidationDeleteParams
                ),
            ),
            cast_to=NoneType,
        )


class ValidationsResourceWithRawResponse:
    def __init__(self, validations: ValidationsResource) -> None:
        self._validations = validations

        self.create = to_raw_response_wrapper(
            validations.create,
        )
        self.retrieve = to_raw_response_wrapper(
            validations.retrieve,
        )
        self.update = to_raw_response_wrapper(
            validations.update,
        )
        self.list = to_raw_response_wrapper(
            validations.list,
        )
        self.delete = to_raw_response_wrapper(
            validations.delete,
        )


class AsyncValidationsResourceWithRawResponse:
    def __init__(self, validations: AsyncValidationsResource) -> None:
        self._validations = validations

        self.create = async_to_raw_response_wrapper(
            validations.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            validations.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            validations.update,
        )
        self.list = async_to_raw_response_wrapper(
            validations.list,
        )
        self.delete = async_to_raw_response_wrapper(
            validations.delete,
        )


class ValidationsResourceWithStreamingResponse:
    def __init__(self, validations: ValidationsResource) -> None:
        self._validations = validations

        self.create = to_streamed_response_wrapper(
            validations.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            validations.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            validations.update,
        )
        self.list = to_streamed_response_wrapper(
            validations.list,
        )
        self.delete = to_streamed_response_wrapper(
            validations.delete,
        )


class AsyncValidationsResourceWithStreamingResponse:
    def __init__(self, validations: AsyncValidationsResource) -> None:
        self._validations = validations

        self.create = async_to_streamed_response_wrapper(
            validations.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            validations.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            validations.update,
        )
        self.list = async_to_streamed_response_wrapper(
            validations.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            validations.delete,
        )

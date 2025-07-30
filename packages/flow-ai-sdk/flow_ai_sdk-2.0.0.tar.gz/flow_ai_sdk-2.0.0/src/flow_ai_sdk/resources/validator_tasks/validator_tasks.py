# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .validations import (
    ValidationsResource,
    AsyncValidationsResource,
    ValidationsResourceWithRawResponse,
    AsyncValidationsResourceWithRawResponse,
    ValidationsResourceWithStreamingResponse,
    AsyncValidationsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options

__all__ = ["ValidatorTasksResource", "AsyncValidatorTasksResource"]


class ValidatorTasksResource(SyncAPIResource):
    @cached_property
    def validations(self) -> ValidationsResource:
        return ValidationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ValidatorTasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return ValidatorTasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ValidatorTasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return ValidatorTasksResourceWithStreamingResponse(self)

    def list_test_cases(
        self,
        validator_task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Load Test Cases For Validator

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validator_task_id:
            raise ValueError(f"Expected a non-empty value for `validator_task_id` but received {validator_task_id!r}")
        return self._get(
            f"/validator-tasks/{validator_task_id}/test-cases",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def submit(
        self,
        validator_task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Submit Validator Task

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validator_task_id:
            raise ValueError(f"Expected a non-empty value for `validator_task_id` but received {validator_task_id!r}")
        return self._post(
            f"/validator-tasks/{validator_task_id}/submit",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncValidatorTasksResource(AsyncAPIResource):
    @cached_property
    def validations(self) -> AsyncValidationsResource:
        return AsyncValidationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncValidatorTasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncValidatorTasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncValidatorTasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncValidatorTasksResourceWithStreamingResponse(self)

    async def list_test_cases(
        self,
        validator_task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Load Test Cases For Validator

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validator_task_id:
            raise ValueError(f"Expected a non-empty value for `validator_task_id` but received {validator_task_id!r}")
        return await self._get(
            f"/validator-tasks/{validator_task_id}/test-cases",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def submit(
        self,
        validator_task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Submit Validator Task

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validator_task_id:
            raise ValueError(f"Expected a non-empty value for `validator_task_id` but received {validator_task_id!r}")
        return await self._post(
            f"/validator-tasks/{validator_task_id}/submit",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ValidatorTasksResourceWithRawResponse:
    def __init__(self, validator_tasks: ValidatorTasksResource) -> None:
        self._validator_tasks = validator_tasks

        self.list_test_cases = to_raw_response_wrapper(
            validator_tasks.list_test_cases,
        )
        self.submit = to_raw_response_wrapper(
            validator_tasks.submit,
        )

    @cached_property
    def validations(self) -> ValidationsResourceWithRawResponse:
        return ValidationsResourceWithRawResponse(self._validator_tasks.validations)


class AsyncValidatorTasksResourceWithRawResponse:
    def __init__(self, validator_tasks: AsyncValidatorTasksResource) -> None:
        self._validator_tasks = validator_tasks

        self.list_test_cases = async_to_raw_response_wrapper(
            validator_tasks.list_test_cases,
        )
        self.submit = async_to_raw_response_wrapper(
            validator_tasks.submit,
        )

    @cached_property
    def validations(self) -> AsyncValidationsResourceWithRawResponse:
        return AsyncValidationsResourceWithRawResponse(self._validator_tasks.validations)


class ValidatorTasksResourceWithStreamingResponse:
    def __init__(self, validator_tasks: ValidatorTasksResource) -> None:
        self._validator_tasks = validator_tasks

        self.list_test_cases = to_streamed_response_wrapper(
            validator_tasks.list_test_cases,
        )
        self.submit = to_streamed_response_wrapper(
            validator_tasks.submit,
        )

    @cached_property
    def validations(self) -> ValidationsResourceWithStreamingResponse:
        return ValidationsResourceWithStreamingResponse(self._validator_tasks.validations)


class AsyncValidatorTasksResourceWithStreamingResponse:
    def __init__(self, validator_tasks: AsyncValidatorTasksResource) -> None:
        self._validator_tasks = validator_tasks

        self.list_test_cases = async_to_streamed_response_wrapper(
            validator_tasks.list_test_cases,
        )
        self.submit = async_to_streamed_response_wrapper(
            validator_tasks.submit,
        )

    @cached_property
    def validations(self) -> AsyncValidationsResourceWithStreamingResponse:
        return AsyncValidationsResourceWithStreamingResponse(self._validator_tasks.validations)

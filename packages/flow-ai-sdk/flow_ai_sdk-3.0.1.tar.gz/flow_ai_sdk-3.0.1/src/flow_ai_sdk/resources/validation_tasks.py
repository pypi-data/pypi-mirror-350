# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.validation_task_retrieve_response import ValidationTaskRetrieveResponse

__all__ = ["ValidationTasksResource", "AsyncValidationTasksResource"]


class ValidationTasksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ValidationTasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return ValidationTasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ValidationTasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return ValidationTasksResourceWithStreamingResponse(self)

    def retrieve(
        self,
        validation_task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationTaskRetrieveResponse:
        """
        Retrieves the current status and basic information of a specific validation
        task.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_task_id:
            raise ValueError(f"Expected a non-empty value for `validation_task_id` but received {validation_task_id!r}")
        return self._get(
            f"/validation-tasks/{validation_task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ValidationTaskRetrieveResponse,
        )


class AsyncValidationTasksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncValidationTasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncValidationTasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncValidationTasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncValidationTasksResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        validation_task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationTaskRetrieveResponse:
        """
        Retrieves the current status and basic information of a specific validation
        task.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_task_id:
            raise ValueError(f"Expected a non-empty value for `validation_task_id` but received {validation_task_id!r}")
        return await self._get(
            f"/validation-tasks/{validation_task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ValidationTaskRetrieveResponse,
        )


class ValidationTasksResourceWithRawResponse:
    def __init__(self, validation_tasks: ValidationTasksResource) -> None:
        self._validation_tasks = validation_tasks

        self.retrieve = to_raw_response_wrapper(
            validation_tasks.retrieve,
        )


class AsyncValidationTasksResourceWithRawResponse:
    def __init__(self, validation_tasks: AsyncValidationTasksResource) -> None:
        self._validation_tasks = validation_tasks

        self.retrieve = async_to_raw_response_wrapper(
            validation_tasks.retrieve,
        )


class ValidationTasksResourceWithStreamingResponse:
    def __init__(self, validation_tasks: ValidationTasksResource) -> None:
        self._validation_tasks = validation_tasks

        self.retrieve = to_streamed_response_wrapper(
            validation_tasks.retrieve,
        )


class AsyncValidationTasksResourceWithStreamingResponse:
    def __init__(self, validation_tasks: AsyncValidationTasksResource) -> None:
        self._validation_tasks = validation_tasks

        self.retrieve = async_to_streamed_response_wrapper(
            validation_tasks.retrieve,
        )

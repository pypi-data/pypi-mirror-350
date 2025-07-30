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
from ..._base_client import make_request_options

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

    def update(
        self,
        validation_id: str,
        *,
        validator_task_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Edit Test Case Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validator_task_id:
            raise ValueError(f"Expected a non-empty value for `validator_task_id` but received {validator_task_id!r}")
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return self._put(
            f"/validator-tasks/{validator_task_id}/validations/{validation_id}",
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
        Submit Test Case Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validator_task_id:
            raise ValueError(f"Expected a non-empty value for `validator_task_id` but received {validator_task_id!r}")
        return self._post(
            f"/validator-tasks/{validator_task_id}/validations",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
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

    async def update(
        self,
        validation_id: str,
        *,
        validator_task_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Edit Test Case Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validator_task_id:
            raise ValueError(f"Expected a non-empty value for `validator_task_id` but received {validator_task_id!r}")
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return await self._put(
            f"/validator-tasks/{validator_task_id}/validations/{validation_id}",
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
        Submit Test Case Validation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validator_task_id:
            raise ValueError(f"Expected a non-empty value for `validator_task_id` but received {validator_task_id!r}")
        return await self._post(
            f"/validator-tasks/{validator_task_id}/validations",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ValidationsResourceWithRawResponse:
    def __init__(self, validations: ValidationsResource) -> None:
        self._validations = validations

        self.update = to_raw_response_wrapper(
            validations.update,
        )
        self.submit = to_raw_response_wrapper(
            validations.submit,
        )


class AsyncValidationsResourceWithRawResponse:
    def __init__(self, validations: AsyncValidationsResource) -> None:
        self._validations = validations

        self.update = async_to_raw_response_wrapper(
            validations.update,
        )
        self.submit = async_to_raw_response_wrapper(
            validations.submit,
        )


class ValidationsResourceWithStreamingResponse:
    def __init__(self, validations: ValidationsResource) -> None:
        self._validations = validations

        self.update = to_streamed_response_wrapper(
            validations.update,
        )
        self.submit = to_streamed_response_wrapper(
            validations.submit,
        )


class AsyncValidationsResourceWithStreamingResponse:
    def __init__(self, validations: AsyncValidationsResource) -> None:
        self._validations = validations

        self.update = async_to_streamed_response_wrapper(
            validations.update,
        )
        self.submit = async_to_streamed_response_wrapper(
            validations.submit,
        )

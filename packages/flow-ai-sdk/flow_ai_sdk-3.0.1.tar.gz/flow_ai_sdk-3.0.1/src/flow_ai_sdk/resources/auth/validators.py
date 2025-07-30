# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.auth import validator_verify_access_params, validator_complete_signup_params
from ..._base_client import make_request_options

__all__ = ["ValidatorsResource", "AsyncValidatorsResource"]


class ValidatorsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ValidatorsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return ValidatorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ValidatorsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return ValidatorsResourceWithStreamingResponse(self)

    def complete_signup(
        self,
        *,
        unique_url_key: str,
        validation_task_id: str,
        validator_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Complete Validator Signup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auth/validators/complete-signup",
            body=maybe_transform(
                {
                    "unique_url_key": unique_url_key,
                    "validation_task_id": validation_task_id,
                    "validator_id": validator_id,
                },
                validator_complete_signup_params.ValidatorCompleteSignupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def verify_access(
        self,
        *,
        unique_url_key: str,
        validation_task_id: str,
        validator_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Verify Validator Access

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/auth/validators/verify-access",
            body=maybe_transform(
                {
                    "unique_url_key": unique_url_key,
                    "validation_task_id": validation_task_id,
                    "validator_id": validator_id,
                },
                validator_verify_access_params.ValidatorVerifyAccessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncValidatorsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncValidatorsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncValidatorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncValidatorsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncValidatorsResourceWithStreamingResponse(self)

    async def complete_signup(
        self,
        *,
        unique_url_key: str,
        validation_task_id: str,
        validator_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Complete Validator Signup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auth/validators/complete-signup",
            body=await async_maybe_transform(
                {
                    "unique_url_key": unique_url_key,
                    "validation_task_id": validation_task_id,
                    "validator_id": validator_id,
                },
                validator_complete_signup_params.ValidatorCompleteSignupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def verify_access(
        self,
        *,
        unique_url_key: str,
        validation_task_id: str,
        validator_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Verify Validator Access

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/auth/validators/verify-access",
            body=await async_maybe_transform(
                {
                    "unique_url_key": unique_url_key,
                    "validation_task_id": validation_task_id,
                    "validator_id": validator_id,
                },
                validator_verify_access_params.ValidatorVerifyAccessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ValidatorsResourceWithRawResponse:
    def __init__(self, validators: ValidatorsResource) -> None:
        self._validators = validators

        self.complete_signup = to_raw_response_wrapper(
            validators.complete_signup,
        )
        self.verify_access = to_raw_response_wrapper(
            validators.verify_access,
        )


class AsyncValidatorsResourceWithRawResponse:
    def __init__(self, validators: AsyncValidatorsResource) -> None:
        self._validators = validators

        self.complete_signup = async_to_raw_response_wrapper(
            validators.complete_signup,
        )
        self.verify_access = async_to_raw_response_wrapper(
            validators.verify_access,
        )


class ValidatorsResourceWithStreamingResponse:
    def __init__(self, validators: ValidatorsResource) -> None:
        self._validators = validators

        self.complete_signup = to_streamed_response_wrapper(
            validators.complete_signup,
        )
        self.verify_access = to_streamed_response_wrapper(
            validators.verify_access,
        )


class AsyncValidatorsResourceWithStreamingResponse:
    def __init__(self, validators: AsyncValidatorsResource) -> None:
        self._validators = validators

        self.complete_signup = async_to_streamed_response_wrapper(
            validators.complete_signup,
        )
        self.verify_access = async_to_streamed_response_wrapper(
            validators.verify_access,
        )

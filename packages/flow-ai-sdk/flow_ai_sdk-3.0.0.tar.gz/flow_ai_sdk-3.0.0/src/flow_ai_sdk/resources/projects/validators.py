# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.projects import validator_add_params
from ...types.projects.project_validator import ProjectValidator
from ...types.projects.validator_list_response import ValidatorListResponse

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

    def list(
        self,
        project_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidatorListResponse:
        """
        Lists all validators assigned to a specific project.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return self._get(
            f"/projects/{project_id}/validators",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ValidatorListResponse,
        )

    def add(
        self,
        project_id: str,
        *,
        email: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProjectValidator:
        """
        Adds a user (identified by email) as a validator to a specific project.

        Args:
          email: Email address of the user to add as a validator.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return self._post(
            f"/projects/{project_id}/validators",
            body=maybe_transform({"email": email}, validator_add_params.ValidatorAddParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProjectValidator,
        )

    def remove(
        self,
        validator_id: str,
        *,
        project_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Removes a validator assignment from a specific project.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        if not validator_id:
            raise ValueError(f"Expected a non-empty value for `validator_id` but received {validator_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/projects/{project_id}/validators/{validator_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
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

    async def list(
        self,
        project_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidatorListResponse:
        """
        Lists all validators assigned to a specific project.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return await self._get(
            f"/projects/{project_id}/validators",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ValidatorListResponse,
        )

    async def add(
        self,
        project_id: str,
        *,
        email: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProjectValidator:
        """
        Adds a user (identified by email) as a validator to a specific project.

        Args:
          email: Email address of the user to add as a validator.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return await self._post(
            f"/projects/{project_id}/validators",
            body=await async_maybe_transform({"email": email}, validator_add_params.ValidatorAddParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProjectValidator,
        )

    async def remove(
        self,
        validator_id: str,
        *,
        project_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Removes a validator assignment from a specific project.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        if not validator_id:
            raise ValueError(f"Expected a non-empty value for `validator_id` but received {validator_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/projects/{project_id}/validators/{validator_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ValidatorsResourceWithRawResponse:
    def __init__(self, validators: ValidatorsResource) -> None:
        self._validators = validators

        self.list = to_raw_response_wrapper(
            validators.list,
        )
        self.add = to_raw_response_wrapper(
            validators.add,
        )
        self.remove = to_raw_response_wrapper(
            validators.remove,
        )


class AsyncValidatorsResourceWithRawResponse:
    def __init__(self, validators: AsyncValidatorsResource) -> None:
        self._validators = validators

        self.list = async_to_raw_response_wrapper(
            validators.list,
        )
        self.add = async_to_raw_response_wrapper(
            validators.add,
        )
        self.remove = async_to_raw_response_wrapper(
            validators.remove,
        )


class ValidatorsResourceWithStreamingResponse:
    def __init__(self, validators: ValidatorsResource) -> None:
        self._validators = validators

        self.list = to_streamed_response_wrapper(
            validators.list,
        )
        self.add = to_streamed_response_wrapper(
            validators.add,
        )
        self.remove = to_streamed_response_wrapper(
            validators.remove,
        )


class AsyncValidatorsResourceWithStreamingResponse:
    def __init__(self, validators: AsyncValidatorsResource) -> None:
        self._validators = validators

        self.list = async_to_streamed_response_wrapper(
            validators.list,
        )
        self.add = async_to_streamed_response_wrapper(
            validators.add,
        )
        self.remove = async_to_streamed_response_wrapper(
            validators.remove,
        )

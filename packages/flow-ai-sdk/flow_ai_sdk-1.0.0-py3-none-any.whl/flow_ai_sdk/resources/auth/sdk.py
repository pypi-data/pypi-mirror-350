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
from ...types.auth.sdk_login_response import SDKLoginResponse

__all__ = ["SDKResource", "AsyncSDKResource"]


class SDKResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SDKResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return SDKResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SDKResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return SDKResourceWithStreamingResponse(self)

    def login(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SDKLoginResponse:
        """Allows a user to obtain a session token for SDK access.

        If no active session
        exists, creates a new one. Returns a session token that can be used for SDK
        authentication.
        """
        return self._post(
            "/auth/sdk/login",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SDKLoginResponse,
        )


class AsyncSDKResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSDKResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncSDKResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSDKResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncSDKResourceWithStreamingResponse(self)

    async def login(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SDKLoginResponse:
        """Allows a user to obtain a session token for SDK access.

        If no active session
        exists, creates a new one. Returns a session token that can be used for SDK
        authentication.
        """
        return await self._post(
            "/auth/sdk/login",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SDKLoginResponse,
        )


class SDKResourceWithRawResponse:
    def __init__(self, sdk: SDKResource) -> None:
        self._sdk = sdk

        self.login = to_raw_response_wrapper(
            sdk.login,
        )


class AsyncSDKResourceWithRawResponse:
    def __init__(self, sdk: AsyncSDKResource) -> None:
        self._sdk = sdk

        self.login = async_to_raw_response_wrapper(
            sdk.login,
        )


class SDKResourceWithStreamingResponse:
    def __init__(self, sdk: SDKResource) -> None:
        self._sdk = sdk

        self.login = to_streamed_response_wrapper(
            sdk.login,
        )


class AsyncSDKResourceWithStreamingResponse:
    def __init__(self, sdk: AsyncSDKResource) -> None:
        self._sdk = sdk

        self.login = async_to_streamed_response_wrapper(
            sdk.login,
        )

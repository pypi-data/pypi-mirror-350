# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import strip_not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["ClerkWebhooksResource", "AsyncClerkWebhooksResource"]


class ClerkWebhooksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ClerkWebhooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return ClerkWebhooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClerkWebhooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return ClerkWebhooksResourceWithStreamingResponse(self)

    def handle_event(
        self,
        *,
        svix_id: str | NotGiven = NOT_GIVEN,
        svix_signature: str | NotGiven = NOT_GIVEN,
        svix_timestamp: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Handles incoming webhook events from Clerk.

        Verification is done by the
        `verify_clerk_webhook` dependency. Retrieves the verified event from
        request.state for further processing.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "svix-id": svix_id,
                    "svix-signature": svix_signature,
                    "svix-timestamp": svix_timestamp,
                }
            ),
            **(extra_headers or {}),
        }
        return self._post(
            "/clerk-webhooks/clerk-webhooks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncClerkWebhooksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncClerkWebhooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncClerkWebhooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClerkWebhooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncClerkWebhooksResourceWithStreamingResponse(self)

    async def handle_event(
        self,
        *,
        svix_id: str | NotGiven = NOT_GIVEN,
        svix_signature: str | NotGiven = NOT_GIVEN,
        svix_timestamp: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Handles incoming webhook events from Clerk.

        Verification is done by the
        `verify_clerk_webhook` dependency. Retrieves the verified event from
        request.state for further processing.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "svix-id": svix_id,
                    "svix-signature": svix_signature,
                    "svix-timestamp": svix_timestamp,
                }
            ),
            **(extra_headers or {}),
        }
        return await self._post(
            "/clerk-webhooks/clerk-webhooks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ClerkWebhooksResourceWithRawResponse:
    def __init__(self, clerk_webhooks: ClerkWebhooksResource) -> None:
        self._clerk_webhooks = clerk_webhooks

        self.handle_event = to_raw_response_wrapper(
            clerk_webhooks.handle_event,
        )


class AsyncClerkWebhooksResourceWithRawResponse:
    def __init__(self, clerk_webhooks: AsyncClerkWebhooksResource) -> None:
        self._clerk_webhooks = clerk_webhooks

        self.handle_event = async_to_raw_response_wrapper(
            clerk_webhooks.handle_event,
        )


class ClerkWebhooksResourceWithStreamingResponse:
    def __init__(self, clerk_webhooks: ClerkWebhooksResource) -> None:
        self._clerk_webhooks = clerk_webhooks

        self.handle_event = to_streamed_response_wrapper(
            clerk_webhooks.handle_event,
        )


class AsyncClerkWebhooksResourceWithStreamingResponse:
    def __init__(self, clerk_webhooks: AsyncClerkWebhooksResource) -> None:
        self._clerk_webhooks = clerk_webhooks

        self.handle_event = async_to_streamed_response_wrapper(
            clerk_webhooks.handle_event,
        )

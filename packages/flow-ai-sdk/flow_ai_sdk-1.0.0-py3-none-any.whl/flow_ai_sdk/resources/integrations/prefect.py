# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

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
from ..._base_client import make_request_options
from ...types.integrations import prefect_create_webhook_params

__all__ = ["PrefectResource", "AsyncPrefectResource"]


class PrefectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PrefectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return PrefectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PrefectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return PrefectResourceWithStreamingResponse(self)

    def create_webhook(
        self,
        *,
        flow_run: prefect_create_webhook_params.FlowRun,
        queue_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Receives notifications from Prefect about flow run state changes.

        If COMPLETED,
        enqueues a task to RQ for result processing.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/integrations/prefect/webhook",
            body=maybe_transform({"flow_run": flow_run}, prefect_create_webhook_params.PrefectCreateWebhookParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"queue_name": queue_name}, prefect_create_webhook_params.PrefectCreateWebhookParams
                ),
            ),
            cast_to=object,
        )


class AsyncPrefectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPrefectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncPrefectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPrefectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncPrefectResourceWithStreamingResponse(self)

    async def create_webhook(
        self,
        *,
        flow_run: prefect_create_webhook_params.FlowRun,
        queue_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Receives notifications from Prefect about flow run state changes.

        If COMPLETED,
        enqueues a task to RQ for result processing.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/integrations/prefect/webhook",
            body=await async_maybe_transform(
                {"flow_run": flow_run}, prefect_create_webhook_params.PrefectCreateWebhookParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"queue_name": queue_name}, prefect_create_webhook_params.PrefectCreateWebhookParams
                ),
            ),
            cast_to=object,
        )


class PrefectResourceWithRawResponse:
    def __init__(self, prefect: PrefectResource) -> None:
        self._prefect = prefect

        self.create_webhook = to_raw_response_wrapper(
            prefect.create_webhook,
        )


class AsyncPrefectResourceWithRawResponse:
    def __init__(self, prefect: AsyncPrefectResource) -> None:
        self._prefect = prefect

        self.create_webhook = async_to_raw_response_wrapper(
            prefect.create_webhook,
        )


class PrefectResourceWithStreamingResponse:
    def __init__(self, prefect: PrefectResource) -> None:
        self._prefect = prefect

        self.create_webhook = to_streamed_response_wrapper(
            prefect.create_webhook,
        )


class AsyncPrefectResourceWithStreamingResponse:
    def __init__(self, prefect: AsyncPrefectResource) -> None:
        self._prefect = prefect

        self.create_webhook = async_to_streamed_response_wrapper(
            prefect.create_webhook,
        )

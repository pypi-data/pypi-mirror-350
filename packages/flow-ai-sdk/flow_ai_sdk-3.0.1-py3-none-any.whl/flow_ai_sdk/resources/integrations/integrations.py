# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .prefect import (
    PrefectResource,
    AsyncPrefectResource,
    PrefectResourceWithRawResponse,
    AsyncPrefectResourceWithRawResponse,
    PrefectResourceWithStreamingResponse,
    AsyncPrefectResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["IntegrationsResource", "AsyncIntegrationsResource"]


class IntegrationsResource(SyncAPIResource):
    @cached_property
    def prefect(self) -> PrefectResource:
        return PrefectResource(self._client)

    @cached_property
    def with_raw_response(self) -> IntegrationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return IntegrationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> IntegrationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return IntegrationsResourceWithStreamingResponse(self)


class AsyncIntegrationsResource(AsyncAPIResource):
    @cached_property
    def prefect(self) -> AsyncPrefectResource:
        return AsyncPrefectResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncIntegrationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncIntegrationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncIntegrationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncIntegrationsResourceWithStreamingResponse(self)


class IntegrationsResourceWithRawResponse:
    def __init__(self, integrations: IntegrationsResource) -> None:
        self._integrations = integrations

    @cached_property
    def prefect(self) -> PrefectResourceWithRawResponse:
        return PrefectResourceWithRawResponse(self._integrations.prefect)


class AsyncIntegrationsResourceWithRawResponse:
    def __init__(self, integrations: AsyncIntegrationsResource) -> None:
        self._integrations = integrations

    @cached_property
    def prefect(self) -> AsyncPrefectResourceWithRawResponse:
        return AsyncPrefectResourceWithRawResponse(self._integrations.prefect)


class IntegrationsResourceWithStreamingResponse:
    def __init__(self, integrations: IntegrationsResource) -> None:
        self._integrations = integrations

    @cached_property
    def prefect(self) -> PrefectResourceWithStreamingResponse:
        return PrefectResourceWithStreamingResponse(self._integrations.prefect)


class AsyncIntegrationsResourceWithStreamingResponse:
    def __init__(self, integrations: AsyncIntegrationsResource) -> None:
        self._integrations = integrations

    @cached_property
    def prefect(self) -> AsyncPrefectResourceWithStreamingResponse:
        return AsyncPrefectResourceWithStreamingResponse(self._integrations.prefect)

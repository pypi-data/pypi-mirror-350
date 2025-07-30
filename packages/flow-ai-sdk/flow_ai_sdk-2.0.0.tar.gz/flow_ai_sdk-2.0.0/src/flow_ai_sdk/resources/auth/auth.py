# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .sdk import (
    SDKResource,
    AsyncSDKResource,
    SDKResourceWithRawResponse,
    AsyncSDKResourceWithRawResponse,
    SDKResourceWithStreamingResponse,
    AsyncSDKResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .validators import (
    ValidatorsResource,
    AsyncValidatorsResource,
    ValidatorsResourceWithRawResponse,
    AsyncValidatorsResourceWithRawResponse,
    ValidatorsResourceWithStreamingResponse,
    AsyncValidatorsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["AuthResource", "AsyncAuthResource"]


class AuthResource(SyncAPIResource):
    @cached_property
    def sdk(self) -> SDKResource:
        return SDKResource(self._client)

    @cached_property
    def validators(self) -> ValidatorsResource:
        return ValidatorsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AuthResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AuthResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AuthResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AuthResourceWithStreamingResponse(self)


class AsyncAuthResource(AsyncAPIResource):
    @cached_property
    def sdk(self) -> AsyncSDKResource:
        return AsyncSDKResource(self._client)

    @cached_property
    def validators(self) -> AsyncValidatorsResource:
        return AsyncValidatorsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAuthResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAuthResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAuthResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncAuthResourceWithStreamingResponse(self)


class AuthResourceWithRawResponse:
    def __init__(self, auth: AuthResource) -> None:
        self._auth = auth

    @cached_property
    def sdk(self) -> SDKResourceWithRawResponse:
        return SDKResourceWithRawResponse(self._auth.sdk)

    @cached_property
    def validators(self) -> ValidatorsResourceWithRawResponse:
        return ValidatorsResourceWithRawResponse(self._auth.validators)


class AsyncAuthResourceWithRawResponse:
    def __init__(self, auth: AsyncAuthResource) -> None:
        self._auth = auth

    @cached_property
    def sdk(self) -> AsyncSDKResourceWithRawResponse:
        return AsyncSDKResourceWithRawResponse(self._auth.sdk)

    @cached_property
    def validators(self) -> AsyncValidatorsResourceWithRawResponse:
        return AsyncValidatorsResourceWithRawResponse(self._auth.validators)


class AuthResourceWithStreamingResponse:
    def __init__(self, auth: AuthResource) -> None:
        self._auth = auth

    @cached_property
    def sdk(self) -> SDKResourceWithStreamingResponse:
        return SDKResourceWithStreamingResponse(self._auth.sdk)

    @cached_property
    def validators(self) -> ValidatorsResourceWithStreamingResponse:
        return ValidatorsResourceWithStreamingResponse(self._auth.validators)


class AsyncAuthResourceWithStreamingResponse:
    def __init__(self, auth: AsyncAuthResource) -> None:
        self._auth = auth

    @cached_property
    def sdk(self) -> AsyncSDKResourceWithStreamingResponse:
        return AsyncSDKResourceWithStreamingResponse(self._auth.sdk)

    @cached_property
    def validators(self) -> AsyncValidatorsResourceWithStreamingResponse:
        return AsyncValidatorsResourceWithStreamingResponse(self._auth.validators)

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .me import (
    MeResource,
    AsyncMeResource,
    MeResourceWithRawResponse,
    AsyncMeResourceWithRawResponse,
    MeResourceWithStreamingResponse,
    AsyncMeResourceWithStreamingResponse,
)
from ...types import user_update_role_params
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

__all__ = ["UsersResource", "AsyncUsersResource"]


class UsersResource(SyncAPIResource):
    @cached_property
    def me(self) -> MeResource:
        return MeResource(self._client)

    @cached_property
    def with_raw_response(self) -> UsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return UsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return UsersResourceWithStreamingResponse(self)

    def update_role(
        self,
        *,
        args: object,
        kwargs: object,
        role: Literal["user", "validator"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Update the user's role in Clerk's public metadata.

        Only allows setting role to
        either 'user' or 'validator'. Returns 204 No Content on successful update.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._patch(
            "/users/role",
            body=maybe_transform({"role": role}, user_update_role_params.UserUpdateRoleParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "args": args,
                        "kwargs": kwargs,
                    },
                    user_update_role_params.UserUpdateRoleParams,
                ),
            ),
            cast_to=NoneType,
        )


class AsyncUsersResource(AsyncAPIResource):
    @cached_property
    def me(self) -> AsyncMeResource:
        return AsyncMeResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncUsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncUsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncUsersResourceWithStreamingResponse(self)

    async def update_role(
        self,
        *,
        args: object,
        kwargs: object,
        role: Literal["user", "validator"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Update the user's role in Clerk's public metadata.

        Only allows setting role to
        either 'user' or 'validator'. Returns 204 No Content on successful update.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._patch(
            "/users/role",
            body=await async_maybe_transform({"role": role}, user_update_role_params.UserUpdateRoleParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "args": args,
                        "kwargs": kwargs,
                    },
                    user_update_role_params.UserUpdateRoleParams,
                ),
            ),
            cast_to=NoneType,
        )


class UsersResourceWithRawResponse:
    def __init__(self, users: UsersResource) -> None:
        self._users = users

        self.update_role = to_raw_response_wrapper(
            users.update_role,
        )

    @cached_property
    def me(self) -> MeResourceWithRawResponse:
        return MeResourceWithRawResponse(self._users.me)


class AsyncUsersResourceWithRawResponse:
    def __init__(self, users: AsyncUsersResource) -> None:
        self._users = users

        self.update_role = async_to_raw_response_wrapper(
            users.update_role,
        )

    @cached_property
    def me(self) -> AsyncMeResourceWithRawResponse:
        return AsyncMeResourceWithRawResponse(self._users.me)


class UsersResourceWithStreamingResponse:
    def __init__(self, users: UsersResource) -> None:
        self._users = users

        self.update_role = to_streamed_response_wrapper(
            users.update_role,
        )

    @cached_property
    def me(self) -> MeResourceWithStreamingResponse:
        return MeResourceWithStreamingResponse(self._users.me)


class AsyncUsersResourceWithStreamingResponse:
    def __init__(self, users: AsyncUsersResource) -> None:
        self._users = users

        self.update_role = async_to_streamed_response_wrapper(
            users.update_role,
        )

    @cached_property
    def me(self) -> AsyncMeResourceWithStreamingResponse:
        return AsyncMeResourceWithStreamingResponse(self._users.me)

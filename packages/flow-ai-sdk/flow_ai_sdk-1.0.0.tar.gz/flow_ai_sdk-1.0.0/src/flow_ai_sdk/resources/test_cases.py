# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional

import httpx

from ..types import test_case_list_params, test_case_create_params, test_case_delete_params, test_case_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.test_case import TestCase
from ..types.test_case_list_response import TestCaseListResponse

__all__ = ["TestCasesResource", "AsyncTestCasesResource"]


class TestCasesResource(SyncAPIResource):
    __test__ = False

    @cached_property
    def with_raw_response(self) -> TestCasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return TestCasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TestCasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return TestCasesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        expected_output: str,
        status: str,
        api_key_user_id: str | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        is_active: bool | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        trajectory: Iterable[test_case_create_params.Trajectory] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCase:
        """
        Create Test Case

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/test-cases/",
            body=maybe_transform(
                {
                    "expected_output": expected_output,
                    "status": status,
                    "description": description,
                    "is_active": is_active,
                    "name": name,
                    "trajectory": trajectory,
                },
                test_case_create_params.TestCaseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"api_key_user_id": api_key_user_id}, test_case_create_params.TestCaseCreateParams
                ),
            ),
            cast_to=TestCase,
        )

    def retrieve(
        self,
        test_case_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCase:
        """
        Get Test Case

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return self._get(
            f"/test-cases/{test_case_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCase,
        )

    def update(
        self,
        test_case_id: str,
        *,
        current_user_payload: Dict[str, object],
        test_case_in: test_case_update_params.TestCaseIn,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCase:
        """
        Update Test Case

        Args:
          test_case_in: Schema for updating a test case (all fields optional)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return self._put(
            f"/test-cases/{test_case_id}",
            body=maybe_transform(
                {
                    "current_user_payload": current_user_payload,
                    "test_case_in": test_case_in,
                },
                test_case_update_params.TestCaseUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCase,
        )

    def list(
        self,
        *,
        batch_id: Optional[str] | NotGiven = NOT_GIVEN,
        created_after: Optional[str] | NotGiven = NOT_GIVEN,
        created_before: Optional[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
        sort_by: Optional[str] | NotGiven = NOT_GIVEN,
        sort_order: str | NotGiven = NOT_GIVEN,
        status: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseListResponse:
        """
        List Test Cases

        Args:
          batch_id: Filter by Batch ID

          created_after: Filter by creation date (ISO format, YYYY-MM-DDTHH:MM:SSZ)

          created_before: Filter by creation date (ISO format, YYYY-MM-DDTHH:MM:SSZ)

          name: Filter by name (partial match)

          sort_by: Field to sort by (e.g., 'name', 'created_at')

          sort_order: Sort direction ('asc' or 'desc')

          status: Filter by status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/test-cases/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "batch_id": batch_id,
                        "created_after": created_after,
                        "created_before": created_before,
                        "limit": limit,
                        "name": name,
                        "skip": skip,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "status": status,
                    },
                    test_case_list_params.TestCaseListParams,
                ),
            ),
            cast_to=TestCaseListResponse,
        )

    def delete(
        self,
        test_case_id: str,
        *,
        body: Dict[str, object],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Test Case

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/test-cases/{test_case_id}",
            body=maybe_transform(body, test_case_delete_params.TestCaseDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_validation(
        self,
        test_case_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get Single Validation From Batch

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return self._get(
            f"/test-cases/{test_case_id}/validation",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncTestCasesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTestCasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncTestCasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTestCasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncTestCasesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        expected_output: str,
        status: str,
        api_key_user_id: str | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        is_active: bool | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        trajectory: Iterable[test_case_create_params.Trajectory] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCase:
        """
        Create Test Case

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/test-cases/",
            body=await async_maybe_transform(
                {
                    "expected_output": expected_output,
                    "status": status,
                    "description": description,
                    "is_active": is_active,
                    "name": name,
                    "trajectory": trajectory,
                },
                test_case_create_params.TestCaseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key_user_id": api_key_user_id}, test_case_create_params.TestCaseCreateParams
                ),
            ),
            cast_to=TestCase,
        )

    async def retrieve(
        self,
        test_case_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCase:
        """
        Get Test Case

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return await self._get(
            f"/test-cases/{test_case_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCase,
        )

    async def update(
        self,
        test_case_id: str,
        *,
        current_user_payload: Dict[str, object],
        test_case_in: test_case_update_params.TestCaseIn,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCase:
        """
        Update Test Case

        Args:
          test_case_in: Schema for updating a test case (all fields optional)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return await self._put(
            f"/test-cases/{test_case_id}",
            body=await async_maybe_transform(
                {
                    "current_user_payload": current_user_payload,
                    "test_case_in": test_case_in,
                },
                test_case_update_params.TestCaseUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCase,
        )

    async def list(
        self,
        *,
        batch_id: Optional[str] | NotGiven = NOT_GIVEN,
        created_after: Optional[str] | NotGiven = NOT_GIVEN,
        created_before: Optional[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
        sort_by: Optional[str] | NotGiven = NOT_GIVEN,
        sort_order: str | NotGiven = NOT_GIVEN,
        status: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestCaseListResponse:
        """
        List Test Cases

        Args:
          batch_id: Filter by Batch ID

          created_after: Filter by creation date (ISO format, YYYY-MM-DDTHH:MM:SSZ)

          created_before: Filter by creation date (ISO format, YYYY-MM-DDTHH:MM:SSZ)

          name: Filter by name (partial match)

          sort_by: Field to sort by (e.g., 'name', 'created_at')

          sort_order: Sort direction ('asc' or 'desc')

          status: Filter by status

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/test-cases/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "batch_id": batch_id,
                        "created_after": created_after,
                        "created_before": created_before,
                        "limit": limit,
                        "name": name,
                        "skip": skip,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "status": status,
                    },
                    test_case_list_params.TestCaseListParams,
                ),
            ),
            cast_to=TestCaseListResponse,
        )

    async def delete(
        self,
        test_case_id: str,
        *,
        body: Dict[str, object],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Test Case

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/test-cases/{test_case_id}",
            body=await async_maybe_transform(body, test_case_delete_params.TestCaseDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_validation(
        self,
        test_case_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Get Single Validation From Batch

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return await self._get(
            f"/test-cases/{test_case_id}/validation",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class TestCasesResourceWithRawResponse:
    __test__ = False

    def __init__(self, test_cases: TestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = to_raw_response_wrapper(
            test_cases.create,
        )
        self.retrieve = to_raw_response_wrapper(
            test_cases.retrieve,
        )
        self.update = to_raw_response_wrapper(
            test_cases.update,
        )
        self.list = to_raw_response_wrapper(
            test_cases.list,
        )
        self.delete = to_raw_response_wrapper(
            test_cases.delete,
        )
        self.get_validation = to_raw_response_wrapper(
            test_cases.get_validation,
        )


class AsyncTestCasesResourceWithRawResponse:
    def __init__(self, test_cases: AsyncTestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = async_to_raw_response_wrapper(
            test_cases.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            test_cases.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            test_cases.update,
        )
        self.list = async_to_raw_response_wrapper(
            test_cases.list,
        )
        self.delete = async_to_raw_response_wrapper(
            test_cases.delete,
        )
        self.get_validation = async_to_raw_response_wrapper(
            test_cases.get_validation,
        )


class TestCasesResourceWithStreamingResponse:
    __test__ = False

    def __init__(self, test_cases: TestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = to_streamed_response_wrapper(
            test_cases.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            test_cases.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            test_cases.update,
        )
        self.list = to_streamed_response_wrapper(
            test_cases.list,
        )
        self.delete = to_streamed_response_wrapper(
            test_cases.delete,
        )
        self.get_validation = to_streamed_response_wrapper(
            test_cases.get_validation,
        )


class AsyncTestCasesResourceWithStreamingResponse:
    def __init__(self, test_cases: AsyncTestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = async_to_streamed_response_wrapper(
            test_cases.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            test_cases.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            test_cases.update,
        )
        self.list = async_to_streamed_response_wrapper(
            test_cases.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            test_cases.delete,
        )
        self.get_validation = async_to_streamed_response_wrapper(
            test_cases.get_validation,
        )

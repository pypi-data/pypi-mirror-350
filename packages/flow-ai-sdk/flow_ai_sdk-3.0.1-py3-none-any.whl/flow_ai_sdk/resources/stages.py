# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os  # Added for os.PathLike
from io import IOBase, BufferedReader  # Added for IOBase type checking
from typing import List, Union, Mapping, Optional, cast  # Added Union
from pathlib import Path  # Added for Path
from typing_extensions import Literal

import httpx

from ..types import stage_list_params, stage_create_params, stage_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    extract_files,
    maybe_transform,
    deepcopy_minimal,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.stage_details import StageDetails
from ..types.stage_list_response import StageListResponse
from ..types.stage_create_response import StageCreateResponse

__all__ = ["StagesResource", "AsyncStagesResource"]


class StagesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return StagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return StagesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        files: List[Union[str, os.PathLike[str], IOBase]],  # Changed type hint
        project_id: str,
        source_type: Literal[
            "agent_rules", "tool_definitions", "database_schema_rules", "custom_data_files", "relational_db_schema"
        ],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StageCreateResponse:
        """Create new stages by uploading one or more files.

        These stages can then be used
        to manually trigger a job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        opened_by_sdk: List[BufferedReader] = []
        processed_file_objects: List[IOBase] = []

        try:
            for file_input in files:
                if isinstance(file_input, str):
                    path = Path(file_input)
                    if not path.exists():
                        raise FileNotFoundError(f"File not found: {file_input}")
                    stream = path.open("rb")
                    opened_by_sdk.append(stream)
                    processed_file_objects.append(stream)
                elif isinstance(file_input, os.PathLike):  # Check against os.PathLike
                    path = Path(file_input)
                    if not path.exists():
                        raise FileNotFoundError(f"File not found: {file_input}")
                    stream = path.open("rb")
                    opened_by_sdk.append(stream)
                    processed_file_objects.append(stream)
                else:  # Default to IOBase
                    processed_file_objects.append(file_input)

            body = deepcopy_minimal(
                {
                    "files": processed_file_objects,  # Use the list of actual IOBase streams
                    "project_id": project_id,
                    "source_type": source_type,
                }
            )
            # extract_files should operate on the body containing real IOBase streams
            # and prepare them for httpx's `files` parameter.
            extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])

            # CRITICAL FIX: Ensure the 'files' key (with its IOBase objects) is removed from the `body`
            # that goes into the `data` part of the multipart request.
            # `extracted_files` is now what httpx will use for the actual file parts.
            if "files" in body:
                del body["files"]

            final_extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
            return self._post(
                "/stages/",
                body=maybe_transform(
                    body, stage_create_params.StageCreateParams
                ),  # body should be clean of file objects now
                files=extracted_files,
                options=make_request_options(
                    extra_headers=final_extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=StageCreateResponse,
            )
        finally:
            # Ensure any files opened by this method are closed
            for stream in opened_by_sdk:
                if not stream.closed:
                    stream.close()

    def retrieve(
        self,
        stage_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StageDetails:
        """Retrieve details of a specific stage by its ID.

        The service is expected to raise
        ValueError if the stage is not found.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/stages/{stage_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StageDetails,
        )

    def update(
        self,
        stage_id: int,
        *,
        original_filename: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StageDetails:
        """Update an existing stage's metadata (e.g., original_filename).

        The service is
        expected to raise ValueError if the stage is not found.

        Args:
          original_filename: New original filename for the stage.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            f"/stages/{stage_id}",
            body=maybe_transform({"original_filename": original_filename}, stage_update_params.StageUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StageDetails,
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StageListResponse:
        """Retrieve a list of stages with pagination.

        The service is expected to return a
        tuple: (list of stage dicts, total count of all stages).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/stages/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "skip": skip,
                    },
                    stage_list_params.StageListParams,
                ),
            ),
            cast_to=StageListResponse,
        )

    def delete(
        self,
        stage_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Delete a specific stage by its ID.

        This includes deleting the S3 object and the
        database record. The service is expected to raise ValueError if the stage is not
        found.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            f"/stages/{stage_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def ping(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Ping Stages"""
        return self._get(
            "/stages/ping",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncStagesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncStagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/flowaicom/flowai-sdk#with_streaming_response
        """
        return AsyncStagesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        files: List[Union[str, os.PathLike[str], IOBase]],  # Changed type hint
        project_id: str,
        source_type: Literal[
            "agent_rules", "tool_definitions", "database_schema_rules", "custom_data_files", "relational_db_schema"
        ],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StageCreateResponse:
        """Create new stages by uploading one or more files.

        These stages can then be used
        to manually trigger a job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        opened_by_sdk: List[BufferedReader] = []
        processed_file_objects: List[IOBase] = []
        # File opening is synchronous here. For a fully async SDK, consider aiofiles.
        # However, for ergonomic SDK use, sync open before an async HTTP call is often acceptable.
        try:
            for file_input in files:
                if isinstance(file_input, str):
                    path = Path(file_input)
                    if not path.exists():
                        raise FileNotFoundError(f"File not found: {file_input}")
                    stream = path.open("rb")
                    opened_by_sdk.append(stream)
                    processed_file_objects.append(stream)
                elif isinstance(file_input, os.PathLike):  # Check against os.PathLike
                    path = Path(file_input)
                    if not path.exists():
                        raise FileNotFoundError(f"File not found: {file_input}")
                    stream = path.open("rb")
                    opened_by_sdk.append(stream)
                    processed_file_objects.append(stream)
                else:  # Default to IOBase
                    processed_file_objects.append(file_input)

            body = deepcopy_minimal(
                {
                    "files": processed_file_objects,
                    "project_id": project_id,
                    "source_type": source_type,
                }
            )
            # extract_files is synchronous
            extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])

            if "files" in body:
                del body["files"]

            final_extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}

            return await self._post(
                "/stages/",
                body=await async_maybe_transform(body, stage_create_params.StageCreateParams),
                files=extracted_files,  # extracted_files is already prepared
                options=make_request_options(
                    extra_headers=final_extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=StageCreateResponse,
            )
        finally:
            for stream in opened_by_sdk:  # Sync close
                if not stream.closed:
                    stream.close()

    async def retrieve(
        self,
        stage_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StageDetails:
        """Retrieve details of a specific stage by its ID.

        The service is expected to raise
        ValueError if the stage is not found.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/stages/{stage_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StageDetails,
        )

    async def update(
        self,
        stage_id: int,
        *,
        original_filename: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StageDetails:
        """Update an existing stage's metadata (e.g., original_filename).

        The service is
        expected to raise ValueError if the stage is not found.

        Args:
          original_filename: New original filename for the stage.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            f"/stages/{stage_id}",
            body=await async_maybe_transform(
                {"original_filename": original_filename}, stage_update_params.StageUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StageDetails,
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StageListResponse:
        """Retrieve a list of stages with pagination.

        The service is expected to return a
        tuple: (list of stage dicts, total count of all stages).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/stages/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "skip": skip,
                    },
                    stage_list_params.StageListParams,
                ),
            ),
            cast_to=StageListResponse,
        )

    async def delete(
        self,
        stage_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Delete a specific stage by its ID.

        This includes deleting the S3 object and the
        database record. The service is expected to raise ValueError if the stage is not
        found.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            f"/stages/{stage_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def ping(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Ping Stages"""
        return await self._get(
            "/stages/ping",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class StagesResourceWithRawResponse:
    def __init__(self, stages: StagesResource) -> None:
        self._stages = stages

        self.create = to_raw_response_wrapper(
            stages.create,
        )
        self.retrieve = to_raw_response_wrapper(
            stages.retrieve,
        )
        self.update = to_raw_response_wrapper(
            stages.update,
        )
        self.list = to_raw_response_wrapper(
            stages.list,
        )
        self.delete = to_raw_response_wrapper(
            stages.delete,
        )
        self.ping = to_raw_response_wrapper(
            stages.ping,
        )


class AsyncStagesResourceWithRawResponse:
    def __init__(self, stages: AsyncStagesResource) -> None:
        self._stages = stages

        self.create = async_to_raw_response_wrapper(
            stages.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            stages.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            stages.update,
        )
        self.list = async_to_raw_response_wrapper(
            stages.list,
        )
        self.delete = async_to_raw_response_wrapper(
            stages.delete,
        )
        self.ping = async_to_raw_response_wrapper(
            stages.ping,
        )


class StagesResourceWithStreamingResponse:
    def __init__(self, stages: StagesResource) -> None:
        self._stages = stages

        self.create = to_streamed_response_wrapper(
            stages.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            stages.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            stages.update,
        )
        self.list = to_streamed_response_wrapper(
            stages.list,
        )
        self.delete = to_streamed_response_wrapper(
            stages.delete,
        )
        self.ping = to_streamed_response_wrapper(
            stages.ping,
        )


class AsyncStagesResourceWithStreamingResponse:
    def __init__(self, stages: AsyncStagesResource) -> None:
        self._stages = stages

        self.create = async_to_streamed_response_wrapper(
            stages.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            stages.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            stages.update,
        )
        self.list = async_to_streamed_response_wrapper(
            stages.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            stages.delete,
        )
        self.ping = async_to_streamed_response_wrapper(
            stages.ping,
        )

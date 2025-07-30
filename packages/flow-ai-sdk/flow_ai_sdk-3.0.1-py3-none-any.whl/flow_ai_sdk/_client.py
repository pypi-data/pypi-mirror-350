# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import (
    jobs,
    health,
    stages,
    batches,
    api_info,
    api_keys,
    datasets,
    test_cases,
    validations,
    clerk_webhooks,
    validation_tasks,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.auth import auth
from .resources.users import users
from .resources.projects import projects
from .resources.integrations import integrations
from .resources.validator_tasks import validator_tasks

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "FlowAISDK",
    "AsyncFlowAISDK",
    "Client",
    "AsyncClient",
]


class FlowAISDK(SyncAPIClient):
    health: health.HealthResource
    clerk_webhooks: clerk_webhooks.ClerkWebhooksResource
    users: users.UsersResource
    test_cases: test_cases.TestCasesResource
    validations: validations.ValidationsResource
    batches: batches.BatchesResource
    api_keys: api_keys.APIKeysResource
    auth: auth.AuthResource
    datasets: datasets.DatasetsResource
    jobs: jobs.JobsResource
    projects: projects.ProjectsResource
    validation_tasks: validation_tasks.ValidationTasksResource
    validator_tasks: validator_tasks.ValidatorTasksResource
    stages: stages.StagesResource
    integrations: integrations.IntegrationsResource
    api_info: api_info.APIInfoResource
    with_raw_response: FlowAISDKWithRawResponse
    with_streaming_response: FlowAISDKWithStreamedResponse

    # client options
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous FlowAISDK client instance.

        This automatically infers the `api_key` argument from the `FLOW_AI_SDK_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("FLOW_AI_SDK_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("FLOW_AI_SDK_BASE_URL")
        if base_url is None:
            base_url = f"https://api.example.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.health = health.HealthResource(self)
        self.clerk_webhooks = clerk_webhooks.ClerkWebhooksResource(self)
        self.users = users.UsersResource(self)
        self.test_cases = test_cases.TestCasesResource(self)
        self.validations = validations.ValidationsResource(self)
        self.batches = batches.BatchesResource(self)
        self.api_keys = api_keys.APIKeysResource(self)
        self.auth = auth.AuthResource(self)
        self.datasets = datasets.DatasetsResource(self)
        self.jobs = jobs.JobsResource(self)
        self.projects = projects.ProjectsResource(self)
        self.validation_tasks = validation_tasks.ValidationTasksResource(self)
        self.validator_tasks = validator_tasks.ValidatorTasksResource(self)
        self.stages = stages.StagesResource(self)
        self.integrations = integrations.IntegrationsResource(self)
        self.api_info = api_info.APIInfoResource(self)
        self.with_raw_response = FlowAISDKWithRawResponse(self)
        self.with_streaming_response = FlowAISDKWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the api_key to be set. Or for the `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncFlowAISDK(AsyncAPIClient):
    health: health.AsyncHealthResource
    clerk_webhooks: clerk_webhooks.AsyncClerkWebhooksResource
    users: users.AsyncUsersResource
    test_cases: test_cases.AsyncTestCasesResource
    validations: validations.AsyncValidationsResource
    batches: batches.AsyncBatchesResource
    api_keys: api_keys.AsyncAPIKeysResource
    auth: auth.AsyncAuthResource
    datasets: datasets.AsyncDatasetsResource
    jobs: jobs.AsyncJobsResource
    projects: projects.AsyncProjectsResource
    validation_tasks: validation_tasks.AsyncValidationTasksResource
    validator_tasks: validator_tasks.AsyncValidatorTasksResource
    stages: stages.AsyncStagesResource
    integrations: integrations.AsyncIntegrationsResource
    api_info: api_info.AsyncAPIInfoResource
    with_raw_response: AsyncFlowAISDKWithRawResponse
    with_streaming_response: AsyncFlowAISDKWithStreamedResponse

    # client options
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncFlowAISDK client instance.

        This automatically infers the `api_key` argument from the `FLOW_AI_SDK_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("FLOW_AI_SDK_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("FLOW_AI_SDK_BASE_URL")
        if base_url is None:
            base_url = f"https://api.example.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.health = health.AsyncHealthResource(self)
        self.clerk_webhooks = clerk_webhooks.AsyncClerkWebhooksResource(self)
        self.users = users.AsyncUsersResource(self)
        self.test_cases = test_cases.AsyncTestCasesResource(self)
        self.validations = validations.AsyncValidationsResource(self)
        self.batches = batches.AsyncBatchesResource(self)
        self.api_keys = api_keys.AsyncAPIKeysResource(self)
        self.auth = auth.AsyncAuthResource(self)
        self.datasets = datasets.AsyncDatasetsResource(self)
        self.jobs = jobs.AsyncJobsResource(self)
        self.projects = projects.AsyncProjectsResource(self)
        self.validation_tasks = validation_tasks.AsyncValidationTasksResource(self)
        self.validator_tasks = validator_tasks.AsyncValidatorTasksResource(self)
        self.stages = stages.AsyncStagesResource(self)
        self.integrations = integrations.AsyncIntegrationsResource(self)
        self.api_info = api_info.AsyncAPIInfoResource(self)
        self.with_raw_response = AsyncFlowAISDKWithRawResponse(self)
        self.with_streaming_response = AsyncFlowAISDKWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the api_key to be set. Or for the `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class FlowAISDKWithRawResponse:
    def __init__(self, client: FlowAISDK) -> None:
        self.health = health.HealthResourceWithRawResponse(client.health)
        self.clerk_webhooks = clerk_webhooks.ClerkWebhooksResourceWithRawResponse(client.clerk_webhooks)
        self.users = users.UsersResourceWithRawResponse(client.users)
        self.test_cases = test_cases.TestCasesResourceWithRawResponse(client.test_cases)
        self.validations = validations.ValidationsResourceWithRawResponse(client.validations)
        self.batches = batches.BatchesResourceWithRawResponse(client.batches)
        self.api_keys = api_keys.APIKeysResourceWithRawResponse(client.api_keys)
        self.auth = auth.AuthResourceWithRawResponse(client.auth)
        self.datasets = datasets.DatasetsResourceWithRawResponse(client.datasets)
        self.jobs = jobs.JobsResourceWithRawResponse(client.jobs)
        self.projects = projects.ProjectsResourceWithRawResponse(client.projects)
        self.validation_tasks = validation_tasks.ValidationTasksResourceWithRawResponse(client.validation_tasks)
        self.validator_tasks = validator_tasks.ValidatorTasksResourceWithRawResponse(client.validator_tasks)
        self.stages = stages.StagesResourceWithRawResponse(client.stages)
        self.integrations = integrations.IntegrationsResourceWithRawResponse(client.integrations)
        self.api_info = api_info.APIInfoResourceWithRawResponse(client.api_info)


class AsyncFlowAISDKWithRawResponse:
    def __init__(self, client: AsyncFlowAISDK) -> None:
        self.health = health.AsyncHealthResourceWithRawResponse(client.health)
        self.clerk_webhooks = clerk_webhooks.AsyncClerkWebhooksResourceWithRawResponse(client.clerk_webhooks)
        self.users = users.AsyncUsersResourceWithRawResponse(client.users)
        self.test_cases = test_cases.AsyncTestCasesResourceWithRawResponse(client.test_cases)
        self.validations = validations.AsyncValidationsResourceWithRawResponse(client.validations)
        self.batches = batches.AsyncBatchesResourceWithRawResponse(client.batches)
        self.api_keys = api_keys.AsyncAPIKeysResourceWithRawResponse(client.api_keys)
        self.auth = auth.AsyncAuthResourceWithRawResponse(client.auth)
        self.datasets = datasets.AsyncDatasetsResourceWithRawResponse(client.datasets)
        self.jobs = jobs.AsyncJobsResourceWithRawResponse(client.jobs)
        self.projects = projects.AsyncProjectsResourceWithRawResponse(client.projects)
        self.validation_tasks = validation_tasks.AsyncValidationTasksResourceWithRawResponse(client.validation_tasks)
        self.validator_tasks = validator_tasks.AsyncValidatorTasksResourceWithRawResponse(client.validator_tasks)
        self.stages = stages.AsyncStagesResourceWithRawResponse(client.stages)
        self.integrations = integrations.AsyncIntegrationsResourceWithRawResponse(client.integrations)
        self.api_info = api_info.AsyncAPIInfoResourceWithRawResponse(client.api_info)


class FlowAISDKWithStreamedResponse:
    def __init__(self, client: FlowAISDK) -> None:
        self.health = health.HealthResourceWithStreamingResponse(client.health)
        self.clerk_webhooks = clerk_webhooks.ClerkWebhooksResourceWithStreamingResponse(client.clerk_webhooks)
        self.users = users.UsersResourceWithStreamingResponse(client.users)
        self.test_cases = test_cases.TestCasesResourceWithStreamingResponse(client.test_cases)
        self.validations = validations.ValidationsResourceWithStreamingResponse(client.validations)
        self.batches = batches.BatchesResourceWithStreamingResponse(client.batches)
        self.api_keys = api_keys.APIKeysResourceWithStreamingResponse(client.api_keys)
        self.auth = auth.AuthResourceWithStreamingResponse(client.auth)
        self.datasets = datasets.DatasetsResourceWithStreamingResponse(client.datasets)
        self.jobs = jobs.JobsResourceWithStreamingResponse(client.jobs)
        self.projects = projects.ProjectsResourceWithStreamingResponse(client.projects)
        self.validation_tasks = validation_tasks.ValidationTasksResourceWithStreamingResponse(client.validation_tasks)
        self.validator_tasks = validator_tasks.ValidatorTasksResourceWithStreamingResponse(client.validator_tasks)
        self.stages = stages.StagesResourceWithStreamingResponse(client.stages)
        self.integrations = integrations.IntegrationsResourceWithStreamingResponse(client.integrations)
        self.api_info = api_info.APIInfoResourceWithStreamingResponse(client.api_info)


class AsyncFlowAISDKWithStreamedResponse:
    def __init__(self, client: AsyncFlowAISDK) -> None:
        self.health = health.AsyncHealthResourceWithStreamingResponse(client.health)
        self.clerk_webhooks = clerk_webhooks.AsyncClerkWebhooksResourceWithStreamingResponse(client.clerk_webhooks)
        self.users = users.AsyncUsersResourceWithStreamingResponse(client.users)
        self.test_cases = test_cases.AsyncTestCasesResourceWithStreamingResponse(client.test_cases)
        self.validations = validations.AsyncValidationsResourceWithStreamingResponse(client.validations)
        self.batches = batches.AsyncBatchesResourceWithStreamingResponse(client.batches)
        self.api_keys = api_keys.AsyncAPIKeysResourceWithStreamingResponse(client.api_keys)
        self.auth = auth.AsyncAuthResourceWithStreamingResponse(client.auth)
        self.datasets = datasets.AsyncDatasetsResourceWithStreamingResponse(client.datasets)
        self.jobs = jobs.AsyncJobsResourceWithStreamingResponse(client.jobs)
        self.projects = projects.AsyncProjectsResourceWithStreamingResponse(client.projects)
        self.validation_tasks = validation_tasks.AsyncValidationTasksResourceWithStreamingResponse(
            client.validation_tasks
        )
        self.validator_tasks = validator_tasks.AsyncValidatorTasksResourceWithStreamingResponse(client.validator_tasks)
        self.stages = stages.AsyncStagesResourceWithStreamingResponse(client.stages)
        self.integrations = integrations.AsyncIntegrationsResourceWithStreamingResponse(client.integrations)
        self.api_info = api_info.AsyncAPIInfoResourceWithStreamingResponse(client.api_info)


Client = FlowAISDK

AsyncClient = AsyncFlowAISDK

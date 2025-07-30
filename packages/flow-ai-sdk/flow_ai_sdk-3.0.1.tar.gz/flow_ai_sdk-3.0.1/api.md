# Health

Types:

```python
from flow_ai_sdk.types import HealthCheckResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/flow_ai_sdk/resources/health.py">check</a>() -> <a href="./src/flow_ai_sdk/types/health_check_response.py">object</a></code>

# ClerkWebhooks

Types:

```python
from flow_ai_sdk.types import ClerkWebhookHandleEventResponse
```

Methods:

- <code title="post /clerk-webhooks/clerk-webhooks">client.clerk_webhooks.<a href="./src/flow_ai_sdk/resources/clerk_webhooks.py">handle_event</a>() -> <a href="./src/flow_ai_sdk/types/clerk_webhook_handle_event_response.py">object</a></code>

# Users

Methods:

- <code title="patch /users/role">client.users.<a href="./src/flow_ai_sdk/resources/users/users.py">update_role</a>(\*\*<a href="src/flow_ai_sdk/types/user_update_role_params.py">params</a>) -> None</code>

## Me

Types:

```python
from flow_ai_sdk.types.users import UserRead, MeGetBasicInfoResponse
```

Methods:

- <code title="get /users/me">client.users.me.<a href="./src/flow_ai_sdk/resources/users/me.py">retrieve</a>() -> <a href="./src/flow_ai_sdk/types/users/user_read.py">UserRead</a></code>
- <code title="patch /users/me">client.users.me.<a href="./src/flow_ai_sdk/resources/users/me.py">update</a>(\*\*<a href="src/flow_ai_sdk/types/users/me_update_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/users/user_read.py">UserRead</a></code>
- <code title="get /users/me/basic-info">client.users.me.<a href="./src/flow_ai_sdk/resources/users/me.py">get_basic_info</a>() -> <a href="./src/flow_ai_sdk/types/users/me_get_basic_info_response.py">object</a></code>

# TestCases

Types:

```python
from flow_ai_sdk.types import TestCase, TestCaseListResponse, TestCaseGetValidationResponse
```

Methods:

- <code title="post /test-cases/">client.test_cases.<a href="./src/flow_ai_sdk/resources/test_cases.py">create</a>(\*\*<a href="src/flow_ai_sdk/types/test_case_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/test_case.py">TestCase</a></code>
- <code title="get /test-cases/{test_case_id}">client.test_cases.<a href="./src/flow_ai_sdk/resources/test_cases.py">retrieve</a>(test_case_id) -> <a href="./src/flow_ai_sdk/types/test_case.py">TestCase</a></code>
- <code title="put /test-cases/{test_case_id}">client.test_cases.<a href="./src/flow_ai_sdk/resources/test_cases.py">update</a>(test_case_id, \*\*<a href="src/flow_ai_sdk/types/test_case_update_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/test_case.py">TestCase</a></code>
- <code title="get /test-cases/">client.test_cases.<a href="./src/flow_ai_sdk/resources/test_cases.py">list</a>(\*\*<a href="src/flow_ai_sdk/types/test_case_list_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/test_case_list_response.py">TestCaseListResponse</a></code>
- <code title="delete /test-cases/{test_case_id}">client.test_cases.<a href="./src/flow_ai_sdk/resources/test_cases.py">delete</a>(test_case_id, \*\*<a href="src/flow_ai_sdk/types/test_case_delete_params.py">params</a>) -> None</code>
- <code title="get /test-cases/{test_case_id}/validation">client.test_cases.<a href="./src/flow_ai_sdk/resources/test_cases.py">get_validation</a>(test_case_id) -> <a href="./src/flow_ai_sdk/types/test_case_get_validation_response.py">object</a></code>

# Validations

Types:

```python
from flow_ai_sdk.types import TestCaseValidation, ValidationItemFeedback, ValidationListResponse
```

Methods:

- <code title="post /validations">client.validations.<a href="./src/flow_ai_sdk/resources/validations.py">create</a>(\*\*<a href="src/flow_ai_sdk/types/validation_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/test_case_validation.py">TestCaseValidation</a></code>
- <code title="get /validations/{validation_id}">client.validations.<a href="./src/flow_ai_sdk/resources/validations.py">retrieve</a>(validation_id, \*\*<a href="src/flow_ai_sdk/types/validation_retrieve_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/test_case_validation.py">TestCaseValidation</a></code>
- <code title="put /validations/{validation_id}">client.validations.<a href="./src/flow_ai_sdk/resources/validations.py">update</a>(validation_id, \*\*<a href="src/flow_ai_sdk/types/validation_update_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/test_case_validation.py">TestCaseValidation</a></code>
- <code title="get /validations">client.validations.<a href="./src/flow_ai_sdk/resources/validations.py">list</a>(\*\*<a href="src/flow_ai_sdk/types/validation_list_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/validation_list_response.py">ValidationListResponse</a></code>
- <code title="delete /validations/{validation_id}">client.validations.<a href="./src/flow_ai_sdk/resources/validations.py">delete</a>(validation_id, \*\*<a href="src/flow_ai_sdk/types/validation_delete_params.py">params</a>) -> None</code>

# Batches

Types:

```python
from flow_ai_sdk.types import (
    BatchRead,
    BatchCreateValidationTaskResponse,
    BatchListMineResponse,
    BatchListTestcasesResponse,
    BatchListValidationsResponse,
    BatchRetrieveStatusResponse,
    BatchRetrieveValidationTaskResponse,
)
```

Methods:

- <code title="get /batches/{batch_id}">client.batches.<a href="./src/flow_ai_sdk/resources/batches.py">retrieve</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/batch_read.py">BatchRead</a></code>
- <code title="delete /batches/{batch_id}">client.batches.<a href="./src/flow_ai_sdk/resources/batches.py">delete</a>(batch_id) -> None</code>
- <code title="post /batches/{batch_id}/validation-tasks">client.batches.<a href="./src/flow_ai_sdk/resources/batches.py">create_validation_task</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/batch_create_validation_task_response.py">BatchCreateValidationTaskResponse</a></code>
- <code title="get /batches/mine">client.batches.<a href="./src/flow_ai_sdk/resources/batches.py">list_mine</a>() -> <a href="./src/flow_ai_sdk/types/batch_list_mine_response.py">BatchListMineResponse</a></code>
- <code title="get /batches/{batch_id}/testcases">client.batches.<a href="./src/flow_ai_sdk/resources/batches.py">list_testcases</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/batch_list_testcases_response.py">BatchListTestcasesResponse</a></code>
- <code title="get /batches/{batch_id}/validations">client.batches.<a href="./src/flow_ai_sdk/resources/batches.py">list_validations</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/batch_list_validations_response.py">BatchListValidationsResponse</a></code>
- <code title="get /batches/{batch_id}/status">client.batches.<a href="./src/flow_ai_sdk/resources/batches.py">retrieve_status</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/batch_retrieve_status_response.py">BatchRetrieveStatusResponse</a></code>
- <code title="get /batches/{batch_id}/validation-task">client.batches.<a href="./src/flow_ai_sdk/resources/batches.py">retrieve_validation_task</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/batch_retrieve_validation_task_response.py">BatchRetrieveValidationTaskResponse</a></code>

# APIKeys

Types:

```python
from flow_ai_sdk.types import APIKeyCreateResponse, APIKeyUpdateResponse, APIKeyListResponse
```

Methods:

- <code title="post /api-keys">client.api_keys.<a href="./src/flow_ai_sdk/resources/api_keys.py">create</a>(\*\*<a href="src/flow_ai_sdk/types/api_key_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api_key_create_response.py">APIKeyCreateResponse</a></code>
- <code title="put /api-keys/{key_id}">client.api_keys.<a href="./src/flow_ai_sdk/resources/api_keys.py">update</a>(key_id, \*\*<a href="src/flow_ai_sdk/types/api_key_update_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api_key_update_response.py">APIKeyUpdateResponse</a></code>
- <code title="get /api-keys">client.api_keys.<a href="./src/flow_ai_sdk/resources/api_keys.py">list</a>(\*\*<a href="src/flow_ai_sdk/types/api_key_list_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api_key_list_response.py">APIKeyListResponse</a></code>
- <code title="delete /api-keys/{key_id}">client.api_keys.<a href="./src/flow_ai_sdk/resources/api_keys.py">delete</a>(key_id) -> None</code>

# Auth

## SDK

Types:

```python
from flow_ai_sdk.types.auth import SDKLoginResponse
```

Methods:

- <code title="post /auth/sdk/login">client.auth.sdk.<a href="./src/flow_ai_sdk/resources/auth/sdk.py">login</a>() -> <a href="./src/flow_ai_sdk/types/auth/sdk_login_response.py">SDKLoginResponse</a></code>

## Validators

Types:

```python
from flow_ai_sdk.types.auth import ValidatorCompleteSignupResponse, ValidatorVerifyAccessResponse
```

Methods:

- <code title="post /auth/validators/complete-signup">client.auth.validators.<a href="./src/flow_ai_sdk/resources/auth/validators.py">complete_signup</a>(\*\*<a href="src/flow_ai_sdk/types/auth/validator_complete_signup_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/auth/validator_complete_signup_response.py">object</a></code>
- <code title="post /auth/validators/verify-access">client.auth.validators.<a href="./src/flow_ai_sdk/resources/auth/validators.py">verify_access</a>(\*\*<a href="src/flow_ai_sdk/types/auth/validator_verify_access_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/auth/validator_verify_access_response.py">object</a></code>

# Datasets

Types:

```python
from flow_ai_sdk.types import PaginationDetails, DatasetRetrieveItemsResponse
```

Methods:

- <code title="delete /datasets/{dataset_id}">client.datasets.<a href="./src/flow_ai_sdk/resources/datasets.py">delete</a>(dataset_id) -> None</code>
- <code title="get /datasets/{dataset_id}/items">client.datasets.<a href="./src/flow_ai_sdk/resources/datasets.py">retrieve_items</a>(dataset_id, \*\*<a href="src/flow_ai_sdk/types/dataset_retrieve_items_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/dataset_retrieve_items_response.py">DatasetRetrieveItemsResponse</a></code>

# Jobs

Types:

```python
from flow_ai_sdk.types import (
    Job,
    JobBatchGeneration,
    JobCancelResponse,
    JobGenerateDatasetResponse,
    JobListBatchesResponse,
)
```

Methods:

- <code title="get /jobs/{job_id}">client.jobs.<a href="./src/flow_ai_sdk/resources/jobs.py">retrieve</a>(job_id) -> <a href="./src/flow_ai_sdk/types/job.py">Job</a></code>
- <code title="post /jobs/{job_id}/cancel">client.jobs.<a href="./src/flow_ai_sdk/resources/jobs.py">cancel</a>(job_id) -> <a href="./src/flow_ai_sdk/types/job_cancel_response.py">JobCancelResponse</a></code>
- <code title="post /jobs/{job_id}/generate-batch">client.jobs.<a href="./src/flow_ai_sdk/resources/jobs.py">generate_batch</a>(job_id) -> <a href="./src/flow_ai_sdk/types/job_batch_generation.py">JobBatchGeneration</a></code>
- <code title="post /jobs/{job_id}/generate-dataset">client.jobs.<a href="./src/flow_ai_sdk/resources/jobs.py">generate_dataset</a>(job_id, \*\*<a href="src/flow_ai_sdk/types/job_generate_dataset_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/job_generate_dataset_response.py">JobGenerateDatasetResponse</a></code>
- <code title="get /jobs/{job_id}/batches">client.jobs.<a href="./src/flow_ai_sdk/resources/jobs.py">list_batches</a>(job_id, \*\*<a href="src/flow_ai_sdk/types/job_list_batches_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/job_list_batches_response.py">object</a></code>
- <code title="post /jobs/trigger_pipeline_from_stages">client.jobs.<a href="./src/flow_ai_sdk/resources/jobs.py">trigger_pipeline</a>(\*\*<a href="src/flow_ai_sdk/types/job_trigger_pipeline_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/job_batch_generation.py">JobBatchGeneration</a></code>

# Projects

Types:

```python
from flow_ai_sdk.types import (
    Project,
    ProjectListResponse,
    ProjectArchiveResponse,
    ProjectGetDatasetResponse,
)
```

Methods:

- <code title="post /projects/">client.projects.<a href="./src/flow_ai_sdk/resources/projects/projects.py">create</a>(\*\*<a href="src/flow_ai_sdk/types/project_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/project.py">Project</a></code>
- <code title="get /projects/{project_id}">client.projects.<a href="./src/flow_ai_sdk/resources/projects/projects.py">retrieve</a>(project_id) -> <a href="./src/flow_ai_sdk/types/project.py">Project</a></code>
- <code title="patch /projects/{project_id}">client.projects.<a href="./src/flow_ai_sdk/resources/projects/projects.py">update</a>(project_id, \*\*<a href="src/flow_ai_sdk/types/project_update_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/project.py">Project</a></code>
- <code title="get /projects/">client.projects.<a href="./src/flow_ai_sdk/resources/projects/projects.py">list</a>(\*\*<a href="src/flow_ai_sdk/types/project_list_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/project_list_response.py">ProjectListResponse</a></code>
- <code title="delete /projects/{project_id}">client.projects.<a href="./src/flow_ai_sdk/resources/projects/projects.py">delete</a>(project_id) -> None</code>
- <code title="post /projects/{project_id}/archive">client.projects.<a href="./src/flow_ai_sdk/resources/projects/projects.py">archive</a>(project_id) -> <a href="./src/flow_ai_sdk/types/project_archive_response.py">ProjectArchiveResponse</a></code>
- <code title="get /projects/{project_id}/dataset">client.projects.<a href="./src/flow_ai_sdk/resources/projects/projects.py">get_dataset</a>(project_id, \*\*<a href="src/flow_ai_sdk/types/project_get_dataset_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/project_get_dataset_response.py">ProjectGetDatasetResponse</a></code>

## Validators

Types:

```python
from flow_ai_sdk.types.projects import ProjectValidator, ValidatorListResponse
```

Methods:

- <code title="get /projects/{project_id}/validators">client.projects.validators.<a href="./src/flow_ai_sdk/resources/projects/validators.py">list</a>(project_id) -> <a href="./src/flow_ai_sdk/types/projects/validator_list_response.py">ValidatorListResponse</a></code>
- <code title="post /projects/{project_id}/validators">client.projects.validators.<a href="./src/flow_ai_sdk/resources/projects/validators.py">add</a>(project_id, \*\*<a href="src/flow_ai_sdk/types/projects/validator_add_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/projects/project_validator.py">ProjectValidator</a></code>
- <code title="delete /projects/{project_id}/validators/{validator_id}">client.projects.validators.<a href="./src/flow_ai_sdk/resources/projects/validators.py">remove</a>(validator_id, \*, project_id) -> None</code>

## Jobs

Types:

```python
from flow_ai_sdk.types.projects import JobListResponse
```

Methods:

- <code title="post /projects/{project_id}/jobs">client.projects.jobs.<a href="./src/flow_ai_sdk/resources/projects/jobs.py">create</a>(project_id, \*\*<a href="src/flow_ai_sdk/types/projects/job_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/job.py">Job</a></code>
- <code title="get /projects/{project_id}/jobs">client.projects.jobs.<a href="./src/flow_ai_sdk/resources/projects/jobs.py">list</a>(project_id, \*\*<a href="src/flow_ai_sdk/types/projects/job_list_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/projects/job_list_response.py">JobListResponse</a></code>

# ValidationTasks

Types:

```python
from flow_ai_sdk.types import ValidationTaskRetrieveResponse
```

Methods:

- <code title="get /validation-tasks/{validation_task_id}">client.validation_tasks.<a href="./src/flow_ai_sdk/resources/validation_tasks.py">retrieve</a>(validation_task_id) -> <a href="./src/flow_ai_sdk/types/validation_task_retrieve_response.py">ValidationTaskRetrieveResponse</a></code>

# ValidatorTasks

Types:

```python
from flow_ai_sdk.types import ValidatorTaskListTestCasesResponse, ValidatorTaskSubmitResponse
```

Methods:

- <code title="get /validator-tasks/{validator_task_id}/test-cases">client.validator_tasks.<a href="./src/flow_ai_sdk/resources/validator_tasks/validator_tasks.py">list_test_cases</a>(validator_task_id) -> <a href="./src/flow_ai_sdk/types/validator_task_list_test_cases_response.py">object</a></code>
- <code title="post /validator-tasks/{validator_task_id}/submit">client.validator_tasks.<a href="./src/flow_ai_sdk/resources/validator_tasks/validator_tasks.py">submit</a>(validator_task_id) -> <a href="./src/flow_ai_sdk/types/validator_task_submit_response.py">object</a></code>

## Validations

Types:

```python
from flow_ai_sdk.types.validator_tasks import ValidationUpdateResponse, ValidationSubmitResponse
```

Methods:

- <code title="put /validator-tasks/{validator_task_id}/validations/{validation_id}">client.validator_tasks.validations.<a href="./src/flow_ai_sdk/resources/validator_tasks/validations.py">update</a>(validation_id, \*, validator_task_id) -> <a href="./src/flow_ai_sdk/types/validator_tasks/validation_update_response.py">object</a></code>
- <code title="post /validator-tasks/{validator_task_id}/validations">client.validator_tasks.validations.<a href="./src/flow_ai_sdk/resources/validator_tasks/validations.py">submit</a>(validator_task_id) -> <a href="./src/flow_ai_sdk/types/validator_tasks/validation_submit_response.py">object</a></code>

# Stages

Types:

```python
from flow_ai_sdk.types import (
    StageDetails,
    StageCreateResponse,
    StageListResponse,
    StageDeleteResponse,
    StagePingResponse,
)
```

Methods:

- <code title="post /stages/">client.stages.<a href="./src/flow_ai_sdk/resources/stages.py">create</a>(\*\*<a href="src/flow_ai_sdk/types/stage_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/stage_create_response.py">StageCreateResponse</a></code>
- <code title="get /stages/{stage_id}">client.stages.<a href="./src/flow_ai_sdk/resources/stages.py">retrieve</a>(stage_id) -> <a href="./src/flow_ai_sdk/types/stage_details.py">StageDetails</a></code>
- <code title="put /stages/{stage_id}">client.stages.<a href="./src/flow_ai_sdk/resources/stages.py">update</a>(stage_id, \*\*<a href="src/flow_ai_sdk/types/stage_update_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/stage_details.py">StageDetails</a></code>
- <code title="get /stages/">client.stages.<a href="./src/flow_ai_sdk/resources/stages.py">list</a>(\*\*<a href="src/flow_ai_sdk/types/stage_list_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/stage_list_response.py">StageListResponse</a></code>
- <code title="delete /stages/{stage_id}">client.stages.<a href="./src/flow_ai_sdk/resources/stages.py">delete</a>(stage_id) -> <a href="./src/flow_ai_sdk/types/stage_delete_response.py">object</a></code>
- <code title="get /stages/ping">client.stages.<a href="./src/flow_ai_sdk/resources/stages.py">ping</a>() -> <a href="./src/flow_ai_sdk/types/stage_ping_response.py">object</a></code>

# Integrations

## Prefect

Types:

```python
from flow_ai_sdk.types.integrations import PrefectCreateWebhookResponse
```

Methods:

- <code title="post /integrations/prefect/webhook">client.integrations.prefect.<a href="./src/flow_ai_sdk/resources/integrations/prefect.py">create_webhook</a>(\*\*<a href="src/flow_ai_sdk/types/integrations/prefect_create_webhook_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/integrations/prefect_create_webhook_response.py">object</a></code>

# APIInfo

Types:

```python
from flow_ai_sdk.types import APIInfoRetrieveResponse
```

Methods:

- <code title="get /">client.api_info.<a href="./src/flow_ai_sdk/resources/api_info.py">retrieve</a>() -> <a href="./src/flow_ai_sdk/types/api_info_retrieve_response.py">APIInfoRetrieveResponse</a></code>

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["JobBatchGeneration"]


class JobBatchGeneration(BaseModel):
    flow_run_id: str

    flow_run_name: str

    flow_run_state: str

    job_id: str = FieldInfo(alias="jobId")

    message: str

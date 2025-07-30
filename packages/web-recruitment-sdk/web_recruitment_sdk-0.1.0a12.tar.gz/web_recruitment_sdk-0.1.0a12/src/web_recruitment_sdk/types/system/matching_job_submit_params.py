# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .external_job_status import ExternalJobStatus

__all__ = ["MatchingJobSubmitParams"]


class MatchingJobSubmitParams(TypedDict, total=False):
    criteria_id: Required[Annotated[int, PropertyInfo(alias="criteriaId")]]

    site_id: Required[Annotated[int, PropertyInfo(alias="siteId")]]

    batch_size: Optional[int]
    """Number of patients to process in each batch"""

    cancelled_at: Annotated[Union[str, datetime, None], PropertyInfo(alias="cancelledAt", format="iso8601")]

    completed_at: Annotated[Union[str, datetime, None], PropertyInfo(alias="completedAt", format="iso8601")]

    created_at: Annotated[Union[str, datetime], PropertyInfo(alias="createdAt", format="iso8601")]

    status: ExternalJobStatus
    """Enum for the status of an external job."""

    updated_at: Annotated[Union[str, datetime], PropertyInfo(alias="updatedAt", format="iso8601")]

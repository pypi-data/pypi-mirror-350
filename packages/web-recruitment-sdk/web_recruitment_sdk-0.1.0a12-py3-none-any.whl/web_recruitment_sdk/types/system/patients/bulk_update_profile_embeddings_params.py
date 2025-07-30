# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["BulkUpdateProfileEmbeddingsParams", "Body"]


class BulkUpdateProfileEmbeddingsParams(TypedDict, total=False):
    body: Required[Iterable[Body]]


class Body(TypedDict, total=False):
    category: Required[str]

    embedding: Required[Iterable[float]]

    text: Required[str]

    trially_patient_id: Required[Annotated[str, PropertyInfo(alias="triallyPatientId")]]

    id: Optional[int]

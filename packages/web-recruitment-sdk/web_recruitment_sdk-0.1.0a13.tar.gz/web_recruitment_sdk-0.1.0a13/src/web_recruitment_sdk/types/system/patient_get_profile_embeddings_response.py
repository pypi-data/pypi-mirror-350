# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["PatientGetProfileEmbeddingsResponse", "PatientGetProfileEmbeddingsResponseItem"]


class PatientGetProfileEmbeddingsResponseItem(BaseModel):
    category: str

    embedding: List[float]

    text: str

    trially_patient_id: str = FieldInfo(alias="triallyPatientId")

    id: Optional[int] = None


PatientGetProfileEmbeddingsResponse: TypeAlias = List[PatientGetProfileEmbeddingsResponseItem]

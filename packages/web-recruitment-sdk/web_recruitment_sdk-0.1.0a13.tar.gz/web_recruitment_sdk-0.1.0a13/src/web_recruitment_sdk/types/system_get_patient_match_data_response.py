# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["SystemGetPatientMatchDataResponse", "SystemGetPatientMatchDataResponseItem"]


class SystemGetPatientMatchDataResponseItem(BaseModel):
    patient_history: List[object]

    trially_patient_id: str


SystemGetPatientMatchDataResponse: TypeAlias = List[SystemGetPatientMatchDataResponseItem]

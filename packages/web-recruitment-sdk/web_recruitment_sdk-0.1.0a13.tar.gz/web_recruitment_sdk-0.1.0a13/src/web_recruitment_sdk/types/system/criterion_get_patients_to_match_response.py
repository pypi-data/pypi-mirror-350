# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["CriterionGetPatientsToMatchResponse", "CriterionGetPatientsToMatchResponseItem"]


class CriterionGetPatientsToMatchResponseItem(BaseModel):
    full_medical_history: str = FieldInfo(alias="fullMedicalHistory")

    trially_patient_id: str = FieldInfo(alias="triallyPatientId")


CriterionGetPatientsToMatchResponse: TypeAlias = List[CriterionGetPatientsToMatchResponseItem]

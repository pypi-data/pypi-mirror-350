# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SiteRead"]


class SiteRead(BaseModel):
    id: int

    name: str

    trially_site_id: Optional[str] = FieldInfo(alias="triallySiteId", default=None)

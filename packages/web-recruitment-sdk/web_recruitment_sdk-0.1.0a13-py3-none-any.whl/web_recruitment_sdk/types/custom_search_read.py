# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CustomSearchRead", "Site"]


class Site(BaseModel):
    id: int

    name: str

    trially_site_id: Optional[str] = FieldInfo(alias="triallySiteId", default=None)


class CustomSearchRead(BaseModel):
    id: int

    title: str

    sites: Optional[List[Site]] = None

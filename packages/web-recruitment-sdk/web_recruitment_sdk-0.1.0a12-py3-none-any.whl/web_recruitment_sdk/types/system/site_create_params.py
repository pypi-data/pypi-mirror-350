# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["SiteCreateParams"]


class SiteCreateParams(TypedDict, total=False):
    name: Required[str]

    trially_site_id: Annotated[Optional[str], PropertyInfo(alias="triallySiteId")]

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PromptUpdateMetadataParams"]


class PromptUpdateMetadataParams(TypedDict, total=False):
    body_id: Required[Annotated[str, PropertyInfo(alias="id")]]
    """The id of the prompt"""

    category: Optional[str]
    """The category of the prompt"""

    description: Optional[str]
    """The description of the prompt"""

    name: Optional[str]
    """The name of the prompt"""

    tags: Optional[List[str]]
    """The tags of the prompt"""

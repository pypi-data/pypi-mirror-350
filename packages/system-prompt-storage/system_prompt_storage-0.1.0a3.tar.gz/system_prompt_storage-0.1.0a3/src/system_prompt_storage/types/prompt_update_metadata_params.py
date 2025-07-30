# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["PromptUpdateMetadataParams"]


class PromptUpdateMetadataParams(TypedDict, total=False):
    id: Required[str]
    """The id of the prompt"""

    category: Optional[str]
    """The category of the prompt"""

    description: Optional[str]
    """The description of the prompt"""

    name: Optional[str]
    """The name of the prompt"""

    tags: Optional[List[str]]
    """The tags of the prompt"""

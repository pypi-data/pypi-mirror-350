# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["Prompt", "Metadata"]


class Metadata(BaseModel):
    category: Optional[str] = None
    """Category of the prompt ie React, typescript, etc."""

    description: Optional[str] = None
    """Description of the prompt"""

    name: Optional[str] = None
    """Name of the prompt"""

    tags: Optional[List[str]] = None
    """Tags of the prompt ie [react, typescript, etc.]"""


class Prompt(BaseModel):
    id: str
    """The id of the prompt"""

    content: str
    """The content of the prompt"""

    created_at: int
    """The creation date of the prompt"""

    parent: str
    """The parent of the prompt"""

    version: int
    """The version of the prompt"""

    archived: Optional[bool] = None
    """Whether the prompt is archived"""

    branched: Optional[bool] = None
    """Whether the prompt is being branched"""

    metadata: Optional[Metadata] = None
    """The metadata of the prompt"""

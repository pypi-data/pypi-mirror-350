# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["PromptCreateParams"]


class PromptCreateParams(TypedDict, total=False):
    content: Required[str]
    """The content of the prompt"""

    branched: Optional[bool]
    """Whether the prompt is being branched"""

    category: Optional[str]
    """The category of the prompt"""

    description: Optional[str]
    """The description of the prompt"""

    name: Optional[str]
    """The name of the prompt"""

    parent: Optional[str]
    """The parent of the prompt.

    If its a new prompt with no lineage, this should be None.
    """

    tags: Optional[List[str]]
    """The tags of the prompt"""

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PromptUpdateParams"]


class PromptUpdateParams(TypedDict, total=False):
    body_id: Required[Annotated[str, PropertyInfo(alias="id")]]
    """The id of the prompt to update"""

    content: Required[str]
    """The content of the updated prompt"""

    parent: Required[str]
    """The parent of the updated prompt.

    Most times its the same as the id of the prompt to update.
    """

    branched: Optional[bool]
    """Whether the updated prompt is branched"""

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PromptListParams"]


class PromptListParams(TypedDict, total=False):
    category: Required[str]
    """The category of the prompts to return"""

    from_: Required[Annotated[int, PropertyInfo(alias="from")]]
    """The pagination offset to start from (0-based)"""

    size: Required[int]
    """The number of prompts to return"""

    to: Required[int]
    """The pagination offset to end at (exclusive)"""

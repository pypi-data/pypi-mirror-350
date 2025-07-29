# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PromptListParams"]


class PromptListParams(TypedDict, total=False):
    category: str
    """The category of the prompts to return"""

    limit: int
    """The number of prompts to return. Default is 10."""

    offset: int
    """The pagination offset to start from (0-based). Default is 0."""

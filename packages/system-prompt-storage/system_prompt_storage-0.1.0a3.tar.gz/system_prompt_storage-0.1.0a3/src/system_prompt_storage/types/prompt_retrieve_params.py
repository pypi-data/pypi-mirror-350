# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PromptRetrieveParams"]


class PromptRetrieveParams(TypedDict, total=False):
    metadata: bool
    """Whether to include metadata in the response"""

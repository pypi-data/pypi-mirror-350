# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PromptRetrieveContentParams"]


class PromptRetrieveContentParams(TypedDict, total=False):
    latest: Required[bool]
    """Latest version of the prompt"""

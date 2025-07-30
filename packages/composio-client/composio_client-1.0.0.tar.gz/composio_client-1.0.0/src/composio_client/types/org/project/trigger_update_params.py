# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["TriggerUpdateParams"]


class TriggerUpdateParams(TypedDict, total=False):
    enabled: Required[bool]
    """
    Boolean flag indicating whether triggers should be enabled (true) or disabled
    (false) for the project
    """

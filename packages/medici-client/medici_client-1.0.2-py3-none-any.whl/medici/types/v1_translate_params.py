# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

__all__ = ["V1TranslateParams"]


class V1TranslateParams(TypedDict, total=False):
    content: Required[str]
    """Text to translate verbatim"""

    target_language: Required[Literal["en", "es", "fr", "de", "it"]]
    """Target language code (ISO-639-1)"""

    metadata: Dict[str, object]
    """Arbitrary metadata echoed back"""

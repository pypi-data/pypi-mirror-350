# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["V1DeidentifyParams", "Config"]


class V1DeidentifyParams(TypedDict, total=False):
    content: Required[str]
    """Test with PHI to deidentify"""

    config: Config
    """Configuration parameters"""

    metadata: Dict[str, str]
    """Ad hoc configuration properties, eg for logging or observability"""


class Config(TypedDict, total=False):
    approach: Literal["replace", "redact"]
    """Approach to identified entities"""

    fixed_mrns: Optional[List[str]]
    """List of known MRNs as fallback for primary deidentifier"""

    fixed_names: Optional[List[str]]
    """List of known names as fallback for primary deidentifiers.

    Names are split to word and only 3+ letter words are used.
            First names are supplemented by known matching nicknames.
    """

    return_analysis: bool
    """Whether to return the analysis process"""

    return_explanation: bool
    """Whether to return an explanation of the analysis process"""

    user_id: str
    """UserID for caller"""

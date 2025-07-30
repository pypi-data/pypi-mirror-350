# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["V1DeidentifyResponse", "Config"]


class Config(BaseModel):
    pipeline_name: Optional[str] = None
    """Name of the pipeline used for deidentification"""

    server_version: Optional[str] = None
    """Version of the Medici server"""

    transformers_model: Optional[str] = None
    """HuggingFace model path used for deidentification via transformers"""


class V1DeidentifyResponse(BaseModel):
    config: Config
    """Configuration parameters used"""

    content: str
    """Content stripped of PHI"""

    explanation: Optional[Dict[str, object]] = None
    """An explanation of the deidentification process, as a JSON object"""

    metadata: Optional[Dict[str, str]] = None
    """Additional output metadata"""

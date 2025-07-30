# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["V1TranslateResponse"]


class V1TranslateResponse(BaseModel):
    original_language_name: str
    """The language of the original text, as detected by the parser"""

    translated_language_name: str
    """The target language for translation, as specified in the request"""

    translated_text: str
    """The original text translated into the target language"""

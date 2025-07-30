# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal

import httpx

from ..types import v1_translate_params, v1_deidentify_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.v1_translate_response import V1TranslateResponse
from ..types.v1_deidentify_response import V1DeidentifyResponse

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> V1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/natecobb/medici-client#accessing-raw-response-data-eg-headers
        """
        return V1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/natecobb/medici-client#with_streaming_response
        """
        return V1ResourceWithStreamingResponse(self)

    def deidentify(
        self,
        pipeline: Literal["roberta_i2b2", "stanford_aimi"],
        *,
        content: str,
        config: v1_deidentify_params.Config | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1DeidentifyResponse:
        """
        Deidentify

        Args:
          content: Test with PHI to deidentify

          config: Configuration parameters

          metadata: Ad hoc configuration properties, eg for logging or observability

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pipeline:
            raise ValueError(f"Expected a non-empty value for `pipeline` but received {pipeline!r}")
        return self._post(
            f"/api/v1/deidentify/{pipeline}",
            body=maybe_transform(
                {
                    "content": content,
                    "config": config,
                    "metadata": metadata,
                },
                v1_deidentify_params.V1DeidentifyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1DeidentifyResponse,
        )

    def translate(
        self,
        *,
        content: str,
        target_language: Literal["en", "es", "fr", "de", "it"],
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1TranslateResponse:
        """
        Translate

        Args:
          content: Text to translate verbatim

          target_language: Target language code (ISO-639-1)

          metadata: Arbitrary metadata echoed back

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/translate",
            body=maybe_transform(
                {
                    "content": content,
                    "target_language": target_language,
                    "metadata": metadata,
                },
                v1_translate_params.V1TranslateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1TranslateResponse,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncV1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/natecobb/medici-client#accessing-raw-response-data-eg-headers
        """
        return AsyncV1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/natecobb/medici-client#with_streaming_response
        """
        return AsyncV1ResourceWithStreamingResponse(self)

    async def deidentify(
        self,
        pipeline: Literal["roberta_i2b2", "stanford_aimi"],
        *,
        content: str,
        config: v1_deidentify_params.Config | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1DeidentifyResponse:
        """
        Deidentify

        Args:
          content: Test with PHI to deidentify

          config: Configuration parameters

          metadata: Ad hoc configuration properties, eg for logging or observability

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not pipeline:
            raise ValueError(f"Expected a non-empty value for `pipeline` but received {pipeline!r}")
        return await self._post(
            f"/api/v1/deidentify/{pipeline}",
            body=await async_maybe_transform(
                {
                    "content": content,
                    "config": config,
                    "metadata": metadata,
                },
                v1_deidentify_params.V1DeidentifyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1DeidentifyResponse,
        )

    async def translate(
        self,
        *,
        content: str,
        target_language: Literal["en", "es", "fr", "de", "it"],
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1TranslateResponse:
        """
        Translate

        Args:
          content: Text to translate verbatim

          target_language: Target language code (ISO-639-1)

          metadata: Arbitrary metadata echoed back

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/translate",
            body=await async_maybe_transform(
                {
                    "content": content,
                    "target_language": target_language,
                    "metadata": metadata,
                },
                v1_translate_params.V1TranslateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1TranslateResponse,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.deidentify = to_raw_response_wrapper(
            v1.deidentify,
        )
        self.translate = to_raw_response_wrapper(
            v1.translate,
        )


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.deidentify = async_to_raw_response_wrapper(
            v1.deidentify,
        )
        self.translate = async_to_raw_response_wrapper(
            v1.translate,
        )


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.deidentify = to_streamed_response_wrapper(
            v1.deidentify,
        )
        self.translate = to_streamed_response_wrapper(
            v1.translate,
        )


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.deidentify = async_to_streamed_response_wrapper(
            v1.deidentify,
        )
        self.translate = async_to_streamed_response_wrapper(
            v1.translate,
        )

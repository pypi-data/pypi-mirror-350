# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from medici import Medici, AsyncMedici
from tests.utils import assert_matches_type
from medici.types import V1TranslateResponse, V1DeidentifyResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestV1:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_deidentify(self, client: Medici) -> None:
        v1 = client.v1.deidentify(
            pipeline="roberta_i2b2",
            content="x",
        )
        assert_matches_type(V1DeidentifyResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_deidentify_with_all_params(self, client: Medici) -> None:
        v1 = client.v1.deidentify(
            pipeline="roberta_i2b2",
            content="x",
            config={
                "approach": "replace",
                "fixed_mrns": ["string"],
                "fixed_names": ["string"],
                "return_analysis": True,
                "return_explanation": True,
                "user_id": "user_id",
            },
            metadata={"foo": "string"},
        )
        assert_matches_type(V1DeidentifyResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_deidentify(self, client: Medici) -> None:
        response = client.v1.with_raw_response.deidentify(
            pipeline="roberta_i2b2",
            content="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1DeidentifyResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_deidentify(self, client: Medici) -> None:
        with client.v1.with_streaming_response.deidentify(
            pipeline="roberta_i2b2",
            content="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1DeidentifyResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_translate(self, client: Medici) -> None:
        v1 = client.v1.translate(
            content="content",
            target_language="en",
        )
        assert_matches_type(V1TranslateResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_translate_with_all_params(self, client: Medici) -> None:
        v1 = client.v1.translate(
            content="content",
            target_language="en",
            metadata={"foo": "bar"},
        )
        assert_matches_type(V1TranslateResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_translate(self, client: Medici) -> None:
        response = client.v1.with_raw_response.translate(
            content="content",
            target_language="en",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1TranslateResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_translate(self, client: Medici) -> None:
        with client.v1.with_streaming_response.translate(
            content="content",
            target_language="en",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1TranslateResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncV1:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_deidentify(self, async_client: AsyncMedici) -> None:
        v1 = await async_client.v1.deidentify(
            pipeline="roberta_i2b2",
            content="x",
        )
        assert_matches_type(V1DeidentifyResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_deidentify_with_all_params(self, async_client: AsyncMedici) -> None:
        v1 = await async_client.v1.deidentify(
            pipeline="roberta_i2b2",
            content="x",
            config={
                "approach": "replace",
                "fixed_mrns": ["string"],
                "fixed_names": ["string"],
                "return_analysis": True,
                "return_explanation": True,
                "user_id": "user_id",
            },
            metadata={"foo": "string"},
        )
        assert_matches_type(V1DeidentifyResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_deidentify(self, async_client: AsyncMedici) -> None:
        response = await async_client.v1.with_raw_response.deidentify(
            pipeline="roberta_i2b2",
            content="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1DeidentifyResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_deidentify(self, async_client: AsyncMedici) -> None:
        async with async_client.v1.with_streaming_response.deidentify(
            pipeline="roberta_i2b2",
            content="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1DeidentifyResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_translate(self, async_client: AsyncMedici) -> None:
        v1 = await async_client.v1.translate(
            content="content",
            target_language="en",
        )
        assert_matches_type(V1TranslateResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_translate_with_all_params(self, async_client: AsyncMedici) -> None:
        v1 = await async_client.v1.translate(
            content="content",
            target_language="en",
            metadata={"foo": "bar"},
        )
        assert_matches_type(V1TranslateResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_translate(self, async_client: AsyncMedici) -> None:
        response = await async_client.v1.with_raw_response.translate(
            content="content",
            target_language="en",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1TranslateResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_translate(self, async_client: AsyncMedici) -> None:
        async with async_client.v1.with_streaming_response.translate(
            content="content",
            target_language="en",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1TranslateResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

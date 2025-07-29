# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from system_prompt_storage import SystemPromptStorage, AsyncSystemPromptStorage
from system_prompt_storage.types import (
    Prompt,
    PromptListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPrompts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.create(
            content="content",
        )
        assert_matches_type(Prompt, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.create(
            content="content",
            branched=True,
            category="category",
            description="description",
            name="name",
            parent="parent",
            tags=["string"],
        )
        assert_matches_type(Prompt, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: SystemPromptStorage) -> None:
        response = client.prompts.with_raw_response.create(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(Prompt, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: SystemPromptStorage) -> None:
        with client.prompts.with_streaming_response.create(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(Prompt, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.retrieve(
            "id",
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SystemPromptStorage) -> None:
        response = client.prompts.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SystemPromptStorage) -> None:
        with client.prompts.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(str, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: SystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.prompts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.update(
            path_id="id",
            body_id="id",
            content="content",
            parent="parent",
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.update(
            path_id="id",
            body_id="id",
            content="content",
            parent="parent",
            branched=True,
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: SystemPromptStorage) -> None:
        response = client.prompts.with_raw_response.update(
            path_id="id",
            body_id="id",
            content="content",
            parent="parent",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: SystemPromptStorage) -> None:
        with client.prompts.with_streaming_response.update(
            path_id="id",
            body_id="id",
            content="content",
            parent="parent",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(str, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: SystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            client.prompts.with_raw_response.update(
                path_id="",
                body_id="id",
                content="content",
                parent="parent",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.list(
            category="category",
            from_=0,
            size=0,
            to=0,
        )
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: SystemPromptStorage) -> None:
        response = client.prompts.with_raw_response.list(
            category="category",
            from_=0,
            size=0,
            to=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: SystemPromptStorage) -> None:
        with client.prompts.with_streaming_response.list(
            category="category",
            from_=0,
            size=0,
            to=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(PromptListResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.delete(
            "id",
        )
        assert prompt is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: SystemPromptStorage) -> None:
        response = client.prompts.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert prompt is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: SystemPromptStorage) -> None:
        with client.prompts.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: SystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.prompts.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_content(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.retrieve_content(
            id="id",
            latest=True,
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_content(self, client: SystemPromptStorage) -> None:
        response = client.prompts.with_raw_response.retrieve_content(
            id="id",
            latest=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_content(self, client: SystemPromptStorage) -> None:
        with client.prompts.with_streaming_response.retrieve_content(
            id="id",
            latest=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(str, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_content(self, client: SystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.prompts.with_raw_response.retrieve_content(
                id="",
                latest=True,
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_metadata(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.update_metadata(
            path_id="id",
            body_id="id",
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_metadata_with_all_params(self, client: SystemPromptStorage) -> None:
        prompt = client.prompts.update_metadata(
            path_id="id",
            body_id="id",
            category="category",
            description="description",
            name="name",
            tags=["string"],
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_metadata(self, client: SystemPromptStorage) -> None:
        response = client.prompts.with_raw_response.update_metadata(
            path_id="id",
            body_id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_metadata(self, client: SystemPromptStorage) -> None:
        with client.prompts.with_streaming_response.update_metadata(
            path_id="id",
            body_id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(str, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_metadata(self, client: SystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            client.prompts.with_raw_response.update_metadata(
                path_id="",
                body_id="id",
            )


class TestAsyncPrompts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.create(
            content="content",
        )
        assert_matches_type(Prompt, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.create(
            content="content",
            branched=True,
            category="category",
            description="description",
            name="name",
            parent="parent",
            tags=["string"],
        )
        assert_matches_type(Prompt, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSystemPromptStorage) -> None:
        response = await async_client.prompts.with_raw_response.create(
            content="content",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(Prompt, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSystemPromptStorage) -> None:
        async with async_client.prompts.with_streaming_response.create(
            content="content",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(Prompt, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.retrieve(
            "id",
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSystemPromptStorage) -> None:
        response = await async_client.prompts.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSystemPromptStorage) -> None:
        async with async_client.prompts.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(str, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.prompts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.update(
            path_id="id",
            body_id="id",
            content="content",
            parent="parent",
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.update(
            path_id="id",
            body_id="id",
            content="content",
            parent="parent",
            branched=True,
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSystemPromptStorage) -> None:
        response = await async_client.prompts.with_raw_response.update(
            path_id="id",
            body_id="id",
            content="content",
            parent="parent",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSystemPromptStorage) -> None:
        async with async_client.prompts.with_streaming_response.update(
            path_id="id",
            body_id="id",
            content="content",
            parent="parent",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(str, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncSystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            await async_client.prompts.with_raw_response.update(
                path_id="",
                body_id="id",
                content="content",
                parent="parent",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.list(
            category="category",
            from_=0,
            size=0,
            to=0,
        )
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSystemPromptStorage) -> None:
        response = await async_client.prompts.with_raw_response.list(
            category="category",
            from_=0,
            size=0,
            to=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSystemPromptStorage) -> None:
        async with async_client.prompts.with_streaming_response.list(
            category="category",
            from_=0,
            size=0,
            to=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(PromptListResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.delete(
            "id",
        )
        assert prompt is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSystemPromptStorage) -> None:
        response = await async_client.prompts.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert prompt is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSystemPromptStorage) -> None:
        async with async_client.prompts.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.prompts.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_content(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.retrieve_content(
            id="id",
            latest=True,
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_content(self, async_client: AsyncSystemPromptStorage) -> None:
        response = await async_client.prompts.with_raw_response.retrieve_content(
            id="id",
            latest=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_content(self, async_client: AsyncSystemPromptStorage) -> None:
        async with async_client.prompts.with_streaming_response.retrieve_content(
            id="id",
            latest=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(str, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_content(self, async_client: AsyncSystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.prompts.with_raw_response.retrieve_content(
                id="",
                latest=True,
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_metadata(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.update_metadata(
            path_id="id",
            body_id="id",
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_metadata_with_all_params(self, async_client: AsyncSystemPromptStorage) -> None:
        prompt = await async_client.prompts.update_metadata(
            path_id="id",
            body_id="id",
            category="category",
            description="description",
            name="name",
            tags=["string"],
        )
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_metadata(self, async_client: AsyncSystemPromptStorage) -> None:
        response = await async_client.prompts.with_raw_response.update_metadata(
            path_id="id",
            body_id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(str, prompt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_metadata(self, async_client: AsyncSystemPromptStorage) -> None:
        async with async_client.prompts.with_streaming_response.update_metadata(
            path_id="id",
            body_id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(str, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_metadata(self, async_client: AsyncSystemPromptStorage) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            await async_client.prompts.with_raw_response.update_metadata(
                path_id="",
                body_id="id",
            )

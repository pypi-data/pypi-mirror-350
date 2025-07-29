# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

import httpx

from ..types import (
    prompt_list_params,
    prompt_create_params,
    prompt_update_params,
    prompt_update_metadata_params,
    prompt_retrieve_content_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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
from ..types.prompt_list_response import PromptListResponse
from ..types.prompt_create_response import PromptCreateResponse

__all__ = ["PromptResource", "AsyncPromptResource"]


class PromptResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PromptResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cruzluna/sps-python#accessing-raw-response-data-eg-headers
        """
        return PromptResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PromptResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cruzluna/sps-python#with_streaming_response
        """
        return PromptResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        content: str,
        branched: Optional[bool] | NotGiven = NOT_GIVEN,
        category: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        parent: Optional[str] | NotGiven = NOT_GIVEN,
        tags: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateResponse:
        """
        Create prompt

        Args:
          content: The content of the prompt

          branched: Whether the prompt is being branched

          category: The category of the prompt

          description: The description of the prompt

          name: The name of the prompt

          parent: The parent of the prompt. If its a new prompt with no lineage, this should be
              None.

          tags: The tags of the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/prompt",
            body=maybe_transform(
                {
                    "content": content,
                    "branched": branched,
                    "category": category,
                    "description": description,
                    "name": name,
                    "parent": parent,
                    "tags": tags,
                },
                prompt_create_params.PromptCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptCreateResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Get prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return self._get(
            f"/prompt/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    def update(
        self,
        path_id: str,
        *,
        body_id: str,
        content: str,
        parent: str,
        branched: Optional[bool] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Update prompt

        Args:
          body_id: The id of the prompt to update

          content: The content of the updated prompt

          parent: The parent of the updated prompt. Most times its the same as the id of the
              prompt to update.

          branched: Whether the updated prompt is branched

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_id:
            raise ValueError(f"Expected a non-empty value for `path_id` but received {path_id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return self._put(
            f"/prompt/{path_id}",
            body=maybe_transform(
                {
                    "body_id": body_id,
                    "content": content,
                    "parent": parent,
                    "branched": branched,
                },
                prompt_update_params.PromptUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    def list(
        self,
        *,
        category: str,
        from_: int,
        size: int,
        to: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptListResponse:
        """
        Get list of prompts with pagination

        Args:
          category: The category of the prompts to return

          from_: The pagination offset to start from (0-based)

          size: The number of prompts to return

          to: The pagination offset to end at (exclusive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/prompts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "category": category,
                        "from_": from_,
                        "size": size,
                        "to": to,
                    },
                    prompt_list_params.PromptListParams,
                ),
            ),
            cast_to=PromptListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/prompt/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def retrieve_content(
        self,
        id: str,
        *,
        latest: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Get prompt content

        Args:
          latest: Latest version of the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return self._get(
            f"/prompt/{id}/content",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"latest": latest}, prompt_retrieve_content_params.PromptRetrieveContentParams),
            ),
            cast_to=str,
        )

    def update_metadata(
        self,
        path_id: str,
        *,
        body_id: str,
        category: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        tags: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Update prompt metadata

        Args:
          body_id: The id of the prompt

          category: The category of the prompt

          description: The description of the prompt

          name: The name of the prompt

          tags: The tags of the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_id:
            raise ValueError(f"Expected a non-empty value for `path_id` but received {path_id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return self._put(
            f"/prompt/{path_id}/metadata",
            body=maybe_transform(
                {
                    "body_id": body_id,
                    "category": category,
                    "description": description,
                    "name": name,
                    "tags": tags,
                },
                prompt_update_metadata_params.PromptUpdateMetadataParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class AsyncPromptResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPromptResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cruzluna/sps-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPromptResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPromptResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cruzluna/sps-python#with_streaming_response
        """
        return AsyncPromptResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        content: str,
        branched: Optional[bool] | NotGiven = NOT_GIVEN,
        category: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        parent: Optional[str] | NotGiven = NOT_GIVEN,
        tags: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateResponse:
        """
        Create prompt

        Args:
          content: The content of the prompt

          branched: Whether the prompt is being branched

          category: The category of the prompt

          description: The description of the prompt

          name: The name of the prompt

          parent: The parent of the prompt. If its a new prompt with no lineage, this should be
              None.

          tags: The tags of the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/prompt",
            body=await async_maybe_transform(
                {
                    "content": content,
                    "branched": branched,
                    "category": category,
                    "description": description,
                    "name": name,
                    "parent": parent,
                    "tags": tags,
                },
                prompt_create_params.PromptCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptCreateResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Get prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return await self._get(
            f"/prompt/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    async def update(
        self,
        path_id: str,
        *,
        body_id: str,
        content: str,
        parent: str,
        branched: Optional[bool] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Update prompt

        Args:
          body_id: The id of the prompt to update

          content: The content of the updated prompt

          parent: The parent of the updated prompt. Most times its the same as the id of the
              prompt to update.

          branched: Whether the updated prompt is branched

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_id:
            raise ValueError(f"Expected a non-empty value for `path_id` but received {path_id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return await self._put(
            f"/prompt/{path_id}",
            body=await async_maybe_transform(
                {
                    "body_id": body_id,
                    "content": content,
                    "parent": parent,
                    "branched": branched,
                },
                prompt_update_params.PromptUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )

    async def list(
        self,
        *,
        category: str,
        from_: int,
        size: int,
        to: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptListResponse:
        """
        Get list of prompts with pagination

        Args:
          category: The category of the prompts to return

          from_: The pagination offset to start from (0-based)

          size: The number of prompts to return

          to: The pagination offset to end at (exclusive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/prompts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "category": category,
                        "from_": from_,
                        "size": size,
                        "to": to,
                    },
                    prompt_list_params.PromptListParams,
                ),
            ),
            cast_to=PromptListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete prompt

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/prompt/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def retrieve_content(
        self,
        id: str,
        *,
        latest: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Get prompt content

        Args:
          latest: Latest version of the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return await self._get(
            f"/prompt/{id}/content",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"latest": latest}, prompt_retrieve_content_params.PromptRetrieveContentParams
                ),
            ),
            cast_to=str,
        )

    async def update_metadata(
        self,
        path_id: str,
        *,
        body_id: str,
        category: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        tags: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Update prompt metadata

        Args:
          body_id: The id of the prompt

          category: The category of the prompt

          description: The description of the prompt

          name: The name of the prompt

          tags: The tags of the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_id:
            raise ValueError(f"Expected a non-empty value for `path_id` but received {path_id!r}")
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return await self._put(
            f"/prompt/{path_id}/metadata",
            body=await async_maybe_transform(
                {
                    "body_id": body_id,
                    "category": category,
                    "description": description,
                    "name": name,
                    "tags": tags,
                },
                prompt_update_metadata_params.PromptUpdateMetadataParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class PromptResourceWithRawResponse:
    def __init__(self, prompt: PromptResource) -> None:
        self._prompt = prompt

        self.create = to_raw_response_wrapper(
            prompt.create,
        )
        self.retrieve = to_raw_response_wrapper(
            prompt.retrieve,
        )
        self.update = to_raw_response_wrapper(
            prompt.update,
        )
        self.list = to_raw_response_wrapper(
            prompt.list,
        )
        self.delete = to_raw_response_wrapper(
            prompt.delete,
        )
        self.retrieve_content = to_raw_response_wrapper(
            prompt.retrieve_content,
        )
        self.update_metadata = to_raw_response_wrapper(
            prompt.update_metadata,
        )


class AsyncPromptResourceWithRawResponse:
    def __init__(self, prompt: AsyncPromptResource) -> None:
        self._prompt = prompt

        self.create = async_to_raw_response_wrapper(
            prompt.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            prompt.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            prompt.update,
        )
        self.list = async_to_raw_response_wrapper(
            prompt.list,
        )
        self.delete = async_to_raw_response_wrapper(
            prompt.delete,
        )
        self.retrieve_content = async_to_raw_response_wrapper(
            prompt.retrieve_content,
        )
        self.update_metadata = async_to_raw_response_wrapper(
            prompt.update_metadata,
        )


class PromptResourceWithStreamingResponse:
    def __init__(self, prompt: PromptResource) -> None:
        self._prompt = prompt

        self.create = to_streamed_response_wrapper(
            prompt.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            prompt.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            prompt.update,
        )
        self.list = to_streamed_response_wrapper(
            prompt.list,
        )
        self.delete = to_streamed_response_wrapper(
            prompt.delete,
        )
        self.retrieve_content = to_streamed_response_wrapper(
            prompt.retrieve_content,
        )
        self.update_metadata = to_streamed_response_wrapper(
            prompt.update_metadata,
        )


class AsyncPromptResourceWithStreamingResponse:
    def __init__(self, prompt: AsyncPromptResource) -> None:
        self._prompt = prompt

        self.create = async_to_streamed_response_wrapper(
            prompt.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            prompt.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            prompt.update,
        )
        self.list = async_to_streamed_response_wrapper(
            prompt.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            prompt.delete,
        )
        self.retrieve_content = async_to_streamed_response_wrapper(
            prompt.retrieve_content,
        )
        self.update_metadata = async_to_streamed_response_wrapper(
            prompt.update_metadata,
        )

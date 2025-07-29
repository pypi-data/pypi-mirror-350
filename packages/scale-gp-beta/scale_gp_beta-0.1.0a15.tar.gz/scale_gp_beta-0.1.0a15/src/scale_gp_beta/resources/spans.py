# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, overload

import httpx

from ..types import span_list_params, span_batch_params, span_create_params, span_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import required_args, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorPage, AsyncCursorPage, SyncAPIListPage, AsyncAPIListPage
from ..types.span import Span
from .._base_client import AsyncPaginator, make_request_options

__all__ = ["SpansResource", "AsyncSpansResource"]


class SpansResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpansResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return SpansResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpansResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return SpansResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        name: str,
        start_timestamp: Union[str, datetime],
        trace_id: str,
        id: str | NotGiven = NOT_GIVEN,
        end_timestamp: Union[str, datetime] | NotGiven = NOT_GIVEN,
        input: Dict[str, object] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        output: Dict[str, object] | NotGiven = NOT_GIVEN,
        parent_id: str | NotGiven = NOT_GIVEN,
        status: Literal["SUCCESS", "ERROR"] | NotGiven = NOT_GIVEN,
        type: Literal[
            "TEXT_INPUT",
            "TEXT_OUTPUT",
            "COMPLETION_INPUT",
            "COMPLETION",
            "KB_RETRIEVAL",
            "KB_INPUT",
            "RERANKING",
            "EXTERNAL_ENDPOINT",
            "PROMPT_ENGINEERING",
            "DOCUMENT_INPUT",
            "MAP_REDUCE",
            "DOCUMENT_SEARCH",
            "DOCUMENT_PROMPT",
            "CUSTOM",
            "INPUT_GUARDRAIL",
            "OUTPUT_GUARDRAIL",
            "CODE_EXECUTION",
            "DATA_MANIPULATION",
            "EVALUATION",
            "FILE_RETRIEVAL",
            "KB_ADD_CHUNK",
            "KB_MANAGEMENT",
            "TRACER",
            "AGENT_TRACER",
            "AGENT_WORKFLOW",
            "STANDALONE",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        """
        Create Span

        Args:
          trace_id: id for grouping traces together, uuid is recommended

          id: The id of the span

          parent_id: Reference to a parent span_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        application_interaction_id: str,
        application_variant_id: str,
        name: str,
        start_timestamp: Union[str, datetime],
        trace_id: str,
        id: str | NotGiven = NOT_GIVEN,
        end_timestamp: Union[str, datetime] | NotGiven = NOT_GIVEN,
        input: Dict[str, object] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        output: Dict[str, object] | NotGiven = NOT_GIVEN,
        parent_id: str | NotGiven = NOT_GIVEN,
        status: Literal["SUCCESS", "ERROR"] | NotGiven = NOT_GIVEN,
        type: Literal[
            "TEXT_INPUT",
            "TEXT_OUTPUT",
            "COMPLETION_INPUT",
            "COMPLETION",
            "KB_RETRIEVAL",
            "KB_INPUT",
            "RERANKING",
            "EXTERNAL_ENDPOINT",
            "PROMPT_ENGINEERING",
            "DOCUMENT_INPUT",
            "MAP_REDUCE",
            "DOCUMENT_SEARCH",
            "DOCUMENT_PROMPT",
            "CUSTOM",
            "INPUT_GUARDRAIL",
            "OUTPUT_GUARDRAIL",
            "CODE_EXECUTION",
            "DATA_MANIPULATION",
            "EVALUATION",
            "FILE_RETRIEVAL",
            "KB_ADD_CHUNK",
            "KB_MANAGEMENT",
            "TRACER",
            "AGENT_TRACER",
            "AGENT_WORKFLOW",
            "STANDALONE",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        """
        Create Span

        Args:
          trace_id: id for grouping traces together, uuid is recommended

          id: The id of the span

          parent_id: Reference to a parent span_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["name", "start_timestamp", "trace_id"],
        ["application_interaction_id", "application_variant_id", "name", "start_timestamp", "trace_id"],
    )
    def create(
        self,
        *,
        name: str,
        start_timestamp: Union[str, datetime],
        trace_id: str,
        id: str | NotGiven = NOT_GIVEN,
        end_timestamp: Union[str, datetime] | NotGiven = NOT_GIVEN,
        input: Dict[str, object] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        output: Dict[str, object] | NotGiven = NOT_GIVEN,
        parent_id: str | NotGiven = NOT_GIVEN,
        status: Literal["SUCCESS", "ERROR"] | NotGiven = NOT_GIVEN,
        type: Literal[
            "TEXT_INPUT",
            "TEXT_OUTPUT",
            "COMPLETION_INPUT",
            "COMPLETION",
            "KB_RETRIEVAL",
            "KB_INPUT",
            "RERANKING",
            "EXTERNAL_ENDPOINT",
            "PROMPT_ENGINEERING",
            "DOCUMENT_INPUT",
            "MAP_REDUCE",
            "DOCUMENT_SEARCH",
            "DOCUMENT_PROMPT",
            "CUSTOM",
            "INPUT_GUARDRAIL",
            "OUTPUT_GUARDRAIL",
            "CODE_EXECUTION",
            "DATA_MANIPULATION",
            "EVALUATION",
            "FILE_RETRIEVAL",
            "KB_ADD_CHUNK",
            "KB_MANAGEMENT",
            "TRACER",
            "AGENT_TRACER",
            "AGENT_WORKFLOW",
            "STANDALONE",
        ]
        | NotGiven = NOT_GIVEN,
        application_interaction_id: str | NotGiven = NOT_GIVEN,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        return self._post(
            "/v5/spans",
            body=maybe_transform(
                {
                    "name": name,
                    "start_timestamp": start_timestamp,
                    "trace_id": trace_id,
                    "id": id,
                    "end_timestamp": end_timestamp,
                    "input": input,
                    "metadata": metadata,
                    "output": output,
                    "parent_id": parent_id,
                    "status": status,
                    "type": type,
                    "application_interaction_id": application_interaction_id,
                    "application_variant_id": application_variant_id,
                },
                span_create_params.SpanCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    def retrieve(
        self,
        span_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        """
        Get Span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_id:
            raise ValueError(f"Expected a non-empty value for `span_id` but received {span_id!r}")
        return self._get(
            f"/v5/spans/{span_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    def update(
        self,
        span_id: str,
        *,
        end_timestamp: Union[str, datetime] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        output: Dict[str, object] | NotGiven = NOT_GIVEN,
        status: Literal["SUCCESS", "ERROR"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        """
        Update Span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_id:
            raise ValueError(f"Expected a non-empty value for `span_id` but received {span_id!r}")
        return self._patch(
            f"/v5/spans/{span_id}",
            body=maybe_transform(
                {
                    "end_timestamp": end_timestamp,
                    "metadata": metadata,
                    "name": name,
                    "output": output,
                    "status": status,
                },
                span_update_params.SpanUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    def list(
        self,
        *,
        ending_before: str | NotGiven = NOT_GIVEN,
        from_ts: int | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        parents_only: bool | NotGiven = NOT_GIVEN,
        sort_order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        to_ts: int | NotGiven = NOT_GIVEN,
        trace_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[Span]:
        """
        List Spans

        Args:
          from_ts: The starting (oldest) timestamp window in seconds.

          to_ts: The ending (most recent) timestamp in seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/spans",
            page=SyncCursorPage[Span],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "from_ts": from_ts,
                        "limit": limit,
                        "parents_only": parents_only,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "to_ts": to_ts,
                        "trace_id": trace_id,
                    },
                    span_list_params.SpanListParams,
                ),
            ),
            model=Span,
        )

    def batch(
        self,
        *,
        items: Iterable[span_batch_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncAPIListPage[Span]:
        """
        Create Spans in Batch

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/spans/batch",
            page=SyncAPIListPage[Span],
            body=maybe_transform({"items": items}, span_batch_params.SpanBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=Span,
            method="post",
        )


class AsyncSpansResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpansResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncSpansResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpansResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncSpansResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        name: str,
        start_timestamp: Union[str, datetime],
        trace_id: str,
        id: str | NotGiven = NOT_GIVEN,
        end_timestamp: Union[str, datetime] | NotGiven = NOT_GIVEN,
        input: Dict[str, object] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        output: Dict[str, object] | NotGiven = NOT_GIVEN,
        parent_id: str | NotGiven = NOT_GIVEN,
        status: Literal["SUCCESS", "ERROR"] | NotGiven = NOT_GIVEN,
        type: Literal[
            "TEXT_INPUT",
            "TEXT_OUTPUT",
            "COMPLETION_INPUT",
            "COMPLETION",
            "KB_RETRIEVAL",
            "KB_INPUT",
            "RERANKING",
            "EXTERNAL_ENDPOINT",
            "PROMPT_ENGINEERING",
            "DOCUMENT_INPUT",
            "MAP_REDUCE",
            "DOCUMENT_SEARCH",
            "DOCUMENT_PROMPT",
            "CUSTOM",
            "INPUT_GUARDRAIL",
            "OUTPUT_GUARDRAIL",
            "CODE_EXECUTION",
            "DATA_MANIPULATION",
            "EVALUATION",
            "FILE_RETRIEVAL",
            "KB_ADD_CHUNK",
            "KB_MANAGEMENT",
            "TRACER",
            "AGENT_TRACER",
            "AGENT_WORKFLOW",
            "STANDALONE",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        """
        Create Span

        Args:
          trace_id: id for grouping traces together, uuid is recommended

          id: The id of the span

          parent_id: Reference to a parent span_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        application_interaction_id: str,
        application_variant_id: str,
        name: str,
        start_timestamp: Union[str, datetime],
        trace_id: str,
        id: str | NotGiven = NOT_GIVEN,
        end_timestamp: Union[str, datetime] | NotGiven = NOT_GIVEN,
        input: Dict[str, object] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        output: Dict[str, object] | NotGiven = NOT_GIVEN,
        parent_id: str | NotGiven = NOT_GIVEN,
        status: Literal["SUCCESS", "ERROR"] | NotGiven = NOT_GIVEN,
        type: Literal[
            "TEXT_INPUT",
            "TEXT_OUTPUT",
            "COMPLETION_INPUT",
            "COMPLETION",
            "KB_RETRIEVAL",
            "KB_INPUT",
            "RERANKING",
            "EXTERNAL_ENDPOINT",
            "PROMPT_ENGINEERING",
            "DOCUMENT_INPUT",
            "MAP_REDUCE",
            "DOCUMENT_SEARCH",
            "DOCUMENT_PROMPT",
            "CUSTOM",
            "INPUT_GUARDRAIL",
            "OUTPUT_GUARDRAIL",
            "CODE_EXECUTION",
            "DATA_MANIPULATION",
            "EVALUATION",
            "FILE_RETRIEVAL",
            "KB_ADD_CHUNK",
            "KB_MANAGEMENT",
            "TRACER",
            "AGENT_TRACER",
            "AGENT_WORKFLOW",
            "STANDALONE",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        """
        Create Span

        Args:
          trace_id: id for grouping traces together, uuid is recommended

          id: The id of the span

          parent_id: Reference to a parent span_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["name", "start_timestamp", "trace_id"],
        ["application_interaction_id", "application_variant_id", "name", "start_timestamp", "trace_id"],
    )
    async def create(
        self,
        *,
        name: str,
        start_timestamp: Union[str, datetime],
        trace_id: str,
        id: str | NotGiven = NOT_GIVEN,
        end_timestamp: Union[str, datetime] | NotGiven = NOT_GIVEN,
        input: Dict[str, object] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        output: Dict[str, object] | NotGiven = NOT_GIVEN,
        parent_id: str | NotGiven = NOT_GIVEN,
        status: Literal["SUCCESS", "ERROR"] | NotGiven = NOT_GIVEN,
        type: Literal[
            "TEXT_INPUT",
            "TEXT_OUTPUT",
            "COMPLETION_INPUT",
            "COMPLETION",
            "KB_RETRIEVAL",
            "KB_INPUT",
            "RERANKING",
            "EXTERNAL_ENDPOINT",
            "PROMPT_ENGINEERING",
            "DOCUMENT_INPUT",
            "MAP_REDUCE",
            "DOCUMENT_SEARCH",
            "DOCUMENT_PROMPT",
            "CUSTOM",
            "INPUT_GUARDRAIL",
            "OUTPUT_GUARDRAIL",
            "CODE_EXECUTION",
            "DATA_MANIPULATION",
            "EVALUATION",
            "FILE_RETRIEVAL",
            "KB_ADD_CHUNK",
            "KB_MANAGEMENT",
            "TRACER",
            "AGENT_TRACER",
            "AGENT_WORKFLOW",
            "STANDALONE",
        ]
        | NotGiven = NOT_GIVEN,
        application_interaction_id: str | NotGiven = NOT_GIVEN,
        application_variant_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        return await self._post(
            "/v5/spans",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "start_timestamp": start_timestamp,
                    "trace_id": trace_id,
                    "id": id,
                    "end_timestamp": end_timestamp,
                    "input": input,
                    "metadata": metadata,
                    "output": output,
                    "parent_id": parent_id,
                    "status": status,
                    "type": type,
                    "application_interaction_id": application_interaction_id,
                    "application_variant_id": application_variant_id,
                },
                span_create_params.SpanCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    async def retrieve(
        self,
        span_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        """
        Get Span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_id:
            raise ValueError(f"Expected a non-empty value for `span_id` but received {span_id!r}")
        return await self._get(
            f"/v5/spans/{span_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    async def update(
        self,
        span_id: str,
        *,
        end_timestamp: Union[str, datetime] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, object] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        output: Dict[str, object] | NotGiven = NOT_GIVEN,
        status: Literal["SUCCESS", "ERROR"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Span:
        """
        Update Span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_id:
            raise ValueError(f"Expected a non-empty value for `span_id` but received {span_id!r}")
        return await self._patch(
            f"/v5/spans/{span_id}",
            body=await async_maybe_transform(
                {
                    "end_timestamp": end_timestamp,
                    "metadata": metadata,
                    "name": name,
                    "output": output,
                    "status": status,
                },
                span_update_params.SpanUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    def list(
        self,
        *,
        ending_before: str | NotGiven = NOT_GIVEN,
        from_ts: int | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        parents_only: bool | NotGiven = NOT_GIVEN,
        sort_order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        to_ts: int | NotGiven = NOT_GIVEN,
        trace_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Span, AsyncCursorPage[Span]]:
        """
        List Spans

        Args:
          from_ts: The starting (oldest) timestamp window in seconds.

          to_ts: The ending (most recent) timestamp in seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/spans",
            page=AsyncCursorPage[Span],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "from_ts": from_ts,
                        "limit": limit,
                        "parents_only": parents_only,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "to_ts": to_ts,
                        "trace_id": trace_id,
                    },
                    span_list_params.SpanListParams,
                ),
            ),
            model=Span,
        )

    def batch(
        self,
        *,
        items: Iterable[span_batch_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Span, AsyncAPIListPage[Span]]:
        """
        Create Spans in Batch

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/spans/batch",
            page=AsyncAPIListPage[Span],
            body=maybe_transform({"items": items}, span_batch_params.SpanBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=Span,
            method="post",
        )


class SpansResourceWithRawResponse:
    def __init__(self, spans: SpansResource) -> None:
        self._spans = spans

        self.create = to_raw_response_wrapper(
            spans.create,
        )
        self.retrieve = to_raw_response_wrapper(
            spans.retrieve,
        )
        self.update = to_raw_response_wrapper(
            spans.update,
        )
        self.list = to_raw_response_wrapper(
            spans.list,
        )
        self.batch = to_raw_response_wrapper(
            spans.batch,
        )


class AsyncSpansResourceWithRawResponse:
    def __init__(self, spans: AsyncSpansResource) -> None:
        self._spans = spans

        self.create = async_to_raw_response_wrapper(
            spans.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            spans.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            spans.update,
        )
        self.list = async_to_raw_response_wrapper(
            spans.list,
        )
        self.batch = async_to_raw_response_wrapper(
            spans.batch,
        )


class SpansResourceWithStreamingResponse:
    def __init__(self, spans: SpansResource) -> None:
        self._spans = spans

        self.create = to_streamed_response_wrapper(
            spans.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            spans.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            spans.update,
        )
        self.list = to_streamed_response_wrapper(
            spans.list,
        )
        self.batch = to_streamed_response_wrapper(
            spans.batch,
        )


class AsyncSpansResourceWithStreamingResponse:
    def __init__(self, spans: AsyncSpansResource) -> None:
        self._spans = spans

        self.create = async_to_streamed_response_wrapper(
            spans.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            spans.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            spans.update,
        )
        self.list = async_to_streamed_response_wrapper(
            spans.list,
        )
        self.batch = async_to_streamed_response_wrapper(
            spans.batch,
        )

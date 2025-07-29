# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = ["SpanBatchParams", "Item", "ItemBaseSpanCreateRequest", "ItemLegacyApplicationSpanCreateRequest"]


class SpanBatchParams(TypedDict, total=False):
    items: Required[Iterable[Item]]


class ItemBaseSpanCreateRequest(TypedDict, total=False):
    name: Required[str]

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    trace_id: Required[str]
    """id for grouping traces together, uuid is recommended"""

    id: str
    """The id of the span"""

    end_timestamp: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    input: Dict[str, object]

    metadata: Dict[str, object]

    output: Dict[str, object]

    parent_id: str
    """Reference to a parent span_id"""

    status: Literal["SUCCESS", "ERROR"]

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


class ItemLegacyApplicationSpanCreateRequest(TypedDict, total=False):
    application_interaction_id: Required[str]

    application_variant_id: Required[str]

    name: Required[str]

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    trace_id: Required[str]
    """id for grouping traces together, uuid is recommended"""

    id: str
    """The id of the span"""

    end_timestamp: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    input: Dict[str, object]

    metadata: Dict[str, object]

    output: Dict[str, object]

    parent_id: str
    """Reference to a parent span_id"""

    status: Literal["SUCCESS", "ERROR"]

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


Item: TypeAlias = Union[ItemBaseSpanCreateRequest, ItemLegacyApplicationSpanCreateRequest]

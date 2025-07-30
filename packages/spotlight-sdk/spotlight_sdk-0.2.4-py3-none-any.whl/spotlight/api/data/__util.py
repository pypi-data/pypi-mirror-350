import json
from typing import Optional

from spotlight.api.data.model import (
    TimeseriesQueryRequest,
    DistinctQueryRequest,
    QueryRequest,
)


def _query_timeseries_request_info(
    request: TimeseriesQueryRequest, one: Optional[bool] = False
) -> dict:
    return {
        "endpoint": f"data/v1.1/timeseries",
        "json": request.request_dict(),
        "params": {"one": True} if one else {},
    }


def _query_timeseries_csv_request_info(
    id: str, request: TimeseriesQueryRequest
) -> dict:
    return {"endpoint": f"data/v1.1/{id}.csv", "json": request.request_dict()}


def _query_distinct_fields_request_info(
    request: DistinctQueryRequest, use_cache: Optional[bool] = None
) -> dict:
    return {
        "endpoint": f"data/v1.1/distinct",
        "json": request.request_dict(),
        "params": {"cache": str(use_cache)},
    }


def _query_request_info(request: QueryRequest, one: Optional[bool] = False) -> dict:
    return {
        "endpoint": f"data/v1.1/query",
        "json": request.request_dict(),
        "params": {"one": "true"} if one else {},
    }


def _query_csv_request_info(id: str, request: QueryRequest) -> dict:
    json_str = json.dumps(request.request_dict(), separators=(",", ":"))

    return {
        "endpoint": f"data/v1.1/query/{id}.csv",
        "params": {"query": json_str},
    }

"""
Data classes for API requests.
"""

from typing import List, Optional, Any

from pydantic import Field as PyField

from spotlight.core.common.base import Base
from spotlight.core.common.decorators.serializable import (
    serializable_base_class,
    serializable,
)
from spotlight.core.common.enum import (
    Order,
    ComparisonOperator,
    LogicalOperator,
    SqlFunction,
)


class Sort(Base):
    field: str
    order: Order


class Filter(Base):
    field: str
    operator: ComparisonOperator
    value: Any


class WhereClause(Base):
    filter: Optional[Filter] = PyField(default=None)
    operator: Optional[LogicalOperator] = PyField(default=None)
    left: Optional["WhereClause"] = PyField(default=None)
    right: Optional["WhereClause"] = PyField(default=None)


class TimeseriesQueryRequest(Base):
    id: Optional[str] = PyField(default=None)
    dataset_name: Optional[str] = PyField(default=None)
    reference_name: Optional[str] = PyField(default=None)
    page: Optional[int] = PyField(default=None)
    limit: Optional[int] = PyField(default=None)
    fields: Optional[List[str]] = PyField(default=None)
    sort: Optional[List[Sort]] = PyField(default=None)
    where: Optional[WhereClause] = PyField(default=None)


class DistinctQueryRequest(Base):
    id: Optional[str] = PyField(default=None)
    dataset_name: Optional[str] = PyField(default=None)
    reference_name: Optional[str] = PyField(default=None)
    field: str = PyField(default=None)
    sort: Optional[List[Sort]] = PyField(default=None)
    where: Optional[WhereClause] = PyField(default=None)


@serializable_base_class
class Expression(Base):
    pass


@serializable
class FieldExpression(Expression):
    pass


@serializable
class FunctionExpression(FieldExpression):
    pass


@serializable
class Field(FieldExpression):
    name: str
    alias: Optional[str] = PyField(default=None)


@serializable
class SingleExpression(FunctionExpression):
    parameter: FieldExpression
    operator: SqlFunction
    alias: Optional[str] = PyField(default=None)


@serializable
class MultiExpression(FunctionExpression):
    parameters: List[FieldExpression]
    operator: SqlFunction
    alias: Optional[str] = PyField(default=None)


class QueryRequest(Base):
    id: Optional[str] = PyField(default=None)
    dataset_name: Optional[str] = PyField(default=None)
    reference_name: Optional[str] = PyField(default=None)
    fields: Optional[List[FieldExpression]] = PyField(default=None)
    where: Optional[WhereClause] = PyField(default=None)
    groups: Optional[List[str]] = PyField(default=None)
    page: Optional[int] = PyField(default=None)
    limit: Optional[int] = PyField(default=None)
    sort: Optional[List[Sort]] = PyField(default=None)

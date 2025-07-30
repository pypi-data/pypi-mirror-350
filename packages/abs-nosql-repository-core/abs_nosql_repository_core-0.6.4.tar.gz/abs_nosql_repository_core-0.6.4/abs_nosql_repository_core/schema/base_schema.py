from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum
from typing import Optional, Union, List, Any, Literal

class Operator(str, Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NIN = "nin"
    LIKE = "like"
    ILIKE = "ilike"
    BETWEEN = "between"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"

class LogicalOperator(str, Enum):
    AND = "and"
    OR = "or"

class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"

class FieldTypeEnum(str, Enum):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"
    DATETIME = "datetime"

class BaseSchema(BaseModel):
    _id: str
    uuid: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BaseDraftSchema(BaseSchema):
    is_draft: bool = Field(default=True)

# Schema for getting distinct values of a field
class FindUniqueByFieldInput(BaseModel):
    field_name: str
    ordering: Optional[Literal["asc", "desc"]] = None
    page: Optional[int] = Field(default=1)
    page_size: Optional[int] = Field(default=10)
    search: Optional[str] = None

# Primitive field condition
class FieldOperatorCondition(BaseModel):
    field: str
    operator: Operator
    value: Any

# Base structure for a logical group
class LogicalCondition(BaseModel):
    operator: LogicalOperator
    conditions: List["ConditionType"]

# Each item in conditions list can be:
# 1. a logical condition (nested group)
# 2. a dict like {field: ..., operator: ..., value: ...}
ConditionType = Union["LogicalCondition", "FieldOperatorCondition"]

# Top-level filter schema
class FilterSchema(BaseModel):
    operator: LogicalOperator
    conditions: List[ConditionType]

# Sort schema
class SortSchema(BaseModel):
    field: str
    direction: SortDirection

# Schema for displaying search operations
class SearchOptions(BaseModel):
    search: Optional[str] = None
    sort_order: Optional[List[SortSchema]] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    total_pages: Optional[int] = None
    total_count: Optional[int] = None

# Schema for displaying find operations' result
class ListResponse(BaseModel):
    founds: List[Any]
    search_options: SearchOptions

class AggregationType(str, Enum):
    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    MAX = "max"
    MIN = "min"

class AggregationSpec(BaseModel):
    field: str
    type: AggregationType
    alias: str

class Aggregations(BaseModel):
    group_by: List[str]
    document_inclusion_mode: Optional[Literal["none", "all", "partial"]] = Field(
        default="none",
        description="Options: 'none', 'all', 'partial' . 'none' means no document fields will be included in the response, 'all' means all document fields will be included in the response, 'partial' means only the document fields that match the included_fields will be included in the response"
    )
    included_fields: Optional[List[str]] = Field(
        default=None,
        description="Fields to include when document_inclusion_mode is 'partial'"
    )
    aggregation_fields: Optional[List[AggregationSpec]] = None

class FieldRule(BaseModel):
    action: Literal["include", "exclude"]
    field: str
    conditions: Optional[FilterSchema] = None

class GraphLookup(BaseModel):
    max_depth: Optional[int] = Field(default=1)
    connect_from_field: str = Field(default=None)
    connect_to_field: str = Field(default=None)

class ReferenceField(BaseModel):
    local_field: str = Field(description="The field of the local entity")
    foreign_field: str = Field(description="The field of the foreign entity")
    foreign_entity: str = Field(description="The name of the foreign entity")
    alias: str = Field(description="The alias of the foreign entity")
    view_fields: Optional[List[str]] = None
    use_graph_lookup: Optional[GraphLookup] = Field(default=None)

class ListFilter(BaseModel):
    filters: Optional[FilterSchema] = None
    sort_order: Optional[List[SortSchema]] = None
    page: Optional[int] = Field(default=1)
    page_size: Optional[int] = Field(default=20)
    search: Optional[str] = None
    searchable_fields: Optional[List[str]] = None
    field_rules: Optional[List[FieldRule]] = None
    reference_fields: Optional[List[ReferenceField]] = None
    aggregations: Optional[Aggregations] = None
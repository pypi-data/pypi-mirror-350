"""Types definitions."""

from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum
from typing import Any, Type

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class ContentType(StrEnum):
    """Enum representing content types."""

    CSV = "CSV"
    JSON = "JSON"
    PARQUET = "PARQUET"

    def extension(self) -> list[str]:
        """Get file extensions associated with the content type."""
        return {
            ContentType.CSV: [".csv"],
            ContentType.JSON: [".json"],
            ContentType.PARQUET: [".parquet"],
        }[self]


class ParameterType(StrEnum):
    """Input parameters types."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DATE = "date"
    DATETIME = "datetime"
    BOOLEAN = "boolean"

    def get_type(self) -> Type:
        """Get the corresponding Python type for the parameter type."""
        return {
            ParameterType.STRING: str,
            ParameterType.INTEGER: int,
            ParameterType.FLOAT: float,
            ParameterType.DATE: date,
            ParameterType.DATETIME: datetime,
            ParameterType.BOOLEAN: bool,
        }[self]


class ParameterSpec(BaseModel):
    """Parameter specification."""

    name: str
    type: ParameterType
    description: str
    default: str
    required: bool


class TableStr(str):
    """Special string type to mark field that takes table name as input."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Get custom schema for Pydantic validation."""
        return core_schema.no_info_after_validator_function(
            lambda v: TableStr(v), core_schema.str_schema()
        )


class ColumnStr(str):
    """Special string type to mark field that takes column name as input."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Get custom schema for Pydantic validation."""
        return core_schema.no_info_after_validator_function(
            lambda v: ColumnStr(v), core_schema.str_schema()
        )


@dataclass(frozen=True)
class ColumnStrMeta:
    """Metadata for ColumnStr type."""

    table_field: str = "table"
    tables_field: str = "tables"
    table_fields: list[str] | None = None


class BaseOperationModel(BaseModel):
    """Base model for operations."""

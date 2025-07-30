"""Filer row operation."""

from pydantic import Field

from datarush.core.dataflow import Operation, Tableset
from datarush.core.types import BaseOperationModel, ColumnStr, TableStr


class FilterRowModel(BaseOperationModel):
    """Filter row operation model."""

    table: TableStr = Field(title="Table", description="Table to filter")
    column: ColumnStr = Field(title="Column", description="Column to filter by")
    value: str = Field(title="Value", description="Value to filter for")


class FilterByColumn(Operation):
    """Filter row by column value operation."""

    name = "filter"
    title = "Filter"
    description = "Filter table rows by column value"
    model: FilterRowModel

    def summary(self) -> str:
        """Provide operation summary."""
        return f"Filter `{self.model.table}` where {self.model.column} is {self.model.value}"

    def operate(self, tableset: Tableset) -> Tableset:
        """Run operation."""
        table, column, value = self.model.table, self.model.column, self.model.value
        df = tableset.get_df(table)
        filtered_df = df[df[column] == value]
        tableset.set_df(table, filtered_df)
        return tableset

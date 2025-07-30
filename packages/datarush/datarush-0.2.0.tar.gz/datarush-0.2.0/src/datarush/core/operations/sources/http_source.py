"""HTTP Source."""

from io import BytesIO

import requests
from pydantic import BaseModel, Field

from datarush.core.dataflow import Operation, Tableset
from datarush.core.types import ContentType
from datarush.utils.misc import read_file


class HttpSourceModel(BaseModel):
    """HTTP Source model."""

    url: str = Field(title="URL", default="https://api.github.com/users/mralexgray/repos")
    content_type: ContentType = Field(title="Content Type")
    table_name: str = Field(title="table_name", default="http_table")


class HttpSource(Operation):
    """HTTP source operation."""

    name = "http_request"
    title = "HTTP Request"
    description = "Send an HTTP request to get a file"
    model: HttpSourceModel

    def summary(self) -> str:
        """Provide operation summary."""
        return f"Load HTTP resource {self.model.url} as `{self.model.table_name}` table"

    def operate(self, tableset: Tableset) -> Tableset:
        """Run operation."""
        response = requests.get(self.model.url)
        response.raise_for_status()
        file = BytesIO(response.content)
        df = read_file(file, self.model.content_type)
        tableset.set_df(self.model.table_name, df)
        return tableset

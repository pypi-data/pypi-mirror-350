"""S3 dataset source operation."""

from __future__ import annotations

import pandas as pd
from pydantic import BaseModel, Field

from datarush.config import S3Config
from datarush.core.dataflow import Operation, Tableset
from datarush.core.types import ContentType
from datarush.utils.s3_client import DatasetDoesNotExistError, S3Dataset


class S3DatasetSourceModel(BaseModel):
    """S3 dataset Source model."""

    bucket: str = Field(title="Bucket")
    path: str = Field(title="Dataset Path", default="datasets/wrangler/my-dataset-2")
    content_type: ContentType = Field(title="Content Type")
    table_name: str = Field(title="Table Name", default="s3_table")
    error_on_empty: bool = Field(
        title="Error on empty",
        default=True,
        description="Raise an error if the dataset is empty",
    )


class S3DatasetSource(Operation):
    """S3 dataset source operation."""

    name = "s3_dataset_source"
    title = "S3 Dataset Source"
    description = "Download dataset from S3"
    model: S3DatasetSourceModel

    def initialize(self) -> None:
        """Initialize the operation."""
        self._config = S3Config.fromenv()

    def summary(self) -> str:
        """Provide operation summary."""
        return f"Load S3 dataset as `{self.model.table_name}` table"

    def operate(self, tableset: Tableset) -> Tableset:
        """Run operation."""
        dataset = S3Dataset(
            bucket=self.model.bucket,
            prefix=self.model.path,
            content_type=self.model.content_type,
            config=self._config,
        )
        try:
            df = dataset.read()
        except DatasetDoesNotExistError:
            if self.model.error_on_empty:
                raise
            df = pd.DataFrame()
        tableset.set_df(self.model.table_name, df)
        return tableset

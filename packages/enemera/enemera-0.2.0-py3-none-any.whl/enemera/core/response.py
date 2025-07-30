"""
Response handling for the Enemera API.

This module provides the APIResponse class, which extends the built-in list 
to provide additional functionality for converting API responses to various
data formats (pandas DataFrames, polars DataFrames, CSV, Excel, etc.)
"""

import pathlib
from typing import Union, List, TypeVar

import pandas as pd

from enemera.models.response_models import BaseTimeSeriesResponse
from enemera.validators.validators import validate_filepath

T = TypeVar('T', bound=BaseTimeSeriesResponse)


class APIResponse(List[T]):
    """Enhanced list that supports data conversion methods"""

    def __init__(self, data: List[T]):
        super().__init__(data)
        self._data = data

    def to_pandas(self, index_col: str = 'utc', naive_datetime: bool = False) -> pd.DataFrame:
        """Convert to pandas DataFrame"""
        if not self._data:
            return pd.DataFrame()

        # Convert to dict records
        records = [item.model_dump() for item in self._data]
        df = pd.DataFrame(records)

        # Set datetime index if specified
        if index_col and index_col in df.columns:
            # if the index_col is a datetime, convert it to datetime type
            if pd.api.types.is_datetime64_any_dtype(df[index_col]):
                df[index_col] = pd.to_datetime(df[index_col])
                df.set_index(index_col, inplace=True)

                if naive_datetime and df.index.tz is not None:
                    # convert to naive datetime (remove timezone)
                    df.index = df.index.tz_localize(None)
                    return df

                if not naive_datetime and df.index.tz is None:
                    # localize as UTC timezone if naive datetime
                    df.index = df.index.tz_localize('UTC')
                    return df

            else:
                # if the index_col is not a datetime, just set it as index
                df.set_index(index_col, inplace=True)

        return df

    def to_pandas_cet(self, naive_datetime: bool = False) -> pd.DataFrame:
        """Convert to pandas DataFrame and convert UTC to CET timezone"""
        if not self._data:
            return pd.DataFrame()

        # Convert to dict records
        records = [item.model_dump() for item in self._data]
        df = pd.DataFrame(records)

        # Set datetime index if specified
        index_col = 'utc'
        if index_col in df.columns:
            df[index_col] = pd.to_datetime(df[index_col])
            df.set_index(index_col, inplace=True)
            # localize as UTC timezone if naive datetime
            if df.index.tz is None:
                df.index = df.index.tz_localize('UTC')
            # convert to CET timezone
            df.index = df.index.tz_convert('CET')
            # rename index to 'cet' for clarity
            df.index.name = 'cet'

        # use naive_datetime
        if naive_datetime:
            # convert to naive datetime (remove timezone)
            df.index = df.index.tz_localize(None)

        return df

    def to_polars(self) -> 'pl.DataFrame':
        """Convert to polars DataFrame"""
        try:
            import polars as pl
        except ImportError:
            raise ImportError(
                "polars is required. Install with: pip install polars")

        if not self._data:
            return pl.DataFrame()

        records = [item.model_dump() for item in self._data]
        return pl.DataFrame(records)

    def to_csv(self, filepath: Union[str, pathlib.Path], **kwargs) -> None:
        """Save to CSV file"""

        path = validate_filepath(filepath, 'csv')
        df = self.to_pandas()
        df.to_csv(path, **kwargs)

    def to_excel(self, filepath: Union[str, pathlib.Path], **kwargs) -> None:
        """Save to Excel file"""
        try:
            import openpyxl
        except ImportError:
            raise ImportError(
                "openpyxl is required for Excel export. Install with: pip install openpyxl")

        import warnings
        warnings.warn(
            "Excel does not support timezone-aware datetimes. "
            "The data is being converted to timezone-naive datetimes. "
            "Please put particular care in the correct interpretation of the timezone "
            "when viewing or analyzing this Excel file, as the original timezone information is lost."
        )

        path = validate_filepath(filepath, 'xlsx')
        df = self.to_pandas(naive_datetime=True)
        df.to_excel(path, **kwargs)

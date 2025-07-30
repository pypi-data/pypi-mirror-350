import io
from typing import Any, BinaryIO, Dict, Literal, Protocol


class PandasLikeDataFrame(Protocol):
    def to_parquet(
        self,
        path: Any,
        engine: Any = ...,
        compression: Any = ...,
        index: bool = ...,
    ) -> Any:
        ...


PolarsCompression = Literal[
    "lz4", "uncompressed", "snappy", "gzip", "lzo", "brotli", "zstd"
]


class PolarsLikeDataFrame(Protocol):
    def write_parquet(
        self,
        file: BinaryIO,
        *,
        compression: PolarsCompression,
    ) -> None:
        ...


def pandas_dataframe_to_parquet(
    df: PandasLikeDataFrame,
    context: Any,
    file_name: str,
    *,
    engine: Literal["pyarrow", "fastparquet"] = "pyarrow",
    compression: str = "snappy",
) -> str:
    """
    Converts a Pandas-like DataFrame to Parquet format and writes the result to storage.

    Args:
        df: A Pandas DataFrame instance.
        context (Any): The task context with a write_file method.
        file_name (str): The target file name for storage.
        engine (str): Parquet engine ("pyarrow" or "fastparquet").
        compression (str): Compression method ("snappy", "gzip", "zstd", etc).

    Returns:
        str: The file ID assigned by the storage system.
    """
    if not file_name:
        raise ValueError("file_name is required.")

    buffer = io.BytesIO()
    df.to_parquet(buffer, engine=engine, compression=compression, index=False)
    buffer.seek(0)
    parquet_data = buffer.getvalue()

    file_pointer: Dict[str, str] = context.write_file(
        content=parquet_data,
        file_name=file_name,
        file_category="PROCESSED",
        gzip_compress_level=0,
    )
    return file_pointer["fileId"]


def polars_dataframe_to_parquet(
    df: PolarsLikeDataFrame,
    context: Any,
    file_name: str,
    *,
    compression: PolarsCompression = "snappy",
) -> str:
    """
    Converts a Polars-like DataFrame to Parquet format and writes the result to storage.

    Args:
        df: A Polars DataFrame instance.
        context (Any): The task context with a write_file method.
        file_name (str): The target file name for storage.
        compression (str): Compression method ("snappy", "gzip", "zstd", etc).

    Returns:
        str: The file ID assigned by the storage system.
    """
    if not file_name:
        raise ValueError("file_name is required.")

    buffer = io.BytesIO()
    df.write_parquet(buffer, compression=compression)
    buffer.seek(0)
    parquet_data = buffer.getvalue()

    file_pointer: Dict[str, str] = context.write_file(
        content=parquet_data,
        file_name=file_name,
        file_category="PROCESSED",
        gzip_compress_level=0,
    )
    return file_pointer["fileId"]

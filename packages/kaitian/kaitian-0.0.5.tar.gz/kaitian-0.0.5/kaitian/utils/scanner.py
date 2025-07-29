from __future__ import annotations

import logging
import pickle
from datetime import datetime
from pathlib import Path

import polars as pl

from .cache import get_cache_file


def scan_csv(
    source: str | Path,
    *,
    try_parse_dates: bool = True,
    has_header: bool = True,
    skip_rows_after_header: int = 0,
    skip_rows: int = 0,
    n_rows: int | None = None,
    null_values: str | list[str] | dict[str, str] | None = None,
    separator: str = ",",
    comment_prefix: str | None = None,
    quote_char: str | None = '"',
    low_memory: bool = False,
    use_cache: bool = True,
    cache_folder: str | Path | None = None,
    schema_overrides: pl.Schema | dict[str, pl.DataType] | None = None,
    **kwargs,
) -> pl.LazyFrame:
    """Scanning csv data schema.

    Try to scanning csv data schema with all data and save schema information
    to cache file.

    The cache file name will be the encoding of source's absolute path, and the
    cache data is a python dict saved as pickle file:
    {
        'mtime': file/modified/time,
        'schema': polars.Schema
    }
    """
    logger = logging.getLogger(__name__)
    mtime = datetime.fromtimestamp(Path(source).stat().st_mtime)
    cache_file = get_cache_file(str(Path(source).absolute()), root=cache_folder)

    if cache_file.exists():
        with open(cache_file, "rb") as f:
            cache = pickle.load(f)
            _mtime: datetime = cache.get("mtime")
            _schema: pl.Schema | None = cache.get("schema")
        if schema_overrides is not None and _schema is not None:
            _schema.update(pl.Schema(schema_overrides))
    else:
        _mtime = datetime.now()
        _schema = None

    if use_cache and _mtime == mtime and _schema is not None:
        logger.debug(f"load schema from cache {cache_file}")
        schema = _schema
    else:
        logger.debug(
            f"try to parse {source}, because "
            f"{(_mtime==mtime)=} or "
            f"{(_schema is not None)=} or "
            f"{use_cache=}"
        )
        schema = pl.scan_csv(
            source=source,
            infer_schema=True,
            infer_schema_length=None,
            try_parse_dates=try_parse_dates,
            has_header=has_header,
            skip_rows_after_header=skip_rows_after_header,
            skip_rows=skip_rows,
            n_rows=n_rows,
            null_values=null_values,
            separator=separator,
            comment_prefix=comment_prefix,
            quote_char=quote_char,
            low_memory=low_memory,
            schema_overrides=schema_overrides,
            **kwargs,
        ).collect_schema()
        logger.debug(f"parse {source} done, with {len(schema)} columns")
        cache = {"mtime": mtime, "schema": schema}
        # always update the cache file
        with open(cache_file, "wb") as f:
            pickle.dump(cache, f)
        logger.debug(f"cache schema to {cache_file}")

    return pl.scan_csv(
        source,
        schema=schema,
        try_parse_dates=try_parse_dates,
        has_header=has_header,
        skip_rows_after_header=skip_rows_after_header,
        skip_rows=skip_rows,
        n_rows=n_rows,
        null_values=null_values,
        separator=separator,
        comment_prefix=comment_prefix,
        quote_char=quote_char,
        low_memory=low_memory,
        **kwargs,
    )

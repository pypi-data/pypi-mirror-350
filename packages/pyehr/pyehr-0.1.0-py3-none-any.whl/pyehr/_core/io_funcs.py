# my_io/io_funcs.py
import os
from typing import Callable, Dict

import pandas as pd
import dask.dataframe as dd


def read_stata(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_stata(path, **kwargs)


def read_csv(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, **kwargs)


def read_txt(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", **kwargs)


# Callable functions for reading different file types
_DISPATCH_READ: Dict[str, Callable] = {
    ".dta": pd.read_stata,
    ".csv": dd.read_csv,
    ".txt": dd.read_table,
}


def read_file(path: str, **kwargs) -> pd.DataFrame:
    # Check file extension
    ext = os.path.splitext(path)[1].lower()
    if ext not in _DISPATCH_READ:
        raise ValueError(f"Invalid file extension: {ext}")

    # Check if the file exists
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    # Read the file using the appropriate function
    data = _DISPATCH_READ[ext](path, **kwargs)

    return data


def write_file(df, output_path: str, **kwargs):
    ext = os.path.splitext(output_path)[1].lower()
    if ext == ".csv":
        df.to_csv(output_path, index=False, **kwargs)
    elif ext == ".txt":
        df.to_csv(output_path, index=False, sep="\t", **kwargs)
    elif ext == ".dta":
        df.to_stata(output_path, write_index=False, **kwargs)
    else:
        raise ValueError(f"Invalid file extension: {ext}")


def batch_convert(
    input_paths: list[str],
    output_dir: str,
    output_ext: str = ".csv",
    read_kwargs=None,
    write_kwargs=None,
):
    read_kwargs = read_kwargs or {}
    write_kwargs = write_kwargs or {}
    os.makedirs(output_dir, exist_ok=True)
    for path in input_paths:
        df = read_file(path, **read_kwargs)
        fname = os.path.splitext(os.path.basename(path))[0] + output_ext
        write_file(df, os.path.join(output_dir, fname), **write_kwargs)

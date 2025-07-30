import os
import glob
from typing import Union, Sequence, Set, List, Literal, Any
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd
import dask.dataframe as dd

from ._core.io_funcs import read_file, write_file


def extract_from_file(
    file_path: str,
    id_col: str,
    values: Union[Sequence[Any], Set[Any]],
    **argskwargs: Any,
) -> pd.DataFrame:
    """
    Extract rows from a file based on a specific column and values.

    Args:
        file_path: _path_ to the file from which to extract rows.
        id_col: The column used to filter rows.
        values: The values to filter the id_col against.


    Returns:
        pd.DataFrame: A DataFrame containing the filtered rows.
    """
    # Read the full file into a DataFrame
    df = read_file(file_path, **argskwargs)

    # Ensure the identifier column exists
    if id_col not in df.columns:
        raise KeyError(f"Column '{id_col}' not found in file: {file_path}")

    # Filter rows by membership in values
    return df[df[id_col].isin(values)]


def extract_from_table(
    table_dir: str,
    file_ext: str = "csv",
    id_col: str = "patid",
    values: Union[Sequence[Any], Set[Any]] = list(),
    output_dir: str = "./output",
    single_file: bool = False,
    output_name: str = "extraction",
    output_ext: Literal["csv", "parquet"] = "csv",
):
    """
    Funtion to extract rows from table (files) in a directory based on a specific column and values.

    Args:
        table_dir: files directory for a specific table.
        file_ext: file extensions to look for (e.g., ["txt", "csv"]).
        id_col:  The column used to filter rows.
        values: The values to filter the id_col against.
        single_file: whether to keep output as a single file or not. Defaults to False.
        output_ext: file extension to save. Defaults to "csv".
        output_dir: output directory path. Defaults to "./output".
        output_name: the name of the output file(s). Defaults to "extraction".
    """
    # Check if the table directory exists
    if not table_dir:
        raise FileNotFoundError(
            f"No files found in {table_dir} with extensions {file_ext}"
        )

    # Check if the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read all files in the directory with the specified extensions
    if file_ext == "txt":
        ddf = dd.read_csv(f"{table_dir}/*.{file_ext}", sep="\t", assume_missing=True)
    else:
        ddf = dd.read_csv(f"{table_dir}/*.{file_ext}", assume_missing=True)
    # Extract the rows
    filtered = ddf[ddf[id_col].isin(values)]

    # Output
    if single_file:
        output_path = os.path.join(output_dir, f"{output_name}.{output_ext}")
        write_file(filtered, output_path, single_file=single_file)
    else:
        filtered.to_csv(f"{output_dir}/", index=False, single_file=single_file)


def extract_from_stata(
    table_dir: str,
    file_ext: str = "dta",
    id_col: str = "patid",
    values: Union[Sequence[Any], Set[Any]] = list(),
    cores: int = 1,
    output_dir: str = "./output",
    output_name: str = "extraction",
    output_ext: Literal["csv", "txt"] = "csv",
    single_file: bool = False,
    **argekwargs: Any,
):
    """
    Extract rows from Stata files (for a table) in a directory based on a specific column and values.

    Args:
        table_dir: files directory for a specific table.
        file_ext: file extensions to look for (e.g., ["txt", "csv"]).
        id_col:  The column used to filter rows.
        values: The values to filter the id_col against.
        cores: number of cores to use for parallel processing. Defaults to 1.
        output_dir: _output_ directory path (if single_file is True, the result will be saved as 'combined_output.XXX' in this directory). Defaults to "./output".
        output_ext: file extension to save. Defaults to "csv".
        single_file: whether to keep output as a single file or not. Defaults to False.
    """

    # 1) Get all file paths in the directory with the specified extensions
    file_paths: List[str] = []
    pattern = os.path.join(table_dir, f"*.{file_ext}")
    file_paths.extend(glob.glob(pattern))

    total = len(file_paths)  # Total number of files found

    if not file_paths:
        raise FileNotFoundError(
            f"No files found in {table_dir} with extensions {file_ext}"
        )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2) Parallel processing
    dfs: List[pd.DataFrame] = []
    with ProcessPoolExecutor(max_workers=cores) as executor:
        futures = {
            executor.submit(extract_from_file, fp, id_col, values, **argekwargs): fp
            for fp in file_paths
        }

        completed_count = 0  # Count of completed futures
        for fut in as_completed(futures):
            completed_count += 1
            try:
                result = fut.result()
                if not result.empty:
                    if single_file:
                        dfs.append(result)
                    else:
                        output_path = os.path.join(
                            output_dir,
                            os.path.splitext(os.path.basename(futures[fut]))[0],
                            output_ext,
                        )
                        result.to_csv(output_path, index=False)
                print(f"Completed: [{completed_count}/{total}]")

            except Exception as e:
                fp = futures[fut]
                print(f"Error in processing {fp}: {e}")

        if single_file:
            if dfs:
                print(f"Combining {len(dfs)} files...")
                combined_df = pd.concat(dfs, ignore_index=True)

                output_path = os.path.join(
                    output_dir,
                    f"{output_name}.{output_ext}",
                )
                write_file(combined_df, output_path)
            else:
                print("No matching rows found in any file.")


if __name__ == "__main__":
    pass

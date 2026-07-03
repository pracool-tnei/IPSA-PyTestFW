import os
import pytest
from pathlib import Path

#file copy and unzip
import shutil
import zipfile

from runtime_config import CONFIG

ROOT = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(
    0,
    str(ROOT / "Resources")
)

import Create_difference_file
from Logger import debug, info, error, setLoggerMode

def compare_against_benchmark(result_file,
                               ipsa_version):
    """
    Compare generated result with benchmark.
    """

    result_file = str(result_file)



    benchmark_file = result_file.replace(
        ipsa_version,
        CONFIG.benchmark_version
    )

    diff_file = (
        Path(result_file).parent /
        "pytest_difference.xlsx"
    )

    comparison_status, differences = (
        Create_difference_file.compare_and_highlight(
            benchmark_file,
            result_file,
            str(diff_file)
        )
    )

    return comparison_status, differences, diff_file


def assert_comparison_passed(
        comparison_status,
        differences,
        diff_file):

    if comparison_status:
        return

    msg = "\nComparison failed\n"

    for sheet, diff in differences.items():

        msg += f"\nSheet : {sheet}\n"

        for row in diff[:10]:
            msg += f"{row}\n"

    msg += (
        f"\nDetailed report:\n"
        f"{diff_file}"
    )

    pytest.fail(msg)
    
from pathlib import Path

import pandas as pd
from pathlib import Path


def compare_dataframes(
        benchmark_df,
        result_df,
        tolerance=1e-5):

    differences = []

    if benchmark_df.shape != result_df.shape:

        differences.append(
            f"Shape mismatch : "
            f"{benchmark_df.shape} != "
            f"{result_df.shape}"
        )

        return differences

    for col in benchmark_df.columns:

        if col not in result_df.columns:

            differences.append(
                f"Missing column : {col}"
            )

            continue

        for idx in range(len(benchmark_df)):

            expected = benchmark_df.iloc[idx][col]
            actual = result_df.iloc[idx][col]

            if pd.isna(expected) and pd.isna(actual):
                continue

            try:

                expected = float(expected)
                actual = float(actual)

                if abs(expected - actual) > tolerance:

                    differences.append(
                        f"Row={idx}, "
                        f"Column={col}, "
                        f"Expected={expected}, "
                        f"Actual={actual}"
                    )

            except Exception:

                if str(expected) != str(actual):

                    differences.append(
                        f"Row={idx}, "
                        f"Column={col}, "
                        f"Expected={expected}, "
                        f"Actual={actual}"
                    )

    return differences

def ensure_local_benchmark(cwd, network_path):
    local_benchmark_root = Path(cwd).parent / "Test Results" / f"{CONFIG.benchmark_version}"

    # Already cached locally
    if local_benchmark_root.exists():
        info(f"Using local benchmark cache: {local_benchmark_root}")
        return str(local_benchmark_root)

    network_zip = network_path

    if not os.path.exists(network_zip):
        raise FileNotFoundError(
            f"Benchmark archive not found:\n{network_zip}"
        )

    debug(f"Downloading benchmark archive from : {network_zip}...")

    local_zip = Path(cwd).parent / "Test Results" / f"{CONFIG.benchmark_version}.zip"

    os.makedirs(local_zip.parent, exist_ok=True)

    shutil.copy2(network_zip, local_zip)

    debug("Extracting benchmark archive...")

    with zipfile.ZipFile(local_zip, 'r') as zf:
        zf.extractall(local_zip.parent)

    debug("Benchmark extraction complete.")

    return str(local_benchmark_root)

def set_log_level(log_level):
    if log_level == "DEBUG":
        setLoggerMode(True)
    elif log_level == "INFO":
        setLoggerMode(False)
    else:
        error(f"Invalid log level: {log_level}")
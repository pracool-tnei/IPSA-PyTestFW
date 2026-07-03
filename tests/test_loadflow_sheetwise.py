import sys
from pathlib import Path

import pytest
import pandas as pd

from runtime_config import CONFIG

from Logger import debug, info, error, setLoggerMode

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT / "Resources")
)

import Loadflow

from data_generators import (
    get_sheet_cases
)

from utils import (
    compare_dataframes
)

from conftest import discover_models


def pytest_generate_tests(metafunc):

    if CONFIG.mode == "benchmark-generation":
        metafunc.parametrize("case", [])
        return

    if "case" not in metafunc.fixturenames:
        return

    import ipsa

    ipsa_interface = ipsa.GetInterface()

    resources_dir = ROOT / "Resources"

    cases = []
    ids = []

    for model_path in discover_models():

        net = ipsa_interface.ReadFile(
            str(model_path)
        )

        model_name_stem = model_path.stem
        model_name = model_path.name

        output_file = (
            Loadflow.run_loadflow(
                ipsa_interface,
                net,
                str(resources_dir),
                ipsa_interface.GetVersion(),
                model_name
            )
        )

        debug(f"Test Fault Sheetwise : Output file: {output_file}")
        benchmark_dir = (
            ROOT /
            "Test Results" /
            CONFIG.benchmark_version /
            model_name_stem /
            "Load Flow"
        )

        benchmark_files = list(
            benchmark_dir.glob("*.xlsx")
        )

        if not benchmark_files:
            raise FileNotFoundError(
                f"No benchmark found in {benchmark_dir}"
            )

        benchmark_file = benchmark_files[0]
        
        

        sheet_cases = get_sheet_cases(
            benchmark_file,
            output_file,
            model_name_stem
        )

        for case in sheet_cases:

            cases.append(case)

            ids.append(
                f"{case['model']}-"
                f"{case['sheet']}"
            )

    metafunc.parametrize(
        "case",
        cases,
        ids=ids
    )

@pytest.mark.comparison
@pytest.mark.loadflow_sheet
def test_loadflow_sheet(case):

    benchmark_df = pd.read_excel(
        case["benchmark_file"],
        sheet_name=case["sheet"]
    )

    result_df = pd.read_excel(
        case["result_file"],
        sheet_name=case["sheet"]
    )

    differences = compare_dataframes(
        benchmark_df,
        result_df
    )

    assert not differences, (
        "\n".join(differences[:20])
    )
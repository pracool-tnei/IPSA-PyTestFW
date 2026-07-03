import sys
from pathlib import Path

import pytest

from runtime_config import CONFIG

from Logger import debug, info, error, setLoggerMode

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "Resources"))

import Loadflow

from utils import (
    compare_against_benchmark,
    assert_comparison_passed
)

@pytest.mark.comparison
@pytest.mark.loadflow
def test_loadflow(network, resources_dir):
    ipsa_interface = network["ipsa"]
    net = network["network"]

    ipsa_version = ipsa_interface.GetVersion()

    model_name = network["path"].name

    try:

        output_file = Loadflow.run_loadflow(
            ipsa_interface,
            net,
            str(resources_dir),
            ipsa_version,
            model_name
        )

    except Exception as ex:

        pytest.skip(
            f"Loadflow unsupported : {ex}"
        )

    comparison_status, differences, diff_file = \
        compare_against_benchmark(
            output_file,
            ipsa_version
        )

    assert_comparison_passed(
        comparison_status,
        differences,
        diff_file
    )

@pytest.mark.generation
def test_loadflow_generation(network, resources_dir):
    ipsa_interface = network["ipsa"]
    net = network["network"]

    ipsa_version = ipsa_interface.GetVersion()

    model_name = network["path"].name

    try:

        output_file = Loadflow.run_loadflow(
            ipsa_interface,
            net,
            str(resources_dir),
            CONFIG.benchmark_version,
            model_name
        )

    except Exception as ex:

        pytest.skip(
            f"Loadflow unsupported : {ex}"
        )

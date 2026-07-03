import sys
from pathlib import Path

import pytest
import ipsa

import os

from utils import ensure_local_benchmark, set_log_level

from runtime_config import CONFIG

ROOT = Path(__file__).resolve().parent.parent

RESOURCES_DIR = ROOT / "Resources"
MODELS_DIR = RESOURCES_DIR / "models"

sys.path.insert(0, str(RESOURCES_DIR))

def pytest_addoption(parser):
    parser.addoption(
        "--network-benchmark",
        action="store",
        default=r"S:\Adarsh\vbenchmark.zip",
        help="benchmark network path"
    )

    parser.addoption(
        "--target-version",
        action="store",
        default="v3.3.0",
        help="target version to use"
    )

    parser.addoption(
        "--benchmark-version",
        action="store",
        default="vbenchmark",
        help="Benchmark version to use"
    )

    parser.addoption(
        "--mode",
        action="store",
        default="benchmark-comparison",
        choices=[
            "benchmark-generation",
            "benchmark-comparison"
        ],
        help=(
            "benchmark-generation : generate benchmark only\n"
            "benchmark-comparison : run tests against benchmark"
        )
    )

def pytest_configure(config):
    CONFIG.mode = config.getoption("--mode")

    CONFIG.benchmark_version = config.getoption(
        "--benchmark-version"
    )

    CONFIG.target_version = config.getoption(
        "--target-version"
    )

    CONFIG.network_benchmark = config.getoption(
        "--network-benchmark"
    )

    CONFIG.log_level = config.getoption(
        "--log-level"
    )

@pytest.fixture(scope="session")
def benchmark_version(request):
    return request.config.getoption("--benchmark-version")

@pytest.fixture(scope="session")
def target_version(request):
    return request.config.getoption("--target-version")

@pytest.fixture(scope="session")
def network_path(request):
    return request.config.getoption("--network-path")


@pytest.fixture(scope="session")
def resources_dir():
    return RESOURCES_DIR

@pytest.fixture(scope="session", autouse=True)
def change_working_directory():

    original_dir = os.getcwd()

    os.chdir(str(RESOURCES_DIR))

    yield

    os.chdir(original_dir)


def discover_models():
    """
    Discover all IPSA network files.
    """

    networks = []

    for extension in ("*.i2f", "*.i3f"):
        networks.extend(MODELS_DIR.rglob(extension))

    return sorted(networks)


@pytest.fixture(scope="session")
def ipsa_interface():
    """
    Create IPSA interface once per test session.
    """
    return ipsa.GetInterface()


@pytest.fixture(
    scope="module",
    params=discover_models(),
    ids=lambda p: p.stem
)
def network(request, ipsa_interface):
    """
    Open each network as a separate test parameter.
    """

    model_path = request.param

    net = ipsa_interface.ReadFile(str(model_path))

    return {
        "path": model_path,
        "name": model_path.stem,
        "network": net,
        "ipsa": ipsa_interface
    }

def pytest_sessionstart(session):
    """
    Called once before test collection starts.
    Ensures local benchmark files are available.
    """
    log_level = session.config.getoption(
        "--log-level"
    )
    set_log_level(log_level)

    mode = session.config.getoption(
        "--mode"
    )

    # No benchmark required while generating benchmarks
    if mode == "benchmark-generation":
        return

    network_zip = session.config.getoption(
        "--network-benchmark"
    )
    ensure_local_benchmark(RESOURCES_DIR, network_zip)

def pytest_collection_modifyitems(config, items):

    mode = config.getoption("--mode")

    skip_comparison = pytest.mark.skip(
        reason="Skipped in benchmark generation mode"
    )

    skip_generation = pytest.mark.skip(
        reason="Skipped in benchmark comparison mode"
    )

    for item in items:

        if (
            mode == "benchmark-generation"
            and "comparison" in item.keywords
        ):
            item.add_marker(skip_comparison)

        elif (
            mode == "benchmark-comparison"
            and "generation" in item.keywords
        ):
            item.add_marker(skip_generation)
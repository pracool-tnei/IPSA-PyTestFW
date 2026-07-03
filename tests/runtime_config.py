from dataclasses import dataclass


@dataclass
class RuntimeConfig:
    benchmark_version: str = "vbenchmark"
    target_version: str = "v3.3.0"
    network_benchmark: str = ""
    log_level: str = "INFO"
    mode: str = "benchmark-comparison"


CONFIG = RuntimeConfig()
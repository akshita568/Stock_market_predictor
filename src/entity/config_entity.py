#Using Python @dataclass objects prevents typos in the code by ensuring configuration parameters match strict type definitions.

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    ticker: str
    start_date: str
    end_date: str
    download_path: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    lookback_window: int
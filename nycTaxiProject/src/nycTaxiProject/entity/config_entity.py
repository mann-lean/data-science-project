# ENTITY
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    data_dir: Path
    all_schema: dir

@dataclass(frozen=True) 
class DataTransformationConfig:
    root_dir:Path
    data_dir:Path
    train: Path
    test: Path
    x_train_dir:Path
    y_train_dir:Path
    x_test_dir:Path
    y_test_dir:Path
    before_encoding:Path
    train_before:Path
    test_before:Path
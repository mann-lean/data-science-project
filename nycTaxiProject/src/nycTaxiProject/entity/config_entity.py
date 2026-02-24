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

@dataclass(frozen=True) #frozen=True makes the instance of the class immutable, meaning that once an instance is created, its attributes cannot be modified. This is useful for ensuring that the configuration values remain constant throughout the program's execution, preventing accidental changes and enhancing the integrity of the configuration data.
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
    
@dataclass(frozen=True)
class ModelTrainingConfig:
    root_dir:Path
    xtraining_data:Path
    ytraining_data:Path
    model_dir:Path
    # params for model training
    loss:str
    penalty:str
    alpha:float
    max_iter:int
    tol:float
    random_state:int
    learning_rate:str
    eta0:float
# common.py : This file will contain all the common functions that we will use in our project. We will use these functions in our pipeline and other modules. We will also use these functions in our configuration file to read the configuration file and create the configuration objects.
import os
from box.exceptions import BoxValueError
from nycTaxiProject import logger
import json
import yaml
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64


@ensure_annotations
def read_yaml(path_to_yaml: Path) ->ConfigBox:
    """reads yaml file & returns
    Args:
        path_to_yaml(str):path like input
    Raises:
        ValueError: if yaml file is empty
        e:empty file

    Returns: ConfigBox:COnfigBox type 
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content=yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} LOADED successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories:list,verbose=True):
    """ crete list of directories
    Args:
        path_to_directoreies(list):list of path of direcotries
        ignore_log(bool,optional):ignore if multiple dirs is to be created defatults to False
    """
    for path in path_to_directories:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def get_size(path:Path)->str:
    """get size in KB
    Args:
        path (Path):path of the file
    Returns:
    str:size in KB"""
    size_in_kb=round(os.path.getsize(path)/1024)  # os.path.getsize returns the size of the file in bytes, we divide it by 1024 to convert it to KB and round it to 2 decimal places.
    return f"~ {size_in_kb}KB"
 
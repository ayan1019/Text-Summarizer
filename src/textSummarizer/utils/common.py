import os
from box.exceptions import BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import  ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    '''
    reads yaml file and returns
    Args:
        path_to_yaml: path like input
    Raises: 
        ValueError: if yaml file is empty    
        e: empty
    Returns:
        ConfigBox: ConfigBox type
    '''

    try:
        with open(path_to_yaml) as yaml_file:
            return ConfigBox(yaml.safe_load(yaml_file))
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose=False):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"
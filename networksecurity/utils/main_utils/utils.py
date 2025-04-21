import yaml
from networksecurity.exception.exception import NetworkSecurityException
import networksecurity.logging as logger
import os, sys
import numpy as np
# import dill
import pickle
import json
import joblib
# from box import ConfigBox
from pathlib import Path
from typing import Any
# from box.exceptions import BoxValueError

def read_yaml(path_to_yaml: str):
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input
    
    Raises:
        ValueError: if yaml file is empty
        e: empty file
    
    Returns:
        Content
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.logging.info(f"yaml file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def write_yaml(file_path: str, content: object, replace: bool = False) -> None:
    """write content to yaml file

    Args:
        file_path: file path to yaml file
        content: content to write to yaml file
        replace: to replace the already existing yaml file or not

    Returns:
        None
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_json(path: Path, data:dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    
    logger.logging.logging.info(f"json file saved at: {path}")


def load_json(path: Path):
    """load json files data

    Args:
        path (Path): path to json file
    
    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)
    
    logger.logging.info(f"json file loaded successfully from: {path}")
    return content

def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.logging.info(f"binary file saved at: {path}")

def create_directories(path_to_directories:list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.logging.info(f"created directioy at: {path}")

def save_numpy_array(file_path: str, array: np.array):
    """Save numpy array to file path

    Args:
        file_path (str): Path to save array
        array (numpy array): Array to save

    Returns:
        None  
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
        logger.logging.info(f"Numpy array saved at {file_path}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_object(file_path: str, obj: object):
    """Save object as pickle file
    
    Args:
        file_path (str): Path to save array
        object (object): any object
    
    Returns:
        None
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logger.logging.info(f"{obj} saved at {file_path} as pickle file")
    except Exception as e:
        NetworkSecurityException(e, sys)
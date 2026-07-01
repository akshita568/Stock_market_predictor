#A production project relies on shared utility methods to handle safe file operations and data parsing.

import os
import sys
import yaml
from src.logging.logger import logging
from src.exception.exception import StockPredictorException
from pathlib import Path

def read_yaml(path_to_yaml: Path) -> dict:
    """Reads a YAML file safely with exception tracking."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"YAML file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        raise StockPredictorException(e, sys)

def create_directories(path_to_directories: list, verbose=True):
    """Creates an array of directory strings paths securely."""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging.info(f"Created directory at: {path}")
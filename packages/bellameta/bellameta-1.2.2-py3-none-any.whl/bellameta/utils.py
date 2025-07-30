import os
from os.path import join as _j
import sqlite3
from typing import List
import functools
import pandas as pd
from dotenv import load_dotenv
from ruamel.yaml import YAML

# DATABSES
def sqlite_connection(func):
    '''
    Decorator to facilitate sqlite connection

    Wraps a function that creates a cursor, commits transactions and finally closes the connection
    '''
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        with sqlite3.connect(self.sqlite_path) as conn:
            cursor = conn.cursor()
            try:
                result = func(self, cursor, *args, **kwargs)
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise e
    return wrapper

def get_env(env_path: str|None = None):
    '''
    Searches for a .env file and loads it.

    Parameters
    ----------
    env_path : str|None
        Path to the .env file. If stored at the root of the repository
        load_dotenv will find it automatically.

    Raises
    ------
        RuntimeError if no .env file is found

    Return
    ------
        True if .env file was found
    '''

    success = load_dotenv(env_path)
    if not success:
        raise RuntimeError("No valid .env file found. Make sure to create a .env file at the root of the repository defining CONFIG_PATH.")
    return success

def get_config(config_path: str):
    '''
    Gets the config stored in a .yaml file under the path specified in the .env file
    Parameters
    ----------
    env_path : str|None
        Path to the .env file. If stored at the root of the repository
        load_dotenv will find it automatically.
    
    Return
    ------
        Contents of the yaml file
    '''
    if not os.path.exists(config_path):
        raise RuntimeError("Specified path does not exists. Please define CONFIG_PATH in .env to be a path to a yaml config.")
    yaml = YAML(typ="rt")
    yaml.preserve_quotes = True
    with open(config_path, "r") as f:
        config_data = yaml.load(f)
        return config_data

def custom_title(text):
    '''
    Transform a possibly mispelled text into a consistent title
    '''

    result = []
    make_upper = True
    
    for char in text:
        if char.isalpha():
            if make_upper:
                result.append(char.upper())
            else:
                # Preserve existing case
                result.append(char)
            make_upper = False
        else:
            result.append(char)
            make_upper = True
            
    return ''.join(result)
import os
import json
import tkinter as tk
from tkinter import filedialog


def get_config(config_path):
    '''
    Extract user variables from JSON formatted configuration file.
    Args:
        file_path: <string> config file path
    Returns:
        dictionary: <dict> dictionary of user variables, all values as strings
    '''
    if config_path:
        with open(config_path, 'r') as f:
            return json.load(f)


def dump_json(out_path,
              dictionary):
    '''
    Add a dictionary to a json dictionary.
    Args:
        out_path: <string> path to file, including file name and extension
        dictionary: <dict> python dictionary to put in file
    '''
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2)
        outfile.write('\n')


def check_dir_exists(dir_path):
    '''
    Check to see if a directory path exists and, if not, create one.
    Args:
        dir_path: <string> directory path
    '''
    if os.path.isdir(dir_path) is False:
        os.mkdir(dir_path)

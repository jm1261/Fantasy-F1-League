import os
import json


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


def convert(o):
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def jsonout(out_path,
            dictionary):
    '''
    Add a dictionary to a json dictionary.
    Args:
        out_path: <string> path to file, including file name and extension
        dictionary: <dictionary> python dictionary to put in file
    '''
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')


def check_dir_exists(dir_path):
    '''
    Check to see if a directory path exists and, if not, create one.
    Args:
        dir_path: <string> directory path
    '''
    if os.path.isdir(dir_path) is False:
        os.mkdir(dir_path)

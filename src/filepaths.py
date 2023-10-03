import os

from pathlib import Path


def check_dir_exists(dir_path):
    '''
    Check directory exists, if not make one.
    Args:
        dir_path: <string> path to directory
    Returns:
        None
    '''
    if os.path.isdir(dir_path) is False:
        os.mkdir(dir_path)


def season_dirs(dir_path,
                managers):
    '''
    Create Season Start Directories.
    Args:
        dir_path: <string> path to year directory
    Returns:
        None
    '''
    [
        check_dir_exists(
            dir_path=Path(f'{dir_path}/{manager}'))
        for manager in managers]
    check_dir_exists(dir_path=Path(f'{dir_path}/Figures'))
    check_dir_exists(dir_path=Path(f'{dir_path}/Lineup'))
    check_dir_exists(dir_path=Path(f'{dir_path}/Weekly_Manager'))
    check_dir_exists(dir_path=Path(f'{dir_path}/Managers'))
    check_dir_exists(dir_path=Path(f'{dir_path}/Manager_Formats'))

import os

from pathlib import Path


def check_dir_exists(dir_path : str) -> None:
    """
    Check directory exists.

    Parameters
    ----------
    dir_path: string
        Path to directory to check path exists.

    Returns
    -------
    None

    See Also
    --------
    os.path.isdir
    os.mkdir

    Notes
    -----
    Check directory path exists, if it doesn't it will create a directory at
    the target path.

    Example
    -------
    None

    """
    if os.path.isdir(dir_path) is False:
        os.mkdir(dir_path)


def season_dirs(dir_path : str,
                managers : list) -> None:
    """
    Create the essential directories for a new league.

    Parameters
    ----------
    dir_path: string
        Path to data directory.
    managers: list
        List of partaking managers.

    Returns
    -------
    None

    See Also
    --------
    check_dir_exists

    Notes
    -----
    Checks that the year and essential directory paths exist for a new league.

    Example
    -------
    None

    """
    [
        check_dir_exists(
            dir_path=Path(f'{dir_path}/{manager}'))
        for manager in managers]
    check_dir_exists(dir_path=Path(f'{dir_path}/Figures'))
    check_dir_exists(dir_path=Path(f'{dir_path}/Lineup'))
    check_dir_exists(dir_path=Path(f'{dir_path}/Managers'))


def check_manager_exist(dir_path : str,
                        managers : list) -> list:
    """
    Check to see if there are any new managers.

    Parameters
    ----------
    dir_path: string
        Path to manager format files.
    managers: list
        List of managers.

    Returns
    -------
    new_managers: list
        List of all new managers.

    See Also
    --------
    None

    Notes
    -----
    Checks to see if the managerial format files exist. If they do not, it must
    be a new manager. Adds new managers to a list.

    Example
    -------
    None

    """
    new_managers = []
    for manager in managers:
        manager_path = Path(f'{dir_path}/{manager}.json')
        if manager_path.is_file():
            pass
        else:
            new_managers.append(manager)
    return new_managers
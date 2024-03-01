import os

from pathlib import Path


def check_dir_exists(dir_path : str) -> None:
    """
    Function Details
    ================
    Checks directory path exists.

    Parameters
    ----------
    dir_path: string
        Path to directory.

    Returns
    -------
    None

    See Also
    --------
    None

    Notes
    -----
    If directory does not exist, make one.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Updated documentation.

    """
    if os.path.isdir(dir_path) is False:
        os.mkdir(dir_path)


def season_dirs(dir_path : str,
                managers : list) -> None:
    """
    Function Details
    ================
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

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Updated documentation.

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
    Function Details
    ================
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

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Created.

    """
    new_managers = []
    for manager in managers:
        manager_path = Path(f'{dir_path}/{manager}.json')
        if manager_path.is_file():
            pass
        else:
            new_managers.append(manager)
    return new_managers

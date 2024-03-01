import os
import random

from pathlib import Path
from src.dataIO import load_json, save_json_dicts


def generate_manager_colors(new_managers : list,
                            used_colors : list,
                            dir_path : str) -> None:
    """
    Function Details
    ================
    Generates manager colour files from a list of all matplotlib colours.

    Parameters
    ----------
    new_managers, used_colors: list
        New managers and used color lists.
    dir_path: string
        Path to manager formats directory.

    Returns
    -------
    None

    See Also
    --------
    save_json_dicts

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation.

    """
    all_colors = [
        'dimgrey', 'silver', 'rosybrown', 'lightcoral', 'tomato', 'chocolate',
        'sandybrown', 'peru', 'darkorange', 'wheat', 'goldenrod', 'khaki',
        'olive', 'darkolivegreen', 'palegreen', 'lime', 'aquamarine',
        'turquoise', 'teal', 'cyan', 'skyblue', 'dodgerblue', 'slategrey',
        'royalblue', 'mediumblue', 'slateblue', 'blueviolet',
        'indigo', 'thistle', 'plum', 'violet', 'purple', 'magenta', 'orchid',
        'hotpink', 'crimson', 'brown', 'tan', 'lawngreen', 'cadetblue',
        'rebeccapurple', 'midnightblue']
    colors = [color for color in all_colors if color not in used_colors]
    random.shuffle(colors)
    for index, manager in enumerate(new_managers):
        manager_format = {
            'bold': 'True',
            'size': 12,
            'align': 'centre',
            'font': 'Arial',
            'bg_color': colors[index],
            'teams': []}
        out_path = Path(f'{dir_path}/{manager}.json')
        save_json_dicts(
            out_path=out_path,
            dictionary=manager_format)


def drivers_formats(format_dir : str,
                    driver : str) -> dict:
    """
    Function Details
    ================
    Find driver cell formats, from team colors.

    Parameters
    ----------
    format_dir, driver: string
        Path to format directory and driver name.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation and presentation.

    """
    team_formats = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if 'Perks.json' not in file]
    format_dict = {}
    for team_path in team_formats:
        team_format = load_json(file_path=team_path)
        if driver in team_format['drivers']:
            for key, value in team_format.items():
                if key == 'drivers':
                    pass
                else:
                    format_dict.update({key: value})
    return format_dict


def drivers_colours(format_dir : str,
                    driver : str) -> dict:
    """
    Function Details
    ================
    Find driver colors, from team colors.

    Parameters
    ----------
    format_dir, driver: string
        Path to format directory and driver name.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation and presentation.

    """
    team_formats = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if 'Perks.json' not in file]
    format_dict = {}
    for team_path in team_formats:
        team_format = load_json(file_path=team_path)
        if driver in team_format['drivers']:
            for key, value in team_format.items():
                format_dict.update({key: value})
    return format_dict


def team_format(format_dir : str,
                team : str) -> dict:
    """
    Function Details
    ================
    Find team cell formats, from team colors.

    Parameters
    ----------
    format_dir, team: string
        Path to format directory and team name.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation and presentation.

    """
    paths = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if '.json' in file]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    format_dict = {}
    for index, path in enumerate(paths):
        team_format = load_json(file_path=path)
        if team == teams[index]:
            for key, value in team_format.items():
                if key == 'drivers':
                    pass
                else:
                    format_dict.update({key: value})
    return format_dict


def team_colour(format_dir : str,
                team : str) -> dict:
    """
    Function Details
    ================
    Find team colors, from team colors.

    Parameters
    ----------
    format_dir, team: string
        Path to format directory and tea, name.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation and presentation.

    """
    paths = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if '.json' in file]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    format_dict = {}
    for index, path in enumerate(paths):
        team_format = load_json(file_path=path)
        if team == teams[index]:
            for key, value in team_format.items():
                format_dict.update({key: value})
    return format_dict


def perk_colour(format_dir : str,
                perk : str) -> dict:
    """
    Function Details
    ================
    Find perk colors, from perk colors.

    Parameters
    ----------
    format_dir, perk: string
        Path to format directory and perk name.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation and presentation.

    """
    path = Path(f'{format_dir}/Perks.json')
    perk_formats = load_json(file_path=path)
    all_perks = perk_formats['perks']
    all_colours = perk_formats['bg_color']
    format_dict = {}
    for key, value in perk_formats.items():
        format_dict.update({key: value})
    for p, c in zip(all_perks, all_colours):
        if p == perk:
            format_dict.update({'bg_color': c})
    return format_dict


def manager_team_colour(format_dir : str,
                        team : str) -> dict:
    """
    Function Details
    ================
    Find team colors, from manager colors.

    Parameters
    ----------
    format_dir, team: string
        Path to format directory and team name.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation and presentation.

    """
    paths = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if '.json' in file]
    managers = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    format_dict = {}
    for index, path in enumerate(paths):
        manager_format = load_json(file_path=path)
        if team in manager_format['teams']:
            for key, value in manager_format.items():
                format_dict.update({key: value})
    return format_dict


def managers_colour(format_dir : str,
                    manager : str) -> dict:
    """
    Function Details
    ================
    Find manager colors, from manager colors.

    Parameters
    ----------
    format_dir, manager: string
        Path to format directory and manager name.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation and presentation.

    """
    format_dict = load_json(
        file_path=Path(f'{format_dir}/{manager}.json'))
    return format_dict

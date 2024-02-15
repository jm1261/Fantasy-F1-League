import os
import random

from pathlib import Path
from src.dataIO import load_json, save_json_dicts


def generate_manager_colors(new_managers : list,
                            used_colors : list,
                            dir_path : str) -> None:
    """
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

    Example
    -------
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
import os
import random
import logging
import matplotlib.colors as mcolors

from pathlib import Path
from GeneralUtils.DataIO import load_json, save_json_dicts

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def generate_manager_colors(new_managers: list,
                            used_colors: list,
                            directory_path: str) -> None:
    # 1. Combine all color dictionaries to get Name -> Hex mapping
    # This avoids the "duplicates" issue from your previous version
    color_map = {
        **mcolors.CSS4_COLORS,
        **mcolors.TABLEAU_COLORS,
        **mcolors.BASE_COLORS
    }

    # 2. Filter for unique, unused, and DARK enough colors
    LUMINANCE_THRESHOLD = 0.75  # 0.0 (Black) to 1.0 (White). Adjust as needed.

    valid_colors = []
    for name, hex_val in color_map.items():
        if name in used_colors:
            continue

        # Convert to RGB (values 0.0 - 1.0)
        r, g, b = mcolors.to_rgb(hex_val)

        # Calculate Perceived Luminance
        luminance = 0.2126*r + 0.7152*g + 0.0722*b

        if luminance < LUMINANCE_THRESHOLD:
            valid_colors.append(name)

    # 3. Shuffle and Assign
    random.shuffle(valid_colors)

    if len(valid_colors) < len(new_managers):
        logger.warning(
            "Not enough dark colors found. Consider raising threshold."
        )

    for index, manager in enumerate(new_managers):
        # Prevent index errors by cycling if necessary
        color = valid_colors[index % len(valid_colors)]

        manager_format = {
            'bold': 'True',
            'size': 12,
            'align': 'centre',
            'font': 'Arial',
            'bg_color': color,
            'teams': []
        }

        out_path = Path(directory_path) / f"{manager}.json"
        save_json_dicts(out_path=out_path, dictionary=manager_format)

    logger.info(f'Manager colors generated for {len(new_managers)} managers.')


def plotting_colors(format_dir: Path,
                    year: str,
                    context: str,
                    entity: str) -> dict:
    """
    Function Details
    ================
    Determine plotting colors based on input. Takes data from format dictionary
    to create the marker and line colors for teams, drivers, managers, etc.

    Parameters
    ----------
    format_dir: Path
        Path to format directory.
    year, context, entity: str
        Year for color codes. Context for plotting (e.g., 'driver'). Specific
        entity for which colors are being selected.

    Returns
    -------
    dictionary
        Plotting colors dictionary.

    Notes
    -----
    Uses specific formatting functions to determine the plotting colors for
    drivers, teams, managers, manager teams, and perks.

    ---------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Copied and updated documentation.

    02/03/2024
    ----------
    Update to manager team colors, now just uses matplotlib colors in order for
    multiple teams. Added year for colour codes.

    24/07/2024
    ----------
    Streamlined rewrite.

    15/09/2024
    ----------
    Update for context handling.

    11/04/2025
    ----------
    Moved to format utilities.

    """
    colors_dictionary = {}

    def get_format_dict(subdir: Path,
                        context: str) -> dict:
        """
        Function Details
        ================
        Retrieve the format dictionary for a given entity type.

        Parameters
        ----------
        subdir: Path
            Path to the main format directory.
        context: str
            Specific entity for which the format is being retrieved.

        Returns
        -------
        dictionary
            Format dictionary containing the colors and styles for entity.

        -----------------------------------------------------------------------
        Update History
        ==============

        24/07/2024
        ----------
        Created.

        11/04/2025
        ----------
        Moved to format utilities.

        """
        return {
            'driver': drivers_colours,
            'constructor': constructors_colour,
            'team': team_colour,
            'manager': managers_colour,
            'perk': perk_colour
        }[context](
            format_dir=Path(f'{format_dir}/{subdir}'),
            **{context: entity, 'year': year})

    subdir_map = {
        "driver": "Lineup_Formats",
        "constructor": "Lineup_Formats",
        "team": "Manager_Formats",
        "manager": "Manager_Formats",
        "perk": "Lineup_Formats"
    }
    subdir = subdir_map.get(context, "Lineup_Formats")
    logger.info(f'Getting plot colors for {context} using {subdir} path')
    format_dict = get_format_dict(
        subdir=subdir,
        context=context
    )

    if context == 'driver':
        style = [
            'solid',
            'dashed',
            'dashdot',
            'dotted'
        ]
        colors_dictionary.update(
            {
                "color": format_dict["color"],
                "bg_color": format_dict["bg_color"],
                "linestyle": style[format_dict["drivers"].index(entity)]
            }
        )

    elif context == 'constructor':
        colors_dictionary.update(
            {
                "color": format_dict["color"],
                "bg_color": format_dict["bg_color"],
                "linestyle": '-'
            }
        )

    elif context == 'team':
        team_styles = [
            ('red', 'solid'),
            ('yellow', 'dashed'),
            ('blue', 'dashdot'),
            ('blue', 'solid'),
            ('yellow', 'dashed'),
            ('red', 'dashdot'),
            ('red', 'solid'),
            ('yellow', 'dashed'),
            ('blue', 'dashdot'),
            ('blue', 'solid')
        ]
        color, linestyle = team_styles[
            format_dict["teams"].index(entity) % len(team_styles)
        ]
        colors_dictionary.update(
            {
                "color": color,
                "bg_color": format_dict["bg_color"],
                "linestyle": linestyle
            }
        )

    elif context == 'manager':
        colors_dictionary.update(
            {
                "bg_color": format_dict["bg_color"]
            }
        )

    elif context == 'perk':
        colors_dictionary.update(
            {
                "color": format_dict["color"],
                "bg_color": format_dict["bg_color"]
            }
        )

    logger.info(f'Plotting colours found: {colors_dictionary}')
    return colors_dictionary


def drivers_formats(format_dir: str,
                    driver: str,
                    year: str) -> dict:
    """
    Function Details
    ================
    Find driver cell formats, from team colors.

    Parameters
    ----------
    format_dir, driver, year: string
        Path to format directory and driver name. Yeah for formats.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

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
        team_formats = load_json(file_path=team_path)
        if f'{year}' in team_formats.keys():
            team_format = team_formats[f'{year}']
            if driver in team_format['drivers']:
                for key, value in team_format.items():
                    if key == 'drivers':
                        pass
                    else:
                        format_dict.update({key: value})
    logger.info(f'Driver formats: {format_dict}')
    return format_dict


def drivers_colours(format_dir: str,
                    driver: str,
                    year: str) -> dict:
    """
    Function Details
    ================
    Find driver colors, from team colors.

    Parameters
    ----------
    format_dir, driver, year: string
        Path to format directory and driver name. Year for colour codes.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

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
        team_formats = load_json(file_path=team_path)
        if f'{year}' in team_formats.keys():
            team_format = team_formats[f'{year}']
            if driver in team_format['drivers']:
                for key, value in team_format.items():
                    format_dict.update({key: value})
    logger.info(f'Driver colors: {format_dict}')
    return format_dict


def constructors_format(format_dir: str,
                        constructor: str,
                        year: str) -> dict:
    """
    Function Details
    ================
    Find team cell formats, from team colors.

    Parameters
    ----------
    format_dir, constructor, year: string
        Path to format directory and team name. Year for colour code.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

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
        team_formats = load_json(file_path=path)
        if f'{year}' in team_formats.keys():
            team_format = team_formats[f'{year}']
            if constructor == teams[index]:
                for key, value in team_format.items():
                    if key == 'drivers':
                        pass
                    else:
                        format_dict.update({key: value})
    logger.info(f'Constructor formats: {format_dict}')
    return format_dict


def constructors_colour(format_dir: str,
                        constructor: str,
                        year: str) -> dict:
    """
    Function Details
    ================
    Find team colors, from team colors.

    Parameters
    ----------
    format_dir, constructor: string
        Path to format directory and tea, name.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

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
        team_formats = load_json(file_path=path)
        if f'{year}' in team_formats.keys():
            team_format = team_formats[f'{year}']
            if constructor == teams[index]:
                for key, value in team_format.items():
                    format_dict.update({key: value})
    logger.info(f'Constructor colors: {format_dict}')
    return format_dict


def perk_colour(format_dir: str,
                perk: str,
                year: str) -> dict:
    """
    Function Details
    ================
    Find perk colors, from perk colors.

    Parameters
    ----------
    format_dir, perk, year: string
        Path to format directory and perk name. Year for colour code.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation and presentation.

    """
    path = Path(f'{format_dir}/Perks.json')
    perk_formats = load_json(file_path=path)
    if f'{year}' in perk_formats.keys():
        perk_format = perk_formats[f'{year}']
        all_perks = perk_format['perks']
        all_colours = perk_format['bg_color']
        format_dict = {}
        for key, value in perk_format.items():
            format_dict.update({key: value})
        for p, c in zip(all_perks, all_colours):
            if p == perk:
                format_dict.update({'bg_color': c})
    logger.info(f'Perk colors: {format_dict}')
    return format_dict


def team_colour(format_dir: str,
                team: str,
                year: str) -> dict:
    """
    Function Details
    ================
    Find team colors, from manager colors.

    Parameters
    ----------
    format_dir, team, year: string
        Path to format directory and team name. Unused.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

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
    format_dict = {}
    for path in paths: 
        manager_format = load_json(file_path=path)
        if team in manager_format['teams']:
            for key, value in manager_format.items():
                format_dict.update({key: value})
    logger.info(f'Team colors: {format_dict}')
    return format_dict


def managers_colour(format_dir: str,
                    manager: str,
                    year: str) -> dict:
    """
    Function Details
    ================
    Find manager colors, from manager colors.

    Parameters
    ----------
    format_dir, manager, year: string
        Path to format directory and manager name. Unused.

    Returns
    -------
    format_dict: dictionary
        Dictionary containing color formats.

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation and presentation.

    """
    format_dict = load_json(
        file_path=Path(f'{format_dir}/{manager}.json'))
    logger.info(f'Manager colors: {format_dict}')
    return format_dict

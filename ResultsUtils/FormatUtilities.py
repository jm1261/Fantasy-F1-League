import os
import random
import logging

from pathlib import Path
from GeneralUtils.DataIO import load_json, save_json_dicts

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


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

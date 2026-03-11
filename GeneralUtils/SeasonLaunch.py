###############################################################################
###############################################################################
#                             File: Season Launch                             #
#                             Author: Joshua Male                             #
#              Description: Script for launching a new F1 season              #
#                         Project: Fantasy F1 League                          #
#                              Date: 11/03/2025                               #
#                           Copyright © Joshua Male                           #
###############################################################################
###############################################################################

# Imports
import InitializeGeneralUtils  # noqa

import logging
import DataIO as io
import ManagerUtils.ManagerAnalysis as ma
import ResultsUtils.FormatUtilities as form

from pathlib import Path

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def launches_new_season(root: Path,
                        year: str) -> None:
    """
    Function Details
    ================
    Begin a new season with only the root directory and the given year. Creates
    all the required directory paths and files to begin a new fantasy league
    season.

    Parameters
    ----------
    root: Path
        Path to root directory.
    year: string
        Year for data storage.

    Returns
    -------
    None

    Notes
    -----
    Creates the data path to the year for which a new season is created. Then
    creates the required directory paths. Checks to see if there are any new
    managers this season. If there are, it will create some. Add manager teams
    to the format dictionaries if they don't exist. Finish by setting up the
    weekly lineup, results, and statistics dictionaries if they don't exist.

    ---------------------------------------------------------------------------
    Update History
    ==============

    07/02/2024
    ----------
    Updated to split the function into further segments for a clearer
    understanding to the reader going forward. The format dictionaries have
    been updated for the teams and drivers to allow multiple years of data to
    be stored in one individual file in the .config directory. As such, some of
    the driver and team results/statistics functions have been updated, as well
    as the lineup_format_path. Update to function names for PEP8. This update
    was created by J.Male.

    14/02/2024
    ----------
    Added a year key to the info_dict, changed in this function to pull the
    yearly info dictionary in automatically. This update was created by J.Male.

    15/02/2024
    ----------
    Checked to ensure the lineup results and statistics dictionaries were all
    working properly. They are. This function works as intended as of this
    date.

    """

    # Check path exists
    year_path = Path(f'{root}', 'Data', f'{year}')
    io.check_dir_exists(directory_path=year_path)
    logger.info(f'Year Path Created: {year_path}')

    # Initialize configuration instance and load season information
    config = io.LoadConfigs(
        root_directory=root,
        year=year
    )

    # Load season info
    season_info = config.load_seasoninfo(file_name='SeasonInfo.json')
    logger.info('Lineup configs loaded successfully.')

    # Create Manager Folders
    managers = season_info['Managers'].keys()
    io.seasons_directories(
        directory_path=year_path,
        managers=managers
    )
    new_managers = io.check_manager_exist(
        directory_path=Path(config.format_path, 'Manager_Formats'),
        managers=managers
    )
    used_colors = io.get_used_colors(
        directory_path=Path(config.format_path, 'Manager_Formats')
    )
    form.generate_manager_colors(
        new_managers=new_managers,
        used_colors=used_colors,
        directory_path=Path(config.format_path, 'Manager_Formats')
    )
    io.adds_managers_teams(
        directory_path=Path(config.format_path, 'Manager_Formats'),
        manager_dict=season_info['Managers']
    )

    # Create Lineup Files for Results, Statistics, and Weekly Submission
    lineup_dict = io.creates_driver_team_results(
        lineup_path=Path(config.format_path, 'Lineup_Formats'),
        year=year
    )
    statistics_dict = io.create_drivers_teams_statistics(
        lineup_path=Path(config.format_path, 'Lineup_Formats'),
        year=year
    )
    lineup_weekly_dict = io.create_drivers_teams_weekly(
        lineup_path=Path(config.format_path, 'Lineup_Formats'),
        year=year
    )

    # Save the lineup dictionaries
    paths = [
        Path(year_path, 'Lineup', 'Results.json'),
        Path(year_path, 'Lineup', 'Statistics.json'),
        Path(year_path, 'Lineup_Weekly.json')
    ]
    dictionaries = [lineup_dict, statistics_dict, lineup_weekly_dict]
    for path, dictionary in zip(paths, dictionaries):
        if path.is_file():
            pass
        else:
            io.save_json_dicts(
                out_path=path,
                dictionary=dictionary
            )

    # Create manager team sheet dictionaries
    ma.managers_weekly(
        info_dictionary=season_info,
        data_path=year_path,
        completed_races=[season_info['Races'][0]]
    )


if __name__ == '__main__':
    launches_new_season(
        root=Path().absolute(),
        year='2026'
    )

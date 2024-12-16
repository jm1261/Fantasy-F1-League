import InitializeManager  # noqa

import logging
import ManagerAnalysis as ma
import GeneralUtils.DataIO as io

from pathlib import Path

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def checks_managers(root: str,
                    year: str) -> list:
    """
    Function Details
    ================
    Function to check the weekly manager scores are correct.

    This function checks the weekly manager scores against the league table to
    ensure determine which teams have been altered.

    Parameters
    ----------
    root, year: string
        Path to root directory, year as a string.

    Returns
    -------
    wrong_teams: list
        List of teams that have been altered.

    Notes
    -----
    Creates the weekly manager team sheets in the correct dictionaries and uses
    the results to calculate total points and statistics. Uses this to populate
    a Manager_Check.json file with teams in descending order to be checked
    against the league page so that the manager team sheets can be altered on
    requirement rather than every team entered each week.

    ---------------------------------------------------------------------------
    Update History
    ==============

    16/02/2024
    ----------
    Updated function description to match the new style and provide more info
    to the reader. Update to function layout with section headers for
    readability. Update to the function that gets the completed races, see the
    description for that function separately.

    27/02/2024
    ----------
    Updated to remove the need for getting a race index and added functionality
    to checking the manager team sheet. Will now cycle through all completed
    races in the event that multiple weeks are missed.

    08/05/2024
    ----------
    Update to include positions gained in manager statistics.

    27/08/2024
    ----------
    Updated with configuration class methods.

    30/11/2024
    ----------
    Moved to manager utils.

    """

    # Initialize configuration instance and load season information
    config = io.LoadConfigs(
        root_directory=root,
        year=year
    )

    # Load season info and identify completed races
    season_info = config.load_seasoninfo(file_name='SeasonInfo.json')
    completed_races = config.get_completed_races(races=season_info['Races'])
    lineup_results = config.get_lineups_results(file_name='Results.json')
    logger.info('Manager configs loaded successfully')

    # Update manager weekly team sheets
    ma.managers_weekly(
        info_dictionary=season_info,
        data_path=config.data_path,
        completed_races=completed_races
    )

    # Calculate manager scores
    processor = ma.ManagerProcessor(
        lineup_results=lineup_results,
        info_dictionary=season_info,
        completed_races=completed_races,
        data_path=config.data_path
    )
    manager_results = processor.managers_lineup()
    manager_statistics = processor.manager_stats()
    manager_counts = processor.count_usage()

    # Save manager scores
    io.save_json_dicts(
        out_path=Path(config.manager_path, 'Results.json'),
        dictionary=manager_results
    )
    io.save_json_dicts(
        out_path=Path(config.manager_path, 'Statistics.json'),
        dictionary=manager_statistics
    )
    io.save_json_dicts(
        out_path=Path(config.manager_path, 'Counts.json'),
        dictionary=manager_counts
    )

    # Find wrong teams
    league_check = io.load_json(
        file_path=Path(config.data_path, 'League_Check.json')
    )
    wrong_teams = io.mismatched_team(
        statistics_dictionary=manager_statistics,
        league_records=league_check
    )

    return wrong_teams


if __name__ == '__main__':
    year = 2024
    root = Path().absolute()
    wrong_teams = checks_managers(
        root=root,
        year=year)
    if len(wrong_teams) == 0:
        print('All Good')
    else:
        logger.info(f'Wrong teams = {wrong_teams}')

# import InitializeManager  # noqa

import logging
import GeneralUtils.DataIO as io
import ResultsUtils.Plotting as plot
import ManagerUtils.CheckManager as check

from pathlib import Path

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)

""" Notes
Ideas to add:
    Use images from league table to populate league_check.
    Possibility that we could scrape data from the web.
    Should include position in the league, dnf rate, overtakes, average points,
    podiums, etc.
    Fold into total average across multiple years.
    Spreadsheet.
    Top ten report etc.
    Predict best possible scores.
"""


def managerweek(root: str,
                year: str) -> None:
    """
    Function Details
    ================
    Calculate manager statistics and plot results.

    Parameters
    ----------
    root: str
        Path to root directory.
    year: str
        Year for data processing and config setups.

    Returns
    -------
    None.

    Notes33838
    -----
    Process the manager data, statistics, and plots for the given year. Can be
    called from main repository, notebooks, or used as __main__.

    ---------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Updated documentation.

    10/08/2024
    ----------
    Added config class functionality.

    16/12/2024
    ----------
    Updated for new class methods.

    """

    # Initialize configuration instance and load season information
    config = io.LoadConfigs(
        root_directory=root,
        year=year
    )

    # Load season info and identify completed races
    season_info = config.load_seasoninfo(file_name='SeasonInfo.json')
    completed_races = config.get_completed_races(races=season_info['Races'])
    config.manager_results(file_name='Results.json')
    config.managers_statistics(file_name='Statistics.json')
    config.managers_counts(file_name='Counts.json')
    logger.info('Lineup configs loaded successfully')

    # Check all teams are correct
    wrong_teams = check.checks_managers(
        root=root,
        year=year
    )
    if len(wrong_teams) == 0:
        logger.info('No wrong teams to correct')
    else:
        logger.error(f'There are {len(wrong_teams)} to correct: {wrong_teams}')
        raise ValueError('Wrong teams need to be corrected before proceeding')

    # Produce manager spreadsheet

    # Plot manager results and statistics
    for index, race in enumerate(completed_races):
        manager_plotter = plot.Manager_Plots(
            out_path=Path(config.data_path, 'Figures', f'{race}'),
            format_dir=config.format_path,
            year=year
        )
        manager_plotter.leagues_results(
            race_index=index,
            race=race,
            results_dictionary=config.manager_results
        )
        manager_plotter.league_stat(
            race_index=index,
            races=completed_races[0: index + 1],
            race=race,
            statistics_dictionary=config.manager_statistics
        )
        team_positions = config.get_positions()
        manager_plotter.leaguecount(
            race_index=index,
            races=completed_races[0: index + 1],
            race=race,
            counts_dictionary=config.manager_counts,
            counts=team_positions
        )
        manager_plotter.team_counts(
            race_index=index,
            races=completed_races[0: index + 1],
            race=race,
            counts_dictionary=config.manager_counts,
            counts=['Penalties', 'Substitutes']
        )


if __name__ == '__main__':
    year = 2025
    root = Path().absolute()
    managerweek(
        root=root,
        year=year
    )

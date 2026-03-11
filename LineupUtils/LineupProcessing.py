import InitializeLineup  # noqa

import logging
import GeneralUtils.DataIO as io
import ResultsUtils.Plotting as plot
import LineupUtils.LineupAnalysis as la

from pathlib import Path

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def lineup_week(root: str,
                year: str) -> None:
    """
    Function Details
    ================
    Calculate lineup statistics and plot results.

    Parameters
    ----------
    root: string
        Path to root directory.
    year: string
        Year for data processing and config setups.

    Returns
    -------
    None.

    Notes
    -----
    Process the lineup data, statistics, and plots for the given year. Can be
    called from main repository, notebook, or used as __main__.

    ---------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation.

    10/08/2024
    ----------
    Update to documentation.

    03/11/2024
    ----------
    Move to new directory and improved documentation/work flow.

    23/05/2025
    ----------
    Added time to sleep to allow for file writing.

    """

    # Initialize configuration instance and load season information
    config = io.LoadConfigs(
        root_directory=root,
        year=year
    )

    # Load season info and identify completed races
    season_info = config.load_seasoninfo(file_name='SeasonInfo.json')
    completed_races = config.get_completed_races(races=season_info['Races'])
    logger.info('Lineup configs loaded successfully')

    # Load weekly score car
    weekly_lineup = config.get_weekly_lineup_score(
        file_name='Lineup_Weekly.json'
    )
    logger.info('Weekly scorecard loaded')

    # Process results
    processor = la.LineupProcessor(
        format_path=config.format_path,
        results_path=config.lineup_path,
        year=config.year,
        races=season_info['Races']
    )
    results_dict = processor.update_weeklylineup(
        completed_races=completed_races,
        weekly_dictionary=weekly_lineup
    )
    logger.info('Results dictionary updated')

    # Process lineup statistics
    statistics_dict = processor.update_lineup_stats()
    logger.info('Statistics dictionary updated')

    # Produce lineup spreadsheet

    # Plot lineup results and statistics
    for index, race in enumerate(completed_races):
        lineup_plotter = plot.Lineup_Points(
            out_path=Path(config.data_path, 'Figures', f'{race}'),
            format_dir=config.format_path,
            year=year
        )
        lineup_plotter.lineups_results(
            race_index=index,
            race=race,
            results_dictionary=results_dict
        )
        lineup_plotter.lineup_stat(
            race_index=index,
            races=completed_races[0: index + 1],
            race=race,
            statistics_dictionary=statistics_dict
        )

    # Save results and statistics dictionaries
    logger.info('Saving lineup results and statistics')
    io.save_json_dicts(
        out_path=Path(config.lineup_path, 'Results.json'),
        dictionary=results_dict
    )
    io.save_json_dicts(
        out_path=Path(config.lineup_path, 'Statistics.json'),
        dictionary=statistics_dict
    )
    logger.info('Saved lineup results and statistics')


if __name__ == '__main__':
    year = 2025
    root = Path().absolute()
    lineup_week(
        root=root,
        year=year
    )

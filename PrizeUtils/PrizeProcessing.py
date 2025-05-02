import InitializePrize  # noqa

import logging
import PrizeAnalysis as pa
import GeneralUtils.DataIO as io

from pathlib import Path

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def managers_prizes(root: str,
                    year: str) -> None:
    """
    Function Details
    ================
    Calculate yearly prizes.

    Parameters
    ----------
    root: string
        Path to root directory.
    year: string
        Year for data processing and config setups.

    Returns
    -------
    None.

    ---------------------------------------------------------------------------
    Update History
    ==============

    02/04/2024
    ----------
    Created.

    17/12/2024
    ----------
    Merged with class methods.

    """
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

    # Get Prizes
    config.gets_prizes(file_name=f'{year}.json')
    prize_keys = config.prizes.keys()
    logger.info('Prizes loaded successfully')

    # Process prizes
    prizes_processor = pa.PrizeProcessor(
        info_dictionary=season_info,
        prizes_dictionary=config.prizes,
        manager_results=config.manager_results,
        manager_statistics=config.manager_statistics,
        manager_counts=config.manager_counts,
        completed_races=completed_races
    )
    prizes_dict = prizes_processor._process_prizes(categories=prize_keys)
    logger.info('Prizes dictionary completed')

    # Save out
    io.save_json_dicts(
        out_path=Path(
            config.prizes_path,
            f'{year}.json'
        ),
        dictionary=prizes_dict
    )
    logger.info('Prizes dictionary saved')

    # Initialise plotter
    prize_plotter = pa.PrizePlotter(
        prizes_dictionary=prizes_dict,
        manager_results=config.manager_results,
        manager_statistics=config.manager_statistics,
        manager_counts=config.manager_counts,
        completed_races=completed_races,
        data_path=config.data_path,
        format_path=config.format_path,
        year=year
    )

    prizes = prizes_dict.keys()
    for prize in prizes:
        prize_plotter.call_prizes(prize=prize)

    """
    # Plot achievement graphs
    if 'Achievements' in prize_keys:

        # Extra DRS
        # Figure this one out later, maybe create a dictionary first, wait for
        # someone to use an Extra DRS.

    if 'Championship' in prize_keys:
        pass"
    """


if __name__ == '__main__':
    root = Path().absolute()
    managers_prizes(
        root=root,
        year='2025'
    )

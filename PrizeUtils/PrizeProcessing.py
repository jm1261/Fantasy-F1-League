import InitializePrize  # noqa

import sys
import logging
import PrizeAnalysis as pa
import GeneralUtils.DataIO as io
import ResultsUtils.Plotting as plot

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
    config.managers_results(file_name='Results.json')
    config.managers_statistics(file_name='Statistics.json')
    config.managers_counts(file_name='Counts.json')
    config.gets_prizes(file_name=f'{year}.json')
    prize_keys = config.prizes.keys()

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

    # Save out
    io.save_json_dicts(
        out_path=Path(
            config.prizes_path,
            f'{year}.json'
        ),
        dictionary=prizes_dict
    )

    # Plot output
    manager_plotter = plot.Manager_Plots(
        out_path=Path(config.data_path, 'Figures', 'Prizes'),
        format_dir=config.format_path,
        year=year
    )

    if "Spot" in prize_keys:
        comp_races = [
            race
            for race in
            config.prizes["Spot"]["Spot Max"] +
            config.prizes["Spot"]["Spot Min"]
        ]
        comp_indices = [
            completed_races.index(race)
            for race in comp_races
        ]
        prize_names = [
            config.prizes["Spot"]["Spot Names"][f'{race}']
            for race in comp_races
        ]
        for index, race, name in zip(comp_indices, comp_races, prize_names):
            manager_plotter.spotleagueprize(
                race_index=index,
                race=race,
                results_dictionary=config.manager_results,
                prize=name
            )

    # Custom races not quite working properly. Need to fix. Also add the others


if __name__ == '__main__':
    # year = sys.argv[1]
    year = 2024
    root = Path().absolute()
    managers_prizes(
        root=root,
        year=year
    )

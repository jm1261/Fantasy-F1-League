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


if __name__ == '__main__':
    # year = sys.argv[1]
    year = 2024
    root = Path().absolute()
    managers_prizes(
        root=root,
        year=year
    )

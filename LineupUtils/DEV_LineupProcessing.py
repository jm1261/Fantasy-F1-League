###############################################################################
###############################################################################
#                          File: Lineup Processing                            #
#                             Author: Joshua Male                             #
#               Description: Process weekly lineup and all plots              #
#                         Project: Fantasy F1 League                          #
#                              Date: 02/05/2025                               #
#                           Copyright © Joshua Male                           #
###############################################################################
###############################################################################

# Imports
import InitializeLineup  # noqa

import logging
import GeneralUtils.DEV_DataIO as io
import LineupUtils.LineupAnalysis as la

from pathlib import Path

# Logging parameters
logger = logging.getLogger(name=Path(__file__).stem)


class lineup_week:
    """
    Class Details
    =============
    Process weekly lineup results, calculate lineup statistics, and plot lineup
    results.

    Attributes
    ----------
    root_path: Path
    year: str

    Methods
    ----------
    __init__

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

    02/05/2025
    ----------
    Class method created.

    """

    def __init__(self, root: Path, year: str) -> None:
        """
        Function Details
        ================
        Initialize lineup week class.

        Parameters
        ----------
        root: Path
            Path to root directory.
        year: str
            Year for data processing and config setups.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        02/05/2025
        ----------
        Created.

        """
        self.root_path = root
        self.year = year
        self.config = io.LoadConfigs(
            root_path=self.root_path,
            year=self.year
        )
        self.season_info = self.config.load_seasoninfo(
            file_name='SeasonInfo.json'
        )
        self.completed_races = self.config.get_completed_races(
            races=self.season_info["Races"]
        )
        self.weekly_lineup = self.config.get_weekly_lineup_score(
            file_name='Lineup_Weekly.json'
        )
        self.processor = la.LineupProcessor(
            format_path=self.config.format_path,
            results_path=self.config.lineup_path,
            year=self.year,
            races=self.season_info["Races"]
        )
        logger.info('lineup_week class initialized successfully')

    def _process_lineup_results(self) -> None:
        """
        Function Details
        ================
        Process the weekly lineup results, correct weekly scores, and return
        the updated results dictionary.

        Parameters
        ----------
        None.

        Returns
        -------
        None. Updates self.results_dictionary with the processed results.

        -----------------------------------------------------------------------
        Update History
        ==============

        23/09/2025
        ----------
        Created from combined functions.

        """
        self.results_dictionary = self.processor.update_weeklylineup(
            completed_races=self.completed_races,
            weekly_dictionary=self.weekly_lineup
        )

    def _process_lineup_statistics(self) -> None:
        """
        Function Details
        ================
        Process the weekly lineup statistics and return the updated statistics
        dictionary.

        Parameters
        ----------
        None.

        Returns
        -------
        None. Updates self.statistics_dictionary with the processed statistics.

        -----------------------------------------------------------------------
        Update History
        ==============

        23/09/2025
        ----------
        Created from combined functions.

        """
        self.statistics_dictionary = self.processor.update_lineup_stats()

    def _plot_lineup(self) -> None:
        """
        Function Details
        ================
        Plot the lineup results and statistics.

        Parameters
        ----------
        None.

        Returns
        -------
        None. Generates and saves plots to the output directory.

        -----------------------------------------------------------------------
        Update History
        ==============

        23/09/2025
        ----------
        Created from combined functions.

        """
        return None

    def process_lineup(self) -> None:
        """
        Function Details
        ================
        Process the weekly lineup results, calculate lineup statistics, and
        plot lineup results.

        Parameters
        ----------
        None.

        Returns
        -------
        None. Updates self.results_dictionary and self.statistics_dictionary.

        -----------------------------------------------------------------------
        Update History
        ==============

        02/05/2025
        ----------
        Created from combined functions.

        """
        self._process_lineup_results()
        logger.info('Results dictionary updated')
        self._process_lineup_statistics()
        logger.info('Statistics dictionary updated')

        # Save results and statistics dictionaries
        logger.info('Saving lineup results and statistics')
        io.save_json_dicts(
            out_path=Path(
                self.config.lineup_path,
                'Results.json'
            ),
            dictionary=self.results_dictionary
        )
        io.save_json_dicts(
            out_path=Path(
                self.config.lineup_path,
                'Statistics.json'
            ),
            dictionary=self.statistics_dictionary
        )
        logger.info('Saved lineup results and statistics')

        # Plot lineup results and statistics
        self._plot_lineup()


if __name__ == '__main__':
    root = Path().absolute()
    year = '2025'
    lineup_processor = lineup_week(
        root=root,
        year=year
    )
    lineup_processor.process_lineup()

################################################################################
################################################################################
###                               File: Lineup                               ###
###                           Author: Joshua Male                            ###
###                             Date: 01/01/2021                             ###
###                                                                          ###
###               Description: Lineup Script for Fantasy League              ###
###                        Project: F1 Fantasy League                        ###
###                                                                          ###
###                       Script Designed for Python 3                       ###
###                         © Copyright Joshua Male                          ###
###                                                                          ###
###                       Software Release: Unreleased                       ###
################################################################################
################################################################################
import sys
import src.dataIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot
import src.spreadsheet as ss

import src.plotting_v2 as plot2

from pathlib import Path


def lineup_week(root : str,
                year : str) -> None:
    """
    Function Details
    ================
    Calculate lineup results and plot figures.

    Use weekly lineup reports to calculate team and driver points and statistics
    and plot them as a race-wise figure.

    Parameters
    ----------
    root, year: string
        Path to root directory, year for data storage.

    Returns
    -------
    None

    See Also
    --------
    update_weeklylineup
    update_lineup_stats
    get_completed_races
    line_up_spreadsheet
    results_bar
    check_dir_exists
    lineupstats

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation.

    """

    """ Load Config Files """
    config = io.Configuration(root_directory=root, year=year)
    config.info_dictionary(file_name='Info.json')
    config.get_completed_races(races=config.info_dict['Races'])

    """ Update the Weekly Lineup Points and Values """
    results_dict = io.update_weeklylineup(
        year=year,
        info_dictionary=config.info_dict,
        data_path=config.data_path,
        results_path=config.lineup_path,
        format_path=config.format_path,
        completed_races=config.completed_races)
    stats_dict = anal.update_lineup_stats(
        results_path=config.lineup_path,
        results_dict=results_dict)

    """ Create Spreadsheet """
    ss.line_up_spreadsheet(
        file_path=Path(f'{config.lineup_path}/Results.xlsx'),
        format_dir=Path(f'{config.format_path}/Lineup_Formats'),
        year=year,
        races=config.info_dict['Races'],
        results=results_dict,
        statistics=stats_dict)

    """ Plot """
    for index, race in enumerate(config.completed_races):
        lineup_plotter = plot2.Lineup_Points(
            out_path=Path(f'{config.data_path}/Figures/{race}'),
            format_dir=config.format_path,
            year=year)
        lineup_plotter.results_bar(
            race_index=index,
            race=race,
            results_dictionary=results_dict)
        lineup_plotter.statistics_bars(
            race_index=index,
            race=race,
            statistics_dictionary=stats_dict)
        lineup_plotter.statistics_line(
            race=race,
            races=config.completed_races[0: index + 1],
            statistics_dictionary=stats_dict)


if __name__ == '__main__':
    year = 2024
    #year = sys.argv[1]
    root = Path().absolute()
    lineup_week(
        root=root,
        year=year)

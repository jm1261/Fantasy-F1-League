import sys
import src.dataIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot
import src.spreadsheet as ss

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
    info_path = Path(f'{root}/Info.json')
    info_dict = (io.load_json(file_path=info_path))[f'{year}']
    data_path = Path(f'{root}/Data/{year}')
    results_path = Path(f'{root}/Data/{year}/Lineup')
    format_path = Path(f'{root}/Config')

    """ Update the Weekly Lineup Points and Values """
    results_dict = io.update_weeklylineup(
        year=year,
        info_dictionary=info_dict,
        data_path=data_path,
        results_path=results_path,
        format_path=format_path)
    stats_dict = anal.update_lineup_stats(
        results_path=results_path,
        results_dict=results_dict)

    """ Check Completed Races """
    completed_races = io.get_completed_races(
        results_path=results_path,
        info_dictionary=info_dict)

    """ Create Spreadsheet """
    ss.line_up_spreadsheet(
        file_path=Path(f'{root}/Data/{year}/Lineup/Results.xlsx'),
        format_dir=Path(f'{format_path}/Lineup_Formats'),
        year=year,
        races=info_dict['Races'],
        results=results_dict,
        statistics=stats_dict)

    """ Plot Results Bar """
    for index, race in enumerate(completed_races):
        races = completed_races[0: index + 1]
        out_path = Path(f'{root}/Data/{year}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.results_bar(
            results_dictionary=results_dict,
            race_index=index,
            race=race,
            format_dir=format_path,
            year=year,
            out_path=out_path)

    """ Plot Statistics """
    for index, race in enumerate(completed_races):
        races = completed_races[0: index + 1]
        out_path = Path(f'{root}/Data/{year}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.lineupstats(
            statistics_dictionary=stats_dict,
            race_index=index,
            races=races,
            race=race,
            format_dir=format_path,
            year=year,
            out_path=out_path)


if __name__ == '__main__':
   # year = 2019
    year = sys.argv[1]
    root = Path().absolute()
    lineup_week(
        root=root,
        year=year)

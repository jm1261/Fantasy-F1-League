import src.dataIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot
import src.spreadsheet as ss

from pathlib import Path

''' There is still a problem calculating the difference in race scores '''
''' Seems the problem is with updating the results dictionary, adding points to
wrong place '''
''' Keep an eye on it for the japanese gp weekend '''


def lineup_week(root : str,
                year : str) -> None:
    """
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
    get_races_sofar
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

    """
    results_dict = io.update_weeklylineup(
        root_path=root,
        year=year)
    stats_dict = anal.update_lineup_stats(
        root_path=root,
        year=year,
        results_dict=results_dict)
    info_path = Path(f'{root}/Info.json')
    results_path = Path(f'{root}/Data/{year}/Lineup')
    format_path = Path(f'{root}/Data/{year}/Lineup_Formats')
    races_sofar, races = io.get_races_sofar(
        file_path=info_path,
        results_path=results_path)
    ss.line_up_spreadsheet(
        file_path=Path(f'{root}/Data/{year}/Lineup/Results.xlsx'),
        format_dir=format_path,
        races=races,
        results=results_dict,
        statistics=stats_dict)
    for index, race in enumerate(races_sofar):
        races = races_sofar[0: index + 1]
        out_path = Path(f'{root}/Data/{year}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.results_bar(
            results_dictionary=results_dict,
            race_index=index,
            race=race,
            format_dir=format_path,
            out_path=out_path)
    for index, race in enumerate(races_sofar):
        races = races_sofar[0: index + 1]
        out_path = Path(f'{root}/Data/{year}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.lineupstats(
            statistics_dictionary=stats_dict,
            race_index=index,
            races=races,
            race=race,
            format_dir=format_path,
            out_path=out_path)


if __name__ == '__main__':
    year = 2023
    root = Path().absolute()
    lineup_week(
        root=root,
        year=year)

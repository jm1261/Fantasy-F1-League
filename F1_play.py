import sys
import src.dataIO as io
import src.filepaths as fp
import src.plotting as plot
import src.analysis as anal

from pathlib import Path


def f1_play(root : str,
            year : str) -> None:
    """
    Function Details
    ================
    Plot f1 play results.

    Parameters
    ----------
    root, year: string
        Root directory path and year to process.

    Returns
    -------
    None.

    See Also
    --------
    load_json
    get_completed_races
    sum_dictionary
    f1play_line

    Notes
    -----
    None.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    18/04/2024
    ----------
    Created.

    """

    ''' Config Files and Season Info '''
    info_path = Path(f'{root}/Info.json')
    info_dict = (io.load_json(file_path=info_path))[f'{year}']
    data_path = Path(f'{root}/Data/{year}')
    format_path = Path(f'{root}/Config')
    results_path = Path(f'{data_path}/Lineup')
    out_path = Path(f'{data_path}/Figures/F1_Play')
    fp.check_dir_exists(dir_path=out_path)

    ''' Get F1 Play Dictionary '''
    f1_play = io.load_json(file_path=Path(f'{data_path}/F1_Play.json'))

    ''' Check Completed Races '''
    completed_races = io.get_completed_races(
        results_path=results_path,
        info_dictionary=info_dict)

    ''' Calculate Sum and Average '''
    results_dictionary = anal.sum_dictionary(dictionary=f1_play)

    ''' Plot F1 Play '''
    for index, race in enumerate(completed_races):
        races = completed_races[0: index + 1]
        plot.f1play_line(
            results_dictionary=results_dictionary,
            races=races,
            race=race,
            format_dir=format_path,
            year=year,
            out_path=out_path)


if __name__ == '__main__':
    #year = 2024
    year = sys.agv[1]
    root = Path().absolute()
    f1_play(
        root=root,
        year=year)

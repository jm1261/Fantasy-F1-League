import sys
import src.dataIO as io
import src.filepaths as fp
import plotting as plot
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
    config = io.Configuration(
        root_directory=root,
        year=year)
    config.info_dictionary(file_name='Info.json')
    config.get_completed_races(races=config.info_dict['Races'])

    out_path = Path(config.data_path, 'Figures', 'F1_Play')
    fp.check_dir_exists(dir_path=out_path)

    ''' Get F1 Play Dictionary '''
    f1_play = io.load_json(file_path=Path(config.data_path, 'F1_Play.json'))

    ''' Calculate Sum and Average '''
    results_dictionary = anal.sum_dictionary(dictionary=f1_play)

    ''' Plot F1 Play '''
    for index, race in enumerate(config.completed_races):
        races = config.completed_races[0: index + 1]
        plot.f1play_line(
            results_dictionary=results_dictionary,
            races=races,
            race=race,
            format_dir=config.format_path,
            year=year,
            out_path=out_path)


if __name__ == '__main__':
    year = 2024
    # year = sys.agv[1]
    root = Path().absolute()
    f1_play(
        root=root,
        year=year)

import sys
import src.dataIO as io
import src.filepaths as fp
import src.plotting as plot

from pathlib import Path


""" Fix leaguecount plotting issue. I think this is fixed, driver one a bit
odd though """


"""
Ideas to add:
    * Need to filter in a "Who has gained and lost the most positions" report
    type thing. i.e., who are the big winners and losers?
    * Use images from the league table to populate the league_check.json file.
    This seems like the only guaranteed way to "scrape" the web for this data.
    * Looking at the f1fantasytracker.com site, there is the possibility that we
    could scrape this data, but I just don't know how to do it.
    * Looking at the same site, they also include position in the league, dnf
    rate, average overtakes, average points, etc, as well as podiums, overtakes
    and whatnot.
    * Would like to fold all of the previous years into some kind of "average",
    for both managers that have had repeated entries into the league and the
    drivers and teams that have been across multiple years. Obviously, this is
    going to be tricky based on the different scoring systems.
    * Need to add a spreadsheet of some form, whether that simply be teams in
    the league, or whether that is individual ones for each manager. Some form
    of html insert would be good.
    * This needs to be able to give a top ten report really.
    * Perhaps it could also predict the best possible score? And fold that in to
    how the managers in this league coped with it.
    * Issue where it is no longer resetting teams if final fix is used.
"""

def managerweek(root: str,
                year: str) -> None:
    """
    Function Details
    ================
    Plot manager data for completed races.

    Parameters
    ----------
    root, year: string
        Root directory path, year as a string.

    Returns
    -------
    None

    See Also
    --------
    load_json
    get_completed_races
    check_dir_exists
    league_bars
    leaguecount
    leagueteam_stat
    leagueteam_ppvs

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
    Updated documentation.

    """

    """ Config Files and Season Info """
    info_path = Path(f'{root}/Info.json')
    info_dict = (io.load_json(file_path=info_path))[f'{year}']
    data_path = Path(f'{root}/Data/{year}')
    manager_path = Path(f'{data_path}/Managers')
    format_path = Path(f'{root}/Config')
    manager_results = io.load_json(
        file_path=f'{manager_path}/Results.json')
    manager_stats = io.load_json(
        file_path=f'{manager_path}/Statistics.json')
    counts = io.load_json(
        file_path=f'{manager_path}/Counts.json')

    """ Check Completed Races """
    completed_races = io.get_completed_races(
        results_path=Path(f'{data_path}/Lineup'),
        info_dictionary=info_dict)

    """ Plot League Bars """
    for index, race in enumerate(completed_races):
        races = completed_races[0: index + 1]
        out_path = Path(f'{data_path}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.league_bars(
            results_dictionary=manager_results,
            race_index=index,
            race=race,
            format_dir=format_path,
            year=year,
            out_path=out_path)

    """ Plot League Count """
    for index, race in enumerate(completed_races):
        races = completed_races[0: index + 1]
        out_path = Path(f'{data_path}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.leaguecount(
            results_dictionary=counts,
            race_index=index,
            race=race,
            races=races,
            format_dir=format_path,
            year=year,
            out_path=out_path)

    """ Plot League Statistics """
    for index, race in enumerate(completed_races):
        races = completed_races[0: index + 1]
        out_path = Path(f'{data_path}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.leagueteam_stat(
            statistics_dictionary=manager_stats,
            races=races,
            race=race,
            format_dir=format_path,
            year=year,
            out_path=out_path)

    """ Plot League Price Per Values """
    for index, race in enumerate(completed_races):
        races = completed_races[0: index + 1]
        out_path = Path(f'{data_path}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.leagueteam_ppvs(
            statistics_dictionary=manager_stats,
            race_index=index,
            races=races,
            race=race,
            format_dir=format_path,
            year=year,
            out_path=out_path)


if __name__ == '__main__':
    year = sys.argv[1]
    root = Path().absolute()
    managerweek(
        root=root,
        year=year)

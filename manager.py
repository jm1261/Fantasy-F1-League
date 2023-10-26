import src.dataIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot

from pathlib import Path

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
    * Also need to add a prizes report for the people that have won the sprint
    or world prizes etc.
"""


def check_managers_week(root: str,
                        year: str) -> list:
    """
    Check weekly manager scores.

    Populate the Manager_Check dictionary and manager/team results/stats.

    Parameters
    ----------
    root, year: string
        Root directory path, year as a string.

    Returns
    -------
    wrong_teams: list
        List of teams with the wrong points.

    See Also
    --------
    get_races_sofar
    load_json
    managers_lineup
    save_json_dicts
    manager_statistics
    manager_checked

    Notes
    -----
    Creates the weekly manager lineup json files in the correct managerial
    directories, uses those to calculate results and statistics. Uses the
    statistics to populate the Manager_Checked.json file in descending order to
    be checked against the league page so that lineup files can be altered on
    requirement rather than every team every week as the default option.

    Example
    -------
    None

    """
    info_path = Path(f'{root}/Info.json')
    data_path = Path(f'{root}/Data/{year}')
    races_sofar, races = io.get_races_sofar(
        file_path=info_path,
        results_path=Path(f'{data_path}/Lineup'))
    info_dict = io.load_json(file_path=info_path)
    io.managers_weekly(
        info_dictionary=info_dict,
        data_path=data_path,
        races_sofar=races_sofar,
        races=races)
    lineup_dict = io.load_json(
        file_path=Path(f'{data_path}/Lineup/Results.json'))
    manager_results = anal.managers_lineup(
        lineup_results=lineup_dict,
        info_dictionary=info_dict,
        races_so_far=races_sofar,
        data_path=data_path)
    io.save_json_dicts(
        out_path=Path(f'{data_path}/Managers/Results.json'),
        dictionary=manager_results)
    manager_stats = anal.manager_statistics(results_dict=manager_results)
    io.save_json_dicts(
        out_path=Path(f'{data_path}/Managers/Statistics.json'),
        dictionary=manager_stats)
    manager_counts = anal.count_usage(
        info_dictionary=info_dict,
        races_so_far=races_sofar,
        data_path=data_path)
    io.save_json_dicts(
        out_path=Path(f'{data_path}/Managers/Counts.json'),
        dictionary=manager_counts)
    manager_check = io.manager_checked(
        statistics_dictionary=manager_stats,
        data_path=data_path)
    league_check = io.load_json(
        file_path=Path(f'{data_path}/League_Check.json'))
    wrong_teams = []
    for team, points in manager_check.items():
        league_points = league_check[f'{team}']
        if league_points == points:
            pass
        else:
            wrong_teams.append(team)
    wrong_teams = []
    return wrong_teams


def managerweek(root: str,
                year: str) -> None:
    """

    Parameters
    ----------
    root, year: string
        Root directory path, year as a string.

    Returns
    -------
    None

    See Also
    --------
    get_races_sofar
    load_json
    managers_lineup
    save_json_dicts
    manager_statistics
    manager_checked

    Notes
    -----

    Example
    -------
    None

    """
    info_path = Path(f'{root}/Info.json')
    data_path = Path(f'{root}/Data/{year}')
    format_path = Path(f'{data_path}/Manager_Formats')
    races_sofar, races = io.get_races_sofar(
        file_path=info_path,
        results_path=Path(f'{data_path}/Lineup'))
    manager_path = Path(f'{data_path}/Managers')
    manager_results = io.load_json(
        file_path=f'{manager_path}/Results.json')
    manager_stats = io.load_json(
        file_path=f'{manager_path}/Statistics.json')
    counts = io.load_json(
        file_path=f'{manager_path}/Counts.json')
    for index, race in enumerate(races_sofar):
        races = races_sofar[0: index + 1]
        out_path = Path(f'{data_path}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.league_bars(
            results_dictionary=manager_results,
            race_index=index,
            race=race,
            format_dir=format_path,
            out_path=out_path)
    for index, race in enumerate(races_sofar):
        races = races_sofar[0: index + 1]
        out_path = Path(f'{data_path}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.leaguecount(
            results_dictionary=counts,
            race_index=index,
            race=race,
            races=races,
            format_dir=Path(f'{data_path}/Lineup_Formats'),
            out_path=out_path)
    for index, race in enumerate(races_sofar):
        races = races_sofar[0: index + 1]
        out_path = Path(f'{data_path}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.leagueteam_stat(
            statistics_dictionary=manager_stats,
            races=races,
            race=race,
            format_dir=format_path,
            out_path=out_path)
    for index, race in enumerate(races_sofar):
        races = races_sofar[0: index + 1]
        out_path = Path(f'{data_path}/Figures/{race}')
        fp.check_dir_exists(dir_path=out_path)
        plot.leagueteam_ppvs(
            statistics_dictionary=manager_stats,
            race_index=index,
            races=races,
            race=race,
            format_dir=format_path,
            out_path=out_path)


if __name__ == '__main__':
    year = 2023
    root = Path().absolute()
    wrong_teams = check_managers_week(
        root=root,
        year=year)
    if len(wrong_teams) == 0:
        print('All Good')
        managerweek(
            root=root,
            year=year)
    else:
        print(wrong_teams)

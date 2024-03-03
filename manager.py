import sys
import src.dataIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot

from pathlib import Path


""" Fix leaguecount plotting issue. """


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
    Function Details
    ================
    Function to check the weekly manager scores are correct.

    This function checks the weekly manager scores against the league table to
    ensure determine which teams have been altered.

    Parameters
    ----------
    root, year: string
        Path to root directory, year as a string.

    Returns
    -------
    wrong_teams: list
        List of teams that have been altered.

    See Also
    --------
    load_json
    get_completed_races
    managers_weekly
    managers_lineup
    save_json_dicts
    manager_statistics
    count_usage
    manager_checked

    Notes
    -----
    Creates the weekly manager team sheets in the correct dictionaries and uses
    the results to calculate total points and statistics. Uses this to populate
    a Manager_Check.json file with teams in descending order to be checked
    against the league page so that the manager team sheets can be altered on
    requirement rather than every team entered each week.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    16/02/2024
    ----------
    Updated function description to match the new style and provide more info to
    the reader. Update to function layout with section headers for readability.
    Update to the function that gets the completed races, see the description
    for that function separately.

    27/02/2024
    ----------
    Updated to remove the need for getting a race index and added functionality
    to checking the manager team sheet. Will now cycle through all completed
    races in the event that multiple weeks are missed.

    """

    """ Config Files and Season Info """
    info_path = Path(f'{root}/Info.json')
    info_dict = (io.load_json(file_path=info_path))[f'{year}']
    data_path = Path(f'{root}/Data/{year}')
    lineup_dict = io.load_json(
        file_path=Path(f'{data_path}/Lineup/Results.json'))

    """ Check Completed Races """
    completed_races = io.get_completed_races(
        results_path=Path(f'{data_path}/Lineup'),
        info_dictionary=info_dict)

    """ Update Manager Weekly Team Sheets """
    io.managers_weekly(
        info_dictionary=info_dict,
        data_path=data_path,
        completed_races=completed_races)

    """ Calculate Manager Scores """
    manager_results = anal.managers_lineup(
        lineup_results=lineup_dict,
        info_dictionary=info_dict,
        completed_races=completed_races,
        data_path=data_path)
    io.save_json_dicts(
        out_path=Path(f'{data_path}/Managers/Results.json'),
        dictionary=manager_results)

    """ Calculate Manager Statistics """
    manager_stats = anal.manager_statistics(results_dictionary=manager_results)
    io.save_json_dicts(
        out_path=Path(f'{data_path}/Managers/Statistics.json'),
        dictionary=manager_stats)

    """ Count Manager Usage """
    manager_counts = anal.count_usage(
        info_dictionary=info_dict,
        completed_races=completed_races,
        data_path=data_path)
    io.save_json_dicts(
        out_path=Path(f'{data_path}/Managers/Counts.json'),
        dictionary=manager_counts)

    """ Check Manager Scores Against Online Table """
    manager_check = io.manager_checked(
        statistics_dictionary=manager_stats,
        data_path=data_path)
    league_check = io.load_json(
        file_path=Path(f'{data_path}/League_Check.json'))

    """ Check if any Teams are Wrong """
    wrong_teams = []
    for team, points in manager_check.items():
        league_points = league_check[f'{team}']
        if league_points == points:
            pass
        else:
            wrong_teams.append(team)
    return wrong_teams


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
    year = 2024
    #year = sys.argv[1]
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
        print(len(wrong_teams))

import src.dataIO as io
import src.analysis as anal

from pathlib import Path


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


if __name__ == '__main__':
    year = 2024
    root = Path().absolute()
    wrong_teams = check_managers_week(
        root=root,
        year=year)
    if len(wrong_teams) == 0:
        print('All Good')
    else:
        print(wrong_teams)
        print(len(wrong_teams))

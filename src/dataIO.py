import os
import json
import numpy as np

from pathlib import Path


def load_json(file_path : str) -> dict:
    """
    Loads .json file types.

    Use json python library to load a .json file.

    Parameters
    ----------
    file_path : string
        Path to file.

    Returns
    -------
    json file : dictionary
        .json dictionary file.

    See Also
    --------
    save_json_dicts

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    Example
    -------
    >>> my_dictionary = load_json(file_path="/Path/To/File")
    >>> my_dictionary
    {
        "Item 1" : Value 1,
        "Item 2": Value 2
    }

    """
    with open(file_path, 'r') as f:
        return json.load(f)


def convert(o : str) -> TypeError:
    """
    Check data type.

    Check type of data string.

    Parameters
    ----------
    o : string
        String to check.

    Returns
    -------
    TypeError : Boolean
        TypeError if string is not suitable.


    See Also
    --------
    None.

    Notes
    -----
    None.

    Example
    -------
    None.

    """
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path : str,
                    dictionary : dict) -> None:
    """
    Save .json file types.

    Use json python library to save a dictionary to a .json file.

    Parameters
    ----------
    out_path : string
        Path to file.
    dictionary : dictionary
        Dictionary to save.
    
    Returns
    -------
    None

    See Also
    --------
    load_json

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    Example
    -------
    >>> save_json_dicts(
        out_path="/Path/To/File",
        dictionary=my_dictionary)

    """
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=4,
            default=convert)
        outfile.write('\n')


def create_lineup(lineup_path : str) -> dict:
    """
    Create lineup results dictionary.

    Create driver and team points and values dictionary, blank, containing the
    names of drivers and team for the current year.

    Parameters
    ----------
    lineup_path : string
        Path to lineup directory.
    
    Returns
    -------
    dictionary : dictionary
        Dictionary containing driver and team points and values as dictionaries
        containing names with blank arrays.
    
    See Also
    --------
    create_statistics

    Notes
    -----
    Uses the team format json dictionaries to create a list of all drivers and
    teams with points and values dictionaries containing the names of the teams
    and drivers with blank arrays.

    Example
    -------
    >>> results_dictionary = create_lineup(
        lineup_path="/Path/To/Lineup/Directory")
    >>> results_dictionary
    {
        "Driver Points": {
            "Driver 1": [],
            "Driver 2": []
        }
        "Driver Values": {
            "Driver 1": [],
            "Driver 2": []
        }
        "Team Points": {
            "Team 1": [],
            "Team 2": []
        }
        "Team Values": {
            "Team 1": [],
            "Team 2": []
        }
    }

    """
    files = [
        file for file in os.listdir(lineup_path) if 'Perks.json' not in file]
    paths = [Path(f'{lineup_path}/{file}') for file in files]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    team_dict = {}
    driver_dict = {}
    for index, path in enumerate(paths):
        file = load_json(file_path=path)
        drivers = file['drivers']
        team_dict.update({teams[index]: []})
        [driver_dict.update({driver: []}) for driver in drivers]
    return {
        'Driver Points': driver_dict,
        'Driver Values': driver_dict,
        'Team Points': team_dict,
        'Team Values': team_dict}


def create_statistics(lineup_path : str) -> dict:
    """
    Create the teams and drivers statistics dictionary to record key statistics.

    Create the points per value, total points, total values, etc. arrays in a
    dictionary for the teams and drivers.

    Parameters
    ----------
    lineup_path : string
        Path to lineup directory.
    
    Returns
    -------
    statistics : dictionary
        Statistics dictionary containing blank dictionaries with the teams and
        drivers names and their respective fields.
    
    See Also
    --------
    load_json

    Notes
    -----
    Each driver and team has their points per value, total points, total values,
    and averages recorded in an array that serves as the value to the name key
    in a dictionary. This dictionary is then stored under the statistic name as
    the key in the statistics dictionary. This function builds a blank version
    which is populated by a later function.

    Example
    -------
    None

    """
    files = [
        file for file in os.listdir(lineup_path) if 'Perks.json' not in file]
    paths = [Path(f'{lineup_path}/{file}') for file in files]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    team_dict = {}
    driver_dict = {}
    for index, path in enumerate(paths):
        file = load_json(file_path=path)
        drivers = file['drivers']
        team_dict.update({teams[index]: []})
        [driver_dict.update({driver: []}) for driver in drivers]
    return {
        'Driver Points Per Value': driver_dict,
        'Driver Sum Points': driver_dict,
        'Driver Sum Values': driver_dict,
        'Driver Average Points Per Value': driver_dict,
        'Driver Average Points': driver_dict,
        'Driver Average Values': driver_dict,
        'Team Points Per Value': team_dict,
        'Team Sum Points': team_dict,
        'Team Sum Values': team_dict,
        'Team Average Points Per Value': team_dict,
        'Team Average Points': team_dict,
        'Team Average Values': team_dict}


def create_lineup_weekly(lineup_path : str) -> dict:
    """
    Create weekly dictionary to submit points and values for teams and drivers.

    Creates a dictionary containing the names of all teams and drivers with a
    race submission box, to enter points and values for the current race week.

    Parameters
    ----------
    lineup_path : string
        Path to lineup directory.
    
    Returns
    -------
    weekly_dictionary : dict
        Weekly lineup dictionary.
    
    See Also
    --------
    load_json

    Notes
    -----
    The weekly lineup dictionary is used to record the current points total and
    the values of the teams and drivers for a given race weekend. It is best
    used weekly (or whenever a race is completed). The function creates the
    blank dictionary used to complete this task.

    Example
    -------
    >>> weekly_dictionary = create_lineup_weekly(
        lineup_path="/Path/To/Lineup/Directory")
    >>> weekly_dictionary
    {
        "Race": ["Race"],
        "Driver 1": [points, value],
        "Driver 2": [points, value],
        "Team 1": [points, value],
        "Team 2": [points, value]
    }

    """
    files = [
        file for file in os.listdir(lineup_path) if 'Perks.json' not in file]
    paths = [Path(f'{lineup_path}/{file}') for file in files]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    weekly_dictionary = {
        'Name': ['Points', 'Value'],
        'Race': []}
    for path in paths:
        file = load_json(file_path=path)
        drivers = file['drivers']
        [weekly_dictionary.update({driver: []}) for driver in drivers]
    [weekly_dictionary.update({team: []}) for team in teams]
    return weekly_dictionary


def creates_managers_weekly(info_dict : dict,
                            manager_path : str,
                            team : str,
                            races : list,
                            race_index : int) -> None:
    """
    Parameters
    ----------
    info_dict: dictionary
        Info dictionary for the league.
    manager_path, team: string
        Path to manager directory, team name.
    races: list
        List of races in a season.
    race_index: int
        Index for the current race.
    
    Returns
    -------
    None

    See Also
    --------
    load_json
    save_json_dicts

    Notes
    -----
    Creates a manager lineup dictionary for the current race.

    Example
    -------
    None

    """
    manager_team = info_dict['Team']
    weekly_dictionary = {
        'Position': 'Name',
        'Race': [races[race_index]],
        'Team Name': [team]}
    if race_index != 0:
        previous_week = Path(
            f'{manager_path}/{races[race_index - 1]}_{team}.json')
        if previous_week.is_file():
            previous_dict = load_json(file_path=previous_week)
            for k, v in previous_dict.items():
                if k in weekly_dictionary.keys():
                    pass
                else:
                    weekly_dictionary.update({k: v})
        else:
            [weekly_dictionary.update({item: []}) for item in manager_team]
    else:
        [weekly_dictionary.update({item: []}) for item in manager_team]
    save_json_dicts(
        out_path=Path(f'{manager_path}/{races[race_index]}_{team}.json'),
        dictionary=weekly_dictionary)


def managers_weekly(info_dictionary : dict,
                    data_path : str,
                    races_sofar : list,
                    races : list) -> None:
    """
    Checks to see if manager/team weekly lineup exists, if not creates one.

    Parameters
    ----------
    info_dictionary: dictionary
        Info dictionary for season.
    data_path: string
        Path to data directory.
    races_sofar, races: list
        Races completed so far, list of all races.
    
    Returns
    -------
    None

    See Also
    --------
    create_managers_weekly

    Notes
    -----
    None

    Example
    -------
    None

    """
    managers_dict = info_dictionary["Managers"]
    for manager, teams in managers_dict.items():
        for team in teams:
            for index, race in enumerate(races_sofar):
                out_path = Path(f'{data_path}/{manager}/{race}_{team}.json')
                if out_path.is_file():
                    pass
                else:
                    creates_managers_weekly(
                        info_dict=info_dictionary,
                        manager_path=Path(f'{data_path}/{manager}'),
                        team=team,
                        races=races,
                        race_index=index)


def update_results_dict(info_path: str,
                        results_path: str,
                        lineup_path: str) -> dict:
    """
    Update results dictionary from weekly reports.

    Checks for all race reports and ensures results dictionary is up to date.

    Parameters
    ----------
    info_path, results_path, lineup_path : string
        Paths to info dictionary, results directory, lineup format directory.
    
    Returns
    -------
    results_dict : dictionary
        Results dictionary updated from weekly reports.
    
    See Also
    --------
    corrects_weekly
    update_weeklylineup
    load_json
    get_races_sofar
    save_json_dicts

    Notes
    -----
    Checks through the completed race reports in the results directory and makes
    sure the results dictionary is correct from those. Allows the user to fix
    incorrect or altered results without effort.

    Example
    -------
    >>> results_dict = update_results_dict(
        info_path="/Path/To/Info/Dictionary",
        results_path="/Path/To/Results/Directory",
        lineup_path="/Path/To/Lineup/Formats")
    >>> results_dict
    {
        "Driver 1": [1, 2, 3, 4, 5],
        "Team 1": [1, 2, 3, 4, 5]
    }

    """
    files = [
        file for file in os.listdir(lineup_path) if 'Perks.json' not in file]
    paths = [Path(f'{lineup_path}/{file}') for file in files]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    drivers = []
    for team in teams:
        file = load_json(file_path=Path(f'{lineup_path}/{team}.json'))
        driver_names = file['drivers']
        [drivers.append(driver) for driver in driver_names]
    races_sofar, _ = get_races_sofar(
        file_path=info_path,
        results_path=results_path)
    results_dict = load_json(file_path=Path(f'{results_path}/Results.json'))
    for index, race in enumerate(races_sofar):
        race_results = load_json(
            file_path=Path(f'{results_path}/{race}_Results.json'))
        for key, values in race_results.items():
            if key == 'Name' or key == 'Race':
                pass
            else:
                if key in drivers:
                    ((results_dict["Driver Points"])[key])[index] = values[0]
                    ((results_dict["Driver Values"])[key])[index] = values[1]
                if key in teams:
                    ((results_dict["Team Points"])[key])[index] = values[0]
                    ((results_dict["Team Values"])[key])[index] = values[1]
    save_json_dicts(
        out_path=Path(f'{results_path}/Results.json'),
        dictionary=results_dict)
    return results_dict


def check_races(race : str,
                races : list) -> int:
    """
    Check the reported race.

    Check reported race from list of races and find the race index.

    Parameters
    ----------
    race : string
        Race in the weekly report files or team entries.
    races : list
        List of all races in a season.
    
    Returns
    -------
    race_index : int
        Race index from current season list.
    
    See Also
    --------
    get_races_sofar

    Notes
    -----
    Uses list of all races in a season to return the list index of the current
    race. Useful for adding or appending points/values lists.

    Example
    -------
    >>> race = 'Bahrain'
    >>> races = ['Bahrain', 'Chine', 'Imola']
    >>> race_index = check_races(
        race=race,
        races=races)
    >>> race_index
    0

    """
    race_index = []
    for index, r in enumerate(races):
        if r == race:
            race_index.append(index)
    return race_index[0]


def corrects_weekly(weekly_dictionary : dict,
                    info_dictionary : dict,
                    results_path : str) -> dict:
    """
    Corrects weekly lineup report.

    Corrects weekly lineup report to only record points scored in that race week
    into the results dictionary.

    Parameters
    ----------
    weekly_dictionary, info_dictionary : dictionary
        Weekly dictionary containing total points and current values. Info
        dictionary containing season information, specifically list of races.
    results_path : string
        Path to results directory for lineup results dictionary.
    
    Returns
    -------
    individual_points_dict : dictionary
        Corrected weekly points dictionary.
    
    See Also
    --------
    check_races
    load_json
    update_weeklylineup

    Notes
    -----
    Updates the weekly lineup report containing total points and current values
    for drivers and teams. Uses the results dictionary to calculate the points
    scored on that particular race weekend by summing the total scored so far
    and using the total points entered in the weekly report.

    Example
    -------
    >>> weekly_lineup = corrects_weekly(
        weekly_dictionary=lineup_weekly,
        info_dictionary=info_dictionary,
        results_path="/Path/To/Results/Directory")
    >>> weekly_lineup
    {
        "Driver 1": [1, 2, 3, 4, 5],
        "Team 1": [1, 2, 3, 4, 5]
    }
    
    """
    race = weekly_dictionary['Race']
    individual_points_dict = {}
    race_index = check_races(
        race=race[0],
        races=info_dictionary['Races'])
    if race_index == 0:
        for key, inputs in weekly_dictionary.items():
            individual_points_dict.update({key: inputs})
    else:
        previous_races = load_json(
            file_path=Path(
                f'{results_path}/Results.json'))
        for key, inputs in weekly_dictionary.items():
            if key == 'Name' or key == 'Race':
                individual_points_dict.update({key: inputs})
            else:
                previous_results = dict(
                    previous_races['Driver Points'],
                    ** previous_races['Team Points'])
                if inputs[0] == 'N/A':
                    new_points = 0
                    new_values = 0
                else:
                    new_points = inputs[0] - sum(previous_results[key])
                    new_values = inputs[1]
                individual_points_dict.update({key: [new_points, new_values]})
    return individual_points_dict


def update_weeklylineup(root_path : str,
                        year : str) -> dict:
    """
    Update weekly driver and team points and values.

    Uses json dictionaries to update the weekly results for all teams and
    drivers. Uses the new weekly report and current results file to calculate
    weekly values.

    Parameters
    ----------
    root_path, year : string
        Path to root directory. Year of data collection.

    Returns
    -------
    results_dict : dictionary
        Updated results dictionary containing weekly points and values.

    See Also
    --------
    corrects_weekly
    update_results_dict
    load_json
    save_json_dicts

    Notes
    -----
    Reads in previous race results json files and ensure the results dictionary
    is corrected, allowing for replacing values if mistakes are made. Then uses
    the weekly lineup dictionary, if one exists, and uses the total values in
    the results dictionary to correct the weekly lineup so that only points that
    are scored in that race week are reported. This allows the owner to only
    copy total points from the fantasy f1 website into the weekly lineup report.

    Example
    -------
    >>> results_dictionary = update_weeklylineup(
        root="/Path/To/Root/Directory",
        year="example year")
    >>> results_dictionary
    {
        "Driver 1": [1, 2, 56, 2],
        "Team 2": [23, 19, 30, 45]
    }

    """
    info_path = Path(f'{root_path}/Info.json')
    info_dict = load_json(file_path=info_path)
    results_path = Path(f'{root_path}/Data/{year}/Lineup')
    lineup_path = Path(f'{root_path}/Data/{year}/Lineup_Formats')
    results_dict = update_results_dict(
        info_path=info_path,
        results_path=results_path,
        lineup_path=lineup_path)
    weekly_lineup_dict = load_json(
        file_path=Path(f'{root_path}/Data/{year}/Lineup_Weekly.json'))
    race = weekly_lineup_dict['Race']
    if len(race) != 0:
        print(race)
        weekly_dict = corrects_weekly(
            weekly_dictionary=weekly_lineup_dict,
            info_dictionary=info_dict,
            results_path=results_path)
        save_json_dicts(
            out_path=Path(f'{results_path}/{race[0]}_Results.json'),
            dictionary=weekly_dict)
        race_index = check_races(
            race=race[0],
            races=info_dict['Races'])
        update_list = ['Driver', 'Team']
        for category in update_list:
            category_points = results_dict[f'{category} Points']
            category_values = results_dict[f'{category} Values']
            for key, inputs in weekly_dict.items():
                if key == 'Name' or key == 'Race':
                    pass
                else:
                    if key in category_points.keys():
                        if len(category_points[key]) == race_index + 2:
                            print(
                                f'{key} {(info_dict["Races"])[race_index]}'
                                f'Points Recorded')
                        else:
                            category_points[key].append(inputs[0])
                    if key in category_values.keys():
                        if len(category_values[key]) == race_index + 2:
                            print(
                                f'{key} {(info_dict["Races"])[race_index]}'
                                f'Values Recorded')
                        else:
                            category_values[key].append(inputs[0])
            results_dict.update({f'{category} Points': category_points})
            results_dict.update({f'{category} Values': category_values})
    else:
        print('No Race To Report')
    save_json_dicts(
        out_path=Path(f'{results_path}/Results.json'),
        dictionary=results_dict)
    os.remove(path=Path(f'{root_path}/Data/{year}/Lineup_Weekly.json'))
    lineup_dictionary = create_lineup_weekly(
        lineup_path=Path(f'{root_path}/Data/{year}/Lineup_Formats'))
    save_json_dicts(
        out_path=Path(f'{root_path}/Data/{year}/Lineup_Weekly.json'),
        dictionary=lineup_dictionary)
    return results_dict


def get_races_sofar(file_path : str,
                    results_path : str) -> list[str]:
    """
    Get list of all races completed so far.
    
    Use list of all races and reported races to calculate the number of races
    completed to date.

    Parameters
    ----------
    file_path, results_path : string
        Path to info dictionary, path to results directory.

    Returns
    -------
    races_so_far, races : list[string]
        List of races completed so far, list of all races.

    See Also
    --------
    check_races
    load_json

    Notes
    -----
    Checks the results directory to determine how many races have been completed
    to date from the full list of races in a season. Returns both separately.

    Example
    --------
    >>> races_so_far, races = get_races_sofar(
        file_path="/Path/To/Info/File",
        results_path="/Path/To/Results/Directory")
    >>> races_so_far
    races_completed = ['Bahrain', 'China', 'Imola']
    >>> races
    races = ['Bahrain', 'China', 'Imola', 'Monaco', 'Hungary']

    """
    info = load_json(file_path=file_path)
    races = info['Races']
    races_sofar = []
    for race in races:
        results = Path(f'{results_path}/{race}_Results.json')
        if results.is_file():
            races_sofar.append(race)
    return races_sofar, races


def manager_checked(statistics_dictionary : dict,
                    data_path : str) -> None:
    """
    Create predicted manager scores.

    Parameters
    ----------
    statistics_dictionary: dictionary
        Managers statistics dictionary.
    data_path: string
        Path to data directory.
    
    Returns
    -------
    out_dict: dictionary
        Predicted manager scores.
    
    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None
    
    """
    team_names = []
    team_points = []
    team_sum = statistics_dictionary["Team Sum Points"]
    for manager, teams in team_sum.items():
        for team, points in teams.items():
            team_names.append(team)
            team_points.append(points[-1])
    zipped_lists = zip(team_points, team_names)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    sorted_points, sorted_names = [list(tuple) for tuple in tuples]
    out_dict = {}
    [
        out_dict.update({n: p})
        for n, p
        in zip(sorted_names[::-1], sorted_points[::-1])]
    save_json_dicts(
        out_path=Path(f'{data_path}/Manager_Check.json'),
        dictionary=out_dict)
    return out_dict

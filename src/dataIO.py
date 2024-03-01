import os
import json
import numpy as np

from pathlib import Path
from IPython.display import Markdown, display, Image


def load_json(file_path : str) -> dict:
    """
    Function Details
    ================
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
        "Key 1" : Value 1,
        "Key 2": Value 2
    }

    ----------------------------------------------------------------------------
    Update History
    ==============

    """
    with open(file_path, 'r') as f:
        return json.load(f)


def convert(o : str) -> TypeError:
    """
    Function Details
    ================
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
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    """
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path : str,
                    dictionary : dict) -> None:
    """
    Function Details
    ================
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
    
    ----------------------------------------------------------------------------
    Update History
    ==============

    """
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=4,
            default=convert)
        outfile.write('\n')


def extractfile(dir_path : str,
                file_string : str) -> list:
    """
    Function Details
    ================
    Find all files in a target directory.

    Parameters
    ----------
    dir_path, file_string: string
        Path to target directory. Target file string in file names.

    Returns
    -------
    list: list
        List of all files in the target directory.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    """
    return [file for file in os.listdir(dir_path) if file_string in file]


def get_used_colors(dir_path : str) -> list:
    """
    Function Details
    ================
    Get a list of used manager format colors.

    Parameters
    ----------
    dir_path: string
        Path to manager formats.
    
    Returns
    -------
    used_colors: list
        List of used colors.

    See Also
    --------
    extract_files

    Notes
    -----
    Get a list of all the used manager colors.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    """
    used_colors = []
    manager_formats = extractfile(
        dir_path=dir_path,
        file_string='.json')
    for file in manager_formats:
        file_path = Path(f'{dir_path}/{file}')
        manager_format = load_json(file_path=file_path)
        manager_color = manager_format['bg_color']
        used_colors.append(manager_color)
    return used_colors


def adds_managers_teams(dir_path : str,
                        manager_dict : dict) -> None:
    """
    Function Details
    ================
    Add manager teams to manager format files.

    Parameters
    ----------
    dir_path: string
        Path to manager formats.
    manager_dict: dictionary
        Manager and teams dictionary.

    Returns
    -------
    None

    See Also
    --------
    save_json_dicts

    Notes
    -----
    Add manager teams to the manager format files.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    """
    for manager, teams in manager_dict.items():
        format_path = Path(f'{dir_path}/{manager}.json')
        format_dict = load_json(file_path=format_path)
        for team in teams:
            if team in format_dict['teams']:
                pass
            else:
                format_dict['teams'].append(team)
        save_json_dicts(
            out_path=format_path,
            dictionary=format_dict)


def creates_driver_team_results(lineup_path : str,
                                year : str) -> dict:
    """
    Function Details
    =======
    Create driver and team results dictionary.

    Create driver and team points and values dictionary, blank, containing the
    names of drivers and team for the current year.

    Parameters
    ----------
    lineup_path, year : string
        Path to lineup format directory. Year of season to process.
    
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

    ----------------------------------------------------------------------------
    Update History
    ==============
    
    07/02/2024
    ----------
    Updated to allow for team format dictionaries to be stored in the .config
    directory and have multiple years of data stored in one file. The primary
    change to this function was to load the team dictionary and cycle the keys
    to find the year as a key. If the key is present in the dictionary, then
    the format information for that year can be added. Changed name for PEP8
    purposes. This update was created by J.Male.

    """
    files = [
        file for file in os.listdir(lineup_path) if 'Perks.json' not in file]
    paths = [Path(f'{lineup_path}/{file}') for file in files]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    team_dict = {}
    driver_dict = {}
    for index, path in enumerate(paths):
        team_format_dict = load_json(file_path=path)
        for key, format_dict in team_format_dict.items():
            if key == year:
                drivers = format_dict['drivers']
                team_dict.update({teams[index]: []})
                [driver_dict.update({driver: []}) for driver in drivers]
            else:
                print(f'No information for {teams[index]} for {key} season')
    return {
        'Driver Points': driver_dict,
        'Driver Values': driver_dict,
        'Team Points': team_dict,
        'Team Values': team_dict}


def create_drivers_teams_statistics(lineup_path : str,
                                    year : str) -> dict:
    """
    Function Details
    ================
    Create the teams and drivers statistics dictionary to record key statistics.

    Create the points per value, total points, total values, etc. arrays in a
    dictionary for the teams and drivers.

    Parameters
    ----------
    lineup_path, year : string
        Path to lineup directory. Year of season to process.
    
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

    ----------------------------------------------------------------------------
    Update History
    ==============

    07/02/2024
    ----------
    Updated to allow for team format dictionaries to be stored in the .config
    directory and have multiple years of data stored in one file. The primary
    change to this function was to load the team dictionary and cycle the keys
    to find the year as a key. If the key is present in the dictionary, then
    the format information for that year can be added. Changed name for PEP8
    purposes. This update was created by J.Male.

    """
    files = [
        file for file in os.listdir(lineup_path) if 'Perks.json' not in file]
    paths = [Path(f'{lineup_path}/{file}') for file in files]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    team_dict = {}
    driver_dict = {}
    for index, path in enumerate(paths):
        team_format_dict = load_json(file_path=path)
        for key, format_dict in team_format_dict.items():
            if key == year:
                drivers = format_dict['drivers']
                team_dict.update({teams[index]: []})
                [driver_dict.update({driver: []}) for driver in drivers]
            else:
                print(f'No information for {teams[index]} for {key} season')
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


def create_drivers_teams_weekly(lineup_path : str,
                                year : str) -> dict:
    """
    Function Details
    ================
    Create weekly dictionary to submit points and values for teams and drivers.

    Creates a dictionary containing the names of all teams and drivers with a
    race submission box, to enter points and values for the current race week.

    Parameters
    ----------
    lineup_path, year : string
        Path to lineup directory.
    
    Returns
    -------
    weekly_dictionary : dict
        Weekly lineup dictionary. Year of season to process.
    
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

    ----------------------------------------------------------------------------
    Update History
    ==============

    07/02/2024
    ----------
    Updated to allow for team format dictionaries to be stored in the .config
    directory and have multiple years of data stored in one file. The primary
    change to this function was to load the team dictionary and cycle the keys
    to find the year as a key. If the key is present in the dictionary, then
    the format information for that year can be added. Changed name for PEP8
    purposes. This update was created by J.Male.

    """
    files = [
        file for file in os.listdir(lineup_path) if 'Perks.json' not in file]
    paths = [Path(f'{lineup_path}/{file}') for file in files]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    weekly_dictionary = {
        'Name': ['Points', 'Value'],
        'Race': []}
    for index, path in enumerate(paths):
        team_format_dict = load_json(file_path=path)
        for key, format_dict in team_format_dict.items():
            if key == year:
                drivers = format_dict['drivers']
                [weekly_dictionary.update({driver: []}) for driver in drivers]
            else:
                print(f'No information for {teams[index]} for {key} season')
    [weekly_dictionary.update({team: []}) for team in teams]
    return weekly_dictionary


def updates_managers_weekly(team_dictionary : dict,
                            race_index : int,
                            races : list,
                            team_sheet : list) -> None:
    """
    Function Details
    ================
    Creates a weekly manager lineup dictionary and adds it to the team
    dictionary.

    Parameters
    ----------
    team_dictionary : dictionary
        Manager team dictionary.
    race_index : int
        Race index in races list.
    races, team_sheet : list
        Season races list and blank team sheet list.

    Returns
    -------
    updated_dictionary: dictionary
        Team sheet dictionary with the new weekly dictionary added.

    See Also
    --------
    load_json
    creates_managers_weekly

    Notes
    -----
    The function loads the existing team dictionary, as it can only be used when
    a team dictionary already exists. It then sets a previous race index number
    and uses this to load the previous team sheet. As most managers make very
    few changes, this will automatically propagate the previous team into the
    current week. If there are any perks that affect the team sheet, the
    function will look back further until it finds a team sheet that isn't with
    one of these perks. If the index goes beyond the start of the season, the
    function will create a blank team sheet entry.

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/02/2024
    ----------
    Updated for manager dictionary path.

    """
    index = race_index - 1
    while index >= 0:
        previous_race = races[index]
        previous_team = team_dictionary[f'{previous_race}']
        reset_perks = ['Limitless', 'Final Fix']
        if previous_team["Perks"] in reset_perks:
            index -= 1
        else:
            race_dictionary = {f'{races[race_index]}': previous_team}
            updated_dictionary = dict(
                team_dictionary,
                **race_dictionary)
            break
    if index < 0:
        race_dictionary = creates_managers_weekly(
            race=races[race_index],
            team_sheet=team_sheet)
        updated_dictionary = dict(
            team_dictionary,
            **race_dictionary)
    return updated_dictionary


def creates_managers_weekly(race : str,
                            team_sheet : list) -> None:
    """
    Function Details
    ================
    Creates the first manager team weekly dictionary.

    Parameters
    ----------
    race: string
        Race name.
    team_sheet: list
        List of the team positions.

    Returns
    -------
    team_dictionary: dictionary
        Blank team sheet dictionary.

    See Also
    --------
    None

    Notes
    -----
    Creates a blank team sheet dictionary with given race key.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    14/02/2024
    ----------
    Changed the way manager team sheets are stored so that they are all stored
    in one file, instead of the weekly individual files. Therefore, there is
    no need to create a weekly dictionary every week. This function now creates
    the first team sheet file of the season. This update was created by J.Male.

    """
    team_dictionary = {f'{race}': {}}
    [
        team_dictionary[f'{race}'].update({f'{position}': "",})
        for position in team_sheet]
    return team_dictionary


def managers_weekly(info_dictionary : dict,
                    data_path : str,
                    completed_races : list):
    """
    Function Details
    ================
    Creates or updates the manager team sheet dictionaries.

    Parameters
    ----------
    info_dictionary: dictionary
        Year information dictionary.
    data_path: string
        Path to yearly data folder.
    completed_races: list
        List of races for which driver/team points/values already exist.

    Returns
    -------
    None

    See Also
    --------
    updates_managers_weekly
    save_json_dicts
    creates_managers_weekly

    Notes
    -----
    General function for the management of team sheet dictionaries. The function
    is given a race index, which could be 0 - length of the season, and will
    update or create a new blank team sheet appropriately.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    14/02/2024
    ----------
    General update to the way team sheet dictionaries are managed and an update
    to the function to reflect that. Also, more functionality for the function
    so that it can determine whether to create a new blank dictionary or update
    an existing dictionary.

    27/02/2024
    ----------
    Updated to check dictionary for completed races.

    """
    managers_dict = info_dictionary["Managers"]
    races = info_dictionary["Races"]
    for manager, teams in managers_dict.items():
        for team in teams:
            dictionary_path = Path(f'{data_path}/{manager}/{team}.json')
            for index, race in enumerate(completed_races):
                if dictionary_path.is_file():
                    team_sheet = load_json(file_path=dictionary_path)
                    if race in team_sheet.keys():
                        pass
                    else:
                        updated_team_sheet = updates_managers_weekly(
                            team_dictionary=team_sheet,
                            race_index=index,
                            races=races,
                            team_sheet=info_dictionary["Team"])
                        save_json_dicts(
                            out_path=dictionary_path,
                            dictionary=updated_team_sheet)                
                else:
                    blank_team_sheet = creates_managers_weekly(
                        race=race,
                        team_sheet=info_dictionary["Team"])
                    save_json_dicts(
                        out_path=dictionary_path,
                        dictionary=blank_team_sheet)


def get_completed_races(results_path : str,
                        info_dictionary : dict) -> list:
    """
    Function Details
    ================
    Get a list of all completed races.

    Uses the list of all races and the results file to determine which races
    have been completed.

    Parameters
    ----------
    results_path: string
        Path to results directory for drivers and teams.
    info_dictionary: dictionary
        Season info dictionary.

    Returns
    -------
    races_completed: list
        List of completed races.

    See Also
    --------
    None

    Notes
    -----
    Uses the driver and team weekly results file to determine if a race has been
    completed. If the file exists, the function assumes that the race has been
    completed (or recorded) and will append the race name to a list of completed
    races.

    Example
    -------
    >>> races_so_far = get_completed_races(
            results_path="/Path/To/Results/Directory",
            info_dictionary=info_dict)
    >>> races_so_far
    ['Bahrain', 'China', 'Imola']

    ----------------------------------------------------------------------------
    Update History
    ==============

    16/02/2024
    ----------
    Update to the function description for readability. Removed the load_json
    info dictionary loading as this is not necessary and reduces RAM usage. Also
    removed the returning of "races" as a variable, this is stored within the
    info dictionary and does not need to be handled twice. This updated was
    created by J.Male.

    """
    races = info_dictionary['Races']
    races_completed = []
    for race in races:
        results = Path(f'{results_path}/{race}_Results.json')
        if results.is_file():
            races_completed.append(race)
    return races_completed


def manager_checked(statistics_dictionary : dict,
                    data_path : str) -> None:
    """
    Function Details
    ================
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

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation.

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


def update_weeklylineup(year : str,
                        info_dictionary : dict,
                        data_path : str,
                        results_path : str,
                        format_path : str) -> dict:
    """
    Function Details
    ================
    Update weekly driver and team points and values.

    Uses json dictionaries to update the weekly results for all teams and
    drivers. Uses the new weekly report and current results file to calculate
    weekly values.

    Parameters
    ----------
    year : string
        Year of data collection.
    info_dictionary: dictionary
        Information dictionary for the year.
    data_path, results_path, format_path: string
        Path to data. Path to results directory. Path to format directory.

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

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Updated documentation.

    """

    """ Update Race Results """
    results_dict = update_results_dict(
        info_dictionary=info_dictionary,
        results_path=results_path,
        lineup_path=format_path)

    """ Load New Week and Find Race """
    weekly_lineup_dict = load_json(
        file_path=Path(f'{data_path}/Lineup_Weekly.json'))
    race = weekly_lineup_dict['Race']

    """ If New Week """
    if len(race) != 0:
        print(race)
        weekly_dict = corrects_weekly(
            weekly_dictionary=weekly_lineup_dict,
            info_dictionary=info_dictionary,
            results_path=results_path)
        save_json_dicts(
            out_path=Path(f'{results_path}/{race[0]}_Results.json'),
            dictionary=weekly_dict)
        race_index = check_races(
            race=race[0],
            races=info_dictionary['Races'])
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
                                f'{key} '
                                f'{(info_dictionary["Races"])[race_index]} '
                                f'Points Recorded')
                        else:
                            category_points[key].append(inputs[0])
                    if key in category_values.keys():
                        if len(category_values[key]) == race_index + 2:
                            print(
                                f'{key} '
                                f'{(info_dictionary["Races"])[race_index]} '
                                f'Values Recorded')
                        else:
                            category_values[key].append(inputs[0])
            results_dict.update({f'{category} Points': category_points})
            results_dict.update({f'{category} Values': category_values})
    else:
        print('No Race To Report')

    """ Save and Reset Weekly """
    save_json_dicts(
        out_path=Path(f'{results_path}/Results.json'),
        dictionary=results_dict)
    os.remove(path=Path(f'{data_path}/Lineup_Weekly.json'))
    lineup_dictionary = create_drivers_teams_weekly(
        lineup_path=format_path,
        year=year)
    save_json_dicts(
        out_path=Path(f'{data_path}/Lineup_Weekly.json'),
        dictionary=lineup_dictionary)
    return results_dict


def corrects_weekly(weekly_dictionary : dict,
                    info_dictionary : dict,
                    results_path : str) -> dict:
    """
    Function Details
    ================
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

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Updated Documentation.

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


def check_races(race : str,
                races : list) -> int:
    """
    Function Details
    ================
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
    >>> races = ['Bahrain', 'China', 'Imola']
    >>> race_index = check_races(
        race=race,
        races=races)
    >>> race_index
    0

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Documentation updated.

    """
    race_index = []
    for index, r in enumerate(races):
        if r == race:
            race_index.append(index)
    return race_index[0]


def update_results_dict(info_dictionary: dict,
                        results_path: str,
                        lineup_path: str) -> dict:
    """
    Function Details
    ================
    Update results dictionary from weekly reports.

    Checks for all race reports and ensures results dictionary is up to date.

    Parameters
    ----------
    info_dictionary: dictionary
        Information dictionary for the season.
    results_path, lineup_path : string
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
    get_completed_races
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

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Updated documentation and minor function name changes.

    """

    """ Find Config Files """
    files = [
        file for file in os.listdir(lineup_path) if 'Perks.json' not in file]
    paths = [Path(f'{lineup_path}/{file}') for file in files]

    """ Append Drivers and Teams """
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    drivers = []
    for team in teams:
        file = load_json(file_path=Path(f'{lineup_path}/{team}.json'))
        driver_names = file['drivers']
        [drivers.append(driver) for driver in driver_names]

    """ Get Completed Races """
    completed_races = get_completed_races(
        results_path=results_path,
        info_dictionary=info_dictionary)

    """ Update Race Results """
    results_dict = load_json(file_path=Path(f'{results_path}/Results.json'))
    for index, race in enumerate(completed_races):
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


def output_string(string: str) -> None:
    """
    Function Details
    ================
    Display string file as text.

    Display string as text in Jupyter notebook (or elsewhere).

    Parameters
    ----------
    string: string
        String
    
    Returns
    -------
    Display
        Prints a display to a Jupyter notebook
    
    See Also
    --------

    Notes
    -----
    Uses the Ipython library to display a string as a printed cell output
    in Jupyter notebooks. The returned cell output is then displayed in the html
    export.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Copied and documentation update.
    """
    display(Markdown(string))


def output_json(dictionary : dict) -> None:
    """
    Function Details
    ================
    Display python dictionary file as text.

    Display python dictionary file as text in Jupyter notebook (or elsewhere).

    Parameters
    ----------
    dictionary: dict
        Dictionary object
    
    Returns
    -------
    Display
        Prints a display to a Jupyter notebook
    
    See Also
    --------

    Notes
    -----
    Uses the Ipython library to display a markdown file as a printed cell output
    in Jupyter notebooks. The returned cell output is then displayed in the html
    export.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Copied and documentation update.

    """
    display(Markdown(f'{dictionary}'))


def display_img(file_path : str,
                width=False,
                height=False) -> None:
    """
    Function Details
    ================
    Display image file as text.

    Display image file as text in Jupyter notebook (or elsewhere).

    Parameters
    ----------
    file_path: string
        Path to image.
    
    Returns
    -------
    Display
        Prints a display to a Jupyter notebook
    
    See Also
    --------

    Notes
    -----
    Uses the Ipython library to display an image file as a printed cell output
    in Jupyter notebooks. The returned cell output is then displayed in the html
    export.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Copied and documentation update.

    """
    if height:
        display(Image(filename=file_path, width=width, height=height))
    else:
        display(Image(filename=file_path))

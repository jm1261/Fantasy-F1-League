import os
import json
import numpy as np

from pathlib import Path


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


def updates_managers_weekly(dictionary_path : str,
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
    dictionary_path : string
        Path to manager team dictionary.
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

    """
    team_dictionary = load_json(file_path=dictionary_path)
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
                    race_index : int):
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
    race_index: int
        Race index to update, note if 0 then the function creates a new blank
        team sheet.

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

    """
    managers_dict = info_dictionary["Managers"]
    races = info_dictionary["Races"]
    for manager, teams in managers_dict.items():
        for team in teams:
            dictionary_path = Path(f'{data_path}/{manager}/{team}.json')
            if dictionary_path.is_file():
                updated_team_sheet = updates_managers_weekly(
                    dictionary_path=dictionary_path,
                    race_index=race_index,
                    races=races,
                    team_sheet=info_dictionary["Team"])
                save_json_dicts(
                    out_path=dictionary_path,
                    dictionary=updated_team_sheet)
            else:
                blank_team_sheet = creates_managers_weekly(
                    race=races[race_index],
                    team_sheet=info_dictionary["Team"])
                save_json_dicts(
                    out_path=dictionary_path,
                    dictionary=blank_team_sheet)

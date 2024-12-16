import os
import json
import logging
import numpy as np

from pathlib import Path
from typing import List, Dict

logging.basicConfig(level=logging.INFO)


def extractfile(dir_path: str,
                file_string: str) -> list:
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
        List of all files in the target directory that contain the desired file
        string.

    See Also
    --------
    python - os - listdir

    Notes
    -----
    Target file string can be any string contained within the file, it could be
    a file name identifier (e.g., "Sample_A1"), a number (such as a date or
    time string, e.g., "240516"), or a file extension (e.g., ".png").

    Example
    -------
    None

    ---------------------------------------------------------------------------
    Update History
    ==============

    16/05/2024
    ----------
    Added to repository. Function has been part of a larger resource for a few
    years.

    """
    return [file for file in os.listdir(dir_path) if file_string in file]


def get_used_colors(dir_path: str) -> list:
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

    ---------------------------------------------------------------------------
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


def adds_managers_teams(dir_path: str,
                        manager_dict: dict) -> None:
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

    ---------------------------------------------------------------------------
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


def creates_driver_team_results(lineup_path: str,
                                year: str) -> dict:
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

    ---------------------------------------------------------------------------
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


def create_drivers_teams_statistics(lineup_path: str,
                                    year: str) -> dict:
    """
    Function Details
    ================
    Create the teams and drivers statistics dictionary to record key
    statistics.

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
    Each driver and team has their points per value, total points, total
    values, and averages recorded in an array that serves as the value to the
    name key in a dictionary. This dictionary is then stored under the
    statistic name as the key in the statistics dictionary. This function
    builds a blank version which is populated by a later function.

    Example
    -------
    None

    ---------------------------------------------------------------------------
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


def create_drivers_teams_weekly(lineup_path: str,
                                year: str) -> dict:
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

    ---------------------------------------------------------------------------
    Update History
    ==============

    07/02/2024
    ----------
    Updated to allow for team format dictionaries to be stored in the .config
    directory and have multiple years of data stored in one file. The primary
    change to this function was to load the team dictionary and cycle the keys
    to find the year as a key. If the key is present in the dictionary, then
    the format information for that year can be added. Changed name for PEP8
    purposes.

    02/03/2024
    ----------
    Fixed an issue where the weekly dictionary was bringing in teams that are
    no longer available for certain seasons. This was an easy fix as now it
    appends teams only if those teams have information for the current year.

    """
    files = [
        file for file in os.listdir(lineup_path) if 'Perks.json' not in file]
    paths = [Path(f'{lineup_path}/{file}') for file in files]
    teams = []
    weekly_dictionary = {
        'Name': ['Points', 'Value'],
        'Race': []}
    for index, path in enumerate(paths):
        team_format_dict = load_json(file_path=path)
        for key, format_dict in team_format_dict.items():
            if key == year:
                teams.append(os.path.splitext(os.path.basename(path))[0])
                drivers = format_dict['drivers']
                [weekly_dictionary.update({driver: []}) for driver in drivers]
            else:
                print(f'No information for {paths[index]} for {key} season')
    [weekly_dictionary.update({team: []}) for team in teams]
    return weekly_dictionary


class Configuration:
    """
    Class Details
    =============

    Attributes
    ----------
    root, year: string
        Root directory path, year to process.
    data_path, lineup_path, format_path, manager_path: string
        Assigned attributes from root directory and year to data, lineup
        results, configuration, and manager paths.
    info_dict, manager_results, managers_statistics, managers_counts: dict
        Assigned attributes from manager path dictionaries.
    completed_races: list
        Assigned attribute for completed races in a season.

    Functions
    ---------
    __init__(self, root_directory : str, year : str)
    load_seasoninfo(self, file_name: str)
    get_completed_race(self, races: List[str])
    _has_race_completed(self, race: str)

    ---------------------------------------------------------------------------
    Update History
    ==============

    10/08/2024
    ----------
    Created from repeated scripts.

    """

    def __init__(
            self,
            root_directory: str,
            year: str) -> None:
        """
        Function Details
        ================
        Initialise Configuration class.

        Parameters
        ----------
        root_directory, year: string
            Root directory path for the repository. Year of the season data to
            process

        -----------------------------------------------------------------------
        Update History
        ==============

        10/08/2024
        ----------
        Created.

        """
        self.root = Path(root_directory)
        self.year = f'{year}'
        self.data_path = Path(self.root, 'Data', self.year)
        self.lineup_path = Path(self.data_path, 'Lineup')
        self.format_path = Path(self.root, 'Config')
        self.manager_path = Path(self.data_path, 'Managers')
        self.prizes_path = Path(self.root, 'Prizes')
        self.info_dict = {}

    def load_seasoninfo(self,
                        file_name: str) -> Dict:
        """
        Function Details
        ================
        Loads season information from the specified JSON file.

        Parameters
        ----------
        file_name: string
            Name of the JSON configuration file.

        Returns
        -------
        dictionary
            Dictionary containing the season information.

        See Also
        --------
        load_json

        -----------------------------------------------------------------------
        Update History
        ==============

        10/08/2024
        ----------
        Created.

        """
        info_dictionary = load_json(
            file_path=Path(
                self.format_path,
                f'{file_name}'
            )
        )
        self.info_dict = info_dictionary[f'{self.year}']
        return self.info_dict

    def get_completed_races(self,
                            races: List[str]) -> List[str]:
        """
        Function Details
        ================
        Get a list of all completed races.

        Uses the list of all races and the results file to determine which
        races have been completed.

        Parameters
        ----------
        races: list
            List of target races to process.

        Returns
        -------
        List[str]
            List of completed races.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/02/2024
        ----------
        Update to the function description for readability. Removed the
        load_json info dictionary loading as this is not necessary and reduces
        RAM usage. Also removed the returning of "races" as a variable, this is
        stored within the info dictionary and does not need to be handled
        twice.
        This updated was created by J.Male.

        10/08/2024
        ----------
        Turned function into a class method and removed wasted lines for list
        comprehension.

        """
        self.completed_races = [
            race
            for race in races
            if self._has_race_completed(race)
        ]
        return self.completed_races

    def _has_race_completed(self,
                            race: str) -> bool:
        """
        Function Details
        ================
        Checks if a race is completed based on the presence of a result file.

        Parameters
        ----------
        race: string
            Race name to check.

        Returns
        -------
        bool
            True if the race result file exists, False otherwise.

        -----------------------------------------------------------------------
        Update History
        ==============

        02/11/2024
        ----------
        Created.

        """
        race_file = Path(self.lineup_path, f'{race}_Results.json')
        return race_file.is_file()

    

    

    

    def get_lineups_results(self,
                            file_name: str) -> dict:
        """
        Function Details
        ================
        Get lineup results dictionary.

        Parameters
        ----------
        file_name: string
            Lineup results dictionary name.

        Returns
        -------
        lineup_results: dictionary
            Lineup results for current year.

        See Also
        --------
        load_json

        Notes
        -----
        None.

        Example
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        22/08/2024
        ----------
        Created from info_dictionary.

        """
        self.lineup_results = load_json(
            file_path=Path(f'{self.lineup_path}/{file_name}'))

    def gets_prizes(self,
                    file_name: str) -> dict:
        """
        Function Details
        ================
        Get prizes dictionary.

        Parameters
        ----------
        file_name: string
            Prizes dictionary name.

        Returns
        -------
        prizes: dictionary
            Prizes for current year.

        See Also
        --------
        load_json

        Notes
        -----
        None.

        Example
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        22/08/2024
        ----------
        Created from info_dictionary.

        """
        self.prizes = load_json(
            file_path=Path(f'{self.prizes_path}/{file_name}'))

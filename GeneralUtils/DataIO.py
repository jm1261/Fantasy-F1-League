###############################################################################
###############################################################################
#                           File: Data Input/Output                           #
#                             Author: Joshua Male                             #
#     Description: Functions for general data input, output, and handling     #
#                         Project: Fantasy F1 League                          #
#                              Date: 02/05/2025                               #
#                           Copyright © Joshua Male                           #
###############################################################################
###############################################################################

# Imports
import os
import json
import logging
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.image import imread
from IPython.display import display, Image

# Logging parameters
logger = logging.getLogger(name=Path(__file__).stem)


def load_json(file_path: Path) -> dict:
    """
    Function Details
    ================
    Loads .json file types.

    Use json python library to load a .json file.

    Parameters
    ----------
    file_path: os.PathLike
        Path to file.

    Returns
    -------
    dictionary
        JSON dictionary file.

    ---------------------------------------------------------------------------
    Update History
    ==============

    """
    try:
        with open(file_path, 'r') as f:
            logger.info(f'{file_path} loaded successfully')
            return json.load(f)
    except FileNotFoundError:
        logger.error(f'{file_path} not found')
        raise FileNotFoundError(f'{file_path} not found')


def convert(o: str) -> TypeError:
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

    ---------------------------------------------------------------------------
    Update History
    ==============

    """
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path: Path,
                    dictionary: dict) -> None:
    """
    Function Details
    ================
    Save JSON file types.

    Use JSON python library to save a dictionary to a JSON file.

    Parameters
    ----------
    out_path: os.PathLike
        Path to file.
    dictionary
        Dictionary to save.

    Returns
    -------
    None

    ---------------------------------------------------------------------------
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
        logger.info(f'{out_path} saved successfully')


def check_dir_exists(directory_path: os.PathLike) -> None:
    """
    Function Details
    ================
    Checks directory path exists.

    Parameters
    ----------
    directory_path: os.PathLike
        Path to directory.

    Returns
    -------
    None.

    ---------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Updated documentation.

    """
    if os.path.isdir(directory_path) is False:
        os.mkdir(directory_path)
        logger.info(f'{directory_path} created successfully')


def extractfile(directory_path: str,
                file_string: str) -> list:
    """
    Function Details
    ================
    Find all files in a target directory.

    Parameters
    ----------
    directory_path, file_string: string
        Path to target directory. Target file string in file names.

    Returns
    -------
    list: list
        List of all files in the target directory that contain the desired file
        string.

    Notes
    -----
    Target file string can be any string contained within the file, it could be
    a file name identifier (e.g., "Sample_A1"), a number (such as a date or
    time string, e.g., "240516"), or a file extension (e.g., ".png").

    ---------------------------------------------------------------------------
    Update History
    ==============

    16/05/2024
    ----------
    Added to repository. Function has been part of a larger resource for a few
    years.

    """
    return [file for file in os.listdir(directory_path) if file_string in file]


class LoadConfigs:
    """
    Class Details
    =============
    Loads basic config files required to run the code.

    Attributes
    ----------
    root, data_path, lineup_path: os.PathLike
        Root directory, data storage, lineup output paths.
    format_path, manager_path, prizes_path: os.PathLike
        Config directory, manager output, prizes paths.
    year: string
        Year to process.
    info_dict, lineup_results, weekly_lineup: dictionary
        Season information dictionary. Lineup results dictionary. Weekly
        lineup dictionary (scorecard).
    completed_races: list
        List of completed races based on existing results JSON files.

    Methods
    -------
    __init__
    load_seasoninfo
    get_completed_races
    _has_race_completed
    get_weekly_lineup_score

    ---------------------------------------------------------------------------
    Update History
    ==============

    10/08/2024
    ----------
    Created from repeated scripts.

    03/11/2024
    ----------
    Update to functionality.

    """

    def __init__(self, root_path: Path, year: str) -> None:
        """
        Function Details
        ================
        Initialize LoadConfigs class.

        Parameters
        ----------
        root_directory: os.PathLike
            Root directory path for the main repository.
        year: string
            Year of the season data to process.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        10/08/2024
        ----------
        Created.

        """
        self.root = root_path
        self.year = year
        self.data_path = Path(
            self.root,
            'Data',
            self.year
        )
        self.lineup_path = Path(
            self.data_path,
            'Lineup'
        )
        self.format_path = Path(
            self.root,
            'config'
        )
        self.manager_path = Path(
            self.data_path,
            'Managers'
        )
        self.prizes_path = Path(
            self.root,
            'config'
        )
        self.info_dict = {}
        logger.info('LoadConfigs initialized successfully')

    def load_seasoninfo(self,
                        file_name: str) -> dict:
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
        logger.info('Season info dictionary assigned')
        return self.info_dict

    def get_completed_races(self,
                            races: list) -> list:
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
        logger.info(f'Completed races: {self.completed_races}')
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

        -----------------------------------------------------------------------
        Update History
        ==============

        22/08/2024
        ----------
        Created from info_dictionary.

        """
        self.lineup_results = load_json(
            file_path=Path(f'{self.lineup_path}/{file_name}'))
        logger.info('Lineup results successfully assigned')
        return self.lineup_results

    def get_weekly_lineup_score(self,
                                file_name: str) -> dict:
        """
        Function Details
        ================
        Get weekly lineup results dictionary.

        Parameters
        ----------
        file_name: string
            Weekly lineup results dictionary name.

        Returns
        -------
        weekly_results: dictionary
            Weekly lineup results for current year.

        -----------------------------------------------------------------------
        Update History
        ==============

        03/11/2024
        ----------
        Created from info_dictionary.

        """
        self.weekly_lineup = load_json(
            file_path=Path(f'{self.data_path}/{file_name}'))
        logger.info('Weekly lineup results successfully assigned')
        return self.weekly_lineup

    def get_lineup_stat(self,
                        file_name: str) -> dict:
        """
        Function Details
        ================
        Get lineup statistics dictionary.

        Parameters
        ----------
        file_name: string
            Lineup statistics dictionary name.

        Returns
        -------
        lineup_stats: dictionary
            Lineup statistics for current year.

        -----------------------------------------------------------------------
        Update History
        ==============

        05/11/2024
        ----------
        Created from get_lineup_results.

        """
        self.lineup_stats = load_json(
            file_path=Path(f'{self.lineup_path}', f'{file_name}')
        )
        return self.lineup_stats

    def manager_results(self,
                        file_name: str) -> dict:
        """
        Function Details
        ================
        Get manager results dictionary.

        Parameters
        ----------
        file_name: string
            Manager dictionary name.

        Returns
        -------
        manager_results: dictionary
            Manager results for current year.

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
        self.manager_results = load_json(
            file_path=Path(f'{self.manager_path}/{file_name}'))

    def managers_statistics(self,
                            file_name: str) -> dict:
        """
        Function Details
        ================
        Get manager statistics dictionary.

        Parameters
        ----------
        file_name: string
            Manager dictionary name.

        Returns
        -------
        manager_results: dictionary
            Manager statistics for current year.

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
        self.manager_statistics = load_json(
            file_path=Path(f'{self.manager_path}/{file_name}'))

    def managers_counts(self,
                        file_name: str) -> dict:
        """
        Function Details
        ================
        Get manager counts dictionary.

        Parameters
        ----------
        file_name: string
            Manager dictionary name.

        Returns
        -------
        manager_results: dictionary
            Manager counts for current year.

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
        self.manager_counts = load_json(
            file_path=Path(f'{self.manager_path}/{file_name}'))

    def get_positions(self) -> list:
        """
        Function Details
        ================
        Build a list of team positions to plot based on season info dictionary
        list.

        Parameters
        ----------
        None.

        Returns
        -------
        positions: list
            List of team sheet positions to plot.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/12/2024
        ----------
        Copied from ManagerAnalysis.

        17/12/2024
        ----------
        Updated for immutability.

        """
        # Base positions
        positions = ["Driver", "Constructor", "Perks"]

        # Extend positions based on year-specific perks and team data
        year_positions = self.info_dict["Team"]
        year_perks = self.info_dict["Perks"]

        # Add perks if they match specific values
        perks_to_add = {"Extra DRS", "Mega Driver"}
        positions.extend(
            [
                perk
                for perk in year_perks
                if perk in perks_to_add
            ]
        )

        # Add team positions if they match specific values
        positions_to_add = {"DRS Boost", "Turbo"}
        positions.extend(
            [
                position
                for position in year_positions
                if position in positions_to_add
            ]
        )

        # Return a copy to ensure immutability
        return positions[:]

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
        prizes_file = load_json(
            file_path=Path(f'{self.prizes_path}/{file_name}'))
        self.prizes = prizes_file[f'{self.year}']


class SeasonLaunch:
    """
    Class Details
    =============
    Launches the season by creating necessary directories, manager configs,
    team files, and lineup files.

    Attributes
    ----------
    root_path: Path
        Path to root directory.
    year: string
        Year of season to launch.
    new_managers: list
        List of new managers to create format files for.
    used_colors: list
        List of used colors to avoid when creating new manager format files.

    Methods
    -------
    __init__
    _season_directories
    check_manager_exists
    get_used_colors
    _adds_managers_team

    ---------------------------------------------------------------------------
    Update History
    ==============

    11/03/2026
    ----------
    Created.

    """

    def __init__(self, root_path: Path, year: str) -> None:
        """
        Function Details
        ================
        Initialize SeasonLaunch class.

        Parameters
        ----------

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        11/03/2026
        ----------
        Created.

        """
        self.root = root_path
        self.year = year
        self.data_path = Path(
            self.root,
            'Data',
            self.year
        )

    def _season_directories(self,
                            managers: list) -> None:
        """
        Function Details
        =================
        Create essential directories for a new league.

        Parameters
        ----------
        managers: list
            List of partaking managers.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/03/2024
        ----------
        Updated documentation.

        11/03/2026
        ----------
        Merged into class.

        """
        [
            check_dir_exists(
                directory_path=Path(f'{self.data_path}/{manager}'))
            for manager in managers
        ]
        check_dir_exists(directory_path=Path(f'{self.data_path}/Figures'))
        check_dir_exists(directory_path=Path(f'{self.data_path}/Lineup'))
        check_dir_exists(directory_path=Path(f'{self.data_path}/Managers'))
        logger.info(
            f'Season directories created: {self.data_path}, '
            f'/Figures, /Lineup, /Managers'
        )

    def check_manager_exist(self,
                            config_path: Path,
                            managers: list) -> None:
        """
        Function Details
        ================
        Check to see if there are any new managers.

        Parameters
        ----------
        config_path: Path
            Path to manager format files.
        managers: list
            List of managers.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/03/2024
        ----------
        Created.

        11/03/2026
        ----------
        Merged into class.

        """
        self.new_managers = []
        for manager in managers:
            manager_path = Path(f'{config_path}/{manager}.json')
            if manager_path.is_file():
                pass
            else:
                self.new_managers.append(manager)
        logger.info(f'New managers: {self.new_managers}')

    def get_used_colors(self,
                        config_path: Path) -> None:
        """
        Function Details
        ================
        Get a list of used manager format colors.

        Parameters
        ----------
        directory_path: string
            Path to manager format files.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/03/2024
        ----------
        Created.

        11/03/2026
        ----------
        Merged into class.

        """
        self.used_colors = []
        manager_formats = extractfile(
            directory_path=config_path,
            file_string='.json'
        )
        for file in manager_formats:
            file_path = Path(f'{config_path}', f'{file}')
            manager_format = load_json(file_path=file_path)
            self.used_colors.append(manager_format['bg_color'])
        logger.info(f'Used colors: {self.used_colors}')

    def _adds_managers_team(self,
                            config_path: Path,
                            manager_dict: dict) -> None:
        """
        Function Details
        ================
        Add manager teams to manager format files.

        Parameters
        ----------
        directory_path: string
            Path to manager formats.
        manager_dict: dictionary
            Manager and teams dictionary.

        Returns
        -------
        None

        -----------------------------------------------------------------------
        Update History
        ==============

        19/03/2025
        ----------
        Documentation updated.

        11/03/2026
        ----------
        Merged into class.

        """

        for manager, teams in manager_dict.items():
            format_path = Path(f'{config_path}/{manager}.json')
            format_dict = load_json(file_path=format_path)

            # Convert existing teams to a set for O(1) lookups and easy union
            existing_teams = set(format_dict.get('teams', []))
            new_teams = set(teams)

            # Combine them and convert back to a list
            format_dict['teams'] = list(existing_teams | new_teams)

            save_json_dicts(
                out_path=format_path,
                dictionary=format_dict)
        logger.info('Manager teams added to format files')


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

    Notes
    -----
    Uses the team format json dictionaries to create a list of all drivers and
    teams with points and values dictionaries containing the names of the teams
    and drivers with blank arrays.

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

    19/03/2025
    ----------
    Documentation updated.

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
    logger.info('Driver and team results dictionary created')
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

    Notes
    -----
    Each driver and team has their points per value, total points, total
    values, and averages recorded in an array that serves as the value to the
    name key in a dictionary. This dictionary is then stored under the
    statistic name as the key in the statistics dictionary. This function
    builds a blank version which is populated by a later function.

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

    19/03/2025
    ----------
    Documentation update.

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
    logger.info('Driver and team statistics dictionary created')
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

    Notes
    -----
    The weekly lineup dictionary is used to record the current points total and
    the values of the teams and drivers for a given race weekend. It is best
    used weekly (or whenever a race is completed). The function creates the
    blank dictionary used to complete this task.

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

    19/03/2025
    ----------
    Documentation updated.

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
    logger.info('Weekly lineup dictionary Created')
    return weekly_dictionary


def display_img(file_path: str,
                width: int,
                height: int) -> None:
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
    in Jupyter notebooks. The returned cell output is then displayed in the
    html export.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Copied and documentation update.

    03/05/2024
    ----------
    Removed height and width optionality.

    """
    display(Image(filename=file_path, width=width, height=height))


def cm_to_inches(cm: float) -> float:
    """
    Returns centimeters as inches.

    Parameters
    ----------
    cm : float
        Value in centimeters.

    Returns
    -------
    inches : float
        Value in inches.

    ----------------------------------------------------------------------------
    Update History
    ==============

    24/07/2024
    ----------
    Update to documentation and conversion scalar.

    """
    return round(cm / 2.45, 2)


def displays_images(file_paths: list) -> None:
    """
    Function Details
    ================
    Build a figure containing multiple images to Jupyter display.

    Parameters
    ----------
    file_paths: list
        List of image file paths.

    Returns
    -------
    None.

    ---------------------------------------------------------------------------
    Update History
    ==============

    15/02/2025
    ----------
    Created.

    """
    number_images = len(file_paths)
    number_columns = 2
    number_rows = (number_images + number_columns - 1) // number_columns
    fig, axes = plt.subplots(
        nrows=number_rows,
        ncols=number_columns,
        figsize=[
            cm_to_inches(cm=30 * number_columns),
            cm_to_inches(cm=18 * number_rows)
        ]
    )
    axes = axes.flatten()
    for index, image_path in enumerate(file_paths):
        image = imread(fname=image_path)
        ax = axes[index]
        ax.imshow(image)
        ax.axis('off')
    [fig.delaxes(axes[j]) for j in range(number_images, len(axes))]
    fig.tight_layout()
    plt.show()


def mismatched_team(statistics_dictionary: dict,
                    league_records: dict) -> dict:
    """
    Function Details
    ================
    Identify teams with mismatched points between statistics and the league
    records.

    Parameters
    ----------
    statistics_dictionary, league_records: dict
        Manager statistics dictionary. League check dictionary, manual input.

    Returns
    -------
    mismatched_teams: list
        List of teams that do not match.

    Notes
    -----
    Built on old manager_checked function.

    ---------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation.

    13/12/2024
    ----------
    Change to function name and refactoring.

    """
    # Extract team names and their latest points
    team_points = {
        team: points[-1]
        for teams in statistics_dictionary.get("Team Sum Points", {}).values()
        for team, points in teams.items()
    }

    # Find teams with mismatched points
    mismatched_teams = [
        team for team, points in team_points.items()
        if league_records.get(team) != points
    ]

    return mismatched_teams

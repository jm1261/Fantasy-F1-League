import os
import json
import logging
import numpy as np

from pathlib import Path
from IPython.display import display, Image

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def load_json(file_path: os.PathLike) -> dict:
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


def save_json_dicts(out_path: os.PathLike,
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


class LoadConfigs:
    """
    Class Details
    =============
    Loads the basic config files required to run the code.

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
    get_lineup_results
    get_weekly_lineup_score
    get_lineup_stat
    manager_results
    managers_statistics
    managers_counts
    get_positions
    gets_prizes

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

    def __init__(
            self,
            root_directory: os.PathLike,
            year: str) -> None:
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
        self.root = Path(root_directory)
        self.year = f'{year}'
        self.data_path = Path(self.root, 'Data', self.year)
        self.lineup_path = Path(self.data_path, 'Lineup')
        self.format_path = Path(self.root, 'config')
        self.manager_path = Path(self.data_path, 'Managers')
        self.prizes_path = Path(self.root, 'Prizes')
        self.info_dict = {}
        logger.info('LoadConfigs initialized')

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

    def managers_results(self,
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
        self.prizes = load_json(
            file_path=Path(f'{self.prizes_path}/{file_name}'))


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

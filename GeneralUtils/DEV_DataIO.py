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
import json
import logging
import numpy as np

from pathlib import Path

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
            'Prizes'
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
        logger.info(f'Season info dictionary assigned: {self.year}')
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
            file_path=Path(
                f'{self.data_path}',
                f'{file_name}'))
        logger.info('Weekly lineup results successfully assigned')
        return self.weekly_lineup

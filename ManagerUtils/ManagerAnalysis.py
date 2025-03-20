import os
import logging

from pathlib import Path
from typing import List, Dict
from GeneralUtils.DataIO import load_json, save_json_dicts

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def creates_managers_weekly(race: str,
                            team_template: List[str]) -> Dict[str, Dict]:
    """
    Function Details
    ================
    Creates a blank team sheet dictionary for the specified race.

    Parameters
    ----------
    race: str
        Race name.
    team_template: list
        List of the team positions.

    Returns
    -------
    team_dictionary: dict
        Blank team sheet dictionary.

    Notes
    -----
    Creates a blank team sheet dictionary with given race key.

    ---------------------------------------------------------------------------
    Update History
    ==============

    14/02/2024
    ----------
    Changed the way manager team sheets are stored so that they are all stored
    in one file, instead of the weekly individual files. Therefore, there is
    no need to create a weekly dictionary every week. This function now creates
    the first team sheet file of the season. This update was created by J.Male.

    30/11/2024
    ----------
    Function streamlined.

    """
    return {race: {position: "" for position in team_template}}


def updates_managers_weekly(team_dictionary: Dict[str, Dict],
                            race_index: int,
                            races: List[str],
                            team_template: List[str]) -> Dict[str, Dict]:
    """
    Function Details
    ================
    Updates the weekly manager lineup by propagating the previous team
    unless perks require a blank team sheet.

    Parameters
    ----------
    team_dictionary: dict
        Manager team dictionary.
    race_index: int
        Race index in races list.
    races, team_template: list
        Season races list. Blank team sheet list.

    Returns
    -------
    updated_dictionary: dict
        Team sheet dictionary with the new weekly dictionary added.

    Notes
    -----
    Loads existing team dictionary, can only be used if a team dictionary
    already exists. Sets a previous race index and uses it to load previous
    team sheet. Automatically propagates the previous team into the current
    week. If there are any perks that affect the team sheet, it will be reset.
    Failure mode is a blank team sheet.

    ---------------------------------------------------------------------------
    Update History
    ==============

    27/02/2024
    ----------
    Updated for manager dictionary path.

    30/11/2024
    ----------
    Changed to reset team sheet if perk is anything other than "None".

    """
    index = race_index - 1

    # Propagate previous team if no perks applied
    while index >= 0:
        previous_race = races[index]
        previous_team = team_dictionary[f'{previous_race}']
        if previous_team["Perks"] == "None":
            return {
                **team_dictionary,
                races[race_index]: previous_team
            }
        index -= 1

    # If no valid previous team found, create a blank team sheet
    return {
        **team_dictionary,
        races[race_index]: creates_managers_weekly(
            race=races[race_index],
            team_template=team_template
        )
    }


def managers_weekly(info_dictionary: Dict,
                    data_path: os.PathLike,
                    completed_races: List[str]) -> None:
    """
    Function Details
    ================
    Manages team sheet dictionaries for all managers, updating or creating them
    as needed.

    Parameters
    ----------
    info_dictionary: dict
        Year information dictionary.
    data_path: os.PathLike
        Path to yearly data directory.
    completed_races: list
        List of races for which driver/constructor points/values already exist.

    Returns
    -------
    None.

    Notes
    -----
    General function for the management of team sheet dictionaries. Update or
    create a new blank team sheet appropriately.

    ---------------------------------------------------------------------------
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

    30/11/2024
    ----------
    Tidied function.

    """
    managers_dict = info_dictionary["Managers"]
    races = info_dictionary["Races"]
    team_template = info_dictionary["Team"]

    for manager, teams in managers_dict.items():
        for team in teams:
            team_file_path = Path(data_path, f'{manager}', f'{team}.json')

            # Update team sheet for each race
            for race_index, race in enumerate(completed_races):
                logger.info(f'Updating {manager} {team} {race}')
                # Load or create team sheet
                if team_file_path.is_file():
                    team_sheet = load_json(file_path=team_file_path)
                else:
                    logger.info(f'Creating {manager} {team} blank sheet')
                    team_sheet = {}
                if race not in team_sheet:
                    if race_index < len(races):
                        updated_sheet = updates_managers_weekly(
                            team_dictionary=team_sheet,
                            race_index=race_index,
                            races=races,
                            team_template=team_template
                        )
                        save_json_dicts(
                            out_path=team_file_path,
                            dictionary=updated_sheet
                        )
                    else:
                        blank_sheet = creates_managers_weekly(
                            race=race,
                            team_template=team_template
                        )
                        save_json_dicts(
                            out_path=team_file_path,
                            dictionary=blank_sheet
                        )
            logger.info(f'Updated {manager} {team}')


class RaceScoreCalculator:
    """
    Class Details
    =============
    Calculate manager team race points based on perk selection.

    Attributes
    ----------
    category: str
    driver_names, constructor_names, double_names: list
    driver_results, constructor_results: list

    Methods
    -------
    __init__
    calculate_score
    no_perk
    _extra_drs_
    mega_driver
    _limitless_
    no_negative
    _final_fix_

    ---------------------------------------------------------------------------
    Update History
    ==============

    05/12/2024
    ----------
    Created.

    """

    def __init__(
            self,
            category: str,
            driver_names: list,
            constructor_names: list,
            double_names: list,
            driver_results: dict,
            constructor_results: dict) -> None:
        """
        Function Details
        ================
        Initialize race score calculator functions.

        Parameters
        ----------
        category: str
            Points or Values.
        driver_names, constructor_names, double_names: list
            Manager team selections for drivers, constructors, and boosted.
        driver_results, constructor_results: dict
            Dictionary of all driver and constructor points and values.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        06/12/2024
        ----------
        Created.

        """
        self.category = category
        self.driver_names = driver_names
        self.constructor_names = constructor_names
        self.double_names = double_names
        self.driver_results = driver_results
        self.constructor_results = constructor_results
        logger.info('Race score calculator initialized')

    def calculate_score(self,
                        race_index: int):
        """
        Function Details
        ================
        Calculates the basic scores for drivers, constructors, and doubles.

        Parameters
        ----------
        race_index: int
            Race index in races list.

        Returns
        -------
        driver_scores, constructor_scores, double_scores: list
            Driver points, constructor points, boosted points.

        -----------------------------------------------------------------------
        Update History
        ==============

        30/11/2024
        ----------
        Created from old code.

        """
        driver_scores = [
            self.driver_results[name][race_index]
            for name in self.driver_names
        ]
        constructor_scores = [
            self.constructor_results[name][race_index]
            for name in self.constructor_names
        ]
        double_scores = [
            self.driver_results[name][race_index]
            for name in self.double_names
        ]
        logger.info(f'Calculated race score for race {race_index + 1}')
        return driver_scores, constructor_scores, double_scores

    def no_perk(self, score_dictionary: dict) -> float:
        """
        Function Details
        ================
        Calculate race score and values if no perk given.

        Parameters
        ----------
        score_dictionary: dict
            Dictionary for calculating various perks, must contain "race_index"
            as a key with a number. Also requires "penalties" and the number
            of deducted points as a dictionary entry.

        Returns
        -------
        total_scores: float
            Total score or value for no given perk.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Created.

        01/12/2024
        ----------
        Merged into class method.

        """
        race_index = score_dictionary["race_index"]
        penalties = score_dictionary["penalties"]
        driver, constructor, double = self.calculate_score(
            race_index=race_index
        )
        if self.category == 'Points':
            logger.info('Calculating no perk points')
            total_score = (
                sum(driver) +
                sum(constructor) +
                sum(double) +
                penalties
            )
        else:
            logger.info('Calculating no perk values')
            total_score = (
                sum(driver) +
                sum(constructor)
            )
        return total_score

    def wildcard(self, score_dictionary: dict) -> float:
        """
        Function Details
        ================
        Calculate race score and values if perk is wildcard.

        Parameters
        ----------
        score_dictionary: dict
            Dictionary for calculating various perks, must contain "race_index"
            as a key with a number. Also requires "penalties" and the number
            of deducted points as a dictionary entry.

        Returns
        -------
        total_scores: float
            Total score or value for no wildcard.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Created.

        01/12/2024
        ----------
        Merged into class method.

        """
        race_index = score_dictionary["race_index"]
        penalties = score_dictionary["penalties"]
        driver, constructor, double = self.calculate_score(
            race_index=race_index
        )
        if self.category == 'Points':
            logger.info('Calculating no perk points')
            total_score = (
                sum(driver) +
                sum(constructor) +
                sum(double) +
                penalties
            )
        else:
            logger.info('Calculating no perk values')
            total_score = (
                sum(driver) +
                sum(constructor)
            )
        return total_score

    def auto_pilot(self, score_dictionary: dict) -> float:
        """
        Function Details
        ================
        Calculate race score and values if perk is auto pilot.

        Parameters
        ----------
        score_dictionary: dict
            Dictionary for calculating various perks, must contain "race_index"
            as a key with a number. Also requires "penalties" and the number
            of deducted points as a dictionary entry.

        Returns
        -------
        total_scores: float
            Total score or value for auto pilot.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Created.

        01/12/2024
        ----------
        Merged into class method.

        """
        race_index = score_dictionary["race_index"]
        penalties = score_dictionary["penalties"]
        driver, constructor, double = self.calculate_score(
            race_index=race_index
        )
        if self.category == 'Points':
            logger.info('Calculating no perk points')
            total_score = (
                sum(driver) +
                sum(constructor) +
                sum(double) +
                penalties
            )
        else:
            logger.info('Calculating no perk values')
            total_score = (
                sum(driver) +
                sum(constructor)
            )
        return total_score

    def extra_drs(self, score_dictionary: dict) -> float:
        """
        Function Details
        ================
        Calculate race scores and values if perk is Extra DRS.

        Parameters
        ----------
        score_dictionary: dict
            Dictionary for calculating various perks, must contain "race_index"
            as a key with a number. Also requires "penalties" and the number
            of deducted points as a dictionary entry. Requires the name of the
            extra DRS driver and a string as dictionary entry.

        Returns
        -------
        total_score: float
            Total points or values for the race week.

        Notes
        -----
        Extra DRS is a triple score for a driver. Since function knows the
        driver score already, it adds a double score to the total.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Created.

        01/12/2024
        ----------
        Merged into class method.

        """
        race_index = score_dictionary["race_index"]
        penalties = score_dictionary["penalties"]
        extra_name = score_dictionary["extra_drs"]
        driver, constructor, double = self.calculate_score(
            race_index=race_index
        )
        extra = self.driver_results[extra_name][race_index] * 2
        if self.category == 'Points':
            logger.info('Calculating Extra DRS points')
            total_score = (
                sum(driver) +
                sum(constructor) +
                sum(double) +
                extra +
                penalties
            )
        else:
            logger.info('Calculating Extra DRS values')
            total_score = (
                sum(driver) +
                sum(constructor)
            )
        return total_score

    def mega_driver(self, score_dictionary: dict) -> float:
        """
        Function Details
        ================
        Calculate race scores and values if perk is mega driver.

        Parameters
        ----------
        score_dictionary: dict
            Dictionary for calculating various perks, must contain "race_index"
            as a key with a number. Also requires "penalties" and the number
            of deducted points as a dictionary entry. Requires the name of the
            mega driver and a string as dictionary entry.

        Returns
        -------
        total_score: float
            Total points or values for the race week.

        Notes
        -----
        Mega driver is a triple score for a driver. Since function knows the
        driver score already, it adds a double score to the total.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Created.

        01/12/2024
        ----------
        Merged into class method.

        """
        race_index = score_dictionary["race_index"]
        penalties = score_dictionary["penalties"]
        mega_name = score_dictionary["mega_driver"]
        driver, constructor, double = self.calculate_score(
            race_index=race_index
        )
        mega = self.driver_results[mega_name][race_index] * 2
        if self.category == 'Points':
            logger.info('Calculating mega driver points')
            total_score = (
                sum(driver) +
                sum(constructor) +
                sum(double) +
                mega +
                penalties
            )
        else:
            logger.info('Calculating mega driver values')
            total_score = (
                sum(driver) +
                sum(constructor)
            )
        return total_score

    def limitless(self, score_dictionary: dict) -> float:
        """
        Function Details
        ================
        Calculate race scores and values if perk is limitless.

        Parameters
        ----------
        score_dictionary: dict
            Dictionary for calculating various perks, must contain "race_index"
            as a key with a number. Also requires "penalties" and the number
            of deducted points as a dictionary entry.

        Returns
        -------
        total_score: float
            Total points or values for the race week.

        Notes
        -----
        Limitless removes cost cap limitations, allowing any driver and
        constructor combination. Defaults values to cost cap.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Created.

        05/12/2024
        ----------
        Merged into class method.

        """
        race_index = score_dictionary["race_index"]
        penalties = score_dictionary["penalties"]
        driver, constructor, double = self.calculate_score(
            race_index=race_index
        )
        if self.category == 'Values':
            logger.info('Default scores to 100.00 under limitless')
            total_score = 100.00
        else:
            logger.info('Calculating limitless points')
            total_score = (
                sum(driver) +
                sum(constructor) +
                sum(double) +
                penalties
            )
        return total_score

    def no_negative(self, score_dictionary: dict) -> float:
        """
        Function Details
        ================

        Parameters
        ----------
        score_dictionary: dict
            Dictionary for calculating various perks, must contain "race_index"
            as a key with a number. Also requires "penalties" and the number
            of deducted points as a dictionary entry. Final entry should be the
            team sheet perk entry, either a string or a list.

        Returns
        -------
        total_score: float
            Total points or values for the race week.

        Notes
        -----
        No negative is a perk that discounts any negative points scored in a
        race week. It does not affect team values.

        -----------------------------------------------------------------------
        Update History
        ==============

        27/02/2024
        ----------
        Created

        15/03/2024
        ----------
        No Negative has changed for the 2024 season, now it only includes
        positive scores for all driver points, i.e., if they score a -2 and a
        2, they would normally get 0, now they score 2. This is an issue, but
        can be treated in the same way as the final fix perk.

        05/12/2024
        ----------
        Merged into class method.

        """
        race_index = score_dictionary["race_index"]
        penalties = score_dictionary["penalties"]
        perk = score_dictionary["perk"]
        if isinstance(perk, str):
            logger.info('No negative simple version selected')
            driver, constructor, double = self.calculate_score(
                race_index=race_index
            )
            if self.category == 'Points':
                all_points = []
                all_points.extend(driver)
                all_points.extend(constructor)
                all_points.extend(double)
                positive_points = [x for x in all_points if x > 0]
                total_score = sum(positive_points) + penalties
            else:
                total_score = (
                    sum(driver) +
                    sum(constructor)
                )
        else:
            logger.info('No negative complex version selected')
            no_negative_names = [
                name
                for name in perk[1:]
                if isinstance(name, str)
            ]
            if self.category == 'Points':
                driver = [
                    (self.driver_results[name])[race_index]
                    for name in self.driver_names
                    if name not in no_negative_names
                ]
                constructor = [
                    (self.constructor_results[name])[race_index]
                    for name in self.constructor_names
                    if name not in no_negative_names
                ]
                double = [
                    (self.driver_results[name])[race_index]
                    for name in self.double_names
                    if name not in no_negative_names
                ]
                [
                    driver.append(score)
                    for score in perk[1:]
                    if isinstance(score, int)
                ]
                all_points = []
                all_points.extend(driver)
                all_points.extend(constructor)
                all_points.extend(double)
                total_score = sum(all_points) + penalties
            else:
                driver, constructor, double = self.calculate_score(
                    race_index=race_index
                )
                total_score = sum(driver) + sum(constructor)
        return total_score

    def final_fix(self, score_dictionary: dict) -> float:
        """
        Function Details
        ================
        Calculate race scores or values if Final Fix is the perk.

        Parameters
        ----------
        score_dictionary: dict
            Dictionary for calculating various perks, must contain "race_index"
            as a key with a number. Also requires "penalties" and the number
            of deducted points as a dictionary entry. Must contain the keys
            "replaced_names" and "replaced_scores" with the lists of the
            replaced driver token(s) and their score(s). Replaced driver goes
            first.

        Returns
        -------
        total_score: float
            Total points or values for the race week.

        Notes
        -----
        Final fix allows a manager to replace a driver or team. The perk only
        affects the score of the individual and should be addressed as such.

        -----------------------------------------------------------------------
        Update History
        ==============

        27/02/2024
        ----------
        Created.

        15/03/2024
        ----------
        No updates, just a note that if the replaced driver is a x2, then the
        driver to replace them should have their score as the individual, not
        the x2 as the function already applies the x2.

        05/12/2024
        ----------
        Merged into class method.

        """
        race_index = score_dictionary["race_index"]
        penalties = score_dictionary["penalties"]
        replaced_names = score_dictionary["replaced_names"]
        replaced_scores = score_dictionary["replaced_scores"]
        if self.category == 'Points':
            logger.info('Logging final fix points')
            driver, constructor, double = [], [], []
            for name in self.driver_names:
                if name in replaced_names:
                    [driver.append(score) for score in replaced_scores]
                else:
                    driver.append((self.driver_results[name])[race_index])
            for name in self.constructor_names:
                if name in replaced_names:
                    [constructor.append(score) for score in replaced_scores]
                else:
                    constructor.append(
                        (self.constructor_results[name])[race_index]
                    )
            for name in self.double_names:
                if name in replaced_names:
                    [double.append(score) for score in replaced_scores]
                else:
                    double.append((self.driver_results[name])[race_index])
            total_score = (
                sum(driver) +
                sum(constructor) +
                sum(double) +
                penalties
            )
        else:
            logger.info('Logging final fix values')
            driver, constructor, _ = self.calculate_score(
                race_index=race_index
            )
            total_score = sum(driver) + sum(constructor)
        return total_score


class TokenCounting:
    """
    Class Details
    =============
    Count various token usage and team substitutes.

    Attributes
    ----------
    position
    team_dictionary
    keys

    Methods
    -------
    __init__
    turbo
    drs_boost
    extra_drs
    mega_driver
    perks
    driver
    constructor
    penalties
    substitutes

    ---------------------------------------------------------------------------
    Update History
    ==============

    15/12/2024
    ----------
    Created.

    """

    def __init__(
            self,
            position: str,
            team_dictionary: dict) -> None:
        """
        Function Details
        ================
        Initialize token counting calculator functions.

        Parameters
        ----------
        position: str
            Position to count within team sheet.
        team_dictionary: dict
            Team dictionary for each manager team.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        self.position = position
        self.team_dictionary = team_dictionary
        self.keys = self.team_dictionary.keys()
        logger.info('Token counter initialized')

    def turbo(self) -> list:
        """
        Function Details
        ================
        Count turbo selected drivers.

        Parameters
        ----------
        None.

        Returns
        -------
        count_name: list
            List of names within the specified position.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        count_names = [
            self.team_dictionary[key]
            for key in self.keys
            if self.position in key
        ]
        return count_names

    def drs_boost(self) -> list:
        """
        Function Details
        ================
        Count drs boost selected drivers.

        Parameters
        ----------
        None.

        Returns
        -------
        count_name: list
            List of names within the specified position.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        count_names = [
            self.team_dictionary[key]
            for key in self.keys
            if self.position in key
        ]
        return count_names

    def extra_drs(self) -> list:
        """
        Function Details
        ================
        Count extra drs selected drivers.

        Parameters
        ----------
        None.

        Returns
        -------
        count_name: list
            List of names within the specified position.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        perks = self.team_dictionary["Perks"]
        if isinstance(perks, list) and self.position in perks:
            # Use the second item in the list, if it exists
            count_names = [perks[1]] if len(perks) > 1 else []
        elif isinstance(perks, dict) and self.position in perks:
            # Use the perk associated with the position in the dictionary
            count_names = [perks[self.position]]
        else:
            # Handle cases where perks is neither
            count_names = []
        return count_names

    def mega_driver(self) -> list:
        """
        Function Details
        ================
        Count mega driver selected drivers.

        Parameters
        ----------
        None.

        Returns
        -------
        count_name: list
            List of names within the specified position.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        perks = self.team_dictionary["Perks"]
        if isinstance(perks, list) and self.position in perks:
            # Use the second item in the list, if it exists
            count_names = [perks[1]] if len(perks) > 1 else []
        elif isinstance(perks, dict) and self.position in perks:
            # Use the perk associated with the position in the dictionary
            count_names = [perks[self.position]]
        else:
            # Handle cases where perks is neither
            count_names = []
        return count_names

    def perks(self) -> list:
        """
        Function Details
        ================
        Count perks selection.

        Parameters
        ----------
        None.

        Returns
        -------
        count_name: list
            List of names within the specified position.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        perks = self.team_dictionary["Perks"]
        count_names = [
            (self.team_dictionary[f'{self.position}'])[0]
            if isinstance(perks, list)
            else self.team_dictionary[f'{self.position}']
        ]
        return count_names

    def driver(self) -> list:
        """
        Function Details
        ================
        Count selected drivers.

        Parameters
        ----------
        None.

        Returns
        -------
        count_name: list
            List of names within the specified position.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        count_names = [
            self.team_dictionary[key]
            for key in self.keys
            if self.position in key
        ]
        return count_names

    def constructor(self) -> list:
        """
        Function Details
        ================
        Count selected constructors.

        Parameters
        ----------
        None.

        Returns
        -------
        count_name: list
            List of names within the specified position.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        count_names = [
            self.team_dictionary[key]
            for key in self.keys
            if self.position in key
        ]
        return count_names

    def penalties(self) -> list:
        """
        Function Details
        ================
        Count penalties.

        Parameters
        ----------
        None.

        Returns
        -------
        count_name: list
            List of names within the specified position.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        count_names = [
            self.team_dictionary[key]
            for key in self.keys
            if self.position in key
        ]
        return count_names

    def substitutes(self) -> list:
        """
        Function Details
        ================
        Count substitutes.

        Parameters
        ----------
        None.

        Returns
        -------
        count_name: list
            List of names within the specified position.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        count_names = []
        positions = ['Driver', 'Constructor']
        for position in positions:
            for key in self.keys:
                if position in key:
                    count_names.append(self.team_dictionary[key])
        return count_names


class ManagerProcessor:
    """
    Class Details
    =============
    Calculates manager and team results.

    Attributes
    ----------
    lineup_results, info_dict: dict
    completed_races: list
    data_path: str
    driver_results, constructor_results: dict
    results
    statistics
    counts

    Methods
    -------
    __init__
    _team_keys_
    _call_perks
    team_scores
    managers_scores
    category_scores
    managers_lineup
    teamSum
    manager_sum
    teamPPV
    manager_ppv
    position_gains
    manager_stats
    _call_count
    team_counts
    _manager_counts
    leaguecount
    get_positions
    count_usage

    ---------------------------------------------------------------------------
    Update History
    ==============

    06/12/2024
    ----------
    Created.

    """

    def __init__(
            self,
            lineup_results: dict,
            info_dictionary: dict,
            completed_races: list,
            data_path: os.PathLike) -> None:
        """
        Function Details
        ================
        Initialize manager processor.

        Parameters
        ----------
        lineup_results, info_dictionary: dict
            Lineup results dictionary. Season info dictionary.
        completed_races: list
            List of completed races.
        data_path: os.PathLike
            Path to yearly data.

        Returns
        -------
        None.

        Notes
        -----
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        06/12/2024
        ----------
        Created.

        """
        self.lineup_results = lineup_results
        self.info_dict = info_dictionary
        self.completed_races = completed_races
        self.data_path = data_path
        self.driver_results = {}
        self.constructor_results = {}
        self.results = {}
        self.statistics = {}
        self.counts = {}
        logger.info('Manager Processor initialized')

    def _team_keys_(self,
                    team_dictionary: dict,
                    race: str) -> float:
        """
        Function Details
        ================
        Pull the required team keys from the team sheet dictionary.

        Parameters
        ----------
        team_dictionary: dict
            Manager team dictionary.
        race: str
            Race name.

        Returns
        -------
        driver_names, constructor_names, double_names, perks, penalties: list
            Driver names, constructor names, double/turbo names, and perks list
            for given race.

        Notes
        -----
        Pull names from a team sheet for a given race name.

        -----------------------------------------------------------------------
        Update History
        ==============

        06/12/2024
        ----------
        Created.

        """
        team_sheet = team_dictionary[f'{race}']
        team_keys = team_sheet.keys()
        driver_names = [
            team_sheet[key]
            for key in team_keys
            if 'Driver' in key
        ]
        constructor_names = [
            team_sheet[key]
            for key in team_keys
            if 'Constructor' in key or 'Team' in key
        ]
        double_names = [
            team_sheet[key]
            for key in team_keys
            if 'DRS' in key or 'Turbo' in key
        ]
        perks = team_sheet['Perks']
        penalties = team_sheet['Penalties']
        return driver_names, constructor_names, double_names, perks, penalties

    def _call_perks(self,
                    perk: str,
                    instance,
                    score_dictionary: dict) -> float:
        """
        Function Details
        ================
        Use the given team sheet perk to call the correct race score calculator
        and provide the correct details required to calculate the score.

        Parameters
        ----------
        perk: str
            Perk name.
        instance: class/function
            Function name or class name to call the race scores.
        score_dictionary: dict
            Score dictionary containing the relevant keys for each perk score
            calculator instance.

        Returns
        -------
        race_scores: float
            Race scores.

        Notes
        -----
        Score dictionary needs to contain the required keys for all the race
        score calculator functions.

        -----------------------------------------------------------------------
        Update History
        ==============

        06/12/2024
        ----------
        Created.

        """
        function_map = {
            "None": instance.no_perk,
            "Wildcard": instance.wildcard,
            "Auto Pilot": instance.auto_pilot,
            "Extra DRS": instance.extra_drs,
            "Mega": instance.mega_driver,
            "Limitless": instance.limitless,
            "No Negative": instance.no_negative,
            "Final Fix": instance.final_fix
        }
        if perk in function_map:
            race_scores = function_map[f'{perk}'](score_dictionary)
            logger.info('Race scores calculated')
        else:
            race_scores = 0
            logger.error(f'No function mapped for perk {perk}')
        return race_scores

    def team_scores(self,
                    category: str,
                    team_dictionary: dict) -> list:
        """
        Function Details
        ================
        Calculate a team's score for all completed races and build a list.

        Parameters
        ----------
        category: str
            "Points" or "Values".
        team_dictionary: dict
            Team sheet dictionary for the season so far.

        Returns
        -------
        team_scores: list
            List of team scores for category input.

        Notes
        -----
        Uses the perk logic in race calculator to determine the points or the
        values total for each race week.

        -----------------------------------------------------------------------
        Update History
        ==============

        06/12/2024
        ----------
        Created.

        """
        team_scores = []
        for index, race in enumerate(self.completed_races):
            driver, constructor, double, perks, penalties = self._team_keys_(
                team_dictionary=team_dictionary,
                race=race
            )
            # Determine the perk to use
            if isinstance(perks, list):
                perk = perks[0]
            elif isinstance(perks, str):
                perk = perks
            else:
                logger.error('Invalid perk type. Must be a string or list')
                break
            score_dictionary = {
                "race_index": index,
                "penalties": penalties
            }
            if perk == 'None':
                logger.info('Building score dictionary for no perk')
            elif perk == 'Extra DRS':
                logger.info('Building score dictionary for extra drs')
                score_dictionary.update({
                    "extra_drs": perks[1]
                })
            elif perk == 'Mega':
                logger.info('Building score dictionary for mega driver')
                score_dictionary.update({
                    "mega_driver": perks[1]
                })
            elif perk == 'Limitless':
                logger.info('Building score dictionary for limitless')
            elif perk == 'No Negative':
                logger.info('Building score dictionary for no negative')
                score_dictionary.update({
                    "perk": perks
                })
            elif perk == 'Final Fix':
                logger.info('Building score dictionary for final fix')
                score_dictionary.update({
                    "replaced_names": [perks[1], perks[3]],
                    "replaced_scores": [perks[2], perks[4]]
                })
            calculator = RaceScoreCalculator(
                category=category,
                driver_names=driver,
                constructor_names=constructor,
                double_names=double,
                driver_results=self.driver_results,
                constructor_results=self.constructor_results
            )
            race_score = self._call_perks(
                perk=perk,
                instance=calculator,
                score_dictionary=score_dictionary
            )
            team_scores.append(race_score)
        return team_scores

    def managers_scores(self,
                        category: str,
                        manager: str,
                        teams: list) -> tuple:
        """
        Function Details
        ================
        Calculate manager individual, sum, and average scores per race week.

        Parameters
        ----------
        category, manager: str
            "Points" or "Values". Manager name.
        teams: list
            List of teams for given manager.

        Returns
        -------
        manager_results: dict
            Manager results dictionary containing all associated teams and
            their scores/values.
        manager_sum, manager_average: list
            Sum of manager teams. Average of manager teams.

        Notes
        -----
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        11/12/2024
        ----------
        Created.

        """
        team_results = {}
        manager_scores = []
        for team in teams:
            team_dictionary = load_json(
                file_path=Path(
                    self.data_path,
                    f'{manager}',
                    f'{team}.json'
                )
            )
            race_scores = self.team_scores(
                category=category,
                team_dictionary=team_dictionary
            )
            manager_scores.append(race_scores)
            team_results.update({team: race_scores})
        manager_sum = [sum(i) for i in zip(*manager_scores)]
        manager_average = [
            sum(i) / len(manager_scores)
            for i in zip(*manager_scores)
        ]
        return team_results, manager_sum, manager_average

    def category_scores(self,
                        category: str) -> tuple:
        """
        Function Details
        ================
        Calculate results, sums, and averages for all managers for a given
        category.

        Parameters
        ----------
        category: str
            "Points" or "Values".

        Returns
        -------
        team_results, manager_sums, manager_averages: dict
            Results, sums, and averages for all managers for given category.

        Notes
        -----
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        11/12/2024
        ----------
        Created.

        """
        team_results, manager_sums, manager_averages = {}, {}, {}
        self.driver_results = self.lineup_results[f'Driver {category}']
        self.constructor_results = self.lineup_results[
            f'Constructor {category}'
        ]
        for manager, teams in self.info_dict['Managers'].items():
            results, sums, average = self.managers_scores(
                category=category,
                manager=manager,
                teams=teams
            )
            team_results.update({manager: results})
            manager_sums.update({manager: sums})
            manager_averages.update({manager: average})
        return team_results, manager_sums, manager_averages

    def managers_lineup(self) -> dict:
        """
        Function Details
        ================
        Calculate results, sums, and averages for points and values for all
        managers and teams.

        Parameters
        ----------
        None.

        Returns
        -------
        results: dict
            Results dictionary.

        Notes
        -----
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        12/12/2024
        ----------
        Created.

        """
        categories = ['Points', 'Values']
        for category in categories:
            team_result, manager_sum, manager_average = self.category_scores(
                category=category
            )
            self.results.update({f'Team {category}': team_result})
            self.results.update({f'Manager {category}': manager_sum})
            self.results.update({
                f'Manager Average {category}': manager_average
            })
        return self.results

    def teamSum(self,
                category: str,
                manager: str) -> dict:
        """
        Function Details
        ================
        Calculate manager points, values, average points, and average values.

        Parameters
        ----------
        category, manager: str
            Points or values. Manager name.

        Returns
        -------
        teams_sum: dict
            Team sum and team average points or values.

        Notes
        -----
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Copied from old code. Documentation updated to current coding
        practices.

        12/12/2024
        ----------
        Merged with class method.

        """
        teams_sum = {}
        category_team_dictionary = (
            self.results[f'Team {category}']
        )[f'{manager}']
        for team, entries in category_team_dictionary.items():
            team_sum = []
            for index, entry in enumerate(entries):
                if index == 0:
                    team_sum.append(entry)
                else:
                    team_sum.append(entry + team_sum[index - 1])
            teams_sum.update({team: team_sum})
        return teams_sum

    def manager_sum(self,
                    category: str) -> tuple[Dict, Dict]:
        """
        Function Details
        ================
        Calculate manager points, values, average points, and average values.

        Parameters
        ----------
        category: str
            Points or values.

        Returns
        -------
        tuple: dict, dict
            Manager sum and manager average points or values.

        Notes
        -----
        Also returns team sums if category is not average.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Copied from old code. Documentation updated to current coding
        practices.

        12/12/2024
        ----------
        Merged with class method.

        """
        category_manager_dict = (
            self.results[f'Manager {category}']
        )
        managers_sum, manager_teams_sum = {}, {}
        for manager, entries in category_manager_dict.items():
            if 'Average' in category:
                teams_sum = {}
            else:
                teams_sum = self.teamSum(
                    category=category,
                    manager=manager
                )
            manager_sum = []
            for index, entry in enumerate(entries):
                if index == 0:
                    manager_sum.append(entry)
                else:
                    manager_sum.append(entry + manager_sum[index - 1])
            managers_sum.update({manager: manager_sum})
            manager_teams_sum.update({manager: teams_sum})
        return manager_teams_sum, managers_sum

    def teamPPV(self,
                manager: str) -> tuple[Dict, Dict]:
        """
        Function Details
        ================
        Calculate race-wise and season-average team points per value.

        Parameters
        ----------
        manager: str
            Manager name.

        Returns
        -------
        tuple: dict, dict
            Team points per value, team average points per value.

        Notes
        -----
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Copied from old code. Documentation updated to current coding
        practices.

        12/12/2024
        ----------
        Merged into class method.

        """
        teams_ppv, teams_avg_ppv = {}, {}
        team_points = (self.results['Team Points'])[f'{manager}']
        team_values = (self.results['Team Values'])[f'{manager}']
        for team, entries in team_points.items():
            values = team_values[team]
            team_ppv = [
                p / v
                if v != 0 else 0
                for p, v in zip(entries, values)]
            team_avg_ppv = []
            for index, entry in enumerate(team_ppv):
                if index == 0:
                    team_avg_ppv.append(entry)
                else:
                    team_avg_ppv.append(
                        sum(team_ppv[0: index + 1]) / (index + 1)
                    )
            teams_ppv.update({team: team_ppv})
            teams_avg_ppv.update({team: team_avg_ppv})
        return teams_ppv, teams_avg_ppv

    def manager_ppv(self) -> None:
        """
        Function Details
        ================
        Calculate race-wise and season-average manager points per value.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        Notes
        -----
        Updates statistics dictionary.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Copied from old code. Documentation updated to current coding
        practices.

        12/12/2024
        ----------
        Merged into class method.

        """
        manager_teams_ppvs, manager_teams_avg_ppvs = {}, {}
        manager_ppvs, manager_avg_ppvs = {}, {}
        managers = self.results['Manager Points'].keys()
        for manager in managers:
            teams_ppv, teams_avg_ppv = self.teamPPV(manager=manager)
            manager_points = (self.results['Manager Points'])[f'{manager}']
            manager_values = (self.results['Manager Values'])[f'{manager}']
            manager_ppv = [
                p / v
                if v != 0 else 0
                for p, v
                in zip(manager_points, manager_values)
            ]
            manager_avg_ppv = []
            for index, entry in enumerate(manager_ppv):
                if index == 0:
                    manager_avg_ppv.append(entry)
                else:
                    manager_avg_ppv.append(
                        sum(manager_ppv[0: index + 1]) / (index + 1)
                    )
            manager_teams_ppvs.update({manager: teams_ppv})
            manager_teams_avg_ppvs.update({manager: teams_avg_ppv})
            manager_ppvs.update({manager: manager_ppv})
            manager_avg_ppvs.update({manager: manager_avg_ppv})
        self.statistics.update({'Team Points Per Value': manager_teams_ppvs})
        self.statistics.update({
            'Team Average Points Per Value': manager_teams_avg_ppvs
        })
        self.statistics.update({'Manager Points Per Value': manager_ppvs})
        self.statistics.update({
            'Manager Average Points Per Value': manager_avg_ppvs
        })

    def position_gains(self) -> dict:
        """
        Function Details
        ================
        Determine positions gained and lost on a weekly basis.

        Parameters
        ----------
        None.

        Returns
        -------
        positions_gained: dict
            Dictionary containing the positions gained (positive) and positions
            lost (negative) for all entered teams, sorted with their respective
            managers.

        Notes
        -----
        Function will always update the positions gained dictionary with a list
        with 0 as the first entry for the first race, in which no positions
        were gained.

        -----------------------------------------------------------------------
        Update History
        ==============

        08/05/2024
        ----------
        Created.

        13/12/2024
        ----------
        Merged into class method.

        """
        pos_gained = {}

        # Loop races
        for index, race in enumerate(self.completed_races):

            # Points and previous points lists
            current_points = []
            previous_points = []
            team_names = []

            for _, teams in self.statistics["Team Sum Points"].items():
                for team, values in teams.items():

                    # Sort for first race
                    if index == 0:
                        logger.info(
                            f'Initial positions gained for {team} '
                            f'in first race set to 0')
                        pos_gained[f'{team}'] = [0]

                    # Otherwise
                    else:

                        # Collect current and previous points
                        current_points.append(values[index])
                        previous_points.append(values[index - 1])
                        team_names.append(team)

            # Process subsequent races
            if index > 0:

                # Calculate position gains
                current_ranking = {
                    team: rank
                    for rank, (_, team)
                    in enumerate(sorted(zip(current_points, team_names)))
                }
                previous_ranking = {
                    team: rank
                    for rank, (_, team)
                    in enumerate(sorted(zip(previous_points, team_names)))
                }
                for team in team_names:
                    gain = -(previous_ranking[team] - current_ranking[team])
                    logger.info(
                        f'Positions gained for {team} in {race} is {gain}')
                    pos_gained[f'{team}'].append(gain)

        # Group teams into managers
        positions_gained = {
            manager: {
                team: pos_gained[team]
                for team in teams if team in pos_gained
            }
            for manager, teams in self.info_dict['Managers'].items()
        }
        return positions_gained

    def manager_stats(self) -> dict:
        """
        Function Details
        ================
        Calculate manager and team statistics.

        Parameters
        ----------
        None.

        Returns
        -------
        statistics: dict
            Manager statistics dictionary.

        Notes
        -----
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        28/02/2024
        ----------
        Brought across from old code.

        05/05/2024
        ----------
        Added positions gained.

        12/12/2024
        ----------
        Merged into class method.

        """
        categories = ['Points', 'Values', 'Average Points', 'Average Values']
        for category in categories:
            if 'Average' in category:
                _, manager_sum = self.manager_sum(category=category)
                self.statistics.update({
                    f'Manager Sum {category}': manager_sum
                })
            else:
                team_sum, manager_sum = self.manager_sum(category=category)
                self.statistics.update({f'Team Sum {category}': team_sum})
                self.statistics.update({
                    f'Manager Sum {category}': manager_sum
                })
        self.manager_ppv()
        positions_gained = self.position_gains()
        self.statistics.update({"Team Positions Gained": positions_gained})
        return self.statistics

    def _call_count(self,
                    position: str,
                    instance) -> list:
        """
        Function Details
        ================
        Use the given team sheet position to call the correct token counter
        and provide the correct details required to count their usage.

        Parameters
        ----------
        position: str
            Position name.
        instance: class/function
            Function name or class name to call the token calculator.

        Returns
        -------
        count_names: list
            List of names to count.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        function_map = {
            "Turbo": instance.turbo,
            "DRS Boost": instance.drs_boost,
            "Extra DRS": instance.extra_drs,
            "Mega Driver": instance.mega_driver,
            "Perks": instance.perks,
            "Driver": instance.driver,
            "Constructor": instance.constructor,
            "Penalties": instance.penalties,
            "Substitutes": instance.substitutes
        }
        if position in function_map:
            count_names = function_map[f'{position}']()
            logger.info('Counting completed')
        else:
            count_names = 0
            logger.error(f'No function mapped for position {position}')
        return count_names

    def team_counts(self,
                    position: str,
                    team_dictionary: dict) -> tuple[Dict, Dict]:
        """
        Function Details
        ================
        Count team positions for all completed races and build a dictionary.

        Parameters
        ----------
        position: str
            Position to count.
        team_dictionary: dict
            Annual team dictionary for given team.

        Returns
        -------
        team_count, team_sum_count: dict
            Team count for position for individual races, sum count for season.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        team_count, team_sum_count = {}, {}

        # Loop through completed races
        for index, race in enumerate(self.completed_races):
            counter = TokenCounting(
                position=position,
                team_dictionary=team_dictionary[f'{race}']
            )
            count_names = self._call_count(
                position=position,
                instance=counter
            )

            # Update team counts for the current race
            if position == 'Penalties':
                for name in count_names:
                    if 'Penalties' in team_count:
                        team_count['Penalties'].append(name)
                    else:
                        team_count['Penalties'] = [name]
            elif position == 'Substitutes':
                if index == 0:
                    team_count['Substitutes'] = [0]
                else:
                    previous_race = self.completed_races[index - 1]
                    previous = TokenCounting(
                        position=position,
                        team_dictionary=team_dictionary[
                            f'{previous_race}'
                        ]
                    )
                    previous_names = self._call_count(
                        position=position,
                        instance=previous
                    )
                    set_current = set(count_names)
                    set_previous = set(previous_names)
                    differences = (
                        (set_current - set_previous) |
                        (set_previous - set_current))
                    number_differences = len(differences) / 2
                    team_count['Substitutes'].append(int(number_differences))
            else:
                for name in count_names:
                    if name in team_count:
                        team_count[name].append(1)
                    else:
                        team_count[name] = [0] * index + [1]

            # Add zeros for names not present in the current race
            if position == 'Penalties':
                pass
            elif position == 'Substitutes':
                pass
            else:
                for name in team_count:
                    if name not in count_names:
                        team_count[name].append(0)

        # Calculate cumulative sums for each team
        for name, usage in team_count.items():
            team_sum_count[name] = [
                sum(usage[:i + 1])
                for i in range(len(usage))
            ]

        return team_count, team_sum_count

    def _manager_counts(self,
                        team_count: dict) -> tuple[Dict, Dict]:
        """
        Function Details
        ================
        Count manager positions for all completed races and build a dictionary.

        Parameters
        ----------
        team_count: dict
            Team count dictionary from self.team_counts.

        Returns
        -------
        manager_count, manager_sum_count: dict
            Manager count for position for individual races, sum count for
            season.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        manager_count, manager_sum_count = {}, {}

        # Loop team dictionaries in team counts
        for team, team_dictionary in team_count.items():
            for name, usage in team_dictionary.items():
                if name in manager_count.keys():
                    manager_count.update(
                        {name: [
                            x + y
                            for x, y
                            in zip(manager_count[name], usage)
                        ]}
                    )
                else:
                    manager_count.update({name: usage})

        # Calculate cumulative sums for each manager
        for name, usage in manager_count.items():
            manager_sum_count[name] = [
                sum(usage[: i + 1])
                for i in range(len(usage))
            ]

        return manager_count, manager_sum_count

    def leaguecount(self,
                    manager_count: dict) -> tuple[Dict, Dict]:
        """
        Function Details
        ================
        Count league positions for all completed races and build a dictionary.

        Parameters
        ----------
        manager_count: dict
            Output of self._manager_counts.

        Returns
        -------
        league_count, league_sum_count: dict
            League count for position for individual races, sum count for
            season.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        league_count, league_sum_count = {}, {}

        # Loop manager dictionaries in team counts
        for manager, manager_dictionary in manager_count.items():
            for name, usage in manager_dictionary.items():
                if name in league_count.keys():
                    league_count.update(
                        {name: [
                            x + y
                            for x, y
                            in zip(league_count[name], usage)
                        ]}
                    )
                else:
                    league_count.update({name: usage})

        # Calculate cumulative sums for the league
        for name, usage in league_count.items():
            league_sum_count[name] = [
                sum(usage[: i + 1])
                for i in range(len(usage))
            ]

        return league_count, league_sum_count

    def get_positions(self) -> list:
        """
        Function Details
        ================
        Build a list of team positions to count based on season info dictionary
        list.

        Parameters
        ----------
        None.

        Returns
        -------
        positions: list
            List of team sheet positions to count.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        # Determine positions to count 
        year_positions = self.info_dict["Team"]
        year_perks = self.info_dict["Perks"]
        positions = ["Driver", "Constructor", "Substitutes"]
        [
            positions.append(position)
            for position in year_positions
            if (position.split(' '))[0] not in positions
        ]
        [
            positions.append(position)
            for position in year_perks
            if position == "Extra DRS" or position == "Mega Driver"
        ]
        return positions

    def count_usage(self) -> dict:
        """
        Function Details
        ================
        Count league, manager, and team token uses throughout the season.

        Parameters
        ----------
        None.

        Returns
        -------
        counts: dict
            Count dictionary for all tokens, teams, and managers.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/12/2024
        ----------
        Created.

        """
        # Get positions and managers lists
        positions = self.get_positions()
        managers = self.info_dict["Managers"]

        # Loop positions
        for position in positions:
            logger.info(f'Counting usage for {position}')

            # Set up out dictionaries
            league_team, league_sum_team = {}, {}
            league_manager, league_sum_manager = {}, {}

            # Loop managers
            for manager, teams in managers.items():

                # Set up out dictionaries
                manager_team, manager_sum_team = {}, {}

                # Loop teams
                for team in teams:
                    team_dictionary = load_json(
                        file_path=Path(
                            self.data_path,
                            f'{manager}',
                            f'{team}.json'
                        )
                    )
                    team_count, team_sum_count = self.team_counts(
                        position=position,
                        team_dictionary=team_dictionary
                    )

                    # Add team counts to a manager-wise dictionary
                    manager_team.update({team: team_count})
                    manager_sum_team.update({team: team_sum_count})

                    logger.info(f'{manager} {team} {position} counted')

                # Add team counts to a league-wise dictionary
                league_team.update({manager: manager_team})
                league_sum_team.update({manager: manager_sum_team})

                # Count manager usage
                manager_count, manager_sum_count = self._manager_counts(
                    team_count=manager_team
                )
                logger.info(f'{manager} {position} counted')

                # Add to league-wise dictionary
                league_manager.update({manager: manager_count})
                league_sum_manager.update({manager: manager_sum_count})

            # Count league usage
            league_count, league_sum_count = self.leaguecount(
                manager_count=league_manager
            )

            # Add to counts dictionary
            self.counts.update({f'Teams {position}': league_team})
            self.counts.update({f'Teams Sum {position}': league_sum_team})
            self.counts.update({f'Manager {position}': league_manager})
            self.counts.update({f'Manager Sum {position}': league_sum_manager})
            self.counts.update({f'League {position}': league_count})
            self.counts.update({f'League Sum {position}': league_sum_count})
            logger.info(f'Counts dictionary updated for {position}')

        return self.counts

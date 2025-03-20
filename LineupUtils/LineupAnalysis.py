import os
import logging
import GeneralUtils.DataIO as io
import GeneralUtils.StatisticalAnalysis as sa

from pathlib import Path

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


class LineupProcessor:
    """
    Class Details
    =============
    Class for processing the driver and constructor points and values.

    Attributes
    ----------
    format_path : os.PathLike
        Path to the directory containing format files.
    results_path : os.PathLike
        Path to the directory where lineup results are stored.
    year : str
        The year of the season being processed.
    races : list
        List of race names for the season.
    results_dict : dict
        Dictionary storing driver and constructor points and values.
    stats_dict : dict
        Dictionary initialized empty to store calculated statistics
        such as total points, values, averages, and points-per-value.

    Methods
    -------
    __init__(self, format_path, results_path, year, races)
        Initializes paths, year, race list, and empty results and stats
        dictionaries.
    update_results_dict(self, completed_races)
        Updates results dictionary based on completed races.
    get_constructors_drivers(self)
        Retrieves lists of constructors and drivers from the format files.
    corrects_weekly(self, weekly_dictionary)
        Corrects weekly scorecard based on previous results and inputs.
    update_weeklylineup(self, completed_races, weekly_dictionary)
        Updates results dictionary and saves corrected weekly scorecards.
    update_lineup_stats(self)
        Calculates and updates statistics dictionary based on results
        dictionary.
    _sum_avg_lineup(self, parameter)
        Helper method to calculate total and average points or values.
    _lineup_ppv(self)
        Helper method to calculate points-per-value and average
        points-per-value.

    ---------------------------------------------------------------------------
    Update History
    ==============

    04/11/2024
    ----------
    Created from combined functions.

    """

    def __init__(
            self,
            format_path: os.PathLike,
            results_path: os.PathLike,
            year: str,
            races: list) -> None:
        """
        Function Details
        ================
        Initialize LineupProcessor class.

        Parameters
        ----------
        format_path: os.PathLike
            Path to format directory.
        results_path: os.PathLike
            Path to lineup results.
        year: str
            Year for which to process data.
        races: list
            List of season races.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        04/11/2024
        ----------
        Created.

        """
        self.format_path = Path(format_path, 'Lineup_Formats')
        self.results_path = Path(results_path)
        self.year = f'{year}'
        self.races = races
        self.results_dict = {
            "Driver Points": {},
            "Driver Values": {},
            "Constructor Points": {},
            "Constructor Values": {}
        }
        self.stats_dict = {}
        logger.info('Lineup processor initialized')

    def update_results_dict(self,
                            completed_races: list) -> dict:
        """
        Function Details
        ================

        Parameters
        ----------
        self
        completed_races: list
            List of completed races.

        Returns
        -------
        self.results_dict: dict
            Updated results dictionary from completed races.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/03/2024
        ----------
        Updated documentation and minor function name changes.

        02/03/2024
        ----------
        Updated the updating of the results dict to reset the dictionary when
        it is considering the first race of the completed races. This may need
        altering once the other races come in because it might be that it needs
        to append.

        15/03/2024
        ----------
        Issue where ((results_dict["Driver Points"])[key])[i] = values[0] was
        returning a list index out of range issue. Think this is due to the
        array refreshing with every run of a new race. Have fixed to append.

        03/11/2024
        ----------
        Tidy up of function, no change to functionality.

        04/11/2024
        ----------
        Integration into class method.

        """
        constructors, drivers = self.get_constructors_drivers()
        for i, race in enumerate(completed_races):
            race_results = io.load_json(
                file_path=Path(self.results_path, f'{race}_Results.json')
            )
            for key, values in race_results.items():
                if key == 'Name' or key == 'Race':
                    continue
                if key in drivers or key in constructors:
                    points_key = (
                        "Driver Points" if key in drivers
                        else "Constructor Points"
                    )
                    values_key = (
                        "Driver Values" if key in drivers
                        else "Constructor Values"
                    )
                    if key not in self.results_dict[points_key]:
                        self.results_dict[points_key][key] = (
                            [0] * i + [values[0]]
                        )
                        self.results_dict[values_key][key] = (
                            [values[1]] * i + [values[1]]
                        )
                        logger.info(f'New driver/constructor added: {key}')
                    else:
                        self.results_dict[points_key][key].append(values[0])
                        self.results_dict[values_key][key].append(values[1])
        logger.info('Lineup results dictionary updated')
        return self.results_dict

    def get_constructors_drivers(self) -> list:
        """
        Function Details
        ================

        Parameters
        ----------
        self

        Returns
        -------
        constructors, drivers: list
            List of current constructors and drivers.

        -----------------------------------------------------------------------
        Update History
        ==============

        03/11/2024
        ----------
        Branched from another function.

        04/11/2024
        ----------
        Integration into class method.

        """
        constructors, drivers = [], []
        for file in os.listdir(self.format_path):
            if 'Perks.json' not in file:
                data = io.load_json(file_path=Path(self.format_path, file))
                if self.year in data:
                    constructors.append(Path(file).stem)
                    drivers.extend(data[self.year]['drivers'])
        return constructors, drivers

    def corrects_weekly(self,
                        weekly_dictionary: dict) -> dict:
        """
        Function Details
        ================
        Corrects weekly scorecard based on previous results and inputs.

        Parameters
        ----------
        self
        weekly_dictionary: dict
            Weekly scorecard dictionary.

        Returns
        -------
        individual_points_dict: dict
            Dictionary with updated points and values for the current race.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/03/2024
        ----------
        Created.

        04/11/2024
        ----------
        Refactored.

        29/11/2024
        ----------
        Updated sprint points inactive value. If driver inactive for sprint
        weekend, they miss race, qualifying, and sprint race with a -20, -5,
        and -20 points tally. Not sure why no negative for sprint qualifying.

        """
        race = weekly_dictionary['Race'][0]
        individual_points_dict = {}

        if not race:
            logger.error('Race name is missing in weekly dictionary')
            return individual_points_dict

        try:
            race_index = self.races.index(race)
        except ValueError:
            logger.error(f'{race} is not in races')
            return individual_points_dict

        logger.info(f'Processing weekly scores for {race}')

        for key, inputs in weekly_dictionary.items():
            if key in {'Name', 'Race'}:
                individual_points_dict.update({key: inputs})
                continue

            if race_index == 0:
                individual_points_dict.update({key: inputs})

            else:
                previous_results = {
                    **self.results_dict["Driver Points"],
                    **self.results_dict["Constructor Points"]
                }
                if inputs[0] == 'N/A':
                    new_points, new_values = 0, 0
                elif inputs[0] == 'Inactive':
                    new_points, new_values = -25, inputs[1]
                elif inputs[0] == 'Inactive Sprint':
                    new_points, new_values = -25, inputs[1]
                else:
                    previous_points = previous_results[key]
                    new_points = inputs[0] - sum(previous_points)
                    new_values = inputs[1]

                individual_points_dict[key] = [new_points, new_values]

        logger.info(f'{race} points corrected')
        return individual_points_dict

    def update_weeklylineup(self,
                            completed_races: list,
                            weekly_dictionary: dict) -> dict:
        """
        Function Details
        ================
        Update lineup results based on weekly score cards.

        Parameters
        ----------
        completed_races: list
            List of completed races.
        weekly_dictionary: dict
            Weekly score card dictionary.

        Returns
        -------
        self.results_dict: dict
            Updated results dictionary accounting for the up-to-date score
            cards.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/03/2024
        ----------
        Updated documentation.

        04/11/2024
        ----------
        Refactored.

        """

        # Update lineup results directory based on weekly score sheets
        self.update_results_dict(completed_races=completed_races)

        # Correct weekly lineup scores
        corrected_weekly_lineup = self.corrects_weekly(
            weekly_dictionary=weekly_dictionary)

        # Check if corrected weekly lineup is already a file
        race = corrected_weekly_lineup['Race'][0]
        out_path = Path(self.results_path, f'{race}_Results.json')

        if out_path.is_file():
            logger.info(f'{out_path} is file, results not saved')
        else:
            io.save_json_dicts(
                out_path=out_path,
                dictionary=corrected_weekly_lineup
            )
            logger.info(f'{out_path} saved')

            # Refresh the results dictionary in case new data added
            completed_races.append(race)
            self.update_results_dict(completed_races=completed_races)

        # Save the full results dictionary
        results_out_path = Path(self.results_path, 'Results.json')
        io.save_json_dicts(
            out_path=results_out_path,
            dictionary=self.results_dict
        )
        logger.info('Results dictionary updated')

        return self.results_dict

    def update_lineup_stats(self) -> dict:
        """
        Function Details
        ================
        Calculate driver/constructor statistics from the results dictionary,
        including driver/constructor total points, total values, average
        points, average values, points per value, and average points per value.

        Parameters
        ----------

        Returns
        -------
        stats_dict: dict
            Lineup statistics dictionary.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/03/2024
        ----------
        Documentation update and minor function changes.

        05/11/2024
        ----------
        Incorporation into class method.

        """
        logger.info('Building lineup statistics dictionary')

        points_stats = self._sum_avg_lineup(parameter='Points')
        values_stats = self._sum_avg_lineup(parameter='Values')
        ppv_stats = self._lineup_ppv()
        percentages = self._percentage_lineup()

        self.stats_dict.update(points_stats)
        self.stats_dict.update(values_stats)
        self.stats_dict.update(ppv_stats)
        self.stats_dict.update(percentages)

        points_const = self._consistency_lineup(
            parameter='Points',
            dictionary=self.results_dict
        )
        values_const = self._consistency_lineup(
            parameter='Values',
            dictionary=self.results_dict
        )
        ppvs_const = self._consistency_lineup(
            parameter='Points Per Value',
            dictionary=self.stats_dict
        )

        self.stats_dict.update(points_const)
        self.stats_dict.update(values_const)
        self.stats_dict.update(ppvs_const)

        logger.info('Lineup statistics dictionary complete')

        return self.stats_dict

    def _sum_avg_lineup(self,
                        parameter: str) -> dict:
        """
        Function Details
        ================
        Calculate the total (sum) and average points/values from weekly scores.

        Parameters
        ----------
        parameter: str
            Points or values.

        Returns
        -------
        sum_lineup: dict
            Sum and average points/values dictionary.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/03/2024
        ----------
        Documentation update.

        05/11/2024
        ----------
        Integration into class method.

        """
        categories = ['Driver', 'Constructor']
        self.sum_lineup = {}
        for category in categories:
            logger.info(f'Logging sum and average {parameter} for {category}s')
            category_sum, category_avg = {}, {}
            category_data = self.results_dict[f'{category} {parameter}']
            for key, all_entries in category_data.items():
                entries = sa.cumulative_array(array=all_entries)
                avg_entries = sa.rolling_average_array(array=entries)
                category_sum[key], category_avg[key] = entries, avg_entries
            self.sum_lineup[f'{category} Sum {parameter}'] = category_sum
            self.sum_lineup[f'{category} Average {parameter}'] = category_avg
        logger.info(f'Logged sum and average {parameter}')
        return self.sum_lineup

    def _lineup_ppv(self) -> dict:
        """
        Function Details
        ================
        Calculate points per value and average points per value for each race.

        Parameters
        ----------
        self

        Returns
        -------
        ppv: dict
            Lineup points per value (ppv) dictionary.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/03/2024
        ----------
        Documentation update.

        03/03/2024
        ----------
        Changed points per value to count entered race points and values due to
        new processing techniques.

        06/11/2024
        ----------
        Integration into class method.

        """
        categories = ['Driver', 'Constructor']
        self.ppv = {}
        for category in categories:
            logger.info(f'Logging points per value for {category}s')
            category_points = self.results_dict[f'{category} Points']
            category_values = self.results_dict[f'{category} Values']
            cat_ppv, cat_avg_ppv, cat_sum_ppv = {}, {}, {}
            for key in category_points:
                points, values = category_points[key], category_values[key]
                ppv_array = sa.calc_efficiency(
                    points=points,
                    values=values
                )
                cumulative_points = sa.cumulative_array(array=points)
                cumulative_values = sa.cumulative_array(array=values)
                avg_ppv_array = sa.calc_efficiency(
                    points=cumulative_points,
                    values=cumulative_values
                )
                sum_ppv_array = sa.cumulative_array(array=ppv_array)
                cat_ppv[key], cat_avg_ppv[key], cat_sum_ppv[key] = (
                    ppv_array, avg_ppv_array, sum_ppv_array
                )
            self.ppv[f'{category} Points Per Value'] = cat_ppv
            self.ppv[f'{category} Average Points Per Value'] = cat_avg_ppv
            self.ppv[f'{category} Sum Points Per Value'] = cat_sum_ppv
        logger.info('Points per value and averages logged')
        return self.ppv

    def _consistency_lineup(self,
                            parameter: str,
                            dictionary: dict) -> dict:
        """
        Function Details
        ================
        Calculate the standard deviation and coefficient of variation from
        weekly scores.

        Parameters
        ----------
        parameter: str
            Points, values, ppv.
        dictionary: dict
            Dictionary for which parameter is a key.

        Returns
        -------
        consistency: dict
            Standard deviation and coefficient of variation dictionary.

        -----------------------------------------------------------------------
        Update History
        ==============

        07/11/2024
        ----------
        Created.

        """
        categories = ['Driver', 'Constructor']
        self.const_lineup = {}
        for category in categories:
            logger.info(f'Logging {parameter} consistency for {category}s')
            category_std, category_cv = {}, {}
            category_data = dictionary[f'{category} {parameter}']
            for key, all_entries in category_data.items():
                std, cv = sa.calculate_std_variation(array=all_entries)
                category_std[key], category_cv[key] = std, cv
            self.const_lineup[f'{category} Std Dev {parameter}'] = category_std
            self.const_lineup[f'{category} CV {parameter}'] = category_cv
        logger.info(f'Logged {parameter} consistency')
        return self.const_lineup

    def _percentage_lineup(self) -> dict:
        """
        Function Details
        ================
        Calculate percentage of positive and negative race scores from weekly
        scores.

        Parameters
        ----------
        self

        Returns
        -------
        percentage_lineup: dict
            Positive and negative percentages dictionary.

        -----------------------------------------------------------------------
        Update History
        ==============

        07/11/2024
        ----------
        Created.

        """
        categories = ['Driver', 'Constructor']
        self.percentage_lineup = {}
        for category in categories:
            logger.info(
                f'Logging positive and negative percentages for {category}s')
            cat_pos, cat_neg = {}, {}
            category_points = self.results_dict[f'{category} Points']
            for key, all_entries in category_points.items():
                pos, neg = sa.score_percentage(array=all_entries)
                cat_pos[key], cat_neg[key] = pos, neg
            self.percentage_lineup[f'{category} Positive Percentage'] = cat_pos
            self.percentage_lineup[f'{category} Negative Percentage'] = cat_neg
        logger.info('Logged positive and negative percentages')
        return self.percentage_lineup

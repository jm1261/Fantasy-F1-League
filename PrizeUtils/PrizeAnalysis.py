import logging

from pathlib import Path
from itertools import accumulate, islice

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


class PrizeProcessor:
    """
    Class Details
    =============
    Prize calculator method.

    Attributes
    ----------
    info_dict: dict
    prizes_dictionary: dict
    results_dictionary: dict
    statistics_dictionary: dict
    counts_dictionary: dict
    completed_races: list

    Methods
    -------
    __init__
    call_prizes
    _aggregate_dicts_values
    _max_dict_value
    _min_dict_value
    _spot_prizes
    _sum_nesteddict
    _shortseason_result
    _finds_max_dict
    _finds_max_nestdict
    _custom_prizes
    _championship_prizes
    _highest_weekly
    _lowest_weekly
    _highest_value
    _manager_of_the_year
    _substitutions
    _achievements_prizes

    ---------------------------------------------------------------------------
    Update History
    ==============

    17/12/2024
    ----------
    Created.

    """

    def __init__(
            self,
            info_dictionary: dict,
            prizes_dictionary: dict,
            manager_results: dict,
            manager_statistics: dict,
            manager_counts: dict,
            completed_races: list) -> None:
        """
        Function Details
        ================
        Initialize prize processor method.

        Parameters
        ----------
        info_dictionary, prizes_dictionary: dict
            Season info dictionary, season prizes dictionary.
        manager_results, manager_statistics, manager_counts: dict
            Manager results, statistics, and counts dictionaries.
        completed_races: list
            List of completed_races.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        self.info_dict = info_dictionary
        self.prizes_dictionary = prizes_dictionary
        self.results_dictionary = manager_results
        self.statistics_dictionary = manager_statistics
        self.counts_dictionary = manager_counts
        self.completed_races = completed_races
        logger.info('Prize processor initialized')

    def call_prizes(self,
                    prize: str) -> dict:
        """
        Function Details
        ================
        Helper method to handle common logic for determining prizes.

        Parameters
        ----------
        prize: str
            Identifier string for function calling.

        Returns
        -------
        winners_dict: dict
            Winner dictionary, output from separate functions.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        function_map = {
            "Spot": self._spot_prizes,
            "Custom Set": self._custom_prizes,
            "Championship": self._championship_prizes,
            "Achievements": self._achievements_prizes
        }
        if prize in function_map:
            winners_dict = function_map[f'{prize}']()
            logger.info(f'{prize} results calculated')
        else:
            winners_dict = {}
            logger.error(f'No function mapped for {prize}')
        return winners_dict

    def _aggregate_dicts_values(self,
                                results_dictionary: dict,
                                races: list,
                                aggregation_func: callable) -> tuple:
        """
        Function Details
        ================
        Generalized method to find aggregated values (max or min) in a
        dictionary.

        Parameters
        ----------
        results_dictionary: dict
            Nested dictionary containing team points.
        races: list
            List of races to process.
        aggregation_func: callable
            Function to aggregate values (e.g. max or min)

        Returns
        -------
        aggregate_value: list
            Aggregates values for each race in 'races' that is in 'completed
            races'. Each entry is a tuple: (race, manager, team, value).
        ties: list
            List of ties for each race in 'races'. Each entry is a list of
            tuples: (race, manager, team, value).

        -----------------------------------------------------------------------
        Update History
        ==============

        27/03/2024
        ----------
        Old max/min functions.

        17/12/2024
        ----------
        Created from old functions and merged into class method.

        """
        logger.info(f'Logging {aggregation_func} values for {races}')

        # Precompute the race index mapping
        race_index_map = {
            race: idx
            for idx, race in enumerate(self.completed_races)
        }

        aggregate_value, ties = [], []

        for race in races:
            if race not in self.completed_races:
                logger.info(f'{race} not yet completed')
                continue

            race_index = race_index_map[race]

            # Collect race data
            race_data = [
                (race, manager, team, values[race_index])
                for manager, teams in results_dictionary.items()
                for team, values in teams.items()
            ]

            # Find the aggregated entry
            aggregate_entry = aggregation_func(race_data, key=lambda x: x[3])
            aggregate_value.append(aggregate_entry)

            # Find ties excluding the aggregate entry
            race_ties = [
                entry
                for entry in race_data
                if entry[3] == aggregate_entry[3]
                and (entry[1], entry[2])
                != (aggregate_entry[1], aggregate_entry[2])
            ]
            ties.append(race_ties)

        return aggregate_value, ties

    def _max_dict_value(self,
                        results_dictionary: dict,
                        races: list) -> tuple:
        """
        Function Details
        ================
        Find the maximum value in a dictionary at a given index.

        Parameters
        ----------
        results_dictionary: dict
            Nested dictionary containing team points.
        races: list
            List of races to process.

        Returns
        -------
        aggregate_value: list
            Aggregated values for each race in 'races' that is in 'completed
            races'. Each entry is a tuple: (race, manager, team, value).
        ties: list
            List of ties for each race in 'races'. Each entry is a list of
            tuples: (race, manager, team, value).

        -----------------------------------------------------------------------
        Update History
        ==============

        27/03/2024
        ----------
        Created.

        17/12/2024
        ----------
        Trimmed and merged into class method.

        """
        return self._aggregate_dicts_values(
            results_dictionary=results_dictionary,
            races=races,
            aggregation_func=max)

    def _min_dict_value(self,
                        results_dictionary: dict,
                        races: list) -> tuple:
        """
        Function Details
        ================
        Find the maximum value in a dictionary at a given index.

        Parameters
        ----------
        results_dictionary: dict
            Nested dictionary containing team points.
        races: list
            List of races to process.

        Returns
        -------
        aggregate_value: list
            Aggregated values for each race in 'races' that is in 'completed
            races'. Each entry is a tuple: (race, manager, team, value).
        ties: list
            List of ties for each race in 'races'. Each entry is a list of
            tuples: (race, manager, team, value).

        -----------------------------------------------------------------------
        Update History
        ==============

        27/03/2024
        ----------
        Created.

        17/12/2024
        ----------
        Trimmed and merged into class method.

        """
        return self._aggregate_dicts_values(
            results_dictionary=results_dictionary,
            races=races,
            aggregation_func=min)

    def _spot_prizes(self) -> dict:
        """
        Function Details
        ================
        Find the spot prize winners for min/max race results at specific races.
        Called only if "Spot" is a key in the prizes dictionary.

        Parameters
        ----------
        None.

        Returns
        -------
        spot_prizes: dict
            Dictionary containing the original spot prizes dictionary and the
            new "Winners" entry.

        -----------------------------------------------------------------------
        Update History
        ==============

        27/03/2024
        ----------
        Created.

        17/12/2024
        ----------
        Merged into class method.

        """
        spot_prizes = self.prizes_dictionary["Spot"]
        team_dictionary = self.results_dictionary["Team Points"]
        prize_winners = {}
        max_values, max_ties = self._max_dict_value(
            results_dictionary=team_dictionary,
            races=spot_prizes["Spot Max"]
        )
        min_values, min_ties = self._min_dict_value(
            results_dictionary=team_dictionary,
            races=spot_prizes["Spot Min"]
        )
        for winner in max_values:
            prize_key = (spot_prizes["Spot Names"])[f'{winner[0]}']
            prize_winners.update({f'{prize_key}': winner})
        for winner in min_values:
            prize_key = (spot_prizes["Spot Names"])[f'{winner[0]}']
            prize_winners.update({f'{prize_key}': winner})
        prize_winners.update({"Max Ties": max_ties})
        prize_winners.update({"Min Ties": min_ties})
        spot_prizes.update({"Spot Winners": prize_winners})
        return spot_prizes

    def _sum_nesteddict(self,
                        dictionary: dict,
                        item: str) -> dict:
        """
        Function Details
        ================
        Calculate the cumulative sum and average points for a nested dictionary
        containing a key, dict, second key, array data structure.

        Parameters
        ----------
        dictionary: dict
            Nested dictionary.
        item: str
            String to identify the sum and average values in the output.

        Returns
        -------
        dict
            {'Sum {item}': sum_dict, 'Average {item}': average_dict}

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        sum_dict, average_dict = {}, {}

        for key, values in dictionary.items():
            key_sum, key_average = {}, {}

            for second_key, all_values in values.items():

                # Cumulative sum using itertools.accumulate
                cumulative_sum = list(accumulate(all_values))

                # Average points calculation
                cumulative_avg = [
                    round(cumulative_sum[i] / (i + 1), 2)
                    for i in range(len(cumulative_sum))
                ]

                key_sum[second_key] = cumulative_sum
                key_average[second_key] = cumulative_avg

            sum_dict[key] = key_sum
            average_dict[key] = key_average

        return {
            f'Sum {item}': sum_dict,
            f'Average {item}': average_dict
        }

    def _shortseason_result(self,
                            results: dict,
                            specific_races: list) -> dict:
        """
        Function Details
        ================
        Calculate results over a subset of races, such as sprints or grouped
        races.

        Parameters
        ----------
        results: dict
            Manager/team results dictionary, e.g., {manager: {team: [points, 
            list]}}.
        specific_races: list
            Subset of races to consider in the results.

        Returns
        -------
        results_dict: dict
            Aggregated results dictionary, e.g., {"Sum Points": ..., "Average
            Points": ...}.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        points_dict = {}
        for manager, teams in results.items():
            manager_dict = {}
            for team, points in teams.items():
                # Extract points for specific races
                race_points = [
                    points[self.completed_races.index(race)]
                    for race in specific_races
                    if race in self.completed_races
                ]
                manager_dict[team] = race_points
            points_dict[manager] = manager_dict

        # Summing and averaging points
        results_dict = self._sum_nesteddict(
            dictionary=points_dict,
            item='Points'
        )
        return results_dict

    def _finds_max_dict(self,
                        dictionary: dict) -> dict:
        """
        Function Details
        ================
        Finds maximum value in a dictionary.

        Parameters
        ----------
        dictionary: dict
            Dictionary, e.g., {primary: list}.

        Returns
        -------
        find_max: dict
            Dictionary containing {primary: max(list)} data structure.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Updated from old software.

        """
        find_max, names, values = {}, [], []
        for primary, dict_values in dictionary.items():
            names.append(primary)
            values.append(dict_values[-1])
        tuples = zip(*sorted(zip(values, names)))
        all_values, all_names = [list(tuple) for tuple in tuples]
        names_orders = all_names[::-1]
        values_orders = all_values[::-1]
        for name, value in zip(names_orders, values_orders):
            find_max.update({f'{name}': value})
        return find_max

    def _finds_max_nestdict(self,
                            dictionary: dict) -> dict:
        """
        Function Details
        ================
        Find maximum value in a nested dictionary.

        Parameters
        ----------
        dictionary: dict
            Nested dictionary, e.g., {primary: {key: list}}.

        Returns
        -------
        find_max: dict
            Dictionary containing {primary: max(list)} data structure.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Updated from old software.

        """
        find_max, names, values = {}, [], []
        for primary, dicts in dictionary.items():
            for secondary, dict_values in dicts.items():
                names.append(secondary)
                values.append(dict_values[-1])
        tuples = zip(*sorted(zip(values, names)))
        all_values, all_names = [list(tuple) for tuple in tuples]
        names_orders = all_names[::-1]
        values_orders = all_values[::-1]
        for name, value in zip(names_orders, values_orders):
            find_max.update({f'{name}': value})
        return find_max

    def _custom_prizes(self) -> dict:
        """
        Function Details
        ================
        Find the custom prizes winners for prizes for a subset of races.

        Parameters
        ----------
        None.

        Returns
        -------
        custom_prizes: dict
            Dictionary containing the original custom prizes dictionary and the
            new "winners" entry.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        custom_prizes = self.prizes_dictionary["Custom Set"]
        team_dictionary = self.results_dictionary["Team Points"]
        prize_winners = {}
        categories = custom_prizes["Custom Set Names"].keys()
        for category in categories:
            category_races = custom_prizes[f'{category} Races']
            exists = any(
                race in category_races
                for race in self.completed_races
            )
            if exists:
                prize_name = (custom_prizes["Custom Set Names"])[f'{category}']
                category_dict = self._shortseason_result(
                    results=team_dictionary,
                    specific_races=category_races
                )
                sum_prize_dict = self._finds_max_nestdict(
                    dictionary=category_dict["Sum Points"]
                )
                avg_prize_dict = self._finds_max_nestdict(
                    dictionary=category_dict["Average Points"]
                )
                prize_winners.update(
                    {f'{prize_name} Sum Points': sum_prize_dict}
                )
                prize_winners.update(
                    {f'{prize_name} Average Points': avg_prize_dict}
                )
            custom_prizes.update({"Custom Winners": prize_winners})
        return custom_prizes

    def _championship_prizes(self) -> dict:
        """
        Function Details
        ================
        Find the championship prize winners for prizes for the final finishing
        positions.

        Parameters
        ----------
        None.

        Returns
        -------
        championship_prizes: dict
            Dictionary containing the original championship prizes dictionary
            and the new "winners" entry.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        championship_prizes = self.prizes_dictionary["Championship"]
        team_dictionary = self.statistics_dictionary["Team Sum Points"]
        prizes = championship_prizes["Championship Names"]
        prize_positions = prizes.keys()
        total_scores = self._finds_max_nestdict(dictionary=team_dictionary)
        team_names = [key for key, value in total_scores.items()]
        prize_winners = {}
        for position in prize_positions:
            prize_name = prizes[f'{position}']
            team_name = team_names[int(position)]
            team_score = total_scores[f'{team_name}']
            prize_winners.update({prize_name: [team_name, team_score]})
        championship_prizes.update({"Championship Winners": prize_winners})
        return championship_prizes

    def _highest_weekly(self):
        """
        Function Details
        ================
        Finds the highest weekly scores throughout the season for manager team.

        Parameters
        ----------
        None.

        Returns
        -------
        dict
            Dictionary containing the maximum score and any ties.

        -----------------------------------------------------------------------
        Update History
        ==============

        19/03/2024
        ----------
        Created.

        17/12/2024
        ----------
        Split into higher/lower and merged with class method.
        """
        score = ['race', 'manager', 'team', -100000]
        ties = []
        for manager, teams in self.results_dictionary["Team Points"].items():
            for team, points in teams.items():
                for points, race in zip(points, self.completed_races):
                    if points > score[3]:
                        score = [f'{race}', f'{manager}', f'{team}', points]
                    elif points == score[3]:
                        ties.append(
                            [f'{race}', f'{manager}', f'{team}', points]
                        )
                    else:
                        pass
        return {
            'Max Score': score,
            'Ties': ties
        }

    def _lowest_weekly(self):
        """
        Function Details
        ================
        Finds the lowest weekly scores throughout the season for manager team.

        Parameters
        ----------
        None.

        Returns
        -------
        dict
            Dictionary containing the minimum score and any ties.

        -----------------------------------------------------------------------
        Update History
        ==============

        19/03/2024
        ----------
        Created.

        17/12/2024
        ----------
        Split into higher/lower and merged with class method.
        """
        score = ['race', 'manager', 'team', 100000]
        ties = []
        for manager, teams in self.results_dictionary["Team Points"].items():
            for team, points in teams.items():
                for points, race in zip(points, self.completed_races):
                    if points < score[3]:
                        score = [f'{race}', f'{manager}', f'{team}', points]
                    elif points == score[3]:
                        ties.append(
                            [f'{race}', f'{manager}', f'{team}', points]
                        )
                    else:
                        pass
        return {
            'Min Score': score,
            'Ties': ties
        }

    def _highest_value(self) -> dict:
        """
        Function Details
        ================
        Find the highest value team at the end of the season.

        Parameters
        ----------
        None.

        Returns
        -------
        highest_value: dict
            Dictionary containing the top three highest value teams at the
            final race.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        max_value = self._finds_max_nestdict(
            dictionary=self.results_dictionary["Team Values"]
        )
        highest_value = dict(islice(max_value.items(), 3))
        return highest_value

    def _manager_of_the_year(self) -> dict:
        """
        Function Details
        ================
        Find the highest average score for a manager with at least 3 teams.

        Parameters
        ----------
        None.

        Returns
        -------
        highest_average: dict
            Top three highest averages scores for managers with 3 teams.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        all_average_points = self._finds_max_dict(
            dictionary=self.statistics_dictionary["Manager Sum Average Points"]
        )
        managers = self.info_dict['Managers']
        number_teams = {
            manager: len(teams)
            for manager, teams
            in managers.items()
        }
        highest_averages = {}
        for manager, score in all_average_points.items():
            if number_teams[manager] == 3:
                highest_averages.update({manager: score})
            else:
                pass
        highest_average = dict(islice(highest_averages.items(), 3))
        return highest_average

    def _substitutions(self) -> dict:
        """
        Function Details
        ================
        Find the team with the most substitutes throughout a season, as long
        as the team doesn't have more than 5 penalties (< -60).

        Parameters
        ----------
        None.

        Returns
        -------
        most_substitutes: dict
            Dictionary containing top three teams with highest substitutes with
            less than 5 penalties.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        # Count substitutes
        team_sum_sub_counts = {}
        team_subs = self.counts_dictionary["Teams Sum Substitutes"]
        for manager, teams in team_subs.items():
            if manager not in team_sum_sub_counts:
                team_sum_sub_counts[manager] = {}
            for team, substitutes in teams.items():
                for key, subs in substitutes.items():
                    team_sum_sub_counts[manager][team] = subs
        max_substitutes = self._finds_max_nestdict(
            dictionary=team_sum_sub_counts
        )

        # Count penalties
        team_sum_pen_counts = {}
        team_subs = self.counts_dictionary["Teams Sum Penalties"]
        for manager, teams in team_subs.items():
            if manager not in team_sum_pen_counts:
                team_sum_pen_counts[manager] = {}
            for team, penalties in teams.items():
                for key, pens in penalties.items():
                    team_sum_pen_counts[manager][team] = pens
        max_penalties = self._finds_max_nestdict(
            dictionary=team_sum_pen_counts
        )

        # Append subs to new dictionary if penalties claus not broken
        most_subs = {}
        for manager, substitutes in max_substitutes.items():
            penalties = max_penalties[manager]
            if penalties < -60:
                pass
            else:
                most_subs.update({manager: substitutes})

        # Trim
        most_substitutes = dict(islice(most_subs.items(), 3))

        return most_substitutes

    def _achievements_prizes(self) -> dict:
        """
        Function Details
        ================
        Find the achievement prize winners for prizes for the season goals.

        Parameters
        ----------
        None.

        Returns
        -------
        achievement_prizes: dict
            Dictionary containing the original achievements prizes dictionary
            and the new "winners" entry.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        achievement_prizes = self.prizes_dictionary["Achievements"]
        prizes = achievement_prizes["Achievement Names"]

        function_map = {
            "Highest Weekly": self._highest_weekly,
            "Lowest Weekly": self._lowest_weekly,
            "Highest Value": self._highest_value,
            "Manager of the Year": self._manager_of_the_year,
            "Substitutions": self._substitutions
        }

        prize_winners = {}
        for prize in prizes:
            if prize in function_map:
                out_dict = function_map[f'{prize}']()
                prize_winners.update({prizes[f'{prize}']: out_dict})
                logger.info(f'Logged prize for {prize}')
            else:
                logger.error(f'No function mapped for {prize}')

        achievement_prizes.update({"Achievement Winners": prize_winners})
        return achievement_prizes

    def _process_prizes(self,
                        categories: list) -> dict:
        """
        Function Details
        ================
        Loop through prizes dictionary, calculate winners, return dictionary.

        Parameters
        ----------
        categories: list
            List of prize categories, e.g., "Spot", "Championship".

        Returns
        -------
        prizes_dictionary: dict
            Prizes dictionary updated with winners.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/12/2024
        ----------
        Created.

        """
        for category in categories:
            winners_dict = self.call_prizes(prize=category)
            self.prizes_dictionary.update({category: winners_dict})
        return self.prizes_dictionary

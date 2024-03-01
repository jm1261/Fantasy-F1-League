import numpy as np

from pathlib import Path
from src.dataIO import load_json, save_json_dicts


def no_perk(category : str,
            driver_names : list,
            constructor_names: list,
            double_names : list,
            driver_results : dict,
            constructor_results : dict,
            penalties : int,
            race_index : int) -> float:
    """
    Function Details
    ================
    Calculates race scores and values if perk is none.

    Parameters
    ----------
    category: str
        Points or Values.
    driver_names, constructor_names, double_names: list
        List of driver names, team names, and DRS/Turbo names for the race week.
    driver_results, constructor_results: dictionary
        Lineup driver and team results dictionaries for points or values.
    penalties, race_index: int
        Team penalties for the race week, race index for the current race.

    Returns
    -------
    total_scores: float
        Total points or values for the race week.

    See Also
    --------
    None

    Notes
    -----
    Simply adds the team points and values when there is no perk.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    28/02/2024
    ----------
    Created.

    """
    driver_scores = [
        (driver_results[name])[race_index] for name in driver_names]
    constructor_scores = [
        (constructor_results[name])[race_index] for name in constructor_names]
    double_scores = [
        (driver_results[name])[race_index] for name in double_names]
    if category == 'Points':
        total_scores = (
            sum(driver_scores) +
            sum(constructor_scores) +
            sum(double_scores) +
            penalties)
    else:
        total_scores = sum(driver_scores) + sum(constructor_scores)
    return total_scores


def triplescore(category : str,
                driver_names : list,
                constructor_names: list,
                double_names : list,
                triple_name: str,
                driver_results : dict,
                constructor_results : dict,
                penalties : int,
                race_index : int) -> float:
    """
    Function Details
    ================
    Calculates race scores and values if perk is Extra DRS or Mega Driver.

    Parameters
    ----------
    category, triple_name: str
        Points or Values. Extra DRS or Mega Driver name.
    driver_names, constructor_names, double_names: list
        List of driver names, team names, and DRS/Turbo names for the race week.
    driver_results, constructor_results: dictionary
        Lineup driver and team results dictionaries for points or values.
    penalties, race_index: int
        Team penalties for the race week, race index for the current race.

    Returns
    -------
    total_scores: float
        Total points or values for the race week.

    See Also
    --------
    None

    Notes
    -----
    Extra DRS or Mega Driver is a perk that triples a driver score. The function
    already adds the driver score, so the function only adds a double score on
    top of that.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    28/02/2024
    ----------
    Created.

    """
    driver_scores = [
        (driver_results[name])[race_index] for name in driver_names]
    constructor_scores = [
        (constructor_results[name])[race_index] for name in constructor_names]
    double_scores = [
        (driver_results[name])[race_index] for name in double_names]
    extra_scores = (driver_results[triple_name])[race_index] * 2
    if category == 'Points':
        total_scores = (
            sum(driver_scores) +
            sum(constructor_scores) +
            sum(double_scores) +
            extra_scores +
            penalties)
    else:
        total_scores = sum(driver_scores) + sum(constructor_scores)
    return total_scores


def perks_limitless(category : str,
                    driver_names : list,
                    constructor_names: list,
                    double_names : list,
                    driver_results : dict,
                    constructor_results : dict,
                    penalties : int,
                    race_index : int) -> float:
    """
    Function Details
    ================
    Calculates race scores and values if perk is limitless.

    Parameters
    ----------
    category: str
        Points or Values.
    driver_names, constructor_names, double_names: list
        List of driver names, team names, and DRS/Turbo names for the race week.
    driver_results, constructor_results: dictionary
        Lineup driver and team results dictionaries for points or values.
    penalties, race_index: int
        Team penalties for the race week, race index for the current race.

    Returns
    -------
    total_scores: float
        Total points or values for the race week.

    See Also
    --------
    None

    Notes
    -----
    Limitless removes the cost cap limitation on a team, allowing for any driver
    or team combination to be used. When the category is values, the function
    defaults to $100M to prevent inflation of the team value.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    28/02/2024
    ----------
    Created.

    """
    driver_scores = [
        (driver_results[name])[race_index] for name in driver_names]
    constructor_scores = [
        (constructor_results[name])[race_index] for name in constructor_names]
    double_scores = [
        (driver_results[name])[race_index] for name in double_names]
    if category == 'Values':
        total_scores = 100.00
    else:
        total_scores = (
            sum(driver_scores) +
            sum(constructor_scores) +
            sum(double_scores) +
            penalties)
    return total_scores


def no_negative(category : str,
                driver_names : list,
                constructor_names: list,
                double_names : list,
                driver_results : dict,
                constructor_results : dict,
                penalties : int,
                race_index : int) -> float:
    """
    Function Details
    ================
    Calculates race scores and values if perk is no negative.

    Parameters
    ----------
    category: str
        Points or Values.
    driver_names, constructor_names, double_names: list
        List of driver names, team names, and DRS/Turbo names for the race week.
    driver_results, constructor_results: dictionary
        Lineup driver and team results dictionaries for points or values.
    penalties, race_index: int
        Team penalties for the race week, race index for the current race.

    Returns
    -------
    total_scores: float
        Total points or values for the race week.

    See Also
    --------
    None

    Notes
    -----
    No negative is a perk that discounts any negative points scored in a race
    week. It does not affect the team values.

    Example
    -------
    >>> team_score = [20, -5, 10, 2, -3]
    >>> no_neg = no_negative(data)
    >>> no neg
    32

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/02/2024
    ----------
    Created

    """
    driver_scores = [
        (driver_results[name])[race_index] for name in driver_names]
    constructor_scores = [
        (constructor_results[name])[race_index] for name in constructor_names]
    double_scores = [
        (driver_results[name])[race_index] for name in double_names]
    if category == 'Points':
        all_points = []
        [all_points.append(x) for x in driver_scores]
        [all_points.append(x) for x in constructor_scores]
        [all_points.append(x) for x in double_scores]
        positive_points = [x for x in all_points if x > 0]
        total_scores = sum(positive_points) + penalties
    else:
        total_scores = sum(driver_scores) + sum(constructor_scores)
    return total_scores


def perks_final_fix(category : str,
                    driver_names : list,
                    constructor_names : list,
                    double_names : list,
                    replaced_names : list,
                    replaced_scores : list,
                    driver_results : dict,
                    constructor_results : dict,
                    penalties : int,
                    race_index : int) -> float:
    """
    Function Details
    ================
    Calculates race scores or values if Final Fix is the perk.

    Parameters
    ----------
    category: str
        Points or Values.
    driver_names, constructor_names, double_names: list
        List of driver names, team names, and DRS/Turbo names for the race week.
    replaced_names, replaced_scores: list
        Replaced driver names and scores for final fix perk in race week.
    driver_results, constructor_results: dictionary
        Lineup driver and team results dictionaries for points or values.
    penalties, race_index: int
        Team penalties for the race week, race index for the current race.

    Returns
    -------
    total_scores: float
        Total points or values for the race week.

    See Also
    --------
    None

    Notes
    -----
    Final fix is a perk that allows the manager to replace a driver or team. The
    perk affects the score of the team members individually and should be
    addressed as individual scores in an array.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/02/2024
    ----------
    Created

    """
    driver_scores = []
    constructor_scores = []
    double_scores = []
    if category == 'Points':
        for name in driver_names:
            if name in replaced_names:
                [driver_scores.append(score) for score in replaced_scores]
            else:
                driver_scores.append((driver_results[name])[race_index])
        for name in constructor_names:
            if name in replaced_names:
                [constructor_scores.append(score) for score in replaced_scores]
            else:
                constructor_scores.append(
                    (constructor_results[name])[race_index])
        for name in double_names:
            if name in replaced_names:
                [double_scores.append(score) for score in replaced_scores]
            else:
                double_scores.append((driver_results[name])[race_index])
        total_scores = (
            sum(driver_scores) +
            sum(constructor_scores) +
            sum(double_scores) +
            penalties)
    else:
        driver_scores = [
            (driver_results[name])[race_index] for name in driver_names]
        constructor_scores = [
            (constructor_results[name])[race_index]
            for name in constructor_names]
        total_scores = sum(driver_scores) + sum(constructor_scores)
    return total_scores


def managers_lineup(lineup_results : dict,
                    info_dictionary : dict,
                    completed_races : list,
                    data_path : str) -> dict:
    """
    Function Details
    ================
    Calculate points and values from manager team sheets.

    Parameters
    ----------
    lineup_results, info_dictionary: dictionary
        Driver/team results for the lineup, season info dictionary.
    completed_races: list
        Races completed so far.
    data_path: string
        Path to data directory.

    Returns
    -------
    results: dictionary
        Dictionary containing manager team points, values, average points, and
        average values.

    See Also
    --------
    perks_final_fix
    no_negative
    perks_limitless
    triplescore
    no_perk
    load_json

    Notes
    -----
    The function uses the lineup results to calculate manager scores, values,
    totals, and averages for each race week.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/02/2024
    ----------
    Split into sub functions for individual perks.

    """
    results = {}
    categories = ['Points', 'Values']
    for category in categories:
        category_results = {}
        category_sums = {}
        category_averages = {}
        driver_results = lineup_results[f'Driver {category}']
        team_results = lineup_results[f'Team {category}']
        for manager, teams in info_dictionary['Managers'].items():
            manager_results = {}
            manager_scores = []
            for team in teams:
                race_scores = []
                team_dictionary = load_json(
                    file_path=Path(f'{data_path}/{manager}/{team}.json'))
                for index, race in enumerate(completed_races):
                    team_sheet = team_dictionary[f'{race}']
                    driver_names = [
                        team_sheet[key]
                        for key in team_sheet.keys()
                        if 'Driver' in key]
                    constructor_names = [
                        team_sheet[key]
                        for key in team_sheet.keys()
                        if 'Constructor' in key or 'Team' in key]
                    double_names = [
                        team_sheet[key]
                        for key in team_sheet.keys()
                        if 'DRS' in key or 'Turbo' in key]
                    perks = team_sheet["Perks"]
                    if "Final Fix" in perks:
                        replaced_names = [
                            (team_sheet["Perks"])[1],
                            (team_sheet["Perks"])[3]]
                        replaced_scores = [
                            (team_sheet["Perks"])[2],
                            (team_sheet["Perks"])[4]]
                        scores = perks_final_fix(
                            category=category,
                            driver_names=driver_names,
                            constructor_names=constructor_names,
                            double_names=double_names,
                            replaced_names=replaced_names,
                            replaced_scores=replaced_scores,
                            driver_results=driver_results,
                            constructor_results=team_results,
                            penalties=team_sheet['Penalties'],
                            race_index=index)
                        race_scores.append(scores)
                    elif "No Negative" in perks:
                        scores = no_negative(
                            category=category,
                            driver_names=driver_names,
                            constructor_names=constructor_names,
                            double_names=double_names,
                            driver_results=driver_results,
                            constructor_results=team_results,
                            penalties=team_sheet['Penalties'],
                            race_index=index)
                        race_scores.append(scores)
                    elif "Limitless" in perks:
                        scores = perks_limitless(
                            category=category,
                            driver_names=driver_names,
                            constructor_names=constructor_names,
                            double_names=double_names,
                            driver_results=driver_results,
                            constructor_results=team_results,
                            penalties=team_sheet['Penalties'],
                            race_index=index)
                        race_scores.append(scores)
                    elif "Extra DRS" in perks or "Mega" in perks:
                        scores = triplescore(
                            category=category,
                            driver_names=driver_names,
                            constructor_names=constructor_names,
                            double_names=double_names,
                            triple_name=perks[1],
                            driver_results=driver_results,
                            constructor_results=team_results,
                            penalties=team_sheet['Penalties'],
                            race_index=index)
                        race_scores.append(scores)
                    else:
                        scores = no_perk(
                            category=category,
                            driver_names=driver_names,
                            constructor_names=constructor_names,
                            double_names=double_names,
                            driver_results=driver_results,
                            constructor_results=team_results,
                            penalties=team_sheet['Penalties'],
                            race_index=index)
                        race_scores.append(scores)
                manager_scores.append(race_scores)
                manager_results.update({team: race_scores})
            manager_sum = [sum(i) for i in zip(*manager_scores)]
            manager_average = [
                sum(i) / len(manager_scores)
                for i in zip(*manager_scores)]
            category_results.update({manager: manager_results})
            category_sums.update({manager: manager_sum})
            category_averages.update({manager: manager_average})
        results.update({f'Team {category}': category_results})
        results.update({f'Manager {category}': category_sums})
        results.update({f'Manager Average {category}': category_averages})
    return results


def sum_manager_results(results_dictionary : dict) -> dict:
    """
    Function Details
    ================
    Calculate manager and team points, values, average points, and average
    values.

    Parameters
    ----------
    results_dictionary: dictionary
        Manager results dictionary.

    Returns
    -------
    sum_entries: dictionary
        Each category added cumulatively.

    See Also
    --------
    None

    Notes
    -----
    Adds the cumulative results for points, values, average points, and average
    values for managers and individual manager teams. Pulls in the individual
    team data and adds cumulatively, while adding each of those results to a
    manager dictionary for summation.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    28/02/2024
    ----------
    Copied from old code. Documentation updated to current coding practices.

    """
    categories = ['Points', 'Values', 'Average Points', 'Average Values']
    sum_entries = {}
    for category in categories:
        category_manager_dict = results_dictionary[f'Manager {category}']
        teams_sum = {}
        managers_sum = {}
        for manager, values in category_manager_dict.items():
            manager_teams_sum = {}
            manager_sum = []
            for index, value in enumerate(values):
                if index == 0:
                    manager_sum.append(value)
                else:
                    manager_sum.append(value + manager_sum[index - 1])
            managers_sum.update({manager: manager_sum})
            if category == 'Average Points' or category == 'Average Values':
                pass
            else:
                category_team_dict = (
                    results_dictionary[f'Team {category}'])[f'{manager}']
                for team, entries in category_team_dict.items():
                    team_sum = []
                    for index, entry in enumerate(entries):
                        if index == 0:
                            team_sum.append(entry)
                        else:
                            team_sum.append(entry + team_sum[index - 1])
                    manager_teams_sum.update({team: team_sum})
                teams_sum.update({manager: manager_teams_sum})
        if category == 'Average Points' or category == 'Average Values':
                pass
        else:
            sum_entries.update({f'Team Sum {category}': teams_sum})
        sum_entries.update({f'Manager Sum {category}': managers_sum})
    return sum_entries


def manager_points_per_value(results_dictionary : dict) -> dict:
    """
    Function Details
    ================
    Calculates race-wise and season-average manager and team points per value.

    Parameters
    ----------
    results_dictionary: dictionary
        Manager results dictionary.

    Returns
    -------
    ppvs: dictionary
        Manager and team points per value.

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

    28/02/2024
    ----------
    Copied from old code. Documentation updated to current coding practices.

    """
    manager_ppvs = {}
    manager_avg_ppvs = {}
    managers = (results_dictionary['Manager Points']).keys()
    manager_teams_ppvs = {}
    manager_teams_avg_ppvs = {}
    for manager in managers:
        manager_points = (results_dictionary['Manager Points'])[f'{manager}']
        manager_values = (results_dictionary['Manager Values'])[f'{manager}']
        manager_ppv = [p / v for p, v in zip(manager_points, manager_values)]
        manager_avg_ppv = []
        for index, value in enumerate(manager_ppv):
            if index == 0:
                manager_avg_ppv.append(value)
            else:
                manager_avg_ppv.append(
                    sum(manager_ppv[0: index + 1]) / (index + 1))
        manager_ppvs.update({manager: manager_ppv})
        manager_avg_ppvs.update({manager: manager_avg_ppv})
        team_points_dict = (results_dictionary['Team Points'])[f'{manager}']
        team_values_dict = (results_dictionary['Team Values'])[f'{manager}']
        teams_ppvs = {}
        teams_avg_ppvs = {}
        for team, entries in team_points_dict.items():
            values = team_values_dict[team]
            team_ppv = []
            team_avg_ppv = []
            for index, entry in enumerate(entries):
                ppv = entry / values[index]
                team_ppv.append(ppv)
                if index == 0:
                    team_avg_ppv.append(ppv)
                else:
                    team_avg_ppv.append(
                        sum(team_ppv[0: index + 1]) / (index + 1))
            teams_ppvs.update({team: team_ppv})
            teams_avg_ppvs.update({team: team_avg_ppv})
        manager_teams_ppvs.update({manager: teams_ppvs})
        manager_teams_avg_ppvs.update({manager: teams_avg_ppvs})
    ppvs = {}
    ppvs.update({'Manager Points Per Value': manager_ppvs})
    ppvs.update({'Manager Average Points Per Value': manager_avg_ppvs})
    ppvs.update({'Team Points Per Value': manager_teams_ppvs})
    ppvs.update({'Team Average Points Per Value': manager_teams_avg_ppvs})
    return ppvs


def manager_statistics(results_dictionary : dict) -> dict:
    """
    Function Details
    ================
    Calculate manager and team statistics.

    Parameters
    ----------
    results_dictionary: dictionary
        Manager/team results dictionary.

    Returns
    -------
    stats_dictionary: dictionary
        Manager/team statistics dictionary containing team and manager total
        points, average points, average values, and points per value.

    See Also
    --------
    sum_manager_results
    manager_points_per_value

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    28/02/2024
    ----------
    Brought across from old code.

    """
    sum_stats = sum_manager_results(results_dictionary=results_dictionary)
    ppvs = manager_points_per_value(results_dictionary=results_dictionary)
    stats_dictionary = dict(
        sum_stats,
        **ppvs)
    return stats_dictionary


def teams_count(completed_races : list,
                team_dictionary : dict,
                position : str) -> tuple[dict, dict]:
    """
    Function Details
    ================
    Calculate team usage and team sum usage for any of the required category.

    Parameters
    ----------
    completed_races: list
        List of races for which driver and team points exist.
    team_dictionary: dictionary
        Manager team dictionary for the season.
    position: string
        Category of team sheet position to count.

    Returns
    -------
    team_counts, team_sum_counts: dictionary
        Team counts and team sum counts for given position.

    See Also
    --------
    None

    Notes
    -----
    Team sheets loaded in a loop, categories chosen and driver names or team
    names counted. The function creates an empty array of length -1 of the race
    being analysed for brand new entries.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    29/02/2024
    ----------
    Adapted from previous code to match current processing standards, update to
    documentation.

    """

    """ Set Up Individual Counts and Total Counts """
    team_counts = {}
    team_sum_counts = {}

    """ Loop Through Completed Races """
    for index, race in enumerate(completed_races):
        team_sheet = team_dictionary[f'{race}']

        """ Check The Position Indicator and Count the Names """
        if position == "DRS Boost":
            count_names = [
                team_sheet[key]
                for key in team_sheet.keys()
                if position in key
                or 'Turbo Driver' in key]
        elif position == "Extra DRS":
            count_names = [
                team_sheet[key]
                for key in team_sheet.keys()
                if position in key
                or 'Mega Driver' in key]
        elif position == 'Perks':
            count_names = [
                (team_sheet[f'{position}'])[0]
                if 'Extra DRS' in team_sheet[f'{position}']
                or 'Mega Driver' in team_sheet[f'{position}']
                or 'Final Fix' in team_sheet[f'{position}']
                else team_sheet[f'{position}']]
        else:
            count_names = [
                team_sheet[key]
                for key in team_sheet.keys()
                if position in key]

        """ Distinguish Between Races """
        if index == 0:
            [team_counts.update({n: [1]}) for n in count_names]
        else:
            new_entry = [x for x in np.zeros(shape=index, dtype=int)]
            new_entry.append(1)
            for name in count_names:
                if name in team_counts.keys():
                    team_counts[name].append(1)
                else:
                    team_counts.update({name: new_entry})
            for name in team_counts.keys():
                if name not in count_names:
                    team_counts[name].append(0)

    """ Calculate Summation """
    for name, usage in team_counts.items():
        counts = []
        for i in range(len(completed_races)):
            counts.append(sum(usage[0: i + 1]))
        team_sum_counts.update({name: counts})
    return team_counts, team_sum_counts


def managers_counts(team_counts : dict,
                    completed_races : list) -> tuple[dict, dict]:
    """
    Function Details
    ================
    Count manager usage from individual team uses.

    Parameters
    ----------
    team_counts: dictionary
        Team counts dictionary.
    completed_races: list
        List of races for which driver points and team points exist.

    Returns
    -------
    manager_count, manager_sum_count: dictionary
        Manager count and sum manager counts.

    See Also
    --------
    team_count

    Notes
    -----
    Counts the multiple team uses for one manager.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    29/02/2024
    ----------
    Copied and documentation updated.

    """

    """ Set Up Individual Counts and Total Counts """
    manager_count = {}
    manager_sum_count = {}

    """ Loop Team Dictionaries in the Team Counts """
    for team, team_dictionary in team_counts.items():

        """ Loop Names and Counts Data """
        for name, usage in team_dictionary.items():

            """ If Name Exists, Add Counts """
            if name in manager_count.keys():
                manager_count.update(
                    {name: [x + y for x, y in zip(manager_count[name], usage)]})
            else:
                manager_count.update({name: usage})

    """ Sum Counts """
    for name, usage in manager_count.items():
        counts = []
        for i in range(len(completed_races)):
            counts.append(sum(usage[0: i + 1]))
        manager_sum_count.update({name: counts})
    return manager_count, manager_sum_count


def leaguecount(manager_counts : dict,
                completed_races : list) -> tuple[dict, dict]:
    """
    Function Details
    ================
    Count league usage from individual team uses.

    Parameters
    ----------
    manager_counts: dictionary
        Manager counts dictionary.
    completed_races: list
        List of races for which driver points and team points exist.

    Returns
    -------
    league_count, league_sum_count: dictionary
        League count and sum league counts.

    See Also
    --------
    team_count
    managers_counts

    Notes
    -----
    Counts the multiple manager uses for one league.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    29/02/2024
    ----------
    Copied and documentation updated.

    """

    """ Set  Up Individual Counts and Total Counts """
    league_count = {}
    league_sum_count = {}

    """ Loop Manager Dictionaries in the Manager Counts"""
    for manager, manager_dictionary in manager_counts.items():

        """ Loop Names and Counts Data """
        for name, usage in manager_dictionary.items():

            """ If Name Exists, Add Counts """
            if name in league_count.keys():
                league_count.update(
                    {name: [x + y for x, y in zip(league_count[name], usage)]})
            else:
                league_count.update({name: usage})

    """ Sum Counts """
    for name, usage in league_count.items():
        counts = []
        for i in range(len(completed_races)):
            counts.append(sum(usage[0: i + 1]))
        league_sum_count.update({name: counts})
    return league_count, league_sum_count


def count_usage(info_dictionary : dict,
                completed_races : list,
                data_path : str) -> dict:
    """
    Function Details
    ================
    Count team, manager, and league driver/team/perk usage.

    Parameters
    ----------
    info_dictionary: dictionary
        Season information dictionary.
    completed_races: list
        Races for which driver and team points exist.
    data_path: string
        Path to season data storage.

    Returns
    -------
    counts_dictionary: dictionary
        Team, manager, and league driver/team/perk usage.

    See Also
    --------
    leaguecount
    managers_counts
    teams_count

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    29/02/2024
    ----------
    Adapted for new processing style and updated documentation.

    """

    """ Set Up The Counting Dictionaries and Counting Categories """
    counts_dictionary = {}
    counts = [
        'Driver',
        'Constructor',
        'DRS Boost',
        'Extra DRS',
        'Perks']

    """ Loop Through Categories """
    for count in counts:

        """ League Statistics Out """
        league_teams_out = {}
        league_sum_teams_out = {}
        league_managers_out = {}
        league_sum_managers_out = {}

        """ Find Managers and Teams """
        for manager, teams in info_dictionary["Managers"].items():

            """ Set Manager Counts """
            manager_team = {}
            manager_sum_team = {}

            """ Find Teams and Count Usage """
            for team in teams:
                team_dictionary = load_json(
                    file_path=Path(f'{data_path}/{manager}/{team}.json'))
                team_counts, team_sum_counts = teams_count(
                    completed_races=completed_races,
                    team_dictionary=team_dictionary,
                    position=count)

                """ Add Team Counts to Manager Counts """
                manager_team.update({team: team_counts})
                manager_sum_team.update({team: team_sum_counts})

            """ Add Team Counts to League Counts """
            league_teams_out.update({manager: manager_team})
            league_sum_teams_out.update({manager: manager_sum_team})

            """ Find Managers and Count Usage """
            manager_counts, manager_sum_counts = managers_counts(
                team_counts=manager_team,
                completed_races=completed_races)

            """ Add Manager Counts to League Counts """
            league_managers_out.update({manager: manager_counts})
            league_sum_managers_out.update({manager: manager_sum_counts})

        """ Find League and Count Usage """
        league_counts, league_sum_counts = leaguecount(
            manager_counts=league_managers_out,
            completed_races=completed_races)

        """ Add League Counts to Counts """
        counts_dictionary.update({f'Teams {count}': league_teams_out})
        counts_dictionary.update({f'Teams Sum {count}': league_sum_teams_out})
        counts_dictionary.update({f'Manager {count}': league_managers_out})
        counts_dictionary.update(
            {f'Manager Sum {count}': league_sum_managers_out})
        counts_dictionary.update({f'League {count}': league_counts})
        counts_dictionary.update({f'League Sum {count}': league_sum_counts})
    return counts_dictionary


def update_lineup_stats(results_path : str,
                        results_dict : dict) -> dict:
    """
    Function Details
    ================
    Calculate driver/team statistics from results dictionary.

    Calculate driver/team total points, total values, average points, average
    values, points per value, etc. from results dictionary.

    Parameters
    ----------
    results_path: string
        Path to results directory.
    results_dict : dictionary
        Driver/team results dictionary containing points and values.

    Returns
    -------
    stats_dict : dictionary
        Driver/teams statistics dictionary containing total points, total
        values, average points, average values, points per value, average points
        per value.

    See Also
    --------
    load_json
    sum_points
    sum_values,
    lineup_points_per_value
    save_json_dicts

    Notes
    -----
    Uses the weekly results dictionary to calculate a total points, total
    values, average points, average values, points per value, average points per
    value.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Documentation update and minor function changes.

    """
    stats_dict = load_json(file_path=Path(f'{results_path}/Statistics.json'))
    total_points = sum_points(results_dict=results_dict)
    total_values = sum_values(results_dict=results_dict)
    ppv = lineup_points_per_value(
        results_dict=results_dict,
        statistics_dict=stats_dict)
    for key, values in total_points.items():
        if key in stats_dict.keys():
            stats_dict[key].update(values)
    for key, values in total_values.items():
        if key in stats_dict.keys():
            stats_dict[key].update(values)
    for key, values in ppv.items():
        if key in stats_dict.keys():
            stats_dict[key].update(values)
    save_json_dicts(
        out_path=Path(f'{results_path}/Statistics.json'),
        dictionary=stats_dict)
    return stats_dict


def sum_points(results_dict : dict) -> dict:
    """
    Function Details
    ================
    Calculate the total (sum) points from weekly scores.

    Also calculates average scores.

    Parameters
    ----------
    results_dict: dictionary
        Lineup results dictionary.
    
    Returns
    -------
    sum_points: dictionary
        Lineup total points and average points.
    
    See Also
    --------
    sum_values

    Notes
    -----
    Last edited 09/10/2023

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Documentation update.

    """
    categories = ['Driver', 'Team']
    sum_points = {}
    for category in categories:
        category_points = results_dict[f'{category} Points']
        category_sum = {}
        category_avg = {}
        for key, all_points in category_points.items():
            points = []
            avg_points = []
            for index, point in enumerate(all_points):
                if index == 0:
                    points.append(point)
                    avg_points.append(point)
                else:
                    points.append(point + points[index - 1])
                    avg_points.append(points[index] / (index + 1))
            category_sum.update({key: points})
            category_avg.update({key: avg_points})
        sum_points.update({f'{category} Sum Points': category_sum})
        sum_points.update({f'{category} Average Points': category_avg})
    return sum_points


def sum_values(results_dict : dict) -> dict:
    """
    Function Details
    ================
    Calculate the total (sum) values from weekly scores.

    Also calculates average values.

    Parameters
    ----------
    results_dict: dictionary
        Lineup results dictionary.
    
    Returns
    -------
    sum_values: dictionary
        Lineup total points and average values.
    
    See Also
    --------
    sum_points

    Notes
    -----
    Last edited 09/10/2023

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Documentation update.

    """
    categories = ['Driver', 'Team']
    sum_values = {}
    for category in categories:
        category_values = results_dict[f'{category} Values']
        category_sum = {}
        category_avg = {}
        for key, all_values in category_values.items():
            values = []
            avg_values = []
            for index, value in enumerate(all_values):
                if index == 0:
                    values.append(value)
                    avg_values.append(value)
                else:
                    values.append(value + values[index - 1])
                    avg_values.append((values[index] / (index + 1)))
            category_sum.update({key: values})
            category_avg.update({key: avg_values})
        sum_values.update({f'{category} Sum Values': category_sum})
        sum_values.update({f'{category} Average Values': category_avg})
    return sum_values


def lineup_points_per_value(results_dict : dict,
                            statistics_dict : dict) -> dict:
    """
    Function Details
    ================
    Calculate points per value for race weekend.

    Parameters
    ----------
    results_dict, statistics_dict: dictionary
        Lineup results and statistics dictionaries.
    
    Returns
    -------
    ppv: dictionary
        Lineup points per value (ppv) dictionary.
    
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
    Documentation update.

    """
    categories = ['Driver', 'Team']
    ppv = {}
    for category in categories:
        category_points = results_dict[f'{category} Points']
        category_values = results_dict[f'{category} Values']
        category_ppv = statistics_dict[f'{category} Points Per Value']
        category_avg_ppv = statistics_dict[
            f'{category} Average Points Per Value']
        for key, all_points in category_points.items():
            values = category_values[key]
            ppv_array = []
            avg_ppv_array = []
            avg_points = []
            avg_values = []
            for index, points in enumerate(all_points):
                if points == 0:
                    ppv_array.append(0)
                else:
                    if index == 0:
                        ppv_array.append(points / values[index])
                        avg_values.append(values[index])
                    else:
                        ppv_array.append(points / values[index - 1])
                        avg_values.append(values[index - 1])
                avg_points.append(points)
                if sum(avg_points) == 0:
                    avg_ppv_array.append(0)
                else:
                    avg_ppv_array.append(sum(avg_points) / sum(avg_values))
            category_ppv.update({key: ppv_array})
            category_avg_ppv.update({key: avg_ppv_array})
        ppv.update({f'{category} Points Per Value': category_ppv})
        ppv.update({f'{category} Average Points Per Value': category_avg_ppv})
    return ppv

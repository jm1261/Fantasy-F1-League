def sum_dict(dictionary : dict) -> dict:
    """
    Function Details
    ================
    Calculate the total (sum) points from a dictionary of scores.

    Also calculates average scores.

    Parameters
    ----------
    results_dict: dictionary
        Lineup results dictionary.
    
    Returns
    -------
    dictionary: dictionary
        Lineup total points and average points.
    
    See Also
    --------
    sum_values
    sum_points

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/03/2024
    ----------
    Documentation updated.

    """
    sum_points = {}
    average_points = {}
    for manager, teams in dictionary.items():
        manager_sum = {}
        manager_average = {}
        for team, all_points in teams.items():
            points = []
            avg_points = []
            for index, point in enumerate(all_points):
                if index == 0:
                    points.append(point)
                    avg_points.append(point)
                else:
                    points.append(point + points[index - 1])
                    avg_points.append(points[index] / (index + 1))
            manager_sum.update({f'{team}': points})
            manager_average.update({f'{team}': avg_points})
        sum_points.update({f'{manager}': manager_sum})
        average_points.update({f'{manager}': manager_average})
    dictionary = {
        'Sum Points': sum_points,
        'Average Points': average_points}
    return dictionary


def findmax(results_dict : dict) -> dict:
    """
    Function Details
    ================
    Find the maximum values of an array in a dictionary and sort into order.

    Parameters
    ----------
    results_dict: dictionary
        Results dictionary containing manager : {teams} and teams: [values].

    Returns
    -------
    findmax_dict: dictionary
        Dictionary with the maximum values in order.

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

    27/03/2024
    ----------
    Created.

    """
    y_values = []
    names = []
    for manager, teams in results_dict.items():
        for team, values in teams.items():
            y_values.append(values[-1])
            names.append(team)
    zipped_lists = zip(
        y_values,
        names)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    all_y, all_n = [list(tuple) for tuple in tuples]
    teams_orders = all_n[::-1]
    points_order = all_y[::-1]
    findmax_dict = {}
    for team, points in zip(teams_orders, points_order):
        findmax_dict.update({f'{team}': points})
    return findmax_dict


def short_season_result(results : dict,
                        completed_races : list,
                        specific_races : list) -> dict:
    """
    Function Details
    ================
    Find the results for a shortened portion, or grouped races portion, of a
    full season.

    Find the winners and losers for a set of races, sprint races, etc.

    Parameters
    ----------
    results: dictionary
        Manager/team results dictionary.
    completed_races, specific_races: list
        List of all completed races. List of races to consider in the results.

    Returns
    -------
    results_dict: dictionary
        Manager team results dictionary at specific races summed and average.

    See Also
    --------
    sum_dict

    Notes
    -----
    Can be used to find the winners of the sprint king, or champion of the world
    prizes.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    16/03/2024
    ----------
    Created.

    """
    points_dict = {}
    for manager, teams in results.items():
        manager_dict = {}
        for team, points in teams.items():
            race_points = [
                points[completed_races.index(race)]
                for race in specific_races
                if race in completed_races]
            manager_dict.update({f'{team}': race_points})
        points_dict.update({f'{manager}': manager_dict})
    results_dict = sum_dict(dictionary=points_dict)
    return results_dict


def higher_or_lower(results_dictionary : dict,
                    completed_races : list):
    """
    Function Details
    ================
    Finds the highest and lowest weekly scores throughout the season for manager
    teams.

    Parameters
    ----------
    results_dictionary: dictionary
        Manager team results dictionary.
    completed_races: list
        List of completed races.

    Returns
    -------
    prizes_dictionary: dictionary
        Dictionary containing the highest and lowest weekly scores in the list
        of completed races. Will also return ties.

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

    19/03/2024
    ----------
    Created.

    """
    max_score = ['race', 'manager', 'team', 0]
    min_score = ['race', 'manager', 'team', 1000]
    ties = []
    for manager, teams in results_dictionary.items():
        for team, points in teams.items():
            for points, race in zip(points, completed_races):
                if points > max_score[3]:
                    max_score = [f'{race}', f'{manager}', f'{team}', points]
                elif points == max_score[3]:
                    ties.append([f'{race}', f'{manager}', f'{team}', points])
                elif points < min_score[3]:
                    min_score = [f'{race}', f'{manager}', f'{team}', points]
                elif points == min_score[3]:
                    ties.append([f'{race}', f'{manager}', f'{team}', points])
                else:
                    pass
    prizes_dictionary = {
        'Max Score': max_score,
        'Min Score': min_score,
        'Ties': ties}
    return prizes_dictionary


def max_dicts_value(team_dictionary : dict,
                    races : list,
                    completed_races : list):
    """
    Function Details
    ================
    Finds the maximum value in a dictionary at a given index.

    Parameters
    ----------
    team_dictionary: dictionary
        Team points dictionary.
    races, completed_races: list
        List of all and completed races.

    Returns
    -------
    max_value, ties: list
        Maximum values at given race index and any potential ties.

    See Also
    --------
    None

    Notes
    -----
    the key argument ensures that it compares the tuples based on the last list
    element.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/03/2024
    ----------
    Created.

    """
    max_value = [
        max(
            (
                (race, manager, team, values[completed_races.index(race)])
                for manager, teams in team_dictionary.items()
                for team, values in teams.items()),
                key=lambda x: x[3])
        for race in races
        if race in completed_races]
    ties = [
        [
            (race, manager, team, values[completed_races.index(race)])
            for manager, teams in team_dictionary.items()
            for team, values in teams.items()
            if values[completed_races.index(race)] == (max_value[index])[3]
            and (manager, team) != ((max_value[index])[1], (max_value[index])[2])]
        for index, race in enumerate(races)
        if race in completed_races]
    return max_value, ties


def min_dicts_value(team_dictionary : dict,
                    races : list,
                    completed_races : list):
    """
    Function Details
    ================
    Finds the minimum value in a dictionary at a given index.

    Parameters
    ----------
    team_dictionary: dictionary
        Team points dictionary.
    races, completed_races: list
        List of all and completed races.

    Returns
    -------
    max_value, ties: list
        Minimum values at given race index and any potential ties.

    See Also
    --------
    None

    Notes
    -----
    the key argument ensures that it compares the tuples based on the last list
    element.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/03/2024
    ----------
    Created.

    """
    min_value = [
        min(
            (
                (race, manager, team, values[completed_races.index(race)])
                for manager, teams in team_dictionary.items()
                for team, values in teams.items()),
                key=lambda x: x[3])
        for race in races
        if race in completed_races]
    ties = [
        [
            (race, manager, team, values[completed_races.index(race)])
            for manager, teams in team_dictionary.items()
            for team, values in teams.items()
            if values[completed_races.index(race)] == (min_value[index])[3]
            and (manager, team) != (
                (min_value[index])[1], (min_value[index])[2])]
        for index, race in enumerate(races)
        if race in completed_races]
    return min_value, ties


def sort_key(item : tuple) -> tuple:
    """
    Function Details
    ================
    A custom sorting key function for sorting dictionary items based on the
    maximum value in the associated list.

    Parameters
    ----------
    item: tuple
        A tuple representing a key-value pair from the dictionary, where the
        value is a list.

    Returns
    -------
    max_value, key: tuple
        A tuple where max_value is the maximum value in the associated list,
        nd key is the original key from the dictionary. The output is a list
        taken from the dictionary input.

    See Also
    --------
    max()

    Notes
    -----
    Not quite sure why the output of this is a key and a list, but it is.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    20/03/2024
    ----------
    Created.

    """
    key, values = item
    max_value = max(values)
    return max_value, key


def manager_of_the_year(manager_statistics : dict,
                        info_dictionary : dict,
                        number_of_teams_limit : int) -> dict:
    """
    Find manager of the year.

    In some seasons this may have a condition, such as the number of teams.

    Parameters
    ----------
    manager_statistics, info_dictionary: dictionary
        Manager sum average points. Season info dictionary.
    number_of_teams_limit: integer
        Number of teams condition for certain seasons. The function looks for
        greater than or equal to this number.

    Returns
    -------
    winners: dictionary
        Top three managers and their final scores.

    See Also
    --------
    sort_key

    Notes
    -----
    Checks to find the top five managers of the year and their final scores. If
    condition on number of teams present, the function limits which managers
    can be awarded.

    Example
    -------

    ----------------------------------------------------------------------------
    Update History
    ==============

    20/03/2024
    ----------
    Created.

    """
    sorted_keys_and_values = sorted(
        manager_statistics.items(),
        key=sort_key,
        reverse=True)
    sorted_keys = [key for key, _ in sorted_keys_and_values]
    sorted_values = [max(value) for _, value in sorted_keys_and_values]
    winners = {}
    for manager, points in zip(sorted_keys[0: 5], sorted_values[0: 5]):
        number_of_teams = len((info_dictionary["Managers"])[f'{manager}'])
        if number_of_teams >= number_of_teams_limit:
            winners.update({f'{manager}': points})
    return winners


def viking_comeback(team_points : dict,
                    top_index : int) -> dict:
    """
    Function Details
    ================
    Top scorers in the first race as a function of finishing position at the
    end of the season.

    Parameters
    ----------
    team_points: dictionary
        Team summed points.
    top_index: int
        How many teams to include in the output.

    Returns
    -------
    comeback_scores: dictionary
        Top teams from the first race and their final scores.

    See Also
    --------
    None

    Notes
    -----
    Finds the top {index} number of teams from the first race and returns their
    final scores.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/03/2024
    ----------
    Created.

    """
    scores = []
    names = []
    for manager, teams in team_points.items():
        for team, points in teams.items():
            scores.append(points[0])
            names.append(team)
    zipped_lists = zip(scores, names)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs[-top_index: ])
    scores, names = [list(tuple) for tuple in tuples]
    comeback_scores = {}
    for score, name in zip(scores[::-1], names[::-1]):
        comeback_scores.update({f'{name}': [score]})
    for manager, teams in team_points.items():
        for team, points in teams.items():
            if team in comeback_scores.keys():
                comeback_scores[team].append(points[-1])
    return comeback_scores


def spot_prizes(team_dictionary : dict,
                spot_prizes : dict,
                completed_races : list) -> dict:
    """
    Parameters
    ----------
    team_dictionary, spot_prizes: dictionary
        Team points dictionary, spot prizes dictionary containing the max and
        min race names.
    completed_races: list
        List of completed races.

    Returns
    -------
    winners: dictionary
        Dictionary containing the winners of the max and min races, and ties.

    See Also
    --------
    max_dicts_value
    min_dicts_value

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/03/2024
    ----------
    Created.

    """
    winners = {}
    max_values, max_ties = max_dicts_value(
        team_dictionary=team_dictionary,
        races=spot_prizes["Spot Max"],
        completed_races=completed_races)
    min_values, min_ties = min_dicts_value(
        team_dictionary=team_dictionary,
        races=spot_prizes["Spot Min"],
        completed_races=completed_races)
    for winner in max_values:
        prize_key = (spot_prizes["Spot Names"])[f'{winner[0]}']
        winners.update({f'{prize_key}': winner})
    for winner in min_values:
        prize_key = (spot_prizes["Spot Names"])[f'{winner[0]}']
        winners.update({f'{prize_key}': winner})
    winners.update({'Max Ties': max_ties})
    winners.update({'Min Ties': min_ties})
    return winners


def league_achievements(team_points : dict,
                        league_goals : dict):
    """
    Function Details
    ================
    Process league achievement goals.

    Parameters
    ----------
    team_points, league_goals: dictionary
        Team sum points. League goals segment of prizes dictionary.

    Returns
    -------
    winners: dictionary
        League achievement winners dictionary.

    See Also
    --------
    findmax

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/03/2024
    ----------
    Created.

    """
    winners = {}
    total_scores = findmax(results_dict=team_points)
    prize_names = league_goals["League Prize Names"]
    prize_positions = prize_names.keys()
    team_names = [key for key, value in total_scores.items()]
    for position in prize_positions:
        prize_name = prize_names[f'{position}']
        team_name = team_names[int(position)]
        team_score = total_scores[f'{team_name}']
        winners.update({prize_name: [team_name, team_score]})
    return winners

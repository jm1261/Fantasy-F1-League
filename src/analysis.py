import numpy as np

from pathlib import Path
from src.dataIO import load_json, save_json_dicts


def sum_points(results_dict):
    '''
    Calculate sum points from weekly points scored. Also calculate average
    points.
    Args:
        results_dict: <dictionary> lineup results dictionary
    Returns:
        sum_points: <dictionary> lineup total points and average points
    '''
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


def sum_values(results_dict):
    '''
    Calculate sum values from weekly values. Also calculate average values.
    Args:
        results_dict: <dictionary> lineup results dictionary
    Returns:
        sum_values: <dictionary> lineup total values and average values
    '''
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


def update_lineup_stats(root_path : str,
                        year : str,
                        results_dict : dict) -> dict:
    """
    Calculate driver/team statistics from results dictionary.

    Calculate driver/team total points, total values, average points, average
    values, points per value, etc. from results dictionary.

    Parameters
    ----------
    root_path, year : string
        Path to root directory, year to process as a string.
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

    """
    stats_dict = load_json(
        file_path=Path(f'{root_path}/Data/{year}/Lineup/Statistics.json'))
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
        out_path=Path(f'{root_path}/Data/{year}/Lineup/Statistics.json'),
        dictionary=stats_dict)
    return stats_dict


def managers_lineup(lineup_results : dict,
                    info_dictionary : dict,
                    races_so_far : list,
                    data_path : str) -> dict:
    """
    Calculate points and values from manager team lineup.

    Parameters
    ----------
    lineup_results, info_dictionary: dictionary
        Driver/team results for the lineup, season info dictionary.
    races_so_far: list
        Races completed so far.
    data_path: string
        Path to data directory.

    Returns
    -------
    manager_results: dictionary
        Dictionary containing manager team points, values, average points, and
        average values.

    See Also
    --------
    load_json

    Notes
    -----
    None

    Example
    -------
    None

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
                for index, race in enumerate(races_so_far):
                    manager_dict = load_json(
                        file_path=Path(
                            f'{data_path}/{manager}/{race}_{team}.json'))
                    driver_positions = [
                        'Driver 1',
                        'Driver 2',
                        'Driver 3',
                        'Driver 4',
                        'Driver 5']
                    drs_names = manager_dict['DRS Boost']
                    team_positions = [
                        'Constructor 1',
                        'Constructor 2']
                    extra_drs_names = manager_dict['Extra DRS']
                    penalties = manager_dict['Penalties'][0]
                    if manager_dict['Perks'][0] == 'Final Fix':
                        replaced = manager_dict['Replaced']
                        replaced_scores = manager_dict['Replaced Scores']
                        driver_names = [
                            (manager_dict[name])[0]
                            for name in driver_positions]
                        team_names = [
                            (manager_dict[name])[0]
                            for name in team_positions]
                        if category == 'Points':
                            driver_scores = []
                            team_scores = []
                            drs_scores = []
                            extra_drs_scores = [
                                0 if name == 0
                                else (driver_results[name])[index] * 2
                                for name in extra_drs_names][0]
                            for name in driver_names:
                                if name == replaced[0]:
                                    driver_scores.append(replaced_scores[0])
                                    driver_scores.append(replaced_scores[1])
                                else:
                                    driver_scores.append(
                                        (driver_results[name])[index])
                            for name in team_names:
                                if team == replaced[0]:
                                    team_scores.append(replaced_scores[0])
                                    team_scores.append(replaced_scores[1])
                                else:
                                    team_scores.append(
                                        (team_results[name])[index])
                            for name in drs_names:
                                if name == replaced[0]:
                                    drs_scores.append(replaced_scores[0])
                                    drs_scores.append(replaced_scores[1])
                                else:
                                    drs_scores.append(
                                        (driver_results[name])[index])
                            total_points = (
                                sum(driver_scores)
                                + sum(team_scores)
                                + sum(drs_scores)
                                + extra_drs_scores
                                + penalties)
                            race_scores.append(total_points)
                        else:
                            driver_scores = [
                                (driver_results[name])[index]
                                for name in driver_names]
                            team_scores = [
                                (team_results[name])[index]
                                for name in team_names]
                            total_values = sum(driver_scores) + sum(team_scores)
                            race_scores.append(total_values)
                    elif manager_dict['Perks'][0] == 'No Negative':
                        driver_names = [
                            (manager_dict[name])[0]
                            for name in driver_positions]
                        driver_scores = [
                            (driver_results[name])[index]
                            for name in driver_names]
                        drs_scores = [
                            0 if name == 0
                            else (driver_results[name])[index]
                            for name in drs_names][0]
                        team_names = [
                            (manager_dict[name])[0]
                            for name in team_positions]
                        team_scores = [
                            (team_results[name])[index]
                            for name in team_names]
                        extra_drs_scores = [
                            0 if name == 0
                            else (driver_results[name])[index] * 2
                            for name in extra_drs_names][0]
                        if category == 'Points':
                            all_points = []
                            [all_points.append(x) for x in driver_scores]
                            [all_points.append(x) for x in team_scores]
                            all_points.append(drs_scores)
                            all_points.append(extra_drs_scores)
                            positive_points = [x for x in all_points if x > 0]
                            total_points = sum(positive_points) + penalties
                            race_scores.append(total_points)
                        else:
                            total_values = sum(driver_scores) + sum(team_scores)
                            race_scores.append(total_values)
                    elif manager_dict['Perks'][0] == 'Limitless':
                        driver_names = [
                            (manager_dict[name])[0]
                            for name in driver_positions]
                        driver_scores = [
                            (driver_results[name])[index]
                            for name in driver_names]
                        drs_scores = [
                            0 if name == 0
                            else (driver_results[name])[index]
                            for name in drs_names][0]
                        team_names = [
                            (manager_dict[name])[0]
                            for name in team_positions]
                        team_scores = [
                            (team_results[name])[index]
                            for name in team_names]
                        extra_drs_scores = [
                            0 if name == 0
                            else (driver_results[name])[index] * 2
                            for name in extra_drs_names][0]
                        if category == 'Points':
                            total_points = (
                                sum(driver_scores)
                                + sum(team_scores)
                                + drs_scores
                                + extra_drs_scores
                                + penalties)
                            race_scores.append(total_points)
                        else:
                            total_values = 100.00
                            race_scores.append(total_values)
                    else:
                        driver_names = [
                            (manager_dict[name])[0]
                            for name in driver_positions]
                        driver_scores = [
                            (driver_results[name])[index]
                            for name in driver_names]
                        drs_scores = [
                            0 if name == 0
                            else (driver_results[name])[index]
                            for name in drs_names][0]
                        team_names = [
                            (manager_dict[name])[0]
                            for name in team_positions]
                        team_scores = [
                            (team_results[name])[index]
                            for name in team_names]
                        extra_drs_scores = [
                            0 if name == 0
                            else (driver_results[name])[index] * 2
                            for name in extra_drs_names][0]
                        if category == 'Points':
                            total_points = (
                                sum(driver_scores)
                                + sum(team_scores)
                                + drs_scores
                                + extra_drs_scores
                                + penalties)
                            race_scores.append(total_points)
                        else:
                            total_values = sum(driver_scores) + sum(team_scores)
                            race_scores.append(total_values)
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


def teams_usage(races_so_far,
                data_path,
                manager,
                team,
                positions):
    '''
    Calculate team usage and team sum usage for any of the required categories.
    Args:
        races_so_far: <array> races completed
        data_path: <string> path to year directory
        manager: <string> manager name
        team: <string> team name
        positions: <array> positions to count for
    Returns:
        team_counts: <dict> dictionary containing counted values for given
                        category
        team_sum_counts: <dict> dictionary containing summed counted values for
                        given category
    '''
    team_counts = {}
    team_sum_counts = {}
    for i, race in enumerate(races_so_far):
        manager_dict = load_json(
            file_path=Path(f'{data_path}/{manager}/{race}_{team}.json'))
        count_names = [
            (manager_dict[name])[0]
            for name in positions]
        if i == 0:
            [team_counts.update({n: [1]}) for n in count_names]
        else:
            new_entry = [x for x in np.zeros(shape=i, dtype=int)]
            new_entry.append(1)
            for name in count_names:
                if name in team_counts.keys():
                    team_counts[name].append(1)
                else:
                    team_counts.update({name: new_entry})
            for name in team_counts.keys():
                if name not in count_names:
                    team_counts[name].append(0)
    for name, usage in team_counts.items():
        counts = []
        for i in range(len(races_so_far)):
            counts.append(sum(usage[0: i + 1]))
        team_sum_counts.update({name: counts})
    return team_counts, team_sum_counts


def managers_counts(manager_team,
                    races_so_far):
    '''
    Calculate manager usage and manager sum usage for any of the required
    categories.
    Args:
        manager_team: <dict> managers dictionary containing weekly team usage
        races_so_far: <array> races completed
    Returns:
        manager_count: <dict> weekly manager count for a given category
        manager_sum_count: <dict> weekly manager sum for a given category
    '''
    manager_count = {}
    manager_sum_count = {}
    for team, team_dictionary in manager_team.items():
        for name, usage in team_dictionary.items():
            if name in manager_count.keys():
                manager_count.update(
                    {
                        name: [
                            x + y
                            for x, y
                            in zip(manager_count[name], usage)]})
            else:
                manager_count.update({name: usage})
    for name, usage in manager_count.items():
        counts = []
        for i in range(len(races_so_far)):
            counts.append(sum(usage[0: i + 1]))
        manager_sum_count.update({name: counts})
    return manager_count, manager_sum_count


def leaguecount(manager_counts,
                races_so_far):
    '''
    Calculate league usage and manager sum usage for any of the required
    categories.
    Args:
        manager_counts: <dict> managers dictionary containing weekly manager
                        usage
        races_so_far: <array> races completed
    Returns:
        league_count: <dict> weekly league count for a given category
        league_sum_count: <dict> weekly league sum for a given category
    '''
    league_count = {}
    league_sum_count = {}
    for manager, manager_dictionary in manager_counts.items():
        for name, usage in manager_dictionary.items():
            if name in league_count.keys():
                league_count.update(
                    {
                        name: [
                            x + y
                            for x, y
                            in zip(league_count[name], usage)]})
            else:
                league_count.update({name: usage})
    for name, usage in league_count.items():
        counts = []
        for i in range(len(races_so_far)):
            counts.append(sum(usage[0: i + 1]))
        league_sum_count.update({name: counts})
    return league_count, league_sum_count


def count_usage(info_dictionary,
                races_so_far,
                data_path):
    '''
    Counts league uses for drivers, teams, drs boosts, extra drs, and perks.
    Args:
        info_dictionary: <dict> Info.json
        races_so_far: <array> races complete
        data_path: <string> path to year directory
    Returns:
        counts: <dict> counts dictionary for teams, managers, and league
    '''
    counts_dict = {}
    counts = ['Drivers', 'Constructors', 'DRS Boost', 'Extra DRS', 'Perks']
    count_positions = [
        ['Driver 1', 'Driver 2', 'Driver 3', 'Driver 4', 'Driver 5'],
        ['Constructor 1', 'Constructor 2'],
        ['DRS Boost'],
        ['Extra DRS'],
        ['Perks']]
    for index, count in enumerate(counts):
        league_teams_out = {}
        league_sum_teams_out = {}
        league_managers_out = {}
        league_sum_managers_out = {}
        for manager, teams in info_dictionary['Managers'].items():
            manager_team = {}
            manager_sum_team = {}
            for team in teams:
                team_counts, team_sum_counts = teams_usage(
                    races_so_far=races_so_far,
                    data_path=data_path,
                    manager=manager,
                    team=team,
                    positions=count_positions[index])
                manager_team.update({team: team_counts})
                manager_sum_team.update({team: team_sum_counts})
            league_teams_out.update({manager: manager_team})
            league_sum_teams_out.update({manager: manager_sum_team})
            manager_counts, manager_sum_counts = managers_counts(
                manager_team=manager_team,
                races_so_far=races_so_far)
            league_managers_out.update({manager: manager_counts})
            league_sum_managers_out.update({manager: manager_sum_counts})
        league_counts, league_sum_counts = leaguecount(
            manager_counts=league_managers_out,
            races_so_far=races_so_far)
        counts_dict.update({f'Teams {count}': league_teams_out})
        counts_dict.update({f'Teams Sum {count}': league_sum_teams_out})
        counts_dict.update({f'Manager {count}': league_managers_out})
        counts_dict.update({f'Manager Sum {count}': league_sum_managers_out})
        counts_dict.update({f'League {count}': league_counts})
        counts_dict.update({f'League Sum {count}': league_sum_counts})
    return counts_dict


def sum_manager_results(results_dict):
    '''
    Calculate season long manager and team points, values, average points, and
    average values.
    Args:
        results_dict: <dict> manager Results.json
    Returns:
        sum_entries: <dict> each category added cumulatively
    '''
    categories = ['Points', 'Values', 'Average Points', 'Average Values']
    sum_entries = {}
    for category in categories:
        category_manager_dict = results_dict[f'Manager {category}']
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
                    results_dict[f'Team {category}'])[f'{manager}']
                for team, entries in category_team_dict.items():
                    team_sum = []
                    for index, entry in enumerate(entries):
                        if index == 0:
                            team_sum.append(entry)
                        else:
                            team_sum.append(entry + team_sum[index - 1])
                    manager_teams_sum.update({team: team_sum})
                teams_sum.update({manager: manager_teams_sum})
        sum_entries.update({f'Team Sum {category}': teams_sum})
        sum_entries.update({f'Manager Sum {category}': managers_sum})
    return sum_entries


def manager_points_per_value(results_dict):
    '''
    Calculate race-wise and season-average manager and team points per value.
    Args:
        results_dict: <dict> manager Results.json
    Returns:
        ppvs: <dict> points per value
    '''
    manager_ppvs = {}
    manager_avg_ppvs = {}
    managers = (results_dict['Manager Points']).keys()
    manager_teams_ppvs = {}
    manager_teams_avg_ppvs = {}
    for manager in managers:
        manager_points = (results_dict['Manager Points'])[f'{manager}']
        manager_values = (results_dict['Manager Values'])[f'{manager}']
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
        team_points_dict = (results_dict['Team Points'])[f'{manager}']
        team_values_dict = (results_dict['Team Values'])[f'{manager}']
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


def manager_statistics(results_dict : dict) -> dict:
    """
    Calculate manager and team statistics.

    Parameters
    ----------
    results_dict: dictionary
        Manager/team results dictionary.
    
    Returns
    -------
    stats: dictionary
        Manager/team stats dictionary containing team and manager total points,
        average points, average values, and points per value.
    
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

    """
    sum_stats = sum_manager_results(results_dict=results_dict)
    ppvs = manager_points_per_value(results_dict=results_dict)
    stats = dict(
        sum_stats,
        **ppvs)
    return stats

from collections import Counter
import Functions.Organisation as org


def delta_points(dictionary,
                 out_path):
    '''
    delta_points calculates the difference between array values, for each key,
    in a python dictionary.
    Args:
        dictionary: <dict> dictionary containing teams or drivers points/values
        out_path: <string> path to save
    Returns:
        None
    '''
    delta_dict = {}
    for key, values in dictionary:
        deltas = [
            values[i] if i == 0
            else values[i] - values[i - 1]
            for i in range(0, len(values))]
        delta_dict.update({key: deltas})
    org.dump_json(
        out_path=out_path,
        dictionary=delta_dict)


def delta_values(dictionary,
                 out_path):
    '''
    delta_values calculates the difference between array values, for each key,
    in a python dictionary.
    Args:
        dictionary: <dict> dictionary containing teams or drivers points/values
        out_path: <string> path to save
    Returns:
        None
    '''
    delta_dict = {}
    for key, values in dictionary:
        deltas = [
            0 if i == 0
            else values[i] - values[i - 1]
            for i in range(0, len(values))]
        delta_dict.update({key: deltas})
    org.dump_json(
        out_path=out_path,
        dictionary=delta_dict)


def points_per_value(points_dict,
                     values_dict,
                     out_path,
                     average=False):
    '''
    points_per_value creates a dictionary from a points and value dictionary
    containing the points scored per million pound of cost. The function can be
    used to calculate a rolling average, or a race by race value.
    Args:
        points_dict: <dict> points dictionary
        values_dict: <dict> values dictionary
        out_path: <string> path to save
        average: <bool> if true, values are taken as a season long average
    Returns:
        None
    '''
    pointspervalue = {}
    keys = [key for key, points in points_dict]
    if average:
        sum_points = []
        sum_values = []
        for key, points in points_dict:
            sum_points.append(
                [points[i] if i == 0
                 else sum(points[0: i + 1])
                 for i in range(0, len(points))])
        for key, values in values_dict:
            sum_values.append(
                [values[i] if i == 0
                 else sum(values[0: i + 1])
                 for i in range(0, len(values))])
        for i in range(0, len(sum_points)):
            points_value = [
                (sum_points[i])[j] / (sum_values[i])[j]
                for j in range(0, len(sum_points[i]))]
            pointspervalue.update({keys[i]: points_value})
    else:
        all_points = [points for key, points in points_dict]
        all_values = [values for key, values in values_dict]
        for i in range(0, len(all_points)):
            points_value = [
                (all_points[i])[j] / (all_values[i])[j]
                for j in range(0, len(all_points[i]))]
            pointspervalue.update({keys[i]: points_value})
    org.dump_json(
        out_path=out_path,
        dictionary=pointspervalue)


def team_dict(team_name,
              team_dict,
              driver_points_dict=False,
              driver_values_dict=False,
              team_points_dict=False,
              team_values_dict=False):
    '''
    '''
    manager_dict = {}
    if driver_points_dict:
        for key, values in team_dict:
            points = []
            if key == 'Team':
                for index, name in enumerate(values):
                    points.append(team_points_dict[f'{name}'][index])
            elif key == 'Mega Driver':
                for index, name in enumerate(values):
                    if name == 'None':
                        points.append(0)
                    else:
                        points.append(2 * driver_points_dict[f'{name}'][index])
            elif key == 'Penalties':
                for value in values:
                    points.append(-10 * value)
            elif key == 'Wildcard':
                pass
            else:
                for index, name in enumerate(values):
                    points.append(driver_points_dict[f'{name}'][index])
            manager_dict.update({key: points})
    if driver_values_dict:
        for key, values in team_dict:
            points = []
            if key == 'Team':
                for index, name in enumerate(values):
                    points.append(team_values_dict[f'{name}'][index])
            elif key == 'Mega Driver':
                pass
            elif key == 'Penalties':
                pass
            elif key == 'Wildcard':
                pass
            else:
                for index, name in enumerate(values):
                    points.append(driver_values_dict[f'{name}'][index])
            manager_dict.update({key: points})
    return manager_dict


def team_points(manager_dict,
                races):
    '''
    '''
    season_points = []
    for i in range(0, races):
        weekly_points = []
        for key, points in manager_dict:
            for index, point in enumerate(points):
                if index == i:
                    weekly_points.append(point)
                else:
                    pass
        season_points.append(sum(weekly_points))
    return season_points


def team_counter(manager_dict):
    '''
    '''
    driver = {}
    team = {}
    turbo = {}
    mega = {}
    for key, values in manager_dict:
        if key == 'Team':
            team.update(Counter(values))
        elif key == 'Turbo Driver':
            turbo.update(Counter(values))
        elif key == 'Mega Driver':
            mega.update(Counter(values))
        elif key == 'Penalties':
            pass
        elif key == 'Wildcard':
            pass
        else:
            count = Counter(values)
            for countkey, countvalue in count.items():
                if countkey in driver:
                    newvalue = countvalue + driver[countkey]
                    driver.update({countkey: newvalue})
                else:
                    driver.update({countkey: countvalue})
    return driver, team, turbo, mega

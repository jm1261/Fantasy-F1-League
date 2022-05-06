import math


def total_average_dict(dictionary):
    '''
    Takes sum and average values of multiple arrays in python dictionary. Find
    total and average points/values in driver/team dictionaries. Does not sort.
    Args:
        dictionary: <dict> points/values dictionary
    Returns:
        total: <array> array of total points for each key, length same as the
                number of keys
        average: <array> array of average points for each key, length same as
                the number of keys
    '''
    total = []
    average = []
    for key, values in dictionary:
        total.append(sum(values))
        average.append(sum(values) / len(values))
    return total, average


def min_max_stddev_dict(dictionary):
    '''
    Finds min, max, and standard deviation of arrays within a dictionary. Finds
    min, max, and standard deviation of driver/team points/values. Does not
    sort.
    Args:
        dictionary: <dict> points/values dictionary
    Returns:
        maximum: <array> array of maximum points for each key, length same as
                the number of keys
        minimum: <array> array of minimum points for each key, length same as
                the number of keys
        std_dev: <array> array of standard deviation of the points for each
                key, length same as the number of keys
    '''
    maximum = []
    minimum = []
    std_dev = []
    for key, values in dictionary:
        maximum.append(max(values))
        minimum.append(min(values))
        squares = [value ** 2 for value in values]
        mean_square = sum(squares) / len(values)
        square_mean = (sum(values) / len(values)) ** 2
        variance = mean_square - square_mean
        if variance == 0:
            std_dev.append(0)
        else:
            std_dev.append(variance / math.sqrt(len(values)))
    return maximum, minimum, std_dev


def drvr_team_stats(points_dict,
                    values_dict):
    '''
    Calculate totals, averages, max, min, and stdev values from driver/team
    points and values dictionaries and return all for driver or team.
    Args:
        points_dict: <dict> driver/team individual points dictionary
        values_dict: <dict> driver/team individual values dictionary
    Returns:
        tot_pnts: <array> list of driver/team total points
        avg_pnts: <array> list of driver/team average points
        tot_vals: <array> list of driver/team total values
        avg_vals: <array> list of driver/team average values
        max_pnts: <array> list of driver/team max points
        min_pnts: <array> list of driver/team min points
        stddev_pnts: <array> list of driver/team standard deviation points
        max_vals: <array> list of driver/team max values
        min_vals: <array> list of driver/team min values
        stddev_vals: <array> list of driver/team standard deviation values
    '''
    tot_pnts, avg_pnts = total_average_dict(
        dictionary=points_dict)
    tot_vals, avg_vals = total_average_dict(
        dictionary=values_dict)
    max_pnts, min_pnts, stddev_pnts = min_max_stddev_dict(
        dictionary=points_dict)
    max_vals, min_vals, stddev_vals = min_max_stddev_dict(
        dictionary=values_dict)
    return (tot_pnts, avg_pnts, tot_vals, avg_vals, max_pnts, min_pnts,
            stddev_pnts, max_vals, min_vals, stddev_vals)


def drvs_team_calcs(total_points,
                    total_values,
                    average_points,
                    average_values,
                    max_points,
                    min_points,
                    max_values,
                    min_values):
    '''
    Calculates points per value, average points per average value, points
    range, and values range for drivers/teams.
    Args:
        total_points: <array> driver/team total points
        total_values: <array> driver/team total values
        average_points: <array> driver/team average points
        average_values: <array> driver/team average values
        max_points: <array> driver/team max points
        min_points: <array> driver/team min points
        max_values: <array> driver/team max values
        min_values: <array> driver/team min values
    Returns:
        total_ppv: <array> total points per value for driver/team
        average_ppv: <array> average points per value for driver/team
        range_points: <array> range points for driver/team
        range_values: <array> range values for driver/team
    '''
    total_ppv = [
        total_points[i] / total_values[i]
        for i in range(len(total_points))]
    average_ppv = [
        average_points[i] / average_values[i]
        for i in range(len(average_points))]
    range_points = [
        max_points[i] - min_points[i]
        for i in range(len(max_points))]
    range_values = [
        max_values[i] - min_values[i]
        for i in range(len(max_values))]
    return total_ppv, average_ppv, range_points, range_values

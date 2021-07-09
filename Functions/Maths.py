import math
import Functions.Organisation as org


def correct_points(points_dict,
                   out_path):
    '''
    correct_points takes the input points dictionaries, which are total points
    at after each race, and calculates the individual points scored for each
    race. In other words, it subtracts the race total from the previous total
    to calculate the difference.
    Args:
        points_dict: <dict> dictionary containing teams or drivers and their
                     total points
        out_path: <string> path to save
    Returns:
        None
    '''
    individual_points = {}
    for key, points in points_dict:
        indiv_points = [points[i] if i == 0 else points[i] - points[i - 1]
                        for i in range(0, len(points))]
        individual_points.update({key: indiv_points})
    org.dump_json(
        out_path=out_path,
        dictionary=individual_points)


def total_average_dict(dictionary):
    '''
    total_average_dict takes the sum and average values of a series of arrays
    in a python dictionary. It is used to find the total points and average
    points in the points dict for each key in the dictionary. Note, it does not
    sort values respective to keys, so will return arrays in whatever order
    they are stored in the input dictionary.
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


def min_max_variance_dict(dictionary):
    '''
    min_max_variance_dict takes the maxmimum, minimum, and standard deviation
    of values in an array within a dictionary. It is used to find the maxmimum,
    minimum, and standard deviation of the points in the points dict for each
    key in the dictionary. Note, it does not sort values respective to keys, so
    will return arrays in whatever order they are stored in the input dict.
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

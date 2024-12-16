import logging
import numpy as np

from pathlib import Path

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def cumulative_array(array: list) -> list:
    """
    Function Details
    ================
    Add array elements cumulatively.

    Parameters
    ----------
    array: list
        Array to cumulatively sum.

    Returns
    -------
    cumulative_list: list
        Cumulatively summed array entries.

    ---------------------------------------------------------------------------
    Update History
    ==============

    06/11/2024
    ----------
    Created.

    """
    cumulative_list = []
    for index, entry in enumerate(array):
        cumulative_entry = (
            entry + (cumulative_list[index - 1] if index > 0 else 0))
        cumulative_list.append(cumulative_entry)
    return cumulative_list


def rolling_average_array(array: list) -> list:
    """
    Function Details
    ================
    Calculate a rolling average of an input array.

    Parameters
    ----------
    array: list
        Array to process.

    Returns
    -------
    average_array: list
        Array entries as a rolling average.

    ---------------------------------------------------------------------------
    Update History
    ==============

    06/11/2024
    ----------
    Created.

    """
    average_array = []
    for index, entry in enumerate(array):
        average_array.append(entry / (index + 1))
    return average_array


def calc_efficiency(points: list,
                    values: list) -> list:
    """
    Function Details
    ================
    Calculate efficiency, or points per value, of two input arrays.

    Parameters
    ----------
    points: list
        Points array.
    values: list
        Values array.

    Returns
    -------
    efficiency: list
        Points per value, efficiency, or normalized points array, depending on
        preferred nomenclature.

    ---------------------------------------------------------------------------
    Update History
    ==============

    06/11/2024
    ----------
    Created.

    """
    efficiency = []
    for p, v in zip(points, values):
        if p == 0 or v == 0:
            efficiency.append(0)
        else:
            efficiency.append(p / v)
    return efficiency


def calculate_std_variation(array: list) -> list:
    """
    Function Details
    ================
    Calculate standard deviation and coefficient of variation iteratively.

    Parameters
    ----------
    array: list
        Array to process.

    Returns
    -------
    std: list
        Standard deviation of array up to and including each index of the
        array.
    variation: list
        Coefficient of variation of array up to and including each index of the
        array.

    ---------------------------------------------------------------------------
    Update History
    ==============

    07/11/2024
    ----------
    Created.

    """
    std = []
    variation = []
    for i in range(len(array)):
        data = array[0: i + 1]
        mean = np.mean(data)
        std_dev = np.std(data)
        std.append(std_dev)
        variation.append(std_dev / mean if mean != 0 else 0)
    return std, variation


def score_percentage(array: list) -> list:
    """
    Function Details
    ================
    Calculate percentage of positive and negative scores iteratively from
    weekly scores.

    Parameters
    ----------
    array: list
        Data to process.

    Returns
    -------
    positive_percentage: list
        Percentage of positive scores iteratively.
    negative_percentage: list
        Percentage of negative scores iteratively.

    ---------------------------------------------------------------------------
    Update History
    ==============

    07/11/2024
    ----------
    Created.

    """
    positive_percentage = []
    negative_percentage = []
    for i in range(len(array)):
        data = array[0: i + 1]
        positive_races = sum(1 for d in data if d > 0)
        pos_percentage = positive_races / len(data) * 100
        positive_percentage.append(pos_percentage)

        negative_races = sum(1 for d in data if d < 0)
        neg_percentage = negative_races / len(data) * 100
        negative_percentage.append(neg_percentage)

    return positive_percentage, negative_percentage

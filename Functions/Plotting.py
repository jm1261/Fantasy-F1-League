import os
import matplotlib.pyplot as plt
import Functions.Organisation as org


def plotting_colours(root,
                     array,
                     index,
                     drivers=False,
                     teams=False):
    '''
    plotting_colours uses the format dictionaries to create the marker and line
    colours, and the linestyle, for any driver or team related plots. This
    function requires the format dictionaries, an array of the drivers/teams,
    and the index array from the main code. The function will produce either
    the team colours or the driver colours depending on specified args.
    Args:
        root: <string> path to format directory
        array: <array> array of driver/team names in order
        index: <array> array of driver/team indexes
    Returns:
        colours: <dict> dictionary containing marker colours, line colours, and
                 linestyles
    '''
    markcolour = []
    linecolour = []
    for i in range(0, len(array)):
        config = org.get_config(
            config_path=os.path.join(
                root,
                f'{index[i]}.config'
            ))
        markcolour.append(config['bg_color'])
        linecolour.append(config['color'])
    colours = {}
    if drivers:
        [colours.update({
            f'{array[i]}': [
                f'{markcolour[i]}',
                f'{linecolour[i]}',
                '-']})
        if i % 2 == 0
        else
        colours.update({
            f'{array[i]}': [
                f'{markcolour[i]}',
                f'{linecolour[i]}',
                '--']})
        ]
    if teams:
        [colours.update({
            f'{array[i]}': [
                f'{markcolour[i]}',
                f'{linecolour[i]}',
                '-']})
        ]
    return colours


def

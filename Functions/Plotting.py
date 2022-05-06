import os
import matplotlib.pyplot as plt
import Functions.Organisation as org


def plotting_colour(root,
                    array,
                    index,
                    drivers=False,
                    teams=False):
    '''
    Uses format configs to create marker and line colours for the driver/team
    plots. The function will produce either the team colours or the driver
    colours depending on specified args.
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
        for i in range(0, len(array)):
            if i % 2 == 0:
                colours.update(
                    {
                        f'{array[i]}': [
                            f'{markcolour[i]}',
                            f'{linecolour[i]}',
                            '-']
                    })
            else:
                colours.update(
                    {
                        f'{array[i]}': [
                            f'{markcolour[i]}',
                            f'{linecolour[i]}',
                            '--']
                    })
    if teams:
        for i in range(0, len(array)):
            colours.update(
                    {
                        f'{array[i]}': [
                            f'{markcolour[i]}',
                            f'{linecolour[i]}',
                            '-']
                    })
    return colours


def season_plot(dictionary,
                races,
                colours,
                title,
                y_label,
                out_path,
                cumulative=False,
                average=False):
    '''
    Extract values from dictionary to plot values against relevant races array
    elements. Dictionary keys are placed into legend, and line colours are
    pulled from a colour dictionary.
    Args:
        dictionary: <dict> dictionary for driver/team points/values
        races: <array> races array
        colours: <dict> marker, line, and linstyle colour dictionary
        title: <string> graph title
        y_label: <string> y-axis label
        out_path: <string> save path
    '''
    fig, ax = plt.subplots(
        1,
        figsize=[15, 10.5])
    for key, values in dictionary:
        x_values = races
        if cumulative:
            y_values = [
                values[i] if i == 0
                else sum(values[0: i + 1])
                for i in range(0, len(x_values))]
        elif average:
            y_values = [
                sum(values[0: i + 1]) / len(values[0: i + 1])
                for i in range(0, len(x_values))]
        else:
            y_values = [
                values[i]
                for i in range(0, len(x_values))]
        ax.plot(
            x_values,
            y_values,
            label=f'{key}',
            marker='o',
            linestyle=colours[f'{key}'][2],
            c=colours[f'{key}'][0],
            mfc=colours[f'{key}'][1])
    ax.legend(
        loc=0,
        ncol=2,
        prop={'size': 10})
    ax.grid(True)
    ax.set_xlabel(
        'Races',
        fontsize=18,
        fontweight='bold')
    ax.set_ylabel(
        y_label,
        fontsize=18,
        fontweight='bold')
    ax.set_title(
        title,
        fontsize=24,
        fontweight='bold')
    ax.tick_params(
        axis='x',
        labelsize=14,
        labelrotation=45)
    ax.tick_params(
        axis='y',
        labelsize=14)
    fig.tight_layout()
    plt.savefig(out_path)
    plt.close(fig)
    plt.cla()
    fig.clf()


def average_plot(dictionary,
                 races_array,
                 colour_dict,
                 y_label,
                 title,
                 out_path):
    '''
    average_plot uses the matplotlib pyplot tool and extracts values from a
    config dictionary to plot the dictionary values against the relevant races
    array elements. The key values of the dictionary are given as legend names
    and the function pulls in line- and marker- colours from the previously
    assigned colour dictionary. The function calculates a rolling average for
    each array element in the races array.
    Args:
        dictionary: <dict> dictionary for driver or team, value or points
        races_array: <array> races array
        colour_dict: <dict> marker, line, and linestyle colour dictionary
        title: <string> graph title
        y_label: <string> y-axis label
        out_path: <string> save path
    Returns:
        None
    '''
    fig, ax = plt.subplots(
        1,
        figsize=[15, 10.5])
    for key, values in dictionary:
        x_values = races_array
        y_values = [
            sum(values[0: i + 1]) / len(values[0: i + 1])
            for i in range(0, len(races_array))]
        ax.plot(
            x_values,
            y_values,
            label=f'{key}',
            marker='o',
            linestyle=colour_dict[f'{key}'][2],
            c=colour_dict[f'{key}'][0],
            mfc=colour_dict[f'{key}'][1])
    ax.legend(
        loc=0,
        ncol=2,
        prop={'size': 10})
    ax.grid(True)
    ax.set_xlabel(
        'Races',
        fontsize=18,
        fontweight='bold')
    ax.set_ylabel(
        y_label,
        fontsize=18,
        fontweight='bold')
    ax.set_title(
        title,
        fontsize=24,
        fontweight='bold')
    ax.tick_params(
        axis='x',
        labelsize=14,
        labelrotation=45)
    ax.tick_params(
        axis='y',
        labelsize=14)
    fig.tight_layout()
    plt.savefig(out_path)
    plt.close(fig)
    plt.cla()
    fig.clf()


def season_bar_plot(dictionary,
                    races,
                    colours,
                    title,
                    x_label,
                    out_path,
                    cumulative=False,
                    index=False):
    '''
    Plot sorted list of points/values for drivers/teams as bar plots.
    Args:
        dictionary: <dict> points/values dictionary for drivers/teams
        races: <array> races array
        colours: <dict> marker, line, and linestyle colour dictionary
        title: <string> graph title
        x_label: <string> x-axis label
        out_path: <string> save path
        cumulative: <bool> sums dictionary values
        index: <bool> races array index for non-cumulative values
    Returns:
        None
    '''
    fig, ax = plt.subplots(
        1,
        figsize=[15, 10.5])
    x_values = []
    y_values = []
    barcolours = []
    barborders = []
    for key, points in dictionary:
        x_values.append(key)
        if cumulative:
            y_values.append(sum(points[0: len(races)]))
        else:
            y_values.append(points[index])
        barcolours.append(colours[f'{key}'][0])
        barborders.append(colours[f'{key}'][1])
    zipped_lists = zip(
        y_values,
        x_values,
        barcolours,
        barborders)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    x, y, c, b = [list(tuple) for tuple in tuples]
    ax.barh(
        y,
        x,
        color=c,
        edgecolor=b)
    for i, v in enumerate(x):
        if v < 0:
            ax.text(
                -v,
                i,
                str(round(v, 2)),
                color=c[i],
                fontweight='bold',
                va='center')
        else:
            ax.text(
                v + (v/50),
                i,
                str(round(v, 2)),
                color=c[i],
                fontweight='bold',
                va='center')
    ax.set_title(
        title,
        fontsize=24,
        fontweight='bold')
    ax.set_ylabel(
        'Name',
        fontsize=18,
        fontweight='bold')
    ax.set_xlabel(
        x_label,
        fontsize=18,
        fontweight='bold')
    plt.savefig(out_path)
    plt.close(fig)
    plt.cla()
    fig.clf()


def plot_dictionary(plot_dir,
                    races,
                    race_index,
                    name,
                    dictionary,
                    colours,
                    label,
                    cumulative=False,
                    line=False):
    '''
    '''
    races_dir = os.path.join(
        plot_dir,
        f'{races[race_index]}')
    org.check_dir_exists(dir_path=races_dir)
    if cumulative:
        cumulative_stem = f'{races[race_index]}_Cumulative_{name}'
        if line:
            line_stem = f'{cumulative_stem}_Line.png'
            file_path = os.path.join(
                races_dir,
                line_stem)
            if os.path.isfile(file_path):
                pass
            else:
                print(f'Plotting {line_stem}')
                season_plot(
                    dictionary=dictionary,
                    races=races,
                    colours=colours,
                    title=(' ').join(f'{line_stem[0: -4]}'.split('_')),
                    y_label=label,
                    out_path=file_path,
                    cumulative=True)
        else:
            line_stem = f'{cumulative_stem}_Bar.png'
            file_path = os.path.join(
                races_dir,
                line_stem)
            if os.path.isfile(file_path):
                pass
            else:
                print(f'Plotting {line_stem}')
                season_bar_plot(
                    dictionary=dictionary,
                    races=races,
                    colours=colours,
                    title=(' ').join(f'{line_stem[0: -4]}'.split('_')),
                    x_label=label,
                    out_path=file_path,
                    cumulative=True,
                    index=race_index)
    else:
        cumulative_stem = f'{races[race_index]}_{name}'
        if line:
            line_stem = f'{cumulative_stem}_Line.png'
            file_path = os.path.join(
                races_dir,
                line_stem)
            if os.path.isfile(file_path):
                pass
            else:
                print(f'Plotting {line_stem}')
                season_plot(
                    dictionary=dictionary,
                    races=races,
                    colours=colours,
                    title=(' ').join(f'{line_stem[0: -4]}'.split('_')),
                    y_label=label,
                    out_path=file_path,
                    cumulative=False)
        else:
            line_stem = f'{cumulative_stem}_Bar.png'
            file_path = os.path.join(
                races_dir,
                line_stem)
            if os.path.isfile(file_path):
                pass
            else:
                print(f'Plotting {line_stem}')
                season_bar_plot(
                    dictionary=dictionary,
                    races=races,
                    colours=colours,
                    title=(' ').join(f'{line_stem[0: -4]}'.split('_')),
                    x_label=label,
                    out_path=file_path,
                    cumulative=False,
                    index=race_index)

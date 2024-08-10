################################################################################
################################################################################
###                              File: Plotting                              ###
###                           Author: Joshua Male                            ###
###                             Date: 01/01/2021                             ###
###                                                                          ###
###               Description: Plotting Code for Fantasy League              ###
###                        Project: F1 Fantasy League                        ###
###                                                                          ###
###                       Script Designed for Python 3                       ###
###                         © Copyright Joshua Male                          ###
###                                                                          ###
###                       Software Release: Unreleased                       ###
################################################################################
################################################################################
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from src.formats import drivers_colours, team_colour
from src.formats import managers_colour, manager_team_colour, perk_colour
from matplotlib.ticker import AutoMinorLocator


def cm_to_inches(cm: float) -> float:
    """
    Returns centimeters as inches.

    Uses the conversion rate to convert a value given in centimeters to inches.
    Useful for matplotlib plotting.

    Parameters
    ----------
    cm : float
        Value of the desired figure size in centimeters.

    Returns
    -------
    inches : float
        Value of the desired figure size in inches.

    See Also
    --------
    None

    Notes
    -----
    Conversion rate given to 6 decimal places, but inches rounded to 2 decimal
    places.

    Example
    -------
    >>> cm = 15
    >>> inches = cm_to_inches(cm=cm)
    >>> inches
    5.91

    """
    return round(cm * 0.393701, 2)


def plotting_colour(format_dir : str,
                    year : str,
                    driver=False,
                    team=False,
                    manager_team=False,
                    manager=False,
                    perk=False) -> dict:
    """
    Function Details
    ================
    Determine plotting colours based on input.

    Takes data from format dictionaries to create the marker and line colors for
    the teams and drivers on the plot.

    Parameters
    ----------
    format_dir, year : string
        Path to formats directory. Year for colour codes.
    driver, team, manager_team, manager, perk : boolean
        Determines which format is being selected, one must be True.

    Returns
    -------
    colors_dict : dictionary
        Plotting colors dictionary.
    
    See Also
    --------
    driver_colours
    team_colour
    manager_team_colour
    managers_colour
    perk_colour

    Notes
    -----
    Uses the formatting functions list above to determine the plotting colors
    for various things, such as driver, team, perk, manager, etc. plots. The
    color functions can be found in /src/formats.py.

    Example
    -------
    >>> color_dict = plotting_colour(
        format_dir="/Path/To/Format/Directory",
        team=True)
    >>> color_dict
    {
        "Name": "Team Name"
        "Drivers": ["Driver 1", "Driver 2"],
        "Colors": "Color"
    }

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Copied and updated documentation.

    02/03/2024
    ----------
    Update to manager team colors, now just uses matplotlib colors in order for
    multiple teams. Added year for colour codes.

    """

    """ Set Up Colours Dictionary """
    colors_dictionary = {}

    """ Driver """
    if driver:
        format_dict = drivers_colours(
            format_dir=Path(f'{format_dir}/Lineup_Formats'),
            driver=driver,
            year=year)
        colors_dictionary.update({'color': format_dict['color']})
        colors_dictionary.update({'bg_color': format_dict['bg_color']})
        if driver == (format_dict['drivers'])[0]:
            colors_dictionary.update({'linestyle': 'solid'})
        elif driver == (format_dict['drivers'])[1]:
            colors_dictionary.update({'linestyle': 'dashed'})
        elif driver == (format_dict['drivers'])[2]:
            colors_dictionary.update({'linestyle': 'dashdot'})
        else:
            colors_dictionary.update({'linestyle': 'dotted'})

    """ Team """
    if team:
        format_dict = team_colour(
            format_dir=Path(f'{format_dir}/Lineup_Formats'),
            team=team,
            year=year)
        colors_dictionary.update({'color': format_dict['color']})
        colors_dictionary.update({'bg_color': format_dict['bg_color']})
        colors_dictionary.update({'linestyle': '-'})

    """ Manager Team """
    if manager_team:
        format_dict = manager_team_colour(
                format_dir=Path(f'{format_dir}/Manager_Formats'),
                team=manager_team)
        colors_dictionary.update({'bg_color': format_dict['bg_color']})
        if manager_team == (format_dict['teams'])[0]:
            colors_dictionary.update({'color': 'red'})
            colors_dictionary.update({'linestyle': 'solid'})
        elif manager_team == (format_dict['teams'])[1]:
            colors_dictionary.update({'color': 'yellow'})
            colors_dictionary.update({'linestyle': 'dashed'})
        elif manager_team == (format_dict['teams'])[2]:
            colors_dictionary.update({'color': 'blue'})
            colors_dictionary.update({'linestyle': 'dashdot'})
        elif manager_team == (format_dict['teams'])[3]:
            colors_dictionary.update({'color': 'blue'})
            colors_dictionary.update({'linestyle': 'solid'})
        elif manager_team == (format_dict['teams'])[4]:
            colors_dictionary.update({'color': 'yellow'})
            colors_dictionary.update({'linestyle': 'dashed'})
        elif manager_team == (format_dict['teams'])[5]:
            colors_dictionary.update({'color': 'red'})
            colors_dictionary.update({'linestyle': 'dashdot'})
        elif manager_team == (format_dict['teams'])[6]:
            colors_dictionary.update({'color': 'red'})
            colors_dictionary.update({'linestyle': 'solid'})
        elif manager_team == (format_dict['teams'])[7]:
            colors_dictionary.update({'color': 'yellow'})
            colors_dictionary.update({'linestyle': 'dashed'})
        elif manager_team == (format_dict['teams'])[8]:
            colors_dictionary.update({'color': 'blue'})
            colors_dictionary.update({'linestyle': 'dashdot'})
        elif manager_team == (format_dict['teams'])[9]:
            colors_dictionary.update({'color': 'blue'})
            colors_dictionary.update({'linestyle': 'solid'})
        else:
            colors_dictionary.update({'color': 'yellow'})
            colors_dictionary.update({'linestyle': 'dashdot'})

    """ Manager """
    if manager:
        format_dict = managers_colour(
                format_dir=Path(f'{format_dir}/Manager_Formats'),
                manager=manager)
        colors_dictionary.update({'bg_color': format_dict['bg_color']})

    """ Perk """
    if perk:
        format_dict = perk_colour(
            format_dir=Path(f'{format_dir}/Lineup_Formats'),
            perk=perk,
            year=year)
        colors_dictionary.update({'bg_color': format_dict['bg_color']})
        colors_dictionary.update({'color': format_dict['color']})
    return colors_dictionary


def league_bars(results_dictionary : dict,
                race_index : int,
                race : str,
                format_dir : str,
                year : str,
                out_path : str) -> None:
    """
    Function Details
    ================
    Plot top 10 and bottom 10 managers weekly.

    Plot top 10 and bottom 10 manager teams for each race.

    Parameters
    ----------
    results_dictionary: dictionary
        Manager results dictionary.
    race_index: int
        Integer of races array for which to plot.
    race, format_dir, year, out_path: string
        Race name, path to format directory, year for colours, path to save.
    
    See Also
    --------
    plotting_colour

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
    Updated documentation.

    02/03/2024
    ----------
    Added rotation to x ticks for line plotting. Added cm_to_inches for size.
    Added years for colour codes.

    """
    categories = ['Points', 'Values']
    units = ['[#]', '[$M]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_LeagueTeams_{category}_Bar.png')
        if out_file.is_file():
            pass
        else:
            category_dict = results_dictionary[f'Team {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            bar_colors = []
            bar_borders = []
            for manager, teams in category_dict.items():
                for team, values in teams.items():
                    x_values.append(team)
                    y_values.append(values[race_index])
                    colors = plotting_colour(
                        format_dir=format_dir,
                        manager_team=team,
                        year=year)
                    bar_colors.append(colors['bg_color'])
                    bar_borders.append(colors['color'])
            zipped_lists = zip(
                y_values,
                x_values,
                bar_colors,
                bar_borders)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs[0: 10])
            top_x, top_y, top_c, top_b = [list(tuple) for tuple in tuples]
            top_x.append(0)
            top_y.append('⋮')
            top_c.append('k')
            top_b.append('k')
            tuples = zip(*sorted_pairs[-10:])
            bot_x, bot_y, bot_c, bot_b = [list(tuple) for tuple in tuples]
            x = np.concatenate((top_x, bot_x))
            y = np.concatenate((top_y, bot_y))
            c = np.concatenate((top_c, bot_c))
            b = np.concatenate((top_b, bot_b))
            ax.barh(
                y,
                x,
                color=c,
                edgecolor=b)
            for i, v in enumerate(x):
                if v < 0:
                    ax.text(
                        1 + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
            ax.set_ylabel(
                'Team',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'{category} {unit}',
                fontsize=6,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League Teams {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.set_xlim(min(x) - 30, max(x) + 30)
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
    categories = ['Average Points', 'Average Values']
    units = ['[#]', '[$M]']
    axes = [50, 20]
    for category, unit, a in zip(categories, units, axes):
        out_file = Path(f'{out_path}/{race}_LeagueManagers_{category}_Bar.png')
        if out_file.is_file():
            pass
        else:
            category_dict = results_dictionary[f'Manager {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            bar_colors = []
            bar_borders = []
            for manager, values in category_dict.items():
                colours = plotting_colour(
                    format_dir=format_dir,
                    manager=manager,
                    year=year)
                x_values.append(manager)
                y_values.append(values[race_index])
                bar_colors.append(colours['bg_color'])
                bar_borders.append(colours['bg_color'])
            zipped_lists = zip(
                y_values,
                x_values,
                bar_colors,
                bar_borders)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs[0: 10])
            top_x, top_y, top_c, top_b = [list(tuple) for tuple in tuples]
            top_x.append(0)
            top_y.append('⋮')
            top_c.append('k')
            top_b.append('k')
            tuples = zip(*sorted_pairs[-10:])
            bot_x, bot_y, bot_c, bot_b = [list(tuple) for tuple in tuples]
            x = np.concatenate((top_x, bot_x))
            y = np.concatenate((top_y, bot_y))
            c = np.concatenate((top_c, bot_c))
            b = np.concatenate((top_b, bot_b))
            ax.barh(
                y,
                x,
                color=c,
                edgecolor=c)
            for i, v in enumerate(x):
                if v < 0:
                    ax.text(
                        1 + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
            ax.set_ylabel(
                'Manager',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'{category} {unit}',
                fontsize=6,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.set_xlim(min(x) - 30, max(x) + 30)
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()


def leaguecount(results_dictionary : dict,
                race_index : int,
                race : str,
                races : list,
                format_dir : str,
                year : str,
                out_path : str) -> None:
    """
    Function Details
    ================
    Plot weekly league counts.

    Plot counts for drivers, constructors, DRS, Extra DRS, and perks.

    Parameters
    ----------
    results_dictionary: dictionary
        Count dictionary.
    race_index: int
        Integer of the races array for which to plot.
    race: list
        List of races.
    race, format_dir, year, out_path:
        Race name, format directory, year for colours, path to save.
    
    Returns
    -------
    None

    See Also
    --------
    plotting_colour

    Notes
    -----
    At the end of the 2023 season, remove Nonw from the perks plotter, it is a
    mistake.
    Last checked 09/10/2023

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update to documentation.

    02/03/2024
    ----------
    Added rotation to x ticks for line plotting. Added cm_to_inches for size.
    Added year for colour codes.

    05/05/2024
    ----------
    Update to the y-axis tick labels for the standard plots.

    """
    categories = ['Driver', 'Constructor', 'DRS Boost', 'Extra DRS', 'Perks']
    for category in categories:
        out_file = Path(f'{out_path}/{race}_LeagueCounts_{category}_Bar.png')
        if out_file.is_file():
            pass
        else:
            category_dict = results_dictionary[f'League {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            bar_colors = []
            bar_borders = []
            for name, count in category_dict.items():
                if category == 'Driver':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        driver=name,
                        year=year)
                    bar_colors.append(colours['bg_color'])
                    bar_borders.append(colours['color'])
                    x_values.append(name)
                    y_values.append(count[race_index])
                elif category == 'Constructor':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        team=name,
                        year=year)
                    bar_colors.append(colours['bg_color'])
                    bar_borders.append(colours['color'])
                    x_values.append(name)
                    y_values.append(count[race_index])
                elif category == 'DRS Boost':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        driver=name,
                        year=year)
                    bar_colors.append(colours['bg_color'])
                    bar_borders.append(colours['color'])
                    x_values.append(name)
                    y_values.append(count[race_index])
                elif category == 'Extra DRS':
                    if name == 'None':
                        pass
                    else:
                        colours = plotting_colour(
                            format_dir=format_dir,
                            driver=name,
                            year=year)
                        bar_colors.append(colours['bg_color'])
                        bar_borders.append(colours['color'])
                        x_values.append(name)
                        y_values.append(count[race_index])
                elif category == 'Perks':
                    if name == 'None':
                        pass
                    elif name == 'Nonw':
                        pass
                    else:
                        colours = plotting_colour(
                            format_dir=format_dir,
                            perk=name,
                            year=year)
                        bar_colors.append(colours['bg_color'])
                        bar_borders.append(colours['color'])
                        x_values.append(name)
                        y_values.append(count[race_index])
            if len(x_values) == 0:
                continue
            zipped_lists = zip(
                y_values,
                x_values,
                bar_colors,
                bar_borders)
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
                        1 + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
            ax.set_ylabel(
                'Names',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'Counts [#]',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League {race} {category} Count',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
        out_file = Path(f'{out_path}/{race}_LeagueSumCounts_{category}.png')
        if out_file.is_file():
            pass
        else:
            category_dict = results_dictionary[f'League Sum {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            lines = []
            for name, count in category_dict.items():
                if category == 'Driver':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        driver=name,
                        year=year)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    x_values.append(races)
                    y_values.append([count[i] for i in range(len(races))])
                    names.append(name)
                    lines.append(colours['linestyle'])
                elif category == 'Constructor':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        team=name,
                        year=year)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    x_values.append(races)
                    y_values.append([count[i] for i in range(len(races))])
                    names.append(name)
                    lines.append(colours['linestyle'])
                elif category == 'DRS Boost':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        driver=name,
                        year=year)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    x_values.append(races)
                    y_values.append([count[i] for i in range(len(races))])
                    names.append(name)
                    lines.append(colours['linestyle'])
                elif category == 'Extra DRS':
                    if name == 'None':
                        pass
                    else:
                        colours = plotting_colour(
                            format_dir=format_dir,
                            driver=name,
                            year=year)
                        colors.append(colours['bg_color'])
                        markers.append(colours['color'])
                        x_values.append(races)
                        y_values.append([count[i] for i in range(len(races))])
                        names.append(name)
                        lines.append(colours['linestyle'])
                elif category == 'Perks':
                    if name == 'None':
                        pass
                    elif name == 'Nonw':
                        pass
                    else:
                        colours = plotting_colour(
                            format_dir=format_dir,
                            perk=name,
                            year=year)
                        colors.append(colours['bg_color'])
                        markers.append(colours['color'])
                        x_values.append(races)
                        y_values.append([count[i] for i in range(len(races))])
                        names.append(name)
                        lines.append('solid')
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                markers,
                names,
                lines)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs)
            y, x, c, m, n, l = [list(tuple) for tuple in tuples]
            for i in range(len(x)):
                ax.plot(
                    x[i],
                    y[i],
                    label=n[i],
                    marker='o',
                    linestyle=l[i],
                    c=c[i],
                    mfc=m[i],
                    markersize=4,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 6})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} [#]',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=90)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League {race} {category} Sum Counts',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()


def leagueteam_stat(statistics_dictionary : dict,
                    races : list,
                    race : str,
                    format_dir : str,
                    year : str,
                    out_path : str) -> None:
    """
    Function Details
    ================
    Plot league statistics.

    Plot league teams and manager statistics.

    Parameters
    ----------
    statistics_dictionary: dictionary
        Manager statistics dictionary.
    races: list
        List of races.
    race, format_dir, year, out_path: string
        Race name, format directory, year for colours, path to save.
    
    Returns
    -------
    None

    See Also
    --------
    plotting_color

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
    Updated documentation.

    02/03/2024
    ----------
    Added rotation to x ticks for line plotting. Added cm_to_inches for size.
    Added year for colours.

    05/05/2024
    ----------
    Added y-axis ticks to standard plots.

    """
    categories = ['Sum Points', 'Sum Values']
    units = ['[#]', '[$M]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_LeagueManagers_{category}.png')
        if out_file.is_file():
            pass
        else:
            category_dict = statistics_dictionary[f'Manager {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            for manager, values in category_dict.items():
                x_values.append(races)
                y_values.append([values[i] for i in range(len(races))])
                colours = plotting_colour(
                    format_dir=format_dir,
                    manager=manager,
                    year=year)
                colors.append(colours['bg_color'])
                markers.append(colours['bg_color'])
                names.append(manager)
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                markers,
                names)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs)
            y, x, c, m, n = [
                list(tuple) for tuple in tuples]
            for i in range(len(x)):
                ax.plot(
                    x[i],
                    y[i],
                    label=n[i],
                    marker='o',
                    linestyle='solid',
                    c=c[i],
                    mfc=m[i],
                    markersize=4,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 6})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=90)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
    categories = ['Sum Average Points', 'Sum Average Values']
    units = ['[#]', '[$M]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_LeagueManagers_{category}.png')
        if out_file.is_file():
            pass
        else:
            category_dict = statistics_dictionary[f'Manager {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            for manager, values in category_dict.items():
                x_values.append(races)
                y_values.append([values[i] for i in range(len(races))])
                colours = plotting_colour(
                    format_dir=format_dir,
                    manager=manager,
                    year=year)
                colors.append(colours['bg_color'])
                markers.append(colours['bg_color'])
                names.append(manager)
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                markers,
                names)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs)
            y, x, c, m, n = [
                list(tuple) for tuple in tuples]
            for i in range(len(x)):
                ax.plot(
                    x[i],
                    y[i],
                    label=n[i],
                    marker='o',
                    linestyle='solid',
                    c=c[i],
                    mfc=m[i],
                    markersize=4,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 6})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=90)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
    categories = ['Sum Points', 'Sum Values']
    units = ['[#]', '[$M]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_LeagueTeams_{category}.png')
        if out_file.is_file():
            pass
        else:
            category_dict = statistics_dictionary[f'Team {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            lines = []
            for manager, teams in category_dict.items():
                for team, values in teams.items():
                    x_values.append(races)
                    y_values.append([values[i] for i in range(len(races))])
                    colours = plotting_colour(
                        format_dir=format_dir,
                        manager_team=team,
                        year=year)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    names.append(team)
                    lines.append(colours['linestyle'])
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                markers,
                names,
                lines)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs[0: 10])
            top_y, top_x, top_c, top_m, top_n, top_l = [
                list(tuple) for tuple in tuples]
            tuples = zip(*sorted_pairs[-10:])
            bot_y, bot_x, bot_c, bot_m, bot_n, bot_l = [
                list(tuple) for tuple in tuples]
            x = np.concatenate((top_x, bot_x))
            y = np.concatenate((top_y, bot_y))
            c = np.concatenate((top_c, bot_c))
            m = np.concatenate((top_m, bot_m))
            n = np.concatenate((top_n, bot_n))
            l = np.concatenate((top_l, bot_l))
            for i in range(len(x)):
                ax.plot(
                    x[i],
                    y[i],
                    label=n[i],
                    marker='o',
                    linestyle=l[i],
                    c=c[i],
                    mfc=m[i],
                    markersize=4,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 6})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=90)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League Teams {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()


def leagueteam_ppvs(statistics_dictionary : dict,
                    race_index : int,
                    races : list,
                    race : str,
                    format_dir : str,
                    year : str,
                    out_path : str) -> None:
    """
    Function Details
    ================
    Plot league points per value.

    Plot statistics points per value for managers and teams.

    Parameters
    ----------
    statistics_dictionary: dictionary
        Manager statistics dictionary.
    race_index: int
        Index for the race in races list.
    races: list
        List of races.
    race, format_dir, year, out_path: string
        Race name, format directory, year for colours, path to save.
    
    Returns
    -------
    None

    See Also
    --------
    plotting_color

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
    Update documentation.

    02/03/2024
    ----------
    Added rotation to x ticks for line plotting. Added cm_to_inches for size.

    05/05/2024
    ----------
    Added minor tick labels for x and y axes.

    """
    categories = ['Average Points Per Value']
    units = ['[#/$M]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_LeagueManagers_{category}.png')
        if out_file.is_file():
            pass
        else:
            category_dict = statistics_dictionary[f'Manager {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            for manager, values in category_dict.items():
                x_values.append(races)
                y_values.append([values[i] for i in range(len(races))])
                colours = plotting_colour(
                    format_dir=format_dir,
                    manager=manager,
                    year=year)
                colors.append(colours['bg_color'])
                markers.append(colours['bg_color'])
                names.append(manager)
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                markers,
                names)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs)
            y, x, c, m, n = [
                list(tuple) for tuple in tuples]
            for i in range(len(x)):
                ax.plot(
                    x[i],
                    y[i],
                    label=n[i],
                    marker='o',
                    linestyle='solid',
                    c=c[i],
                    mfc=m[i],
                    markersize=4,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 6})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=90)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
    categories = ['Average Points Per Value']
    units = ['[#/$M]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_LeagueTeams_{category}.png')
        if out_file.is_file():
            pass
        else:
            category_dict = statistics_dictionary[f'Team {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            lines = []
            for manager, teams in category_dict.items():
                for team, values in teams.items():
                    x_values.append(races)
                    y_values.append([values[i] for i in range(len(races))])
                    colours = plotting_colour(
                        format_dir=format_dir,
                        manager_team=team,
                        year=year)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    names.append(team)
                    lines.append(colours['linestyle'])
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                markers,
                names,
                lines)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs[0: 10])
            top_y, top_x, top_c, top_m, top_n, top_l = [
                list(tuple) for tuple in tuples]
            tuples = zip(*sorted_pairs[-10:])
            bot_y, bot_x, bot_c, bot_m, bot_n, bot_l = [
                list(tuple) for tuple in tuples]
            x = np.concatenate((top_x, bot_x))
            y = np.concatenate((top_y, bot_y))
            c = np.concatenate((top_c, bot_c))
            m = np.concatenate((top_m, bot_m))
            n = np.concatenate((top_n, bot_n))
            l = np.concatenate((top_l, bot_l))
            for i in range(len(x)):
                ax.plot(
                    x[i],
                    y[i],
                    label=n[i],
                    marker='o',
                    linestyle=l[i],
                    c=c[i],
                    mfc=m[i],
                    markersize=4,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 6})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=90)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League Teams {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
    categories = ['Points Per Value', 'Sum Points']
    units = ['[#/$M]', '[#]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_LeagueManagers_{category}_Bar.png')
        if out_file.is_file():
            pass
        else:
            category_dict = statistics_dictionary[f'Manager {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            borders = []
            for manager, values in category_dict.items():
                x_values.append(manager)
                y_values.append(values[race_index])
                colours = plotting_colour(
                    format_dir=format_dir,
                    manager=manager,
                    year=year)
                colors.append(colours['bg_color'])
                borders.append(colours['bg_color'])
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                borders)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs)
            x, y, c, b = [
                list(tuple) for tuple in tuples]
            ax.barh(
                y,
                x,
                color=c,
                edgecolor=b)
            for i, v in enumerate(x):
                if v < 0:
                    ax.text(
                        1 + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
            ax.set_ylabel(
                'Name',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'{category} {unit}',
                fontsize=6,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=90)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
    categories = ['Points Per Value', 'Sum Points']
    units = ['[#/$M]', '[#]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_LeagueTeams_{category}_Bar.png')
        if out_file.is_file():
            pass
        else:
            category_dict = statistics_dictionary[f'Team {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            borders = []
            for manager, teams in category_dict.items():
                for team, values in teams.items():
                    x_values.append(team)
                    y_values.append(values[race_index])
                    colours = plotting_colour(
                        format_dir=format_dir,
                        manager_team=team,
                        year=year)
                    colors.append(colours['bg_color'])
                    borders.append(colours['color'])
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                borders)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs[0: 10])
            top_x, top_y, top_c, top_b = [
                list(tuple) for tuple in tuples]
            top_x.append(0)
            top_y.append('⋮')
            top_c.append('k')
            top_b.append('k')
            tuples = zip(*sorted_pairs[-10:])
            bot_x, bot_y, bot_c, bot_b = [
                list(tuple) for tuple in tuples]
            x = np.concatenate((top_x, bot_x))
            y = np.concatenate((top_y, bot_y))
            c = np.concatenate((top_c, bot_c))
            b = np.concatenate((top_b, bot_b))
            ax.barh(
                y,
                x,
                color=c,
                edgecolor=b)
            for i, v in enumerate(x):
                if v < 0:
                    ax.text(
                        1 + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center',
                        fontsize=6)
            ax.set_ylabel(
                'Names',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'{category} {unit}',
                fontsize=6,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'League Teams {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()


def results_bar(results_dictionary : dict,
                race_index : int,
                race : str,
                format_dir : str,
                year : str,
                out_path : str) -> None:
    """
    Function Details
    ================
    Plot sorted results as a bar graph.

    Plot dictionary values against relevant races array elements. Sorts results
    in ascending order and plots as a bar graph.

    Parameters
    ----------
    results_dictionary : dictionary
        Dictionary containing the results needed to plot, must have key and an
        array of the results to plot.
    race_index : int
        Race index as an integer.
    race, format_dir, year, out_path : string
        Race name. Path to format directory. Year for colours. Path to save.
    
    Returns
    -------
    None

    See Also
    --------
    plotting_colour

    Notes
    -----
    None.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Update documentation.

    02/03/2024
    ----------
    Added rotation to x ticks for line plotting. Added cm_to_inches for size.
    Added years for colours.

    """
    categories = ['Driver', 'Team']
    for category in categories:
        plots = ['Points', 'Values']
        units = ['[#]', '[$M]']
        for index, plot in enumerate(plots):
            out_file = Path(f'{out_path}/{race}_{category}_{plot}_Bar.png')
            if out_file.is_file():
                pass
            else:
                plotting_dict = results_dictionary[f'{category} {plot}']
                fig, ax = plt.subplots(
                    nrows=1,
                    ncols=1,
                    figsize=[
                        cm_to_inches(cm=15),
                        cm_to_inches(cm=9)],
                    dpi=600)
                x_values = []
                y_values = []
                bar_colors = []
                bar_borders = []
                for key, values in plotting_dict.items():
                    if category == 'Driver':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            driver=key,
                            year=year)
                    if category == 'Team':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            team=key,
                            year=year)
                    x_values.append(key)
                    y_values.append(values[race_index])
                    bar_colors.append(colors['bg_color'])
                    bar_borders.append(colors['color'])
                zipped_lists = zip(
                    y_values,
                    x_values,
                    bar_colors,
                    bar_borders)
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
                            1 + (v / 50),
                            i,
                            str(round(v, 2)),
                            color=c[i],
                            fontweight='bold',
                            va='center',
                            fontsize=6)
                    else:
                        ax.text(
                            v + (v / 50),
                            i,
                            str(round(v, 2)),
                            color=c[i],
                            fontweight='bold',
                            va='center',
                            fontsize=6)
                ax.set_xlabel(
                    f'{plot} {units[index]}',
                    fontsize=10,
                    fontweight='bold',
                    color='black')
                ax.set_ylabel(
                    'Name',
                    fontsize=10,
                    fontweight='bold',
                    color='black')
                ax.tick_params(
                    axis='x',
                    labelsize=6,
                    labelrotation=45)
                ax.tick_params(
                    axis='y',
                    labelsize=6)
                ax.set_title(
                    f'{race} {category} {plot}',
                    fontsize=14,
                    fontweight='bold',
                    color='black')
                ax.xaxis.set_minor_locator(AutoMinorLocator())
                fig.tight_layout()
                plt.savefig(
                    out_file,
                    bbox_inches='tight')
                plt.close(fig)
                plt.cla()


def lineupstats(statistics_dictionary : dict,
                race_index : float,
                races : list,
                race : str,
                format_dir : str,
                year : str,
                out_path : str) -> None:
    """
    Function Details
    ================
    Plot sorted statistics for drivers and teams.

    Plot sorted statistics dictionary for drivers and teams as lines or bars.

    Parameters
    ----------
    statistics_dictionary: dictionary
        Statistics dictionary for drivers and teams for current year.
    race_index: float
        The index of the races list for which the current race is.
    races: list
        List of all season races.
    Race, format_dir, year, out_path: string
        Current race name, path to formats directory, year for colours, path to
        save.
    
    Returns
    -------
    None

    See Also
    --------
    results_bar
    plotting_colour

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    --------------

    01/03/2024
    ----------
    Update documentation.

    02/03/2024
    ----------
    Added rotation to x ticks for line plotting. Added cm_to_inches for size.
    Added years for colours.

    05/05/2024
    ----------
    Added y-axis tick labels for standard plots.

    """
    categories = ['Driver', 'Team']
    for category in categories:
        plots = [
            'Points Per Value']
        units = ['[#/$M]']
        for index, plot in enumerate(plots):
            out_file = Path(f'{out_path}/{race}_{category}_{plot}_Bar.png')
            if out_file.is_file():
                pass
            else:
                plotting_dict = statistics_dictionary[f'{category} {plot}']
                fig, ax = plt.subplots(
                    nrows=1,
                    ncols=1,
                    figsize=[
                        cm_to_inches(cm=15),
                        cm_to_inches(cm=9)],
                    dpi=600)
                x_values = []
                y_values = []
                bar_colors = []
                bar_borders = []
                for key, values in plotting_dict.items():
                    if category == 'Driver':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            driver=key,
                            year=year)
                    if category == 'Team':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            team=key,
                            year=year)
                    x_values.append(key)
                    y_values.append(values[race_index])
                    bar_colors.append(colors['bg_color'])
                    bar_borders.append(colors['color'])
                zipped_lists = zip(
                    y_values,
                    x_values,
                    bar_colors,
                    bar_borders)
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
                            1 + (v / 50),
                            i,
                            str(round(v, 2)),
                            color=c[i],
                            fontweight='bold',
                            va='center',
                            fontsize=6)
                    else:
                        ax.text(
                            v + (v / 50),
                            i,
                            str(round(v, 2)),
                            color=c[i],
                            fontweight='bold',
                            va='center',
                            fontsize=6)
                ax.set_xlabel(
                    f'{plot} {units[index]}',
                    fontsize=10,
                    fontweight='bold',
                    color='black')
                ax.set_ylabel(
                    'Name',
                    fontsize=10,
                    fontweight='bold',
                    color='black')
                ax.tick_params(
                    axis='x',
                    labelsize=6,
                    labelrotation=45)
                ax.tick_params(
                    axis='y',
                    labelsize=6)
                ax.set_title(
                    f'{race} {category} {plot}',
                    fontsize=14,
                    fontweight='bold',
                    color='black')
                ax.xaxis.set_minor_locator(AutoMinorLocator())
                fig.tight_layout()
                plt.savefig(
                    out_file,
                    bbox_inches='tight')
                plt.close(fig)
                plt.cla()
    categories = ['Driver', 'Team']
    for category in categories:
        plots = [
            'Sum Points',
            'Average Points Per Value',
            'Average Points']
        units = ['[#]', '[#/$M]', '[#]', '[$M]']
        for index, plot in enumerate(plots):
            out_file = Path(f'{out_path}/{race}_{category}_{plot}.png')
            if out_file.is_file():
                pass
            else:
                plotting_dict = statistics_dictionary[f'{category} {plot}']
                fig, ax = plt.subplots(
                    nrows=1,
                    ncols=1,
                    figsize=[
                        cm_to_inches(cm=15),
                        cm_to_inches(cm=9)],
                    dpi=600)
                for key, values in plotting_dict.items():
                    if category == 'Driver':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            driver=key,
                            year=year)
                    if category == 'Team':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            team=key,
                            year=year)
                    x_values = races
                    y_values = [values[i] for i in range(len(x_values))]
                    ax.plot(
                        x_values,
                        y_values,
                        label=f'{key}',
                        marker='o',
                        linestyle=colors['linestyle'],
                        c=colors['bg_color'],
                        mfc=colors['color'],
                        markersize=4,
                        lw=2)
                ax.legend(
                    loc=0,
                    ncol=2,
                    prop={'size': 6})
                ax.grid(True)
                ax.set_xlabel(
                    'Races',
                    fontsize=10,
                    fontweight='bold',
                    color='black')
                ax.set_ylabel(
                    f'{plot} {units[index]}',
                    fontsize=10,
                    fontweight='bold',
                    color='black')
                ax.tick_params(
                    axis='x',
                    labelsize=6,
                    labelrotation=90)
                ax.tick_params(
                    axis='y',
                    labelsize=6)
                ax.set_title(
                    f'{race} {category} {plot}',
                    fontsize=14,
                    fontweight='bold',
                    color='black')
                ax.xaxis.set_minor_locator(AutoMinorLocator())
                ax.yaxis.set_minor_locator(AutoMinorLocator())
                fig.tight_layout()
                plt.savefig(
                    out_file,
                    bbox_inches='tight')
                plt.close(fig)
                plt.cla()


def prizes_bars(category_dictionary : dict,
                race_index : int,
                race : str,
                year : str,
                format_dir : str,
                out_path : str,
                title : str) -> None:
    """
    Function Details
    ================
    Plot top 10 and bottom 10 managers weekly.

    Plot top 10 and bottom 10 manager teams for specified races.

    Parameters
    ----------
    category_dictionary: dictionary
        Manager results dictionary.
    race_index: int
        Integer of races array for which to plot.
    year, race, format_dir, out_path, title: string
        Year to process. Race name, path to format directory, path to save.
        Graph title.

    Returns
    -------
    None

    See Also
    --------
    plotting_colour
    league_bars

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    03/04/2024
    ----------
    Copied from old code with updated documentation.

    """
    out_file = Path(f'{out_path}/{race}_SpotPrize_Bar.png')
    if out_file.is_file():
        pass
    else:
        fig, ax = plt.subplots(
            nrows=1,
            ncols=1,
            figsize=[
                cm_to_inches(cm=15),
                cm_to_inches(cm=9)],
            dpi=600)
        x_values = []
        y_values = []
        bar_colors = []
        bar_borders = []
        for manager, teams in category_dictionary.items():
            for team, values in teams.items():
                x_values.append(team)
                y_values.append(values[race_index])
                colors = plotting_colour(
                    format_dir=format_dir,
                    manager_team=team,
                    year=year)
                bar_colors.append(colors['bg_color'])
                bar_borders.append(colors['color'])
        zipped_lists = zip(
            y_values,
            x_values,
            bar_colors,
            bar_borders)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs[0: 10])
        top_x, top_y, top_c, top_b = [list(tuple) for tuple in tuples]
        top_x.append(0)
        top_y.append('⋮')
        top_c.append('k')
        top_b.append('k')
        tuples = zip(*sorted_pairs[-10:])
        bot_x, bot_y, bot_c, bot_b = [list(tuple) for tuple in tuples]
        x = np.concatenate((top_x, bot_x))
        y = np.concatenate((top_y, bot_y))
        c = np.concatenate((top_c, bot_c))
        b = np.concatenate((top_b, bot_b))
        ax.barh(
            y,
            x,
            color=c,
            edgecolor=b)
        for i, v in enumerate(x):
            if v < 0:
                ax.text(
                    1 + (v / 50),
                    i,
                    str(round(v, 2)),
                    fontweight='bold',
                    va='center',
                    fontsize=6)
            elif v == 0:
                pass
            else:
                ax.text(
                    v + (v / 50),
                    i,
                    str(round(v, 2)),
                    fontweight='bold',
                    va='center',
                    fontsize=6)
        ax.set_ylabel(
            'Team',
            fontsize=10,
            fontweight='bold',
            color='black')
        ax.set_xlabel(
            'Points [#]',
            fontsize=10,
            fontweight='bold',
            color='black')
        ax.tick_params(
            axis='x',
            labelsize=6,
            labelrotation=45)
        ax.tick_params(
            axis='y',
            labelsize=6)
        ax.set_title(
            f'{title}',
            fontsize=14,
            fontweight='bold',
            color='black')
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        fig.tight_layout()
        plt.savefig(
            out_file,
            bbox_inches='tight')
        plt.close(fig)
        plt.cla()


def prize_lines(results_dictionary : dict,
                race : str,
                prize : str,
                races : list,
                format_dir : str,
                year : str,
                out_path : str) -> None:
    """
    Function Details
    ================
    Plot season achievement graphs.

    Parameters
    ----------
    results_dictionary: dictionary
        Manager results dictionary.
    races: list
        List of races.
    race, format_dir, year, out_path, prize: string
        Race name, format directory, year for colours, path to save. Prize name.

    Returns
    -------
    None.

    See Also
    --------
    plotting_colour

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    17/04/2024
    ----------
    Created.

    05/05/2024
    ----------
    Update to tick labels for y axis on standard plots.

    """
    categories = ['Sum Points', 'Average Points']
    units = ['[#]', '[#]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_{prize}_{category}.png')
        if out_file.is_file():
            pass
        else:
            category_dict = results_dictionary[f'{category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            lines = []
            for manager, teams in category_dict.items():
                for team, values in teams.items():
                    x_values.append(races)
                    y_values.append([values[i] for i in range(len(races))])
                    colours = plotting_colour(
                        format_dir=format_dir,
                        manager_team=team,
                        year=year)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    names.append(team)
                    lines.append(colours['linestyle'])
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                markers,
                names,
                lines)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs[0: 10])
            top_y, top_x, top_c, top_m, top_n, top_l = [
                list(tuple) for tuple in tuples]
            tuples = zip(*sorted_pairs[-10:])
            bot_y, bot_x, bot_c, bot_m, bot_n, bot_l = [
                list(tuple) for tuple in tuples]
            x = np.concatenate((top_x, bot_x))
            y = np.concatenate((top_y, bot_y))
            c = np.concatenate((top_c, bot_c))
            m = np.concatenate((top_m, bot_m))
            n = np.concatenate((top_n, bot_n))
            l = np.concatenate((top_l, bot_l))
            for i in range(len(x)):
                ax.plot(
                    x[i],
                    y[i],
                    label=n[i],
                    marker='o',
                    linestyle=l[i],
                    c=c[i],
                    mfc=m[i],
                    markersize=4,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 6})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=90)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'{race} {prize} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)


def f1play_line(results_dictionary : dict,
                races : list,
                race : str,
                format_dir : str,
                year : str,
                out_path : str) -> None:
    """
    Function Details
    ================
    Plot f1 play results.

    Parameters
    ----------
    results_dictionary: dictionary
        Manager results dictionary.
    races: list
        List of races.
    race, format_dir, year, out_path: string
        Race name, format directory, year for colours, path to save.

    Returns
    -------
    None.

    See Also
    --------
    plotting_colour

    Notes
    -----
    None.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    18/04/2024
    ----------
    Created.

    05/05/2024
    ----------
    Update to y axis tick labels on standard plots.

    """
    categories = ['Points', 'Sum Points', 'Average Points']
    units = ['[#]', '[#]', '[#]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{race}_F1Play_{category}.png')
        if out_file.is_file():
            pass
        else:
            category_dict = results_dictionary[f'{category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[
                    cm_to_inches(cm=15),
                    cm_to_inches(cm=9)],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            for manager, values in category_dict.items():
                x_values.append(races)
                y_values.append([values[i] for i in range(len(races))])
                colours = plotting_colour(
                    format_dir=format_dir,
                    manager=manager,
                    year=year)
                colors.append(colours['bg_color'])
                markers.append(colours['bg_color'])
                names.append(manager)
            zipped_lists = zip(
                y_values,
                x_values,
                colors,
                markers,
                names)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs)
            y, x, c, m, n = [
                list(tuple) for tuple in tuples]
            for i in range(len(x)):
                ax.plot(
                    x[i],
                    y[i],
                    label=n[i],
                    marker='o',
                    linestyle='solid',
                    c=c[i],
                    mfc=m[i],
                    markersize=4,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 6})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=10,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=6,
                labelrotation=90)
            ax.tick_params(
                axis='y',
                labelsize=6)
            ax.set_title(
                f'F1 Play {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()


def pos_gained_bars(results_dictionary : dict,
                    race_index : int,
                    race : str,
                    format_dir : str,
                    year : str,
                    out_path : str) -> None:
    """
    Function Details
    ================
    Plot the positions gained and lost by manager teams per race week.

    Parameters
    ----------
    results_dictionary: dictionary
        Manager team positions gained.
    race_index: int
        Integer of races array for which to plot.
    race, format_dir, year out_path: string
        Race name, path to format directory, year for colours, path to save.

    Returns
    -------
    None.

    See Also
    --------
    plotting_colour

    Notes
    -----
    None.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    09/05/2024
    ----------
    Copied from league_bars and changed to fit the purpose.

    """
    out_file = Path(f'{out_path}/{race}_LeagueTeams_PositionsGained_Bar.png')
    if out_file.is_file():
        pass
    else:
        fig, ax = plt.subplots(
            nrows=1,
            ncols=1,
            figsize=[
                cm_to_inches(cm=15),
                cm_to_inches(cm=9)],
            dpi=600)
        x_values = []
        y_values = []
        bar_colors = []
        bar_borders = []
        for manager, teams in results_dictionary.items():
            for team, values in teams.items():
                x_values.append(team)
                y_values.append(values[race_index])
                colors = plotting_colour(
                    format_dir=format_dir,
                    manager_team=team,
                    year=year)
                bar_colors.append(colors['bg_color'])
                bar_borders.append(colors['color'])
        zipped_lists = zip(
            y_values,
            x_values,
            bar_colors,
            bar_borders)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs[0: 10])
        top_x, top_y, top_c, top_b = [list(tuple) for tuple in tuples]
        top_x.append(0)
        top_y.append('⋮')
        top_c.append('k')
        top_b.append('k')
        tuples = zip(*sorted_pairs[-10:])
        bot_x, bot_y, bot_c, bot_b = [list(tuple) for tuple in tuples]
        x = np.concatenate((top_x, bot_x))
        y = np.concatenate((top_y, bot_y))
        c = np.concatenate((top_c, bot_c))
        b = np.concatenate((top_b, bot_b))
        ax.barh(
            y,
            x,
            color=c,
            edgecolor=b)
        for i, v in enumerate(x):
            if v < 0:
                ax.text(
                    1 + (v / 50),
                    i,
                    str(round(v, 2)),
                    fontweight='bold',
                    va='center',
                    fontsize=6)
            elif v == 0:
                pass
            else:
                ax.text(
                    v + (v / 50),
                    i,
                    str(round(v, 2)),
                    fontweight='bold',
                    va='center',
                    fontsize=6)
        ax.set_ylabel(
            'Team',
            fontsize=10,
            fontweight='bold',
            color='black')
        ax.set_xlabel(
            'Positions Gained [#]',
            fontsize=10,
            fontweight='bold',
            color='black')
        ax.tick_params(
            axis='x',
            labelsize=6,
            labelrotation=45)
        ax.tick_params(
            axis='y',
            labelsize=6)
        ax.set_title(
            f'League Teams {race} Positions Gained',
            fontsize=14,
            fontweight='bold',
            color='black')
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        fig.tight_layout()
        plt.savefig(
            out_file,
            bbox_inches='tight')
        plt.close(fig)
        plt.cla()

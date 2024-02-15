import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from src.formats import drivers_colours, team_colour
from src.formats import managers_colour, manager_team_colour, perk_colour
from matplotlib.ticker import MultipleLocator, AutoMinorLocator


def plotting_colour(format_dir : str,
                    driver=False,
                    team=False,
                    manager_team=False,
                    manager=False,
                    perk=False) -> dict:
    """
    Uses format dictionaries to create marker and line colors.

    Takes data from format dictionaries to create the marker and line colors for
    the teams and drivers on the plot.

    Parameters
    ----------
    format_dir : string
        Path to formats directory.
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

    """
    colors_dict = {}
    if driver:
        format_dict = drivers_colours(
            format_dir=format_dir,
            driver=driver)
        colors_dict.update({'color': format_dict['color']})
        colors_dict.update({'bg_color': format_dict['bg_color']})
        if driver == (format_dict['drivers'])[0]:
            colors_dict.update({'linestyle': 'solid'})
        elif driver == (format_dict['drivers'])[1]:
            colors_dict.update({'linestyle': 'dashed'})
        elif driver == (format_dict['drivers'])[2]:
            colors_dict.update({'linestyle': 'dashdot'})
        else:
            colors_dict.update({'linestyle': 'dotted'})
    if team:
        format_dict = team_colour(
            format_dir=format_dir,
            team=team)
        colors_dict.update({'color': format_dict['color']})
        colors_dict.update({'bg_color': format_dict['bg_color']})
        colors_dict.update({'linestyle': '-'})
    if manager_team:
        format_dict = manager_team_colour(
            format_dir=format_dir,
            team=manager_team)
        colors_dict.update({'bg_color': format_dict['bg_color']})
        if manager_team == (format_dict['teams'])[0]:
            colors_dict.update({'color': format_dict['color'][0]})
            colors_dict.update({'linestyle': 'solid'})
        elif manager_team == (format_dict['teams'])[1]:
            colors_dict.update({'color': format_dict['color'][1]})
            colors_dict.update({'linestyle': 'dashed'})
        elif manager_team == (format_dict['teams'])[2]:
            colors_dict.update({'color': format_dict['color'][2]})
            colors_dict.update({'linestyle': 'dashdot'})
        elif manager_team == (format_dict['teams'])[3]:
            colors_dict.update({'color': format_dict['color'][3]})
            colors_dict.update({'linestyle': 'solid'})
        elif manager_team == (format_dict['teams'])[4]:
            colors_dict.update({'color': format_dict['color'][4]})
            colors_dict.update({'linestyle': 'dashed'})
        else:
            colors_dict.update({'color': format_dict['color'][5]})
            colors_dict.update({'linestyle': 'dashdot'})
    if manager:
        format_dict = managers_colour(
            format_dir=format_dir,
            manager=manager)
        colors_dict.update({'bg_color': format_dict['bg_color']})
    if perk:
        format_dict = perk_colour(
            format_dir=format_dir,
            perk=perk)
        colors_dict.update({'bg_color': format_dict['bg_color']})
        colors_dict.update({'color': format_dict['color']})
    return colors_dict


def results_bar(results_dictionary : dict,
                race_index : int,
                race : str,
                format_dir : str,
                out_path : str) -> None:
    """
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
    race, format_dir, out_path : string
        Race name. Path to format directory. Path to save.
    
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
                    figsize=[10, 7],
                    dpi=600)
                x_values = []
                y_values = []
                bar_colors = []
                bar_borders = []
                for key, values in plotting_dict.items():
                    if category == 'Driver':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            driver=key)
                    if category == 'Team':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            team=key)
                    x_values.append(key)
                    if index == 0:
                        y_values.append(values[race_index])
                    if index == 1:
                        if race_index == 0:
                            y_values.append(values[race_index])
                        else:
                            y_values.append(values[race_index - 1])
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
                            va='center')
                    else:
                        ax.text(
                            v + (v / 50),
                            i,
                            str(round(v, 2)),
                            color=c[i],
                            fontweight='bold',
                            va='center')
                ax.set_xlabel(
                    f'{plot} {units[index]}',
                    fontsize=15,
                    fontweight='bold',
                    color='black')
                ax.set_ylabel(
                    'Name',
                    fontsize=15,
                    fontweight='bold',
                    color='black')
                ax.tick_params(
                    axis='x',
                    labelsize=14,
                    labelrotation=45)
                ax.tick_params(
                    axis='y',
                    labelsize=14)
                ax.set_title(
                    f'{race} {category} {plot}',
                    fontsize=14,
                    fontweight='bold',
                    color='black')
                ax.xaxis.set_major_locator(MultipleLocator(10))
                ax.xaxis.set_minor_locator(AutoMinorLocator())
                fig.tight_layout()
                plt.savefig(
                    out_file,
                    bbox_inches='tight')
                plt.close(fig)
                plt.cla()
                fig.clf()


def lineupstats(statistics_dictionary : dict,
                race_index : float,
                races : list,
                race : str,
                format_dir : str,
                out_path : str) -> None:
    """
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
    Race, format_dir, out_path: string
        Current race name, path to formats directory, path to save.
    
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
                    figsize=[10, 7],
                    dpi=600)
                x_values = []
                y_values = []
                bar_colors = []
                bar_borders = []
                for key, values in plotting_dict.items():
                    if category == 'Driver':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            driver=key)
                    if category == 'Team':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            team=key)
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
                            va='center')
                    else:
                        ax.text(
                            v + (v / 50),
                            i,
                            str(round(v, 2)),
                            color=c[i],
                            fontweight='bold',
                            va='center')
                ax.set_xlabel(
                    f'{plot} {units[index]}',
                    fontsize=15,
                    fontweight='bold',
                    color='black')
                ax.set_ylabel(
                    'Name',
                    fontsize=15,
                    fontweight='bold',
                    color='black')
                ax.tick_params(
                    axis='x',
                    labelsize=14,
                    labelrotation=45)
                ax.tick_params(
                    axis='y',
                    labelsize=14)
                ax.set_title(
                    f'{race} {category} {plot}',
                    fontsize=14,
                    fontweight='bold',
                    color='black')
                fig.tight_layout()
                plt.savefig(
                    out_file,
                    bbox_inches='tight')
                plt.close(fig)
                plt.cla()
                fig.clf()
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
                    figsize=[10, 7],
                    dpi=600)
                for key, values in plotting_dict.items():
                    if category == 'Driver':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            driver=key)
                    if category == 'Team':
                        colors = plotting_colour(
                            format_dir=format_dir,
                            team=key)
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
                        markersize=8,
                        lw=2)
                ax.legend(
                    loc=0,
                    ncol=2,
                    prop={'size': 10})
                ax.grid(True)
                ax.set_xlabel(
                    'Races',
                    fontsize=15,
                    fontweight='bold',
                    color='black')
                ax.set_ylabel(
                    f'{plot} {units[index]}',
                    fontsize=15,
                    fontweight='bold',
                    color='black')
                ax.tick_params(
                    axis='x',
                    labelsize=14,
                    labelrotation=45)
                ax.tick_params(
                    axis='y',
                    labelsize=14)
                ax.set_title(
                    f'{race} {category} {plot}',
                    fontsize=14,
                    fontweight='bold',
                    color='black')
                fig.tight_layout()
                plt.savefig(
                    out_file,
                    bbox_inches='tight')
                plt.close(fig)
                plt.cla()
                fig.clf()


def leaguecount(results_dictionary : dict,
                race_index : int,
                race : str,
                races : list,
                format_dir : str,
                out_path : str) -> None:
    """
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
    race, format_dir, out_path:
        Race name, format directory, path to save.
    
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

    """
    categories = ['Drivers', 'Constructors', 'DRS Boost', 'Extra DRS', 'Perks']
    for category in categories:
        out_file = Path(f'{out_path}/{race}_LeagueCounts_{category}_Bar.png')
        if out_file.is_file():
            pass
        else:
            category_dict = results_dictionary[f'League {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[10, 7],
                dpi=600)
            x_values = []
            y_values = []
            bar_colors = []
            bar_borders = []
            for name, count in category_dict.items():
                if category == 'Drivers':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        driver=name)
                    bar_colors.append(colours['bg_color'])
                    bar_borders.append(colours['color'])
                    x_values.append(name)
                    y_values.append(count[race_index])
                elif category == 'Constructors':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        team=name)
                    bar_colors.append(colours['bg_color'])
                    bar_borders.append(colours['color'])
                    x_values.append(name)
                    y_values.append(count[race_index])
                elif category == 'DRS Boost':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        driver=name)
                    bar_colors.append(colours['bg_color'])
                    bar_borders.append(colours['color'])
                    x_values.append(name)
                    y_values.append(count[race_index])
                elif category == 'Extra DRS':
                    if name == '0':
                        pass
                    else:
                        colours = plotting_colour(
                            format_dir=format_dir,
                            driver=name)
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
                            perk=name)
                        bar_colors.append(colours['bg_color'])
                        bar_borders.append(colours['color'])
                        x_values.append(name)
                        y_values.append(count[race_index])
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
                        va='center')
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center')
            ax.set_ylabel(
                'Names',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'{category} [#]',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League {race} {category} Count',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.xaxis.set_major_locator(MultipleLocator(20))
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()
        out_file = Path(f'{out_path}/{race}_LeagueSumCounts_{category}.png')
        if out_file.is_file():
            pass
        else:
            category_dict = results_dictionary[f'League Sum {category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[10, 7],
                dpi=600)
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            lines = []
            for name, count in category_dict.items():
                if category == 'Drivers':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        driver=name)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    x_values.append(races)
                    y_values.append([count[i] for i in range(len(races))])
                    names.append(name)
                    lines.append(colours['linestyle'])
                elif category == 'Constructors':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        team=name)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    x_values.append(races)
                    y_values.append([count[i] for i in range(len(races))])
                    names.append(name)
                    lines.append(colours['linestyle'])
                elif category == 'DRS Boost':
                    colours = plotting_colour(
                        format_dir=format_dir,
                        driver=name)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    x_values.append(races)
                    y_values.append([count[i] for i in range(len(races))])
                    names.append(name)
                    lines.append(colours['linestyle'])
                elif category == 'Extra DRS':
                    if name == '0':
                        pass
                    else:
                        colours = plotting_colour(
                            format_dir=format_dir,
                            driver=name)
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
                            perk=name)
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
                    markersize=8,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 10})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} [#]',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League {race} {category} Sum Counts',
                fontsize=14,
                fontweight='bold',
                color='black')
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()


def league_bars(results_dictionary : dict,
                race_index : int,
                race : str,
                format_dir : str,
                out_path : str) -> None:
    """
    Plot top 10 and bottom 10 managers weekly.

    Plot top 10 and bottom 10 manager teams for each race.

    Parameters
    ----------
    results_dictionary: dictionary
        Manager results dictionary.
    race_index: int
        Integer of races array for which to plot.
    race, format_dir, out_path: string
        Race name, path to format directory, path to save.
    
    See Also
    --------
    plotting_colour

    Notes
    -----
    None

    Example
    -------
    None

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
                figsize=[10, 7],
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
                        manager_team=team)
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
                        va='center')
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center')
            ax.set_ylabel(
                'Team',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'{category} {unit}',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League Teams {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.xaxis.set_major_locator(MultipleLocator(50))
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.set_xlim(min(x) - 30, max(x) + 30)
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()
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
                figsize=[10, 7],
                dpi=600)
            x_values = []
            y_values = []
            bar_colors = []
            bar_borders = []
            for manager, values in category_dict.items():
                colours = plotting_colour(
                    format_dir=format_dir,
                    manager=manager)
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
                        va='center')
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center')
            ax.set_ylabel(
                'Manager',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'{category} {unit}',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            ax.xaxis.set_major_locator(MultipleLocator(a))
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.set_xlim(min(x) - 30, max(x) + 30)
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()


def leagueteam_stat(statistics_dictionary : dict,
                    races : list,
                    race : str,
                    format_dir : str,
                    out_path : str) -> None:
    """
    Plot league statistics.

    Plot league teams and manager statistics.

    Parameters
    ----------
    statistics_dictionary: dictionary
        Manager statistics dictionary.
    races: list
        List of races.
    race, format_dir, out_path: string
        Race name, format directory, path to save.
    
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
                figsize=[10, 7],
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
                    manager=manager)
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
                    markersize=8,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 10})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()
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
                figsize=[10, 7],
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
                    manager=manager)
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
                    markersize=8,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 10})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()
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
                figsize=[10, 7],
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
                        manager_team=team)
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
                    markersize=8,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 10})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League Teams {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()


def leagueteam_ppvs(statistics_dictionary : dict,
                    race_index : int,
                    races : list,
                    race : str,
                    format_dir : str,
                    out_path : str) -> None:
    """
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
    race, format_dir, out_path: string
        Race name, format directory, path to save.
    
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
                figsize=[10, 7],
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
                    manager=manager)
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
                    markersize=8,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 10})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()
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
                figsize=[10, 7],
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
                        manager_team=team)
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
                    markersize=8,
                    lw=2)
            ax.legend(
                loc=0,
                ncol=2,
                prop={'size': 10})
            ax.grid(True)
            ax.set_xlabel(
                'Races',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_ylabel(
                f'{category} {unit}',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League Teams {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()
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
                figsize=[10, 7],
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
                    manager=manager)
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
                        va='center')
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center')
            ax.set_ylabel(
                'Name',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'{category} {unit}',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League Managers {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()
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
                figsize=[10, 7],
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
                        manager_team=team)
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
                        va='center')
                elif v == 0:
                    pass
                else:
                    ax.text(
                        v + (v / 50),
                        i,
                        str(round(v, 2)),
                        fontweight='bold',
                        va='center')
            ax.set_ylabel(
                'Names',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.set_xlabel(
                f'{category} {unit}',
                fontsize=15,
                fontweight='bold',
                color='black')
            ax.tick_params(
                axis='x',
                labelsize=14,
                labelrotation=45)
            ax.tick_params(
                axis='y',
                labelsize=14)
            ax.set_title(
                f'League Teams {race} {category}',
                fontsize=14,
                fontweight='bold',
                color='black')
            fig.tight_layout()
            plt.savefig(
                out_file,
                bbox_inches='tight')
            plt.close(fig)
            plt.cla()
            fig.clf()

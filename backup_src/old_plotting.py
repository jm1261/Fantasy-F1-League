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

import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from src.filepaths import check_dir_exists
from matplotlib.ticker import AutoMinorLocator
from src.formats import (
    drivers_colours,
    team_colour,
    managers_colour,
    manager_team_colour,
    perk_colour)


def plotting_colors(format_dir : str,
                    year : str,
                    driver=None,
                    team=None,
                    manager_team=None,
                    manager=None,
                    perk=None) -> dict:
    """
    Function Details
    ================
    Determine plotting colors based on input.

    Takes data from format dictionaries to create the marker and line colors for
    the teams and drivers on the plot.

    Parameters
    ----------
    format_dir, year: string
        Path fo formats directory. Year for color codes.
    driver, team, manager_team, manager, perk: str or None
        Specific entity for which colors are being selected.

    Returns
    -------
    dict
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
    Uses specific formatting functions to determine the plotting colors for
    drivers, teams, managers, and perks.

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

    24/07/2024
    ----------
    Streamlined rewrite.

    """
    colors_dictionary = {}


    def get_format_dict(subdir : str,
                        entity,
                        entity_type) -> dict:
        """
        Function Details
        ================
        Retrieve the format dictionary for a given entity type.

        Parameters
        ----------
        format_dir, subdir, entity, entity_type, year: string
            Path to the main formats directory. Subdirectory within the format
            directory. The specific entity (driver, team, manager, etc.) for
            which the format is being retrieved. Type of the entity ('driver',
            'team', 'manager_team', 'manager', 'perk'). Year for color codes, if
            applicable.

        Returns
        -------
        dict
            Format dictionary containing the colors and styles for the specified
            entity.

        See Also
        --------
        drivers_colours
        team_colour
        manager_team_colour
        managers_colour
        perk_colour

        Notes
        -----
        None.

        Example
        -------
        None.

        ------------------------------------------------------------------------
        Update History
        ==============

        24/07/2024
        ----------
        Created.

        """
        return {
            'driver': drivers_colours,
            'team': team_colour,
            'manager_team': manager_team_colour,
            'manager': managers_colour,
            'perk': perk_colour
        }[entity_type](
            format_dir=Path(f'{format_dir}/{subdir}'),
            **{entity_type: entity, 'year': year})


    if driver:
        format_dict = get_format_dict(
            subdir='Lineup_Formats',
            entity=driver,
            entity_type='driver'
        )
        style = ['solid', 'dashed', 'dashdot', 'dotted']
        colors_dictionary.update({
            'color': format_dict['color'],
            'bg_color': format_dict['bg_color'],
            'linestyle': style[format_dict['drivers'].index(f'{driver}')]
        })

    if team:
        format_dict = get_format_dict(
            subdir='Lineup_Formats',
            entity=team,
            entity_type='team'
        )
        colors_dictionary.update({
            'color': format_dict['color'],
            'bg_color': format_dict['bg_color'],
            'linestyle': '-'
        })

    if manager_team:
        format_dict = get_format_dict(
            subdir='Manager_Formats',
            entity=manager_team,
            entity_type='manager_team'
        )
        team_styles = [
            ('red', 'solid'), ('yellow', 'dashed'), ('blue', 'dashdot'),
            ('blue', 'solid'), ('yellow', 'dashed'), ('red', 'dashdot'),
            ('red', 'solid'), ('yellow', 'dashed'), ('blue', 'dashdot'),
            ('blue', 'solid')
        ]
        color, linestyle = team_styles[
            format_dict['teams'].index(manager_team) % len(team_styles)
        ]
        colors_dictionary.update({
            'color': color,
            'bg_color': format_dict['bg_color'],
            'linestyle': linestyle
        })

    if manager:
        format_dict = get_format_dict(
            subdir='Manager_Formats',
            entity=manager,
            entity_type='manager'
        )
        colors_dictionary.update({
            'bg_color': format_dict['bg_color']
        })

    if perk:
        format_dict = get_format_dict(
            subdir='Lineup_Formats',
            entity=perk,
            entity_type='perk'
        )
        colors_dictionary.update({
            'color': format_dict['color'],
            'bg_color': format_dict['bg_color']
        })

    return colors_dictionary


def sort_tuples(arrays : list):
    """
    Function Details
    ================
    Concatenates and sorts an array of nested arrays for top and bottom by
    given index.

    Parameters
    ----------
    arrays: list
        An array of nested arrays, with the first array as the array to sort.

    Returns
    -------
    tuples: list[NDArray]
        Sorted arrays.

    See Also
    --------
    None.

    Notes
    -----
    None.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    31/07/2024
    ----------
    Created.

    """
    # Ensure all arrays are of the same length
    min_length = min(len(arr) for arr in arrays)
    data_arrays = [arr[:min_length] for arr in arrays]

    # Zip arrays together
    zipped_lists = zip(*data_arrays)

    # Sort based on the first array
    sorted_arrays = sorted(zipped_lists)

    # Create tuples
    tuples = zip(*sorted_arrays)

    return tuples


def sort_top_tuples(arrays : list,
                    index : int):
    """
    Function Details
    ================
    Concatenates and sorts an array of nested arrays for top and bottom by
    given index.

    Parameters
    ----------
    arrays: list
        An array of nested arrays, with the first array as the array to sort.
    index: integer
        Index at which to slice the top and bottom parts of the array.

    Returns
    -------
    concatenated: list[NDArray]
        Sorted and concatenated arrays.

    See Also
    --------
    None.

    Notes
    -----
    None.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    31/07/2024
    ----------
    Created.

    """
    # Ensure all arrays are of the same length
    min_length = min(len(arr) for arr in arrays)
    data_arrays = [arr[:min_length] for arr in arrays]

    # Zip arrays together
    zipped_lists = zip(*data_arrays)

    # Sort based on the first array
    sorted_arrays = sorted(zipped_lists)

    # Unzip the first x and last x elements
    top_elements = list(zip(*sorted_arrays[: index]))
    bottom_elements = list(zip(*sorted_arrays[-index:]))

    # Initialise lists for top and bottom values
    top = [[] for _ in data_arrays]
    bottom = [[] for _ in data_arrays]

    # Extract top elements
    for i, elements in enumerate(top_elements):
        top[i] = list(elements)

    # Add a separator
    top.append([0, ':', 'k', 'k'])

    # Extract bottom elements
    for i, elements in enumerate(bottom_elements):
        bottom[i] = list(elements)

    # Concatenate the top and bottom elements
    concatenated = [np.concatenate((t, b)) for t, b in zip(top, bottom)]
    return concatenated


class Plot:
    """
    Class Details
    =============
    Style guide for plotting line graphs, bar graphs, and pie charts. Includes
    style dictionary.

    Functions
    ---------
    __init__(self, out_path : str, format_dir : str, year : str,
            plot_style : dict = None)
    save_fig(self, fig : object, out_file : str)
    append_data(self, name : str, count : int, category_type : dict,
                race_index : int)
    append_sum_data(self, name : str, count : int, category_type : dict,
                    races : list)
    bar_spacing(self, data : list)
    barplot(self, x : list, y : list, colors : list, borders : list,
            xlabel : str, ylabel : str, title : str, out_file : str,
            **kwargs : dict)
    lineplt(self, x : list, y : list, colors : list, markers : list,
            labels : list, xlabel : str, ylabel : str, title : str,
            out_file : str, **kwargs : dict)
    pieplot(self, data : list, labels : list, title : str, out_file : str,
            colors=None, explode=None, **kwargs : dict)

    Notes
    -----
    Plot class for use in LeaguePlot class method.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    31/07/2024
    ----------
    Created.

    02/08/2024
    ----------
    Added append_data, append_sum_data, and bar_spacing for better functionality
    and adaptability.

    """


    def __init__(
            self,
            out_path : str,
            format_dir : str,
            year : str,
            plot_style : dict = None) -> None:
        """
        Function Details
        ================
        Initialise class Plot.

        Parameters
        ----------
        self: self
        out_path, format_dir, year: string
            Path to save, path to formats, year as a string.
        plot_style: dictionary, optional
            Dictionary containing style attributes.
            {
                "": ,
            }

        Returns
        -------
        None.

        See Also
        --------
        None.

        Notes
        -----
        If plot_style does not exist, defaults to default_style.

        Example
        -------
        None.

        ------------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Created.

        07/08/2024
        ----------
        Added check_dir_exists to ensure that the out_path is a path.

        """
        self.out_path = out_path
        self.format_dir = format_dir
        self.year = year
        self.default_style = {
            "nrows": 1,
            "ncols": 1,
            "dpi": 600,
            "fig_height": 15,
            "fig_width": 9,
            "fontweight" : "bold",
            "bar_fontsize": 6,
            'axis_fontsize': 10,
            'axis_label_color': 'black',
            'title_fontsize': 14,
            'title_color': 'black',
            'tick_size': 6,
            'marker': 'o',
            'linestyle': 'solid',
            'marker_size': 4,
            'line_width': 2,
            'legend_col': 2,
            'legend_size': 6,
            'auto_percentage': '%1.1f%%',
            'start_angle': 90,
            'label_rotation': 0
        }

        if plot_style:
            self.default_style.update(plot_style)

        check_dir_exists(dir_path=out_path)


    def cm_to_inches(self, cm : float) -> float:
        """
        Returns centimeters as inches.

        Parameters
        ----------
        cm : float
            Value in centimeters.

        Returns
        -------
        inches : float
            Value in inches.

        See Also
        --------
        None.

        Notes
        -----
        Returns value to 2 decimal places.

        Example
        -------
        >>> cm = 15
        >>> inches = cm_to_inches(cm=cm)
        >>> inches
        5.91

        ----------------------------------------------------------------------------
        Update History
        ==============

        24/07/2024
        ----------
        Update to documentation and conversion scalar.

        """
        return round(cm / 2.45, 2)


    


    def save_fig(
            self,
            fig : object,
            out_file : str) -> None:
        """
        Function Details
        ================
        Save figure out.

        Parameters
        ----------
        self: self
        fig: object
            Matplotlib figure.
        out_file: string
            Path to save.

        Returns
        -------
        None.

        See Also
        --------
        None.

        Notes
        -----
        Standard matplotlib save function.

        Example
        -------
        None.

        --------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Created.

        07/08/2024
        ----------
        Moved check if outfile is file to plotting code to reduce memory use.

        """
        outfile = Path(out_file)
        fig.tight_layout()
        plt.savefig(
            outfile,
            bbox_inches='tight')
        plt.close(fig)
        plt.cla()


    def append_data(self,
                    name : str,
                    count : int,
                    category_type : dict,
                    race_index : int) -> list:
        """
        Function Details
        ================
        Helper function to append data to lists based on category type. Intended
        for bar plots.

        Parameters
        ----------
        name: string
            Count name.
        count, race_index: integer
            Number of counts, race index.
        category_type: dictionary
            Category type dictionary containing key and name.

        Returns
        -------
        out_arrays: list
            List for bar graph plotting [y, x, bar colors, bar borders].

        See Also
        --------
        plotting_colors

        Notes
        -----
        None.

        Example
        -------
        None.

        ----------------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Created.

        """
        x_values = []
        y_values = []
        bar_colors = []
        bar_borders = []
        if name in ['None', 'Nonw']:
            return

        colors = plotting_colors(
            format_dir=self.format_dir,
            year=self.year,
            **category_type)
        bar_colors.append(colors['bg_color'])
        bar_borders.append(colors['color'])
        x_values.append(name)
        y_values.append(count[race_index])

        out_arrays = [y_values, x_values, bar_colors, bar_borders]
        return out_arrays


    def append_sum_data(self,
                        name : str,
                        count : int,
                        category_type : dict,
                        races : list) -> list:
        """
        Function Details
        ================
        Helper function to append data to lists based on category type. Intended
        for bar plots.

        Parameters
        ----------
        name: string
            Count name.
        count, race_index: integer
            Number of counts, race index.
        category_type: dictionary
            Category type dictionary containing key and name.
        races: list
            List of all completed races.

        Returns
        -------
        out_arrays: list
            List for bar graph plotting [y, x, bar colors, bar borders].

        See Also
        --------
        plotting_colors

        Notes
        -----
        None.

        Example
        -------
        None.

        ----------------------------------------------------------------------------
        Update History
        ==============

        01/08/2024
        ----------
        Created.

        """
        x_values = []
        y_values = []
        bar_colors = []
        bar_borders = []
        if name in ['None', 'Nonw']:
            return

        colors = plotting_colors(
            format_dir=self.format_dir,
            year=self.year,
            **category_type)
        bar_colors.append(colors['bg_color'])
        bar_borders.append(colors['color'])
        x_values.append(name)
        y_values.append([count[i] for i in range(len(races))])

        out_arrays = [y_values, x_values, bar_colors, bar_borders]
        return out_arrays


    def bar_spacing(self,
                    data : list) -> tuple:
        """
        Function Details
        ================
        Determine the required axis limits and text spacing depending on data
        magnitude.

        Parameters
        ----------
        data: list
            Data list.

        Returns
        -------
        margin, text_spacing: float
            Margin for axis limit. Text spacing parameter.

        See Also
        --------
        None.

        Notes
        -----
        None.

        Example
        -------
        None.

        ------------------------------------------------------------------------
        Update History
        ==============

        02/08/2024
        ----------
        Created.

        """
        data_range = max(data) - min(data)
        magnitude = (
            np.floor(np.log10(abs(data_range))) if data_range != 0 else 0)
        margin = max(0.05 * data_range, 0.1)
        text_spacing = 0.05 * (5 ** magnitude)
        return margin, text_spacing


    def barplot(self,
                x : list,
                y : list,
                colors : list,
                borders : list,
                xlabel : str,
                ylabel : str,
                title : str,
                out_file : str,
                **kwargs : dict) -> None:
        """
        Function Details
        ================
        Plot a bar graph for a collection of x-, y-data.

        Parameters
        ----------
        x, y, colors, borders: list
            x-data, y-data, data bar colors, data bar border colors.
        xlabel, ylabel, title, out_file: string
            x-axis label, y-axis label, title, save path.
        **kwargs : dictionary
            Additional keyword arguments for plot customisation.

        Returns
        -------
        None.

        See Also
        --------
        save_fig

        Notes
        -----
        Uses plot style or defaults.

        Example
        -------
        None.

        ------------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Created.

        02/08/2024
        ----------
        Added formatted text spacing and axis limits for bar plots of different
        data magnitude.

        """
        style = {**self.default_style, **kwargs}

        margin, text_spacing = self.bar_spacing(data=x)

        fig, ax = plt.subplots(
            nrows=style.get('nrows', 1),
            ncols=style.get('ncols', 1),
            figsize=[
                self.cm_to_inches(cm=style.get('fig_height', 15)),
                self.cm_to_inches(cm=style.get('fig_width', 9))],
            dpi=style.get('dpi', 600))
        ax.barh(
            y,
            x,
            color=colors,
            edgecolor=borders)
        for i, v in enumerate(x):
            if v < 0:
                ax.text(
                    0 + margin/2,
                    i,
                    str(round(v, 2)),
                    color=colors[i],
                    fontweight=style.get('fontweight', 'bold'),
                    va='center',
                    fontsize=style.get('bar_fontsize', 6))
            elif v == 0:
                pass
            else:
                ax.text(
                    v + margin/2,
                    i,
                    str(round(v, 2)),
                    color=colors[i],
                    fontweight=style.get('fontweight', 'bold'),
                    va='center',
                    fontsize=style.get('bar_fontsize', 6))
        ax.set_xlabel(
            xlabel,
            fontsize=style.get('axis_fontsize', 10),
            fontweight=style.get('fontweight', 'bold'),
            color=style.get('axis_label_color', 'black'))
        ax.set_ylabel(
            ylabel,
            fontsize=style.get('axis_fontsize', 10),
            fontweight=style.get('fontweight', 'bold'),
            color=style.get('axis_label_color', 'black'))
        ax.set_title(
            title,
            fontsize=style.get('title_fontsize', 14),
            fontweight=style.get('fontweight', 'bold'),
            color=style.get('title_color', 'black'))
        ax.tick_params(
            axis='x',
            labelsize=style.get('tick_size', 6),
            labelrotation=style.get('tick_rotation', 45))
        ax.tick_params(
            axis='y',
            labelsize=style.get('tick_size', 6))
        ax.set_xlim(
            min(x) - margin,
            max(x) + margin + text_spacing * style.get('bar_fontsize', 6))
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        self.save_fig(
            fig=fig,
            out_file=out_file)


    def lineplt(self,
                x : list,
                y : list,
                colors : list,
                markers : list,
                styles : list,
                labels : list,
                xlabel : str,
                ylabel : str,
                title : str,
                out_file : str,
                **kwargs : dict) -> None:
        """
        Function Details
        ================
        Plot a line graph for a collection of x-, y-data.

        Parameters
        ----------
        x, y, colors, markers, styles, labels: list
            x-data, y-data, data line colors, data marker styles, line styles,
            data labels.
        xlabel, ylabel, title, out_file: string
            x-axis label, y-axis label, title, save path.
        **kwargs : dictionary
            Additional keyword arguments for plot customisation.

        Returns
        -------
        None.

        See Also
        --------
        save_fig

        Notes
        -----
        Uses plot style or defaults.

        Example
        -------
        None.

        ------------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Created.

        """
        style = {**self.default_style, **kwargs}
        fig, ax = plt.subplots(
            nrows=style.get('nrows', 1),
            ncols=style.get('ncols', 1),
            figsize=[
                self.cm_to_inches(cm=style.get('fig_height', 15)),
                self.cm_to_inches(cm=style.get('fig_width', 9))],
            dpi=style.get('dpi', 600))
        for i in range(len(x)):
            ax.plot(
                x[i],
                y[i],
                label=labels[i],
                marker=style.get('marker', 'o'),
                linestyle=styles[i],
                color=colors[i],
                mfc=markers[i],
                markersize=style.get('marker_size', 4),
                lw=style.get('line_width', 2))
        ax.legend(
            loc=0,
            ncol=style.get('legend_col', 2),
            prop={'size': style.get('legend_size', 6)})
        ax.set_xlabel(
            xlabel,
            fontsize=style.get('axis_fontsize', 10),
            fontweight=style.get('fontweight', 'bold'),
            color=style.get('axis_label_color', 'black'))
        ax.set_ylabel(
            ylabel,
            fontsize=style.get('axis_fontsize', 10),
            fontweight=style.get('fontweight', 'bold'),
            color=style.get('axis_label_color', 'black'))
        ax.set_title(
            title,
            fontsize=style.get('title_fontsize', 14),
            fontweight=style.get('fontweight', 'bold'),
            color=style.get('title_color', 'black'))
        ax.tick_params(
            axis='x',
            labelsize=style.get('tick_size', 6),
            labelrotation=style.get('tick_rotation', 45))
        ax.tick_params(
            axis='y',
            labelsize=style.get('tick_size', 6))
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        self.save_fig(
            fig=fig,
            out_file=out_file)


    def pieplot(self,
                data : list,
                labels : list,
                title : str,
                out_file : str,
                colors=None,
                explode=None,
                **kwargs : dict) -> None:
        """
        Function Details
        ================
        Plot a pie chart for a collection of y-data.

        Parameters
        ----------
        data, labels,
            Data, data labels.
        numbers, colors, explode: list, optional
            Optional percentage indicator, optional color format, proportion to
            offset each slide. All default to None.
        title, out_file: string
            Figure title, path to save.
        **kwargs : dictionary
            Additional keyword arguments for plot customisation.

        Returns
        -------
        None.

        See Also
        --------
        save_fig

        Notes
        -----
        Uses plot style or defaults.

        Example
        -------
        None.

        ------------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Created.

        """
        style = {**self.default_style, **kwargs}
        fig, ax = plt.subplots(
            nrows=style.get('nrows', 1),
            ncols=style.get('ncols', 1),
            figsize=[
                self.cm_to_inches(cm=style.get('fig_height', 15)),
                self.cm_to_inches(cm=style.get('fig_width', 9))],
            dpi=style.get('dpi', 600))
        wedges, texts, autotexts = ax.pie(
            data,
            labels=labels,
            colors=colors,
            explode=explode,
            autopct=self.style.get('auto_percentage', '%1.1f%%'),
            startangle=self.style.get('start_angle', 90))
        plt.title(
            title,
            fontsize=style.get('title_fontsize', 14),
            fontweight=style.get('fontweight', 'bold'),
            color=style.get('title_color', 'black'))
        for text in texts:
            text.set_rotation(style.get('label_rotation', 45))
        self.save_fig(
            fig=fig,
            out_file=out_file)


class LeagueBars(Plot):
    """
    Class Details
    =============
    Functions for plotting league team and league manager bar graphs.

    Functions
    ---------
    league_team_bar(self, categories : list, units : list,
                    results_dictionary : dict, race_index : int, race : str,
                    sort_top : int=None)
    league_manager_bars(self, categories : list, units : list,
                        results_dictionary : dict, race_index : int, race : str,
                        sort_top : int=None)
    leaguecount(self, categories : list, results_dictionary : dict,
                race_index : int, race : str, races : list, sort_top : int=None,
                sum_arrays=False)

    Notes
    -----
    Plot class built on the Plot class method.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    31/07/2024
    ----------
    Created.

    """


    def league_team_bar(self,
                        categories : list,
                        units : list,
                        results_dictionary : dict,
                        race_index : int,
                        race : str,
                        sort_top : int=None) -> None:
        """
        Function Details
        ================
        Plot sorted manager teams for each race.

        Parameters
        ----------
        categories, units: list
            Category names (dictionary keys), corresponding axis label units.
        results_dictionary: dictionary
            Manager results dictionary.
        race_index: integer
            Integer of races array for which to plot.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        See Also
        --------
        plotting_colors
        bar_plot
        sort_top_tuples
        sort_tuples

        Notes
        -----
        Uses plot method.

        Example
        -------
        >>> results_dictionary = {}
        >>> race_index = 0
        >>> race = 'Race1'
        >>> format_dir = '/path/to/out_path'
        >>> year = '2024'
        >>> out_path = '/path/to/out_path'
        >>> races = ['Race1', 'Race2']
        >>> categories = ['Points', 'Values']
        >>> units = ['[#]', '[$M]']

        >>> league_plotter = LeagueBars(out_path, format_dir, year)
        >>> league_plotter.league_team_bar(
                categories,
                units,
                results_dictionary,
                race_index,
                race)

        ------------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Copied from previous league_bars function with new class method.

        07/08/2024
        ----------
        Added check if outfile is not file to reduce memory use.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                f'{self.out_path}/{race}_LeagueTeams_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Team {category}']
                x_values, y_values, bar_colors, bar_borders = [], [], [], []
                for manager, teams in category_dict.items():
                    for team, values in teams.items():
                        x_values.append(team)
                        y_values.append(values[race_index])
                        colors = plotting_colors(
                            self.format_dir,
                            manager_team=team,
                            year=self.year)
                        bar_colors.append(colors['bg_color'])
                        bar_borders.append(colors['color'])
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders],
                        index=sort_top)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders])
                x, y, c, b = sorted_arrays
                self.barplot(
                    x=x,
                    y=y,
                    colors=c,
                    borders=b,
                    xlabel=f'{category} {unit}',
                    ylabel='Team',
                    title=f'League Teams {race} {category}',
                    out_file=out_file)   


    def league_manager_bars(self,
                            categories : list,
                            units : list,
                            results_dictionary : dict,
                            race_index : int,
                            race : str,
                            sort_top : int=None) -> None:
        """
        Function Details
        ================
        Plot sorted managers weekly.

        Parameters
        ----------
        categories, units: list
            Category names (dictionary keys), corresponding axis label units.
        results_dictionary: dictionary
            Manager results dictionary.
        race_index: integer
            Integer of races array for which to plot.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        See Also
        --------
        plotting_colors
        bar_plot
        sort_top_tuples

        Notes
        -----
        Uses plot method.

        Example
        -------
        >>> results_dictionary = {}
        >>> race_index = 0
        >>> race = 'Race1'
        >>> format_dir = '/path/to/out_path'
        >>> year = '2024'
        >>> out_path = '/path/to/out_path'
        >>> races = ['Race1', 'Race2']
        >>> categories = ['Points', 'Values']
        >>> units = ['[#]', '[$M]']

        >>> league_plotter = LeagueBars(out_path, format_dir, year)
        >>> league_plotter.league_manager_bars(
                categories,
                units,
                results_dictionary,
                race_index,
                race)

        ------------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Copied from previous league_bars function with new class method.

        07/08/2024
        ----------
        Added check if outfile is not file to reduce memory use.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                f'{self.out_path}/{race}_LeagueManagers_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Manager {category}']
                x_values, y_values, bar_colors, bar_borders = [], [], [], []
                for manager, values in category_dict.items():
                    x_values.append(manager)
                    y_values.append(values[race_index])
                    colors = plotting_colors(
                        self.format_dir,
                        manager=manager,
                        year=self.year)
                    bar_colors.append(colors['bg_color'])
                    bar_borders.append(colors['bg_color'])
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders],
                        index=sort_top)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders])
                x, y, c, b = sorted_arrays
                self.barplot(
                    x=x,
                    y=y,
                    colors=c,
                    borders=b,
                    xlabel=f'{category} {unit}',
                    ylabel='Team',
                    title=f'Managers {race} {category}',
                    out_file=out_file)


    def leaguecount(self,
                    categories : list,
                    results_dictionary : dict,
                    race_index : int,
                    race : str,
                    races : list,
                    sort_top : int=None,
                    sum_arrays=False) -> None:
        """
        Function Details
        ================
        Plot driver, constructor, boost, extra, and perk counts.

        Parameters
        ----------
        categories, races: list
            Category names (dictionary keys). List of completed races.
        results_dictionary: dictionary
            Manager results dictionary.
        race_index: integer
            Integer of races array for which to plot.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.
        sum_arrays: Bool
            If true, plots sum of the count array.

        Returns
        -------
        None.

        See Also
        --------
        plotting_colors
        bar_plot
        sort_tuples

        Notes
        -----
        Uses plot method.

        Example
        -------
        >>> results_dictionary = {}
        >>> race_index = 0
        >>> race = 'Race1'
        >>> format_dir = '/path/to/out_path'
        >>> year = '2024'
        >>> out_path = '/path/to/out_path'
        >>> races = ['Race1', 'Race2']
        >>> categories = [
                'Driver',
                'Constructor',
                'DRS Boost',
                'Extra DRS',
                'Perks']

        >>> league_plotter = LeagueBars(out_path, format_dir, year)
        >>> league_plotter.leaguecount(
                categories,
                results_dictionary,
                race_index,
                race,
                races)

        ------------------------------------------------------------------------
        Update History
        ==============

        01/08/2024
        ----------
        Copied from previous leaguecount function with new class method.

        07/08/2024
        ----------
        Added check if outfile is not file to reduce memory use.

        """
        for category in categories:
            out_file = Path(
                f'{self.out_path}/{race}_LeagueCounts_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'League {category}']
                x_values, y_values, bar_colors, bar_borders = [], [], [], []
                for name, count in category_dict.items():
                    non_perk = [
                        'Driver',
                        'Constructor',
                        'DRS Boost',
                        'Extra DRS']
                    non_constructor = ['Driver', 'DRS Boost', 'Extra DRS']
                    if category in non_perk:
                        category_type = (
                            {'driver': name}
                            if category in non_constructor
                            else {'team': name})
                    elif category == 'Perks':
                        category_type = {'perk': name}
                    else:
                        continue
                    if sum_arrays:
                        arrays = self.append_sum_data(
                            name=name,
                            count=count,
                            category_type=category_type,
                            race_index=race_index,
                            races=races)
                    else:
                        arrays = self.append_data(
                            name=name,
                            count=count,
                            category_type=category_type,
                            race_index=race_index)
                    y, x, c, b = sorted_arrays
                    x_values.append(x)
                    y_values.append(y)
                    bar_colors.append(c)
                    bar_borders.append(b)
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders],
                        index=sort_top)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders])
                x, y, c, b = sorted_arrays
                if sorted_arrays:
                    title = f'League {race} {category} Sum Count'
                else:
                    title = f'League {race} {category} Count'
                self.barplot(
                    x=x,
                    y=y,
                    colors=c,
                    borders=b,
                    xlabel=f'Counts [#]',
                    ylabel=f'Names',
                    title=title,
                    out_file=out_file)


class LineupBars(Plot):
    """
    Class Details
    =============
    Functions for plotting lineup driver and constructor bar graphs.

    Functions
    ---------
    driver_bars(self, categories : list, units : list,
                results_dictionary : dict, race_index : int, race : str,
                sort_top : int=None)
    constructor_bar(self, categories : list, units : list,
                    results_dictionary : dict, race_index : int, race : str,
                    sort_top : int=None)

    Notes
    -----
    Plot class built on the Plot class method.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/08/2024
    ----------
    Created.

    """


    def driver_bars(self,
                    categories : list,
                    units : list,
                    results_dictionary : dict,
                    race_index : int,
                    race : str,
                    sort_top : int=None) -> None:
        """
        Function Details
        ================
        Plot sorted drivers for each race.

        Parameters
        ----------
        categories, units: list
            Category names (dictionary keys), corresponding axis label units.
        results_dictionary: dictionary
            Lineup results dictionary.
        race_index: integer
            Integer of races array for which to plot.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        See Also
        --------
        plotting_colors
        bar_plot
        sort_top_tuples
        sort_tuples

        Notes
        -----
        Uses plot method.

        Example
        -------
        >>> results_dictionary = {}
        >>> race_index = 0
        >>> race = 'Race1'
        >>> format_dir = '/path/to/out_path'
        >>> year = '2024'
        >>> out_path = '/path/to/out_path'
        >>> races = ['Race1', 'Race2']
        >>> categories = ['Points', 'Values']
        >>> units = ['[#]', '[$M]']

        >>> lineup_plotter = LineupBars(out_path, format_dir, year)
        >>> lineup_plotter.driver_bars(
                categories,
                units,
                results_dictionary,
                race_index,
                race)

        ------------------------------------------------------------------------
        Update History
        ==============

        01/08/2024
        ----------
        Copied from previous results_bar function with new class method.

        07/08/2024
        ----------
        Added check if outfile is not file to reduce memory use.

        """
        for category, unit in zip(categories, units):
            out_file = Path(f'{self.out_path}/{race}_Driver_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Driver {category}']
                x_values, y_values, bar_colors, bar_borders = [], [], [], []
                for driver, values in category_dict.items():
                    x_values.append(driver)
                    y_values.append(values[race_index])
                    colors = plotting_colors(
                        self.format_dir,
                        driver=driver,
                        year=self.year)
                    bar_colors.append(colors['bg_color'])
                    bar_borders.append(colors['color'])
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders],
                        index=sort_top)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders])
                x, y, c, b = sorted_arrays
                self.barplot(
                    x=x,
                    y=y,
                    colors=c,
                    borders=b,
                    xlabel=f'{category} {unit}',
                    ylabel='Driver',
                    title=f'Drivers {race} {category}',
                    out_file=out_file)


    def constructor_bar(self,
                        categories : list,
                        units : list,
                        results_dictionary : dict,
                        race_index : int,
                        race : str,
                        sort_top : int=None) -> None:
        """
        Function Details
        ================
        Plot sorted constructors for each race.

        Parameters
        ----------
        categories, units: list
            Category names (dictionary keys), corresponding axis label units.
        results_dictionary: dictionary
            Manager results dictionary.
        race_index: integer
            Integer of races array for which to plot.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        See Also
        --------
        plotting_colors
        bar_plot
        sort_top_tuples
        sort_tuples

        Notes
        -----
        Uses plot method.

        Example
        -------
        >>> results_dictionary = {}
        >>> race_index = 0
        >>> race = 'Race1'
        >>> format_dir = '/path/to/out_path'
        >>> year = '2024'
        >>> out_path = '/path/to/out_path'
        >>> races = ['Race1', 'Race2']
        >>> categories = ['Points', 'Values']
        >>> units = ['[#]', '[$M]']

        >>> lineup_plotter = LineupBars(out_path, format_dir, year)
        >>> lineup_plotter.constructor_bar(
                categories,
                units,
                results_dictionary,
                race_index,
                race)

        ------------------------------------------------------------------------
        Update History
        ==============

        01/08/2024
        ----------
        Copied from previous results_bar function with new class method.

        07/08/2024
        ----------
        Added check if outfile is not file to reduce memory use.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                f'{self.out_path}/{race}_Constructors_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Team {category}']
                x_values, y_values, bar_colors, bar_borders = [], [], [], []
                for team, values in category_dict.items():
                    x_values.append(team)
                    y_values.append(values[race_index])
                    colors = plotting_colors(
                        self.format_dir,
                        team=team,
                        year=self.year)
                    bar_colors.append(colors['bg_color'])
                    bar_borders.append(colors['color'])
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders],
                        index=sort_top)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y_values, x_values, bar_colors, bar_borders])
                x, y, c, b = sorted_arrays
                self.barplot(
                    x=x,
                    y=y,
                    colors=c,
                    borders=b,
                    xlabel=f'{category} {unit}',
                    ylabel='Constructor',
                    title=f'Constructors {race} {category}',
                    out_file=out_file)


class LineupLines(Plot):
    """
    Class Details
    =============
    Functions for plotting league team and league manager line graphs.

    Functions
    ---------
    driver_line(self, categories, units, results_dictionary, race, races)
    constructorline(self, categories, units, results_dictionary, race, races)

    Notes
    -----
    Plot class built on the Plot class method.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    06/08/2024
    ----------
    Created.

    """


    def driver_line(self,
                    categories : list,
                    units : list,
                    results_dictionary : dict,
                    race : str,
                    races : list) -> None:
        """
        Function Details
        ================
        Plot drivers for each race.

        Parameters
        ----------
        categories, units, races: list
            Category names (dictionary keys), corresponding axis label units, a
            list of all races.
        results_dictionary: dictionary
            Lineup results dictionary.
        race: string
            Race name.

        Returns
        -------
        None.

        See Also
        --------
        plotting_colors
        lineplt

        Notes
        -----
        Uses plot method.

        Example
        -------
        >>> results_dictionary = {}
        >>> race_index = 0
        >>> race = 'Race1'
        >>> format_dir = '/path/to/out_path'
        >>> year = '2024'
        >>> out_path = '/path/to/out_path'
        >>> races = ['Race1', 'Race2']
        >>> categories = ['Points', 'Values']
        >>> units = ['[#]', '[$M]']

        >>> lineup_plotter = LineupLines(out_path, format_dir, year)
        >>> lineup_plotter.driver_line(
                categories,
                units,
                results_dictionary,
                races,
                race)

        ------------------------------------------------------------------------
        Update History
        ==============

        06/08/2024
        ----------
        Created.

        07/08/2024
        ----------
        Added check if outfile is not file to reduce memory use.

        """
        for category, unit in zip(categories, units):
            out_file = Path(f'{self.out_path}/{race}_Driver_{category}.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Driver {category}']
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for driver, values in category_dict.items():
                    x.append(races)
                    y.append([values[i] for i in range(len(races))])
                    colors = plotting_colors(
                        self.format_dir,
                        driver=driver,
                        year=self.year)
                    l_cs.append(colors['bg_color'])
                    m_cs.append(colors['color'])
                    l_styles.append(colors['linestyle'])
                    labels.append(driver)
                self.lineplt(
                    x=x,
                    y=y,
                    colors=l_cs,
                    markers=m_cs,
                    styles=l_styles,
                    labels=labels,
                    xlabel='Races',
                    ylabel=f'{category} {unit}',
                    title=f'Drivers {race} {category}',
                    out_file=out_file)


    def constructorline(self,
                        categories : list,
                        units : list,
                        results_dictionary : dict,
                        race : str,
                        races : list) -> None:
        """
        Function Details
        ================
        Plot constructors for each race.

        Parameters
        ----------
        categories, units, races: list
            Category names (dictionary keys), corresponding axis label units, a
            list of all races.
        results_dictionary: dictionary
            Lineup results dictionary.
        race: string
            Race name.

        Returns
        -------
        None.

        See Also
        --------
        plotting_colors
        lineplt

        Notes
        -----
        Uses plot method.

        Example
        -------
        >>> results_dictionary = {}
        >>> race_index = 0
        >>> race = 'Race1'
        >>> format_dir = '/path/to/out_path'
        >>> year = '2024'
        >>> out_path = '/path/to/out_path'
        >>> races = ['Race1', 'Race2']
        >>> categories = ['Points', 'Values']
        >>> units = ['[#]', '[$M]']

        >>> lineup_plotter = LineupLines(out_path, format_dir, year)
        >>> lineup_plotter.driver_line(
                categories,
                units,
                results_dictionary,
                races,
                race)

        ------------------------------------------------------------------------
        Update History
        ==============

        06/08/2024
        ----------
        Created.

        07/08/2024
        ----------
        Added check if outfile is not file to reduce memory use.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                f'{self.out_path}/{race}_Constructor_{category}.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Team {category}']
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for team, values in category_dict.items():
                    x.append(races)
                    y.append([values[i] for i in range(len(races))])
                    colors = plotting_colors(
                        self.format_dir,
                        team=team,
                        year=self.year)
                    l_cs.append(colors['bg_color'])
                    m_cs.append(colors['color'])
                    l_styles.append(colors['linestyle'])
                    labels.append(team)
                self.lineplt(
                    x=x,
                    y=y,
                    colors=l_cs,
                    markers=m_cs,
                    styles=l_styles,
                    labels=labels,
                    xlabel='Races',
                    ylabel=f'{category} {unit}',
                    title=f'Constructors {race} {category}',
                    out_file=out_file)


class Lineup_Points(LineupBars,
                    LineupLines):
    """
    Class Details
    =============
    Functions for plotting lineup driver and constructor race points, values,
    sum points, sum values, average points, points per value for each race.

    Functions
    ---------
    results_bar(self, race_index, race, results_dictionary)
    statistics_bar(self, race_index, race, statistics_dictionary)
    statistics_line(self, race, races, statistics_dictionary)

    Notes
    -----
    Plot class built on the LineupBars, LineupLines, and Plot class methods.

    Example
    -------
    None.

    ----------------------------------------------------------------------------
    Update History
    ==============

    07/08/2024
    ----------
    Created.

    """


    def results_bar(self,
                    race_index : int,
                    race : str,
                    results_dictionary : dict) -> None:
        """
        Function Details
        ================

        Parameters
        ----------
        race_index: integer
            Index of races array for which to plot.
        race: string
            Race name.
        results_dictionary: dictionary
            Driver/Constructor results dictionary.

        Returns
        -------
        None.

        See Also
        --------
        driver_bars
        constructor_bar
        driver_line
        constructorline

        Notes
        -----
        Uses Plot method.

        Example
        -------
        >>> lineup_plotter = Lineup_Points(out_path, format_path, year)
        >>> lineup_plotter.results_bar(race_index, race, results_dict)

        ------------------------------------------------------------------------
        Update History
        ==============

        07/08/2024
        ----------
        Created.

        """
        self.driver_bars(
            categories=['Points', 'Values'],
            units=['[#]', '[$M]'],
            results_dictionary=results_dictionary,
            race_index=race_index,
            race=race
        )
        self.constructor_bar(
            categories=['Points', 'Values'],
            units=['[#]', '[$M]'],
            results_dictionary=results_dictionary,
            race_index=race_index,
            race=race
        )


    def statistics_bars(self,
                        race_index : int,
                        race : str,
                        statistics_dictionary : dict) -> None:
        """
        Function Details
        ================

        Parameters
        ----------
        race_index: integer
            Index of races array for which to plot.
        race: string
            Race name.
        statistics_dictionary: dictionary
            Driver/Constructor statistics dictionary.

        Returns
        -------
        None.

        See Also
        --------
        driver_bars
        constructor_bar
        driver_line
        constructorline

        Notes
        -----
        Uses Plot method.

        Example
        -------
        >>> lineup_plotter = Lineup_Points(out_path, format_path, year)
        >>> lineup_plotter.statistics_bar(race_index, race, results_dict)

        ------------------------------------------------------------------------
        Update History
        ==============

        07/08/2024
        ----------
        Created.

        """
        self.driver_bars(
            categories=['Points Per Value'],
            units=['[#/$M]'],
            results_dictionary=statistics_dictionary,
            race_index=race_index,
            race=race
        )
        self.constructor_bar(
            categories=['Points Per Value'],
            units=['[#/$M]'],
            results_dictionary=statistics_dictionary,
            race_index=race_index,
            race=race
        )


    def statistics_line(self,
                        race : str,
                        races : list,
                        statistics_dictionary : dict) -> None:
        """
        Function Details
        ================

        Parameters
        ----------
        race: string
            Race name.
        races: list
            List of completed races.
        statistics_dictionary: dictionary
            Driver/constructor statistics dictionary.

        Returns
        -------
        None.

        See Also
        --------
        driver_bars
        constructor_bar
        driver_line
        constructorline

        Notes
        -----
        Uses Plot method.

        Example
        -------
        >>> lineup_plotter = Lineup_Points(out_path, format_path, year)
        >>> lineup_plotter.statistics_line(race, races, results_dict)

        ------------------------------------------------------------------------
        Update History
        ==============

        07/08/2024
        ----------
        Created.

        """
        self.driver_line(
            categories=[
                'Sum Points',
                'Average Points Per Value',
                'Average Points'],
            units=['[#]', '[#/$M]', '[#]'],
            results_dictionary=statistics_dictionary,
            race=race,
            races=races
        )
        self.constructorline(
            categories=[
                'Sum Points',
                'Average Points Per Value',
                'Average Points'],
            units=['[#]', '[#/$M]', '[#]'],
            results_dictionary=statistics_dictionary,
            race=race,
            races=races
        )

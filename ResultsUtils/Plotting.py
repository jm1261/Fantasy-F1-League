# import InitializeResults  # noqa

import os
import inspect
import logging
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from GeneralUtils.DataIO import check_dir_exists
from matplotlib.ticker import AutoMinorLocator
from ResultsUtils.FormatUtilities import plotting_colors

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)

""" Notes: add the nested/categoried data for line graphs too, same as bars """


def sort_tuples(arrays: list):
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

    ---------------------------------------------------------------------------
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


def sort_top_tuples(arrays: list,
                    index: int,
                    line: bool = False,
                    pie: bool = False) -> list:
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

    ---------------------------------------------------------------------------
    Update History
    ==============

    31/07/2024
    ----------
    Created.

    03/09/2024
    ----------
    Major error with concatenating the top and bottom lists now resolved.

    """
    min_length = min(len(arr) for arr in arrays)
    data_arrays = [arr[:min_length] for arr in arrays]
    zipped_lists = list(zip(*data_arrays))
    sorted_arrays = sorted(zipped_lists)
    top_elements = sorted_arrays[:index]
    bottom_elements = sorted_arrays[-index:]

    if top_elements:
        top = list(zip(*top_elements))
    else:
        top = [[] for _ in arrays]

    if bottom_elements:
        bottom = list(zip(*bottom_elements))
    else:
        bottom = [[] for _ in arrays]

    concatenated = []
    if line or pie:
        for i, arr in enumerate(arrays):
            concatenated.append(np.concatenate((top[i], bottom[i])))
    else:
        separator = [0, ':', 'k', 'k']
        if len(separator) != len(arrays):
            raise ValueError(
                "Separator does not match the number of nested arrays")
        for i, arr in enumerate(arrays):
            concatenated.append(
                np.concatenate((top[i], [separator[i]], bottom[i])))

    return concatenated


class Plot:
    """
    Class Details
    =============
    Style guide for plotting line graphs, bar graphs, and pie charts. Includes
    style dictionary.

    Attributes
    ----------
    out_path: os.PathLike
    format_dir: os.PathLike
    year: str
    plot_dict: dict
    default_style: dict

    Methods
    -------
    __init__
    cm_to_inches
    save_fig
    bar_spacing
    barplot
    lineplt
    pieplot
    _generate_lineups_plots
    _generate_manager_plots
    _plots_bars
    _plot_lines
    _plots_pies
    generate_bars_datas
    generate_nested_bardata
    generates_category_bar_data
    gen_nested_category_bardata
    _generate_bar_plots

    Notes
    -----
    Plot class for use in LeaguePlot class method.

    ---------------------------------------------------------------------------
    Update History
    ==============

    31/07/2024
    ----------
    Created.

    02/08/2024
    ----------
    Added append_data, append_sum_data, and bar_spacing for better
    functionality and adaptability.

    06/09/2024
    ----------
    Removed append_data and append_sum_data as they were no longer required.

    15/09/2024
    ----------
    Refactored by ChatGPT

    """

    def __init__(
            self,
            out_path: os.PathLike,
            format_dir: os.PathLike,
            year: str,
            plot_style: dict = None) -> None:
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

        Returns
        -------
        None.

        -----------------------------------------------------------------------
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
            "fontweight": "bold",
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

        check_dir_exists(directory_path=out_path)

    def cm_to_inches(self, cm: float) -> float:
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
            fig: object,
            out_file: str) -> None:
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

        -----------------------------------------------------------------------
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
        logger.info(f'Plot saved to {outfile}')
        plt.close(fig)

    def bar_spacing(self,
                    data: list) -> tuple:
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

        -----------------------------------------------------------------------
        Update History
        ==============

        02/08/2024
        ----------
        Created.

        06/09/2024
        ----------
        Modified to account for instance where data is a list of lists.

        """
        if any(isinstance(i, list) for i in data):
            data = [item for sublist in data for item in sublist]
        data_range = max(data) - min(data)
        magnitude = (
            np.floor(np.log10(abs(data_range))) if data_range != 0 else 0)
        margin = max(0.05 * data_range, 0.1)
        text_spacing = 0.05 * (5 ** magnitude)
        return margin, text_spacing

    def barplot(self,
                x: list,
                y: list,
                colors: list,
                borders: list,
                xlabel: str,
                ylabel: str,
                title: str,
                out_file: str,
                **kwargs: dict) -> None:
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

        -----------------------------------------------------------------------
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

        logger.info(
            f'Plotting {out_file} with: {style}, {margin}, {text_spacing}')

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
                x: list,
                y: list,
                colors: list,
                markers: list,
                styles: list,
                labels: list,
                xlabel: str,
                ylabel: str,
                title: str,
                out_file: str,
                **kwargs: dict) -> None:
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

        -----------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Created.

        """
        style = {**self.default_style, **kwargs}

        logger.info(f'Plotting {out_file} with: {style}')

        fig, ax = plt.subplots(
            nrows=style.get('nrows', 1),
            ncols=style.get('ncols', 1),
            figsize=[
                self.cm_to_inches(cm=style.get('fig_height', 15)),
                self.cm_to_inches(cm=style.get('fig_width', 9))],
            dpi=style.get('dpi', 600))
        for i in range(len(x)):
            try:
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
            except IndexError:
                ax.plot(
                    x[i],
                    y[i],
                    label=labels[i],
                    marker=style.get('marker', 'o'),
                    linestyle='-',  # Default to solid line
                    color=colors[i],
                    markersize=style.get('marker_size', 4),
                    lw=style.get('line_width', 2))
        ax.legend(
            loc=0,
            ncol=style.get('legend_col', 2),
            prop={'size': style.get('legend_size', 6)})
        ax.grid(
            True,
            alpha=0.5)
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
                data: list,
                labels: list,
                title: str,
                out_file: str,
                colors=None,
                label_colors=None,
                explode=None,
                **kwargs: dict) -> None:
        """
        Function Details
        ================
        Plot a pie chart for a collection of y-data.

        Parameters
        ----------
        data, labels,
            Data, data labels.
        numbers, colors, label_colors, explode: list, optional
            Optional percentage indicator, optional color format, proportion to
            offset each slide. All default to None.
        title, out_file: string
            Figure title, path to save.
        **kwargs : dictionary
            Additional keyword arguments for plot customisation.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        31/07/2024
        ----------
        Created.

        """
        logger.info(f'Plotting {out_file}')

        if all(v == 0 for v in data):
            logger.info(f"No data to plot for {title}. All values are zero.")
            return

        threshold = 0.02
        total = sum(data)
        new_data, new_labels, new_colors, new_label_colors = [], [], [], []
        for i, value in enumerate(data):
            if value / total > threshold:
                new_data.append(value)
                new_labels.append(labels[i])
                new_colors.append(colors[i])
                new_label_colors.append(label_colors[i])
            else:
                if 'Others' in new_labels:
                    index = new_labels.index('Others')
                    new_data[index] += value
                else:
                    new_data.append(
                        sum(v for v in data if v / total <= threshold))
                    new_labels.append('Others')
                    new_colors.append('black')
                    new_label_colors.append('white')
        if new_labels.count('Others') > 1:
            data_sum = sum(
                d for d, l in zip(new_data, new_labels) if l == 'Others')
            new_data = [
                d if l != 'Others' else data_sum
                for d, l in zip(new_data, new_labels)]
            new_labels = [
                label if label != 'Others' else 'Others'
                for label in new_labels]

        style = {**self.default_style, **kwargs}
        fig, ax = plt.subplots(
            nrows=style.get('nrows', 1),
            ncols=style.get('ncols', 1),
            figsize=[
                self.cm_to_inches(cm=style.get('fig_height', 15)),
                self.cm_to_inches(cm=style.get('fig_width', 9))],
            dpi=style.get('dpi', 600))
        wedges, texts, autotexts = ax.pie(
            new_data,
            labels=new_labels,
            colors=new_colors,
            explode=[explode] * len(new_data),
            autopct=style.get('auto_percentage', '%1.1f%%'),
            startangle=style.get('start_angle', 90),
            labeldistance=1.1)
        plt.title(
            title,
            fontsize=style.get('title_fontsize', 14),
            fontweight=style.get('fontweight', 'bold'),
            color=style.get('title_color', 'black'))
        for text in texts:
            text.set_rotation(style.get('label_rotation', 0))
            text.set_fontsize(4)
            text.set_horizontalalignment('center')
            text.set_verticalalignment('center')
        for text in autotexts:
            text.set_fontsize(4)
        if label_colors:
            for text, label in zip(texts, new_colors):
                text.set_color(label)
            for text, label in zip(autotexts, new_label_colors):
                text.set_color(label)
        self.save_fig(
            fig=fig,
            out_file=out_file)

    def _generate_lineups_plots(self,
                                plot_type: str,
                                race_index: int,
                                races: list,
                                race: str,
                                dictionary: dict,
                                additional_parameters: dict = None) -> None:
        """
        Function Details
        ================
        Helper method to handle the common logic for plotting bar, line, and
        pie charts.

        Parameters
        ----------
        plot_type, race: string
            The type of plot to generate ('bar', 'line', 'pie'). Race name.
        race_index: integer
            Index of the races array for which to plot.
        dictionary: dictionary
            Data dictionary to plot.
        additional_params: dictionary, optional
            Additional parameters for customizing the plots.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update history
        ==============

        15/09/2024
        ----------
        Created.

        """
        plot_mappings = {
            "bar": {
                "driver_bar": self.driver_bars,
                "constructor_bar": self.constructor_bar
            },
            "line": {
                "driver_line": self.driver_line,
                "constructor_line": self.constructorline
            }
        }

        if plot_type not in plot_mappings:
            raise ValueError(f'Unsupported plot type {plot_type}')
        if plot_type == 'bar':
            self._plots_bars(
                plot_mappings=plot_mappings,
                race_index=race_index,
                race=race,
                dictionary=dictionary,
                additional_parameters=additional_parameters)
        elif plot_type == 'line':
            self._plot_lines(
                plot_mappings=plot_mappings,
                race_index=race_index,
                races=races,
                race=race,
                dictionary=dictionary,
                additional_parameters=additional_parameters)

    def _generate_manager_plots(self,
                                plot_type: str,
                                race_index: int,
                                races: list,
                                race: str,
                                dictionary: dict,
                                additional_parameters: dict = None) -> None:
        """
        Function Details
        ================
        Helper method to handle the common logic for plotting bar, line, and
        pie charts.

        Parameters
        ----------
        plot_type, race: string
            The type of plot to generate ('bar', 'line', 'pie'). Race name.
        race_index: integer
            Index of the races array for which to plot.
        dictionary: dictionary
            Data dictionary to plot.
        additional_params: dictionary, optional
            Additional parameters for customizing the plots.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update history
        ==============

        15/09/2024
        ----------
        Created.

        """
        plot_mappings = {
            "bar": {
                "team_bar": self.league_team_bar,
                "manager_bar": self.league_manager_bars,
                "team_count_bar": self.teams_count_bar,
                "manager_count_bar": self.managercountbar,
                "count_bar": self.leaguecount_bar,
                "prize_bar": self._prize_bars,
                "prize_count_bar": self.prize_teamscountbar,
            },
            "line": {
                "team_line": self.leagueteam_line,
                "manager_line": self.league_manager_line,
                "team_count_line": self.team_count_line,
                "manager_count_line": self.managers_count_line,
                "count_line": self.leaguecountline,
                "prize_line": self.league_prizes_lines,
                "prize_count_line": self.prize_teamcountline
            },
            "pie": {
                "count_pie": self.leaguecount_pie
            }
        }

        if plot_type not in plot_mappings:
            raise ValueError(f'Unsupported plot type {plot_type}')
        if plot_type == 'bar':
            self._plots_bars(
                plot_mappings=plot_mappings,
                race_index=race_index,
                race=race,
                dictionary=dictionary,
                additional_parameters=additional_parameters)
        elif plot_type == 'line':
            self._plot_lines(
                plot_mappings=plot_mappings,
                race_index=race_index,
                races=races,
                race=race,
                dictionary=dictionary,
                additional_parameters=additional_parameters)
        elif plot_type == 'pie':
            self._plots_pies(
                plot_mappings=plot_mappings,
                race_index=race_index,
                race=race,
                dictionary=dictionary,
                additional_parameters=additional_parameters)

    def _plots_bars(self,
                    plot_mappings: dict,
                    race_index: int,
                    race: str,
                    dictionary: dict,
                    additional_parameters: dict) -> None:
        """
        Function Details
        ================
        Generate bar plots based on the provided parameters.

        Parameters
        ----------
        plot_mappings, dictionary, additional_parameters: dictionary
            Mapping of plot types to methods. Data dictionary to plot.
            Additional parameters for customizing the plots.
        race_index: integer
            Index of the races array for which to plot.
        race: string
            Race name.

        Returns
        -------
        None.

        Notes
        -----
        plot_method is intended to be a function reference that is called to
        generate the actual plot. This method uses the plot_mappings dictionary
        to determine which plotting function to use based on the plot_type.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/09/2024
        ----------
        Created.

        """
        for plot_type, plot_method in plot_mappings['bar'].items():
            if plot_type in additional_parameters.keys():
                parameters = additional_parameters.get(plot_type, {})
                # Get the signature of the plot method
                method_signature = inspect.signature(plot_method)
                # Filter the parameters based on the method's accepted args
                filtered_parameters = {
                    key: value for key, value in parameters.items()
                    if key in method_signature.parameters}
                plot_method(
                    race_index=race_index,
                    race=race,
                    results_dictionary=dictionary,
                    **filtered_parameters)

    def _plot_lines(self,
                    plot_mappings: dict,
                    race_index: int,
                    races: list,
                    race: str,
                    dictionary: dict,
                    additional_parameters: dict) -> None:
        """
        Function Details
        ================
        Generate line plots based on the provided parameters.

        Parameters
        ----------
        plot_mappings, dictionary, additional_parameters: dictionary
            Mapping of plot types to methods. Data dictionary to plot.
            Additional parameters for customizing the plots.
        race_index: integer
            Index of the races array for which to plot.
        races: list
            List of all races to plot.
        race: string
            Race name.

        Returns
        -------
        None.

        Notes
        -----
        plot_method is intended to be a function reference that is called to
        generate the actual plot. This method uses the plot_mappings dictionary
        to determine which plotting function to use based on the plot_type.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/09/2024
        ----------
        Created.

        """
        for plot_type, plot_method in plot_mappings['line'].items():
            if plot_type in additional_parameters.keys():
                parameters = additional_parameters.get(plot_type, {})
                # Get the signature of the plot method
                method_signature = inspect.signature(plot_method)
                # Filter the parameters based on the method's accepted args
                filtered_parameters = {
                    key: value for key, value in parameters.items()
                    if key in method_signature.parameters}
                plot_method(
                    race=race,
                    races=races,
                    results_dictionary=dictionary,
                    **filtered_parameters)

    def _plots_pies(self,
                    plot_mappings: dict,
                    race_index: int,
                    race: str,
                    dictionary: dict,
                    additional_parameters: dict) -> None:
        """
        Function Details
        ================
        Generate pie charts based on the provided parameters.

        Parameters
        ----------
        plot_mappings, dictionary, additional_parameters: dictionary
            Mapping of plot types to methods. Data dictionary to plot.
            Additional parameters for customizing the plots.
        race_index: integer
            Index of the races array for which to plot.
        race: string
            Race name.

        Returns
        -------
        None.

        Notes
        -----
        plot_method is intended to be a function reference that is called to
        generate the actual plot. This method uses the plot_mappings dictionary
        to determine which plotting function to use based on the plot_type.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/09/2024
        ----------
        Created.

        """
        for plot_type, plot_method in plot_mappings['pie'].items():
            if plot_type in additional_parameters.keys():
                parameters = additional_parameters.get(plot_type, {})
                plot_method(
                    race_index=race_index,
                    race=race,
                    results_dictionary=dictionary,
                    **parameters)

    def generate_bars_datas(self,
                            category_dict: dict,
                            race_index: int,
                            context: str):
        """
        Function Details
        ================
        Generate bar graph data from dictionary items.

        Parameters
        ----------
        category_dict: dictionary
            Category dictionary containing data to plot.
        race_index: integer
            Index of races list to plot.
        context: string
            Context manager for plotting_colors.

        Returns
        -------
        x_values, y_values, bar_colors, bar_borders: list
            x- and y- data points, bar colors and bar borders.

        Notes
        -----
        Only retrieves the x, y, bar color, and bar border data.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/09/2024
        ----------
        Created.

        """
        x_values, y_values, bar_colors, bar_borders = [], [], [], []
        for item, values in category_dict.items():
            x_values.append(item)
            y_values.append(values[race_index])
            colors = plotting_colors(
                format_dir=self.format_dir,
                year=self.year,
                context=context,
                entity=item
            )
            bar_colors.append(colors['bg_color'])
            if 'color' in colors.keys():
                bar_borders.append(colors['color'])
            else:
                bar_borders.append(colors['bg_color'])
        return x_values, y_values, bar_colors, bar_borders

    def generate_nested_bardata(self,
                                category_dict: dict,
                                race_index: int,
                                context: str) -> tuple:
        """
        Function Details
        ================
        Generate bar graph data from nested dictionary items.

        Parameters
        ----------
        category_dict: dictionary
            Category dictionary containing data to plot.
        race_index: integer
            Index of races list to plot.
        context: string
            Context manager for plotting_colors.

        Returns
        -------
        x_values, y_values, bar_colors, bar_borders: list
            x- and y- data points, bar colors and bar borders.

        Notes
        -----
        Only retrieves the x, y, bar color, and bar border data.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/09/2024
        ----------
        Created.

        """
        x_values, y_values, bar_colors, bar_borders = [], [], [], []
        for key, dictionary in category_dict.items():
            for item, values in dictionary.items():
                x_values.append(item)
                y_values.append(values[race_index])
                colors = plotting_colors(
                    format_dir=self.format_dir,
                    year=self.year,
                    context=context,
                    entity=item
                )
                bar_colors.append(colors['bg_color'])
                if 'color' in colors.keys():
                    bar_borders.append(colors['color'])
                else:
                    bar_borders.append(colors['bg_color'])
        return x_values, y_values, bar_colors, bar_borders

    def generates_category_bar_data(self,
                                    category_dict: dict,
                                    category: str,
                                    race_index: int,
                                    context: str) -> tuple:
        """
        Function Details
        ================
        Generate bar graph data from nested category dictionary items.

        Parameters
        ----------
        category_dict: dict
            Category dictionary containing data to plot.
        category: str
            Category within category_dict to plot.
        race_index: int
            Index of races list to plot.
        context: str
            Context manager for plotting_colors.

        Returns
        -------
        x_values, y_values, bar_colors, bar_borders: list
            x- and y- data points, bar colors, bar borders.

        Notes
        -----
        Only retrieves the x, y, bar color, and bar border data.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/12/2024
        ----------
        Copied from generate_nested_bardata.

        """
        x_values, y_values, bar_colors, bar_borders = [], [], [], []
        for item, cat in category_dict.items():
            x_values.append(item)
            y_values.append((cat[category])[race_index])
            colors = plotting_colors(
                format_dir=self.format_dir,
                year=self.year,
                context=context,
                entity=item
            )
            bar_colors.append(colors['bg_color'])
            if 'color' in colors.keys():
                bar_borders.append(colors['color'])
            else:
                bar_borders.append(colors['bg_color'])
        return x_values, y_values, bar_colors, bar_borders

    def gen_nested_category_bardata(self,
                                    category_dict: dict,
                                    category: str,
                                    race_index: int,
                                    context: str) -> tuple:
        """
        Function Details
        ================
        Generate bar graph data from nested category dictionary items.

        Parameters
        ----------
        category_dict: dict
            Category dictionary containing data to plot.
        category: str
            Category within category_dict to plot.
        race_index: int
            Index of races list to plot.
        context: str
            Context manager for plotting_colors.

        Returns
        -------
        x_values, y_values, bar_colors, bar_borders: list
            x- and y- data points, bar colors, bar borders.

        Notes
        -----
        Only retrieves the x, y, bar color, and bar border data.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/12/2024
        ----------
        Copied from generate_nested_bardata.

        """
        x_values, y_values, bar_colors, bar_borders = [], [], [], []
        for key, dictionary in category_dict.items():
            for item, cat in dictionary.items():
                x_values.append(item)
                y_values.append((cat[category])[race_index])
                colors = plotting_colors(
                    format_dir=self.format_dir,
                    year=self.year,
                    context=context,
                    entity=item
                )
                bar_colors.append(colors['bg_color'])
                if 'color' in colors.keys():
                    bar_borders.append(colors['color'])
                else:
                    bar_borders.append(colors['bg_color'])
        return x_values, y_values, bar_colors, bar_borders

    def _generate_bar_plots(self,
                            category: str,
                            unit: str,
                            category_dictionary: dict,
                            race_index: int,
                            context: str,
                            title: str,
                            out_file: str,
                            sort_top: int = None,
                            nested: bool = False,
                            categoried: bool = False) -> None:
        """
        Function Details
        ================
        Generate bar graphs for all categories.

        Parameters
        ----------
        category, unit, context, title, out_file: string
            Category name, unit string, context for plotting_colors, figure
            title, out path.
        category_dictionary: dictionary
            Category dictionary from which to plot.
        race_index: integer
            Integer from races array for which to plot.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.
        nested: boolean, optional
            If true, the category dictionary is a nested dictionary, i.e., a
            dictionary within a dictionary.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/09/2024
        ----------
        Created.

        """
        if nested and categoried:
            normalized_category = category.replace('Sum ', '')
            xs, ys, bcs, bbs = self.gen_nested_category_bardata(
                category_dict=category_dictionary,
                category=normalized_category,
                race_index=race_index,
                context=context
            )
        elif nested:
            xs, ys, bcs, bbs = self.generate_nested_bardata(
                category_dict=category_dictionary,
                race_index=race_index,
                context=context
            )
        elif categoried:
            normalized_category = category.replace('Sum ', '')
            xs, ys, bcs, bbs = self.generates_category_bar_data(
                category_dict=category_dictionary,
                category=normalized_category,
                race_index=race_index,
                context=context
            )
        else:
            xs, ys, bcs, bbs = self.generate_bars_datas(
                category_dict=category_dictionary,
                race_index=race_index,
                context=context
            )
        if sort_top:
            sorted_arrays = sort_top_tuples(
                arrays=[ys, xs, bcs, bbs],
                index=sort_top
            )
        else:
            sorted_arrays = sort_tuples(arrays=[ys, xs, bcs, bbs])
        x, y, c, b = sorted_arrays
        self.barplot(
            x=x,
            y=y,
            colors=c,
            borders=b,
            xlabel=f'{category} {unit}',
            ylabel=context.capitalize(),
            title=title,
            out_file=out_file
        )


class LineupBars(Plot):
    """
    Class Details
    =============
    Functions for plotting lineup driver and constructor bar graphs.

    Attributes
    ----------
    None.

    Methods
    -------
    driver_bars
    constructor_bar

    Notes
    -----
    Plot class built on the Plot class method.

    ---------------------------------------------------------------------------
    Update History
    ==============

    01/08/2024
    ----------
    Created.

    """

    def driver_bars(self,
                    categories: list,
                    units: list,
                    results_dictionary: dict,
                    race_index: int,
                    race: str,
                    sort_top: int = None) -> None:
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

        -----------------------------------------------------------------------
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
                f'{self.out_path}/{race}_Driver_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Driver {category}']
                x_values, y_values, bar_colors, bar_borders = [], [], [], []
                for driver, values in category_dict.items():
                    x_values.append(driver)
                    y_values.append(values[race_index])
                    colors = plotting_colors(
                        format_dir=self.format_dir,
                        year=self.year,
                        context='driver',
                        entity=driver)
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
                        categories: list,
                        units: list,
                        results_dictionary: dict,
                        race_index: int,
                        race: str,
                        sort_top: int = None) -> None:
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

        -----------------------------------------------------------------------
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
                f'{self.out_path}/{race}_Constructor_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Constructor {category}']
                x_values, y_values, bar_colors, bar_borders = [], [], [], []
                for team, values in category_dict.items():
                    x_values.append(team)
                    y_values.append(values[race_index])
                    colors = plotting_colors(
                        format_dir=self.format_dir,
                        year=self.year,
                        context='constructor',
                        entity=team)
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

    Attributes
    ----------
    None.

    Methods
    -------
    driver_line
    constructorline

    Notes
    -----
    Plot class built on the Plot class method.

    ---------------------------------------------------------------------------
    Update History
    ==============

    06/08/2024
    ----------
    Created.

    """

    def driver_line(self,
                    categories: list,
                    units: list,
                    results_dictionary: dict,
                    race: str,
                    races: list) -> None:
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

        -----------------------------------------------------------------------
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
                        year=self.year,
                        context='driver',
                        entity=driver)
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
                        categories: list,
                        units: list,
                        results_dictionary: dict,
                        race: str,
                        races: list) -> None:
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

        -----------------------------------------------------------------------
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
                category_dict = results_dictionary[f'Constructor {category}']
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for team, values in category_dict.items():
                    x.append(races)
                    y.append([values[i] for i in range(len(races))])
                    colors = plotting_colors(
                        self.format_dir,
                        year=self.year,
                        context='constructor',
                        entity=team)
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

    Attributes
    ----------
    None.

    Methods
    -------
    lineup_results
    lineup_stat

    Notes
    -----
    Plot class built on the LineupBars, LineupLines, and Plot class methods.

    ---------------------------------------------------------------------------
    Update History
    ==============

    07/08/2024
    ----------
    Created.

    15/09/2024
    ----------
    Refactored by ChatGPT.

    """

    def lineups_results(self,
                        race_index: int,
                        race: str,
                        results_dictionary: dict) -> None:
        """
        Function Details
        ================
        Plot driver and constructor results bar graphs.

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

        Notes
        -----
        Uses Plot method.

        Example
        -------
        >>> lineup_plotter = Lineup_Points(out_path, format_path, year)
        >>> lineup_plotter.results_bar(race_index, race, results_dict)

        -----------------------------------------------------------------------
        Update History
        ==============

        07/08/2024
        ----------
        Created.

        15/09/2024
        ----------
        Refactored by ChatGPT.

        """
        results_parameters = {
            "driver_bar": {
                "categories": ['Points', 'Values'],
                "units": ['[#]', '[$M]']
            },
            "constructor_bar": {
                "categories": ['Points', 'Values'],
                "units": ['[#]', '[$M]']
            }
        }
        self._generate_lineups_plots(
            plot_type='bar',
            race_index=race_index,
            races=None,
            race=race,
            dictionary=results_dictionary,
            additional_parameters=results_parameters
        )

    def lineup_stat(self,
                    race_index: int,
                    races: list,
                    race: str,
                    statistics_dictionary: dict) -> None:
        """
        Function Details
        ================
        Plot lineup statistics dictionary bar and line graphs.

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

        -----------------------------------------------------------------------
        Update History
        ==============

        07/08/2024
        ----------
        Created.

        15/09/2024
        ----------
        Refactored by ChatGPT.

        """
        categories = [
            [
                'Sum Points', 'Average Points', 'Points Per Value',
                'Positive Percentage', 'Negative Percentage',
                'Std Dev Points', 'CV Points',
                'Std Dev Points Per Value', 'CV Points Per Value'
            ],  # bar
            [
                'Sum Points', 'Average Points', 'Average Points Per Value',
                'Std Dev Points', 'Std Dev Points Per Value'
            ]  # line
        ]
        units = [
            [
                '[#]', '[#]', '[#/$M]', '[%]', '[%]',
                '[#]', '[#]', '[#/$M]', '[#/$M]'
            ],  # bar
            [
                '[#]', '[#]', '[#/$M]', '[%]',
                '[#]'
            ]  # line
        ]
        for i, plot_type in enumerate(['bar', 'line']):
            statistics_parameters = {
                f'driver_{plot_type}': {
                    "categories": categories[i], "units": units[i]},
                f'constructor_{plot_type}': {
                    "categories": categories[i], "units": units[i]}
            }
            self._generate_lineups_plots(
                plot_type=plot_type,
                race_index=race_index if plot_type != 'line' else None,
                races=None if plot_type != 'line' else races,
                race=race,
                dictionary=statistics_dictionary,
                additional_parameters=statistics_parameters
            )


class LeagueBars(Plot):
    """
    Class Details
    =============
    Functions for plotting league team and league manager bar graphs.

    Attributes
    ----------
    None.

    Methods
    -------
    league_team_bar
    league_manager_bars
    team_count_bar
    managercountbar
    leaguecount_bar
    spot_prize_bars

    ---------------------------------------------------------------------------
    Update History
    ==============

    31/07/2024
    ----------
    Created.

    02/09/2024
    ----------
    Documentation updated.

    """

    def league_team_bar(self,
                        categories: list,
                        units: list,
                        results_dictionary: dict,
                        race_index: int,
                        race: str,
                        sort_top: int = None) -> None:
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

        Notes
        -----
        Uses plot method.

        -----------------------------------------------------------------------
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
                self.out_path,
                f'{race}_LeagueTeams_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Team {category}']
                self._generate_bar_plots(
                    category=category,
                    unit=unit,
                    category_dictionary=category_dict,
                    race_index=race_index,
                    context='team',
                    title=f'League Team {race} {category}',
                    out_file=out_file,
                    sort_top=sort_top,
                    nested=True
                )

    def league_manager_bars(self,
                            categories: list,
                            units: list,
                            results_dictionary: dict,
                            race_index: int,
                            race: str,
                            sort_top: int = None) -> None:
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

        Notes
        -----
        Uses plot method.

        -----------------------------------------------------------------------
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
                self.out_path,
                f'{race}_LeagueManagers_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Manager {category}']
                self._generate_bar_plots(
                    category=category,
                    unit=unit,
                    category_dictionary=category_dict,
                    race_index=race_index,
                    context='manager',
                    title=f'League Managers {race} {category}',
                    out_file=out_file,
                    sort_top=sort_top
                )

    def teams_count_bar(self,
                        categories: list,
                        units: list,
                        results_dictionary: dict,
                        race_index: int,
                        race: str,
                        sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot sorted manager teams category counts for each race.

        Parameters
        ----------
        categories, units: list
            Category names (dictionary keys), corresponding axis label units.
        results_dictionary: dict
            Manager counts dictionary.
        race_index: int
            Integer of races array for which to plot.
        race: str,
            Race name.
        sort_top: int, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer, else will just sort all.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method. Designed to plot penalties and substitute counts.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/12/2024
        ----------
        Created.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_LeagueTeams_{category}_Bar.png'
            )
            if not out_file.is_file():
                category_dict = results_dictionary[f'Teams {category}']
                self._generate_bar_plots(
                    category=category,
                    unit=unit,
                    category_dictionary=category_dict,
                    race_index=race_index,
                    context='team',
                    title=f'League Team {race} {category}',
                    out_file=out_file,
                    sort_top=sort_top,
                    nested=True,
                    categoried=True
                )

    def managercountbar(self,
                        categories: list,
                        units: list,
                        results_dictionary: dict,
                        race_index: int,
                        race: str,
                        sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot sorted manager category counts for each race.

        Parameters
        ----------
        categories, units: list
            Category names (dictionary keys), corresponding axis label units.
        results_dictionary: dict
            Manager counts dictionary.
        race_index: int
            Integer of races array for which to plot.
        race: str,
            Race name.
        sort_top: int, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer, else will just sort all.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method. Designed to plot penalties and substitute counts.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/12/2024
        ----------
        Created.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_LeagueManagers_{category}_Bar.png'
            )
            if not out_file.is_file():
                category_dict = results_dictionary[f'Manager {category}']
                self._generate_bar_plots(
                    category=category,
                    unit=unit,
                    category_dictionary=category_dict,
                    race_index=race_index,
                    context='manager',
                    title=f'League Manager {race} {category}',
                    out_file=out_file,
                    sort_top=sort_top,
                    categoried=True
                )

    def leaguecount_bar(self,
                        categories: list,
                        results_dictionary: dict,
                        race_index: int,
                        race: str,
                        sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot driver, constructor, boost, extra, and perk counts.

        Parameters
        ----------
        categories: list
            Category names (dictionary keys).
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

        Notes
        -----
        Uses plot method.

        -----------------------------------------------------------------------
        Update History
        ==============

        01/08/2024
        ----------
        Copied from previous leaguecount function with new class method.

        07/08/2024
        ----------
        Added check if outfile is not file to reduce memory use.

        """
        none = [
            'None',
            'Nonw',
            'none',
            'nonw'
        ]
        non_perk = [
            'Driver',
            'Constructor',
            'DRS Boost',
            'Extra DRS'
        ]
        non_constructor = [
            'Driver',
            'DRS Boost',
            'Extra DRS'
        ]
        for category in categories:
            normalized_category = category.replace('Sum ', '')
            out_file = Path(
                self.out_path,
                f'{race}_LeagueCounts_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'League {category}']
                x_values, y_values, bar_colors, bar_borders = [], [], [], []
                for name, count in category_dict.items():
                    if name in none:
                        continue
                    else:
                        if normalized_category in non_perk:
                            category_type = (
                                {'driver': name}
                                if normalized_category in non_constructor
                                else {'constructor': name})
                        elif normalized_category == 'Perks':
                            category_type = {'perk': name}
                        else:
                            continue
                        key, value = list(category_type.items())[0]
                        colors = plotting_colors(
                            format_dir=self.format_dir,
                            year=self.year,
                            context=key,
                            entity=value)
                        x_values.append(name)
                        y_values.append(count[race_index])
                        bar_colors.append(colors['bg_color'])
                        bar_borders.append(colors['color'])
                if len(x_values) == 0:
                    continue
                else:
                    if sort_top:
                        sorted_arrays = sort_top_tuples(
                                arrays=[
                                    y_values,
                                    x_values,
                                    bar_colors,
                                    bar_borders],
                                index=sort_top)
                    else:
                        sorted_arrays = sort_tuples(
                                arrays=[
                                    y_values,
                                    x_values,
                                    bar_colors,
                                    bar_borders])
                    x, y, c, b = sorted_arrays
                    title = f'League {race} {category} Count'
                    self.barplot(
                        x=x,
                        y=y,
                        colors=c,
                        borders=b,
                        xlabel='Counts [#]',
                        ylabel='Names',
                        title=title,
                        out_file=out_file)

    def _prize_bars(self,
                    categories: list,
                    units: list,
                    results_dictionary: dict,
                    race_index: int,
                    race: str,
                    prize: str,
                    sort_top: int = None):
        """
        Function Details
        ================
        Plot sorted manager team prize bars for spot prizes.

        Parameters
        ----------
        categories, units: list
            Category names (dictionary keys), corresponding axis label units.
        results_dictionary: dictionary
            Manager results dictionary.
        race_index: integer
            Integer of races array for which to plot.
        race, prize: string
            Race name. Prize name for title.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/10/2024
        ----------
        Copied from league_team_bar with adjustments.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_{prize}_{category}_Bar.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Team {category}']
                self._generate_bar_plots(
                    category=category,
                    unit=unit,
                    category_dictionary=category_dict,
                    race_index=race_index,
                    context='team',
                    title=f'{prize}',
                    out_file=out_file,
                    sort_top=sort_top,
                    nested=True)

    def prize_teamscountbar(self,
                            categories: list,
                            units: list,
                            results_dictionary: dict,
                            race_index: int,
                            race: str,
                            prize: str,
                            sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot sorted manager teams category counts for each race for count
        prizes.

        Parameters
        ----------
        categories, units: list
            Category names (dictionary keys), corresponding axis label units.
        results_dictionary: dict
            Manager counts dictionary.
        race_index: int
            Integer of races array for which to plot.
        race, prize: str,
            Race name. Prize name for title.
        sort_top: int, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer, else will just sort all.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method. Designed to plot penalties and substitute counts.

        -----------------------------------------------------------------------
        Update History
        ==============

        24/03/2025
        ----------
        Created.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_{prize}_{category}_Bar.png'
            )
            if not out_file.is_file():
                category_dict = results_dictionary[f'Teams {category}']
                self._generate_bar_plots(
                    category=category,
                    unit=unit,
                    category_dictionary=category_dict,
                    race_index=race_index,
                    context='team',
                    title=f'{race} {prize}',
                    out_file=out_file,
                    sort_top=sort_top,
                    nested=True,
                    categoried=True
                )


class LeagueLines(Plot):
    """
    Class Details
    =============
    Function for plotting league team and league manager line graphs.

    Attributes
    ----------
    None.

    Methods
    -------
    leagueteam_line
    league_manager_line
    leaguecountline
    league_prizes_lines

    Notes
    -----
    Plot class built on the Plot class method.

    ---------------------------------------------------------------------------
    Update History
    ==============

    06/09/2024
    ----------
    Created.

    """

    def leagueteam_line(self,
                        categories: list,
                        units: list,
                        results_dictionary: dict,
                        race: str,
                        races: list,
                        sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot league team results line graphs.

        Parameters
        ----------
        categories, units, races: list
            Category names (dictionary keys), corresponding axis label units.
            List of all race names.
        results_dictionary: dictionary
            League results dictionary.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        Example
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        06/09/2024
        ----------
        Created.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_LeagueTeams_{category}.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Team {category}']
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for manager, teams in category_dict.items():
                    for team, values in teams.items():
                        x.append(races)
                        y.append([values[i] for i in range(len(races))])
                        colors = plotting_colors(
                            format_dir=self.format_dir,
                            context='team',
                            entity=team,
                            year=self.year)
                        l_cs.append(colors['bg_color'])
                        m_cs.append(colors['color'])
                        l_styles.append(colors['linestyle'])
                        labels.append(team)
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels],
                        index=sort_top,
                        line=True)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels])
                y, x, l_cs, m_cs, l_styles, labels = sorted_arrays
                self.lineplt(
                    x=x,
                    y=y,
                    colors=l_cs,
                    markers=m_cs,
                    styles=l_styles,
                    labels=labels,
                    xlabel='Races',
                    ylabel=f'{category} {unit}',
                    title=f'League Teams {race} {category}',
                    out_file=out_file)

    def league_manager_line(self,
                            categories: list,
                            units: list,
                            results_dictionary: dict,
                            race: str,
                            races: list,
                            sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot league manager results line graphs.

        Parameters
        ----------
        categories, units, races: list
            Category names (dictionary keys), corresponding axis label units.
            List of all race names.
        results_dictionary: dictionary
            League results dictionary.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        Example
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        14/09/2024
        ----------
        Created.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_LeagueManagers_{category}.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Manager {category}']
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for manager, values in category_dict.items():
                    x.append(races)
                    y.append([values[i] for i in range(len(races))])
                    colors = plotting_colors(
                        format_dir=self.format_dir,
                        context='manager',
                        entity=manager,
                        year=self.year)
                    l_cs.append(colors['bg_color'])
                    m_cs.append(colors['bg_color'])
                    l_styles.append('-')
                    labels.append(manager)
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y, x, l_cs, m_cs, labels],
                        index=sort_top,
                        line=True)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y, x, l_cs, m_cs, labels])
                y, x, l_cs, m_cs, labels = sorted_arrays
                self.lineplt(
                    x=x,
                    y=y,
                    colors=l_cs,
                    markers=m_cs,
                    styles=l_styles,
                    labels=labels,
                    xlabel='Races',
                    ylabel=f'{category} {unit}',
                    title=f'League Managers {race} {category}',
                    out_file=out_file)

    def team_count_line(self,
                        categories: list,
                        units: list,
                        results_dictionary: dict,
                        race: str,
                        races: list,
                        sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot league team counts line graphs.

        Parameters
        ----------
        categories, units, races: list
            Category names (dictionary keys), corresponding axis label units.
            List of all race names.
        results_dictionary: dictionary
            League results dictionary.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/12/2024
        ----------
        Created.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_LeagueTeams_{category}.png'
            )
            if not out_file.is_file():
                category_dict = results_dictionary[f'Teams {category}']
                normalized_category = category.replace('Sum ', '')
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for manager, teams in category_dict.items():
                    for team, values in teams.items():
                        x.append(races)
                        y.append(
                            [
                                (values[f'{normalized_category}'])[i]
                                for i in range(len(races))
                            ]
                        )
                        colors = plotting_colors(
                            format_dir=self.format_dir,
                            context='team',
                            entity=team,
                            year=self.year
                        )
                        l_cs.append(colors['bg_color'])
                        m_cs.append(colors['color'])
                        l_styles.append(colors['linestyle'])
                        labels.append(team)
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels],
                        index=sort_top,
                        line=True)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels])
                y, x, l_cs, m_cs, l_styles, labels = sorted_arrays
                self.lineplt(
                    x=x,
                    y=y,
                    colors=l_cs,
                    markers=m_cs,
                    styles=l_styles,
                    labels=labels,
                    xlabel='Races',
                    ylabel=f'{category} {unit}',
                    title=f'League Teams {race} {category}',
                    out_file=out_file)

    def managers_count_line(self,
                            categories: list,
                            units: list,
                            results_dictionary: dict,
                            race: str,
                            races: list,
                            sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot league manager counts line graphs.

        Parameters
        ----------
        categories, units, races: list
            Category names (dictionary keys), corresponding axis label units.
            List of all race names.
        results_dictionary: dictionary
            League results dictionary.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/12/2024
        ----------
        Created.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_LeagueManagers_{category}.png'
            )
            if not out_file.is_file():
                category_dict = results_dictionary[f'Manager {category}']
                normalized_category = category.replace('Sum ', '')
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for manager, values in category_dict.items():
                    x.append(races)
                    y.append(
                        [
                            (values[f'{normalized_category}'])[i]
                            for i in range(len(races))
                        ]
                    )
                    colors = plotting_colors(
                        format_dir=self.format_dir,
                        context='manager',
                        entity=manager,
                        year=self.year
                    )
                    l_cs.append(colors['bg_color'])
                    m_cs.append(colors['bg_color'])
                    l_styles.append('-')
                    labels.append(manager)
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels],
                        index=sort_top,
                        line=True)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels])
                y, x, l_cs, m_cs, l_styles, labels = sorted_arrays
                self.lineplt(
                    x=x,
                    y=y,
                    colors=l_cs,
                    markers=m_cs,
                    styles=l_styles,
                    labels=labels,
                    xlabel='Races',
                    ylabel=f'{category} {unit}',
                    title=f'League Teams {race} {category}',
                    out_file=out_file)

    def leaguecountline(self,
                        categories: list,
                        results_dictionary: list,
                        race: str,
                        races: list,
                        sort_top: int = None,
                        sum_arrays: bool = False) -> None:
        """
        Function Details
        ================
        Plot driver, constructor, boost, extra, and perk counts.

        Parameters
        ----------
        categories, races: list
            Category names (dictionary keys), list of all race names.
        results_dictionary: dictionary
            Manager results dictionary.
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

        Notes
        -----
        Uses plot method.

        Example
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        14/09/2024
        ----------
        Created.

        """
        none = ['None', 'Nonw', 'none', 'nonw']
        non_perk = ['Driver', 'Constructor', 'DRS Boost', 'Extra DRS']
        non_constructor = ['Driver', 'DRS Boost', 'Extra DRS']
        for category in categories:
            normalized_category = category.replace('Sum ', '')
            out_file = Path(
                self.out_path,
                f'{race}_LeagueCounts_{category}.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'League {category}']
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for name, count in category_dict.items():
                    if name in none:
                        continue
                    else:
                        if normalized_category in non_perk:
                            category_type = (
                                {'driver': name}
                                if normalized_category in non_constructor
                                else {'constructor': name})
                        elif normalized_category == 'Perks':
                            category_type = {'perk': name}
                        else:
                            continue
                        key, value = list(category_type.items())[0]
                        colors = plotting_colors(
                            format_dir=self.format_dir,
                            year=self.year,
                            context=key,
                            entity=value)
                        x.append(races)
                        y.append([count[i] for i in range(len(races))])
                        l_cs.append(colors['bg_color'])
                        m_cs.append(colors['color'])
                        l_styles.append('-')
                        labels.append(name)
                if len(y) == 0:
                    continue
                else:
                    if sort_top:
                        sorted_arrays = sort_top_tuples(
                            arrays=[y, x, l_cs, m_cs, l_styles, labels],
                            index=sort_top,
                            line=True)
                    else:
                        sorted_arrays = sort_tuples(
                            arrays=[y, x, l_cs, m_cs, l_styles, labels])
                    y, x, l_cs, m_cs, l_styles, labels = sorted_arrays
                    if sum_arrays:
                        title = f'League {race} {category} Sum Count'
                    else:
                        title = f'League {race} {category} Count'
                    self.lineplt(
                        x=x,
                        y=y,
                        colors=l_cs,
                        markers=m_cs,
                        styles=l_styles,
                        labels=labels,
                        xlabel='Races',
                        ylabel='Counts [#]',
                        title=title,
                        out_file=out_file)

    def league_prizes_lines(self,
                            categories: list,
                            units: list,
                            results_dictionary: dict,
                            race: str,
                            races: list,
                            prize: str,
                            sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot league team results line graphs.

        Parameters
        ----------
        categories, units, races: list
            Category names (dictionary keys), corresponding axis label units.
            List of all race names.
        results_dictionary: dictionary
            League results dictionary.
        race, prize: string
            Race name. Prize name.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        Example
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        17/10/2024
        ----------
        Created.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_{prize}_{category}.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'Team {category}']
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for manager, teams in category_dict.items():
                    for team, values in teams.items():
                        x.append(races)
                        y.append([values[i] for i in range(len(races))])
                        colors = plotting_colors(
                            format_dir=self.format_dir,
                            context='team',
                            entity=team,
                            year=self.year)
                        l_cs.append(colors['bg_color'])
                        m_cs.append(colors['color'])
                        l_styles.append(colors['linestyle'])
                        labels.append(team)
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels],
                        index=sort_top,
                        line=True)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels])
                y, x, l_cs, m_cs, l_styles, labels = sorted_arrays
                self.lineplt(
                    x=x,
                    y=y,
                    colors=l_cs,
                    markers=m_cs,
                    styles=l_styles,
                    labels=labels,
                    xlabel='Races',
                    ylabel=f'{category} {unit}',
                    title=f'{prize} {race} {category}',
                    out_file=out_file)

    def prize_teamcountline(self,
                            categories: list,
                            units: list,
                            results_dictionary: dict,
                            race: str,
                            prize: str,
                            races: list,
                            sort_top: int = None) -> None:
        """
        Function Details
        ================
        Plot league team counts line graphs for prize counts.

        Parameters
        ----------
        categories, units, races: list
            Category names (dictionary keys), corresponding axis label units.
            List of all race names.
        results_dictionary: dictionary
            League results dictionary.
        race, prize: string
            Race name. Prize name for title.
        sort_top: integer, optional
            If sort top is an integer, will sort bar graphs to top x and bottom
            x, where x is the integer. Else will just sort all.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        16/12/2024
        ----------
        Created.

        """
        for category, unit in zip(categories, units):
            out_file = Path(
                self.out_path,
                f'{race}_{prize}_{category}.png'
            )
            if not out_file.is_file():
                category_dict = results_dictionary[f'Teams {category}']
                normalized_category = category.replace('Sum ', '')
                x, y, l_cs, m_cs, l_styles, labels = [], [], [], [], [], []
                for manager, teams in category_dict.items():
                    for team, values in teams.items():
                        x.append(races)
                        y.append(
                            [
                                (values[f'{normalized_category}'])[i]
                                for i in range(len(races))
                            ]
                        )
                        colors = plotting_colors(
                            format_dir=self.format_dir,
                            context='team',
                            entity=team,
                            year=self.year
                        )
                        l_cs.append(colors['bg_color'])
                        m_cs.append(colors['color'])
                        l_styles.append(colors['linestyle'])
                        labels.append(team)
                if sort_top:
                    sorted_arrays = sort_top_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels],
                        index=sort_top,
                        line=True)
                else:
                    sorted_arrays = sort_tuples(
                        arrays=[y, x, l_cs, m_cs, l_styles, labels])
                y, x, l_cs, m_cs, l_styles, labels = sorted_arrays
                self.lineplt(
                    x=x,
                    y=y,
                    colors=l_cs,
                    markers=m_cs,
                    styles=l_styles,
                    labels=labels,
                    xlabel='Races',
                    ylabel=f'{category} {unit}',
                    title=f'{race} {prize}',
                    out_file=out_file)


class LeaguePies(Plot):
    """
    Class Details
    =============

    Attributes
    ----------
    None.

    Methods
    -------
    leaguecount_pie

    Notes
    -----
    None.

    ---------------------------------------------------------------------------
    Update History
    ==============

    15/09/2024
    ----------
    Created.

    """

    def leaguecount_pie(self,
                        categories: list,
                        results_dictionary: dict,
                        race_index: int,
                        race: str,
                        sort_top: int = None,
                        sum_arrays=False) -> None:
        """
        Function Details
        ================
        Plot driver, constructor, boost, extra, and perk counts.

        Parameters
        ----------
        categories: list
            Category names (dictionary keys).
        results_dictionary: dictionary
            Manager results dictionary.
        race_index: integer
            Integer of races array for which to plot.
        race: string
            Race name.
        sort_top: integer, optional
            If sort top is an integer, will sort pie chart to top x and bottom
            x, where x is the integer. Else will just sort all.
        sum_arrays: Bool
            If true, plots sum of the count array.

        Returns
        -------
        None.

        Notes
        -----
        Uses pieplot method.

        -----------------------------------------------------------------------
        Update History
        ==============

        15/09/2024
        ----------
        Created.

        """
        none = ['None', 'Nonw', 'none', 'nonw']
        non_perk = ['Driver', 'Constructor', 'DRS Boost', 'Extra DRS']
        non_constructor = ['Driver', 'DRS Boost', 'Extra DRS']
        for category in categories:
            normalized_category = category.replace('Sum ', '')
            out_file = Path(
                self.out_path,
                f'{race}_LeagueCounts_{category}_Pie.png')
            if not out_file.is_file():
                category_dict = results_dictionary[f'League {category}']
                x_values, y_values, colors, label_colors = [], [], [], []
                for name, count in category_dict.items():
                    if name in none:
                        continue
                    else:
                        if normalized_category in non_perk:
                            category_type = (
                                {'driver': name}
                                if normalized_category in non_constructor
                                else {'constructor': name})
                        elif normalized_category == 'Perks':
                            category_type = {'perk': name}
                        else:
                            continue
                        key, value = list(category_type.items())[0]
                        plot_colors = plotting_colors(
                            format_dir=self.format_dir,
                            year=self.year,
                            context=key,
                            entity=value)
                        x_values.append(name)
                        y_values.append(count[race_index])
                        colors.append(plot_colors['bg_color'])
                        label_colors.append(plot_colors['color'])
                if len(y_values) == 0:
                    continue
                else:
                    if sort_top:
                        sorted_arrays = sort_top_tuples(
                            arrays=[y_values, x_values, colors, label_colors],
                            index=sort_top,
                            pie=True)
                    else:
                        sorted_arrays = sort_tuples(
                            arrays=[y_values, x_values, colors, label_colors])
                    if sum_arrays:
                        title = f'League {race} {category} Sum Count'
                    else:
                        title = f'League {race} {category} Count'
                    y, x, c, lc = sorted_arrays
                    self.pieplot(
                        data=y,
                        labels=x,
                        title=title,
                        out_file=out_file,
                        colors=c,
                        label_colors=lc,
                        explode=0.1)


class Manager_Plots(LeagueBars,
                    LeagueLines,
                    LeaguePies):
    """
    Class Details
    =============
    Functions for plotting various manager and manager team metrics including
    race points, values, sum points, sum values, average points, and counts.

    Attributes
    ----------
    None.

    Methods
    -------
    league_results
    league_stat
    leaguecount
    spotleagueprize
    achieve_prize_lines

    Notes
    -----
    Builds on methods from LeagueBars, LeagueLines, LeaguePies, and Plot
    classes.

    ---------------------------------------------------------------------------
    Update History
    ==============

    02/09/2024
    ----------
    Created.

    15/09/2024
    ----------
    Refactored by ChatGPT.

    """

    def leagues_results(self,
                        race_index: int,
                        race: str,
                        results_dictionary: dict,
                        sort_top: int = 10) -> None:
        """
        Function Details
        ================
        Plot manager and manager team results bar graphs.

        Parameters
        ----------
        race_index: integer
            Index of races array for which to plot.
        race: string
            Race name.
        results_dictionary: dictionary
            Manager/team results dictionary.
        sort_top: int, optional
            Number of top items to sort by. Defaults to 10.

        Returns
        -------
        None.

        -----------------------------------------------------------------------
        Update History
        ==============

        03/09/2024
        ----------
        Created.

        15/09/2024
        ----------
        Updated for helper functions in Manager_Plots class method.

        """
        results_parameters = {
            "team_bar": {
                "categories": ['Points', 'Values'],
                "units": ['[#]', '[$M]'],
                "sort_top": sort_top
            },
            "manager_bar": {
                "categories": ['Average Points', 'Average Values'],
                "units": ['[#]', '[$M]'],
                "sort_top": sort_top
            }
        }
        self._generate_manager_plots(
            plot_type='bar',
            race_index=race_index,
            races=None,
            race=race,
            dictionary=results_dictionary,
            additional_parameters=results_parameters
        )

    def league_stat(self,
                    race_index: int,
                    races: list,
                    race: str,
                    statistics_dictionary: dict,
                    sort_top: int = 10) -> None:
        """
        Function Details
        ================
        Plot manager and manager team statistics bar and line graphs.

        Parameters
        ----------
        race_index: integer
            Index of races array for which to plot.
        races: list
            List of races to process.
        race: string
            Race name.
        statistics_dictionary: dictionary
            Manager/team statistics dictionary.
        sort_top: int, optional
            Number of top items to sort by. Defaults to 10.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        Example
        -------
        >>> manager_plotter = Manager_Plots(out_path, format_path, year)
        >>> manager_plotter.league_stat(race_index, races, race, stats_dict)

        -----------------------------------------------------------------------
        Update History
        ==============

        03/09/2024
        ----------
        Created.

        15/09/2024
        ----------
        Updated for helper functions in Manager_Plots class method.

        """
        statistics_parameters = {
            "manager_bar": {
                "categories": [
                    'Sum Points',
                    'Sum Average Points',
                    'Points Per Value',
                    'Average Points Per Value'],
                "units": ['[#]', '[#]', '[#/$M]', '[#/$M]'],
                "sort_top": sort_top
            },
            "team_bar": {
                "categories": [
                    'Positions Gained',
                    'Sum Points',
                    'Points Per Value'],
                "units": ['[#]', '[#]', '[#/$M]'],
                "sort_top": sort_top
            },
            "team_line": {
                "categories": [
                    'Sum Points', 'Average Points Per Value'],
                "units": ['[#]', '[#/$M]'],
                "sort_top": sort_top
            },
            "manager_line": {
                "categories": [
                    'Sum Points',
                    'Average Points Per Value'],
                "units": ['[#]', '[#/$M]'],
                "sort_top": sort_top
            }
        }
        for plot_type in ['bar', 'line']:
            self._generate_manager_plots(
                plot_type=plot_type,
                race_index=race_index if plot_type != 'line' else None,
                races=None if plot_type != 'line' else races,
                race=race,
                dictionary=statistics_dictionary,
                additional_parameters=statistics_parameters
            )

    def team_counts(self,
                    race_index: int,
                    races: list,
                    race: str,
                    counts_dictionary: dict,
                    counts: list,
                    sort_top: int = 10) -> None:
        """
        Function Details
        ================
        Plot manager and team counts bar and line graphs.

        Parameters
        ----------
        race_index: integer
            Index of races array for which to plot.
        races, counts: list
            List of completed races. Team sheet list to count.
        race: string
            Race name.
        counts_dictionary: dict
            Counts dictionary.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        -----------------------------------------------------------------------
        Update History
        ==============

        03/09/2024
        ----------
        Created.

        15/09/2024
        ----------
        Updated for helper functions in Manager_Plots class method.

        16/12/2024
        ----------
        Copied from leaguecount.

        """
        sum_counts = [f'Sum {count}' for count in counts]
        counts.extend(sum_counts)
        counts_parameters = {
            "team_count_bar": {
                "categories": counts,
                "units": ['[#]'] * len(counts),
                "sort_top": sort_top
            },
            "team_count_line": {
                "categories": counts,
                "units": ['[#]'] * len(counts),
                "sort_top": sort_top
            },
            "manager_count_bar": {
                "categories": counts,
                "units": ['[#]'] * len(counts),
                "sort_top": sort_top
            },
            "manager_count_line": {
                "categories": counts,
                "units": ['[#]'] * len(counts),
                "sort_top": sort_top
            }
        }
        for plot_type in ['bar', 'line']:
            self._generate_manager_plots(
                plot_type=plot_type,
                race_index=race_index if plot_type != 'line' else None,
                races=None if plot_type != 'line' else races,
                race=race,
                dictionary=counts_dictionary,
                additional_parameters=counts_parameters
            )

    def leaguecount(self,
                    race_index: int,
                    races: list,
                    race: str,
                    counts_dictionary: dict,
                    counts: list) -> None:
        """
        Function Details
        ================
        Plot manager and manager team counts bar, line, and pie graphs.

        Parameters
        ----------
        race_index: integer
            Index of races array for which to plot.
        races, counts: list
            List of completed races. Team sheet list to count.
        race: string
            Race name.
        counts_dictionary: dict
            Counts dictionary.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        -----------------------------------------------------------------------
        Update History
        ==============

        03/09/2024
        ----------
        Created.

        15/09/2024
        ----------
        Updated for helper functions in Manager_Plots class method.

        """
        sum_counts = [f'Sum {count}' for count in counts]
        counts.extend(sum_counts)
        counts_parameters = {
            "count_bar": {"categories": counts},
            "count_line": {"categories": counts},
            "count_pie": {"categories": counts}
        }
        for plot_type in ['bar', 'line', 'pie']:
            self._generate_manager_plots(
                plot_type=plot_type,
                race_index=race_index if plot_type != 'line' else None,
                races=None if plot_type != 'line' else races,
                race=race,
                dictionary=counts_dictionary,
                additional_parameters=counts_parameters
            )

    def spotleagueprize(self,
                        race_index: int,
                        race: str,
                        results_dictionary: dict,
                        prize: str,
                        sort_top: int = 10) -> None:
        """
        Function Details
        ================
        Plot manager team results bar graphs for spot prizes.

        Parameters
        ----------
        race_index: integer
            Index of races array for which to plot.
        race, prize: string
            Race name. Prize name.
        results_dictionary: dictionary
            Manager/team results dictionary.
        sort_top: integer, optional
            Number of top teams to sort by, defaults to 10.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        Example
        -------
        >>> manager_plotter = Manager_Plots(out_path, format_path, year)
        >>> manager_plotter.spotleagueprize(
                race_index, race, results_dict, prize)

        -----------------------------------------------------------------------
        Update History
        ==============

        17/10/2024
        ----------
        Created.

        """
        results_parameters = {
            "prize_bar": {
                "categories": ['Points'],
                "units": ['[#]'],
                "prize": prize,
                "sort_top": sort_top
            }
        }
        self._generate_manager_plots(
            plot_type='bar',
            race_index=race_index,
            races=None,
            race=race,
            dictionary=results_dictionary,
            additional_parameters=results_parameters
        )

    def custom_league_count(self,
                            race_index: int,
                            races: list,
                            race: str,
                            counts_dictionary: dict,
                            prize_type: str,
                            prize: str,
                            sort_top: int = 10) -> None:
        """
        Function Details
        ================
        Plot manager team counts for prizes.

        Parameters
        ----------
        race_index: integer
            Index of races array for which to plot.
        races, counts: list
            List of completed_races. Team sheet list to count.
        race, prize: string
            Race name. Prize name.
        counts_dictionary: dict
            Counts dictionary.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        -----------------------------------------------------------------------
        Update History
        ==============

        24/03/2025
        ----------
        Created.

        """

        # Substitutions
        if prize_type == "Substitutions":
            counts = ['Sum Substitutes', 'Sum Penalties']
            counts_parameters = {
                "prize_count_bar": {
                    "categories": counts,
                    "units": ['[#]'] * len(counts),
                    "prize": prize,
                    "sort_top": sort_top
                },
                "prize_count_line": {
                    "categories": counts,
                    "units": ['[#]'] * len(counts),
                    "prize": prize,
                    "sort_top": sort_top
                }
            }
            self._generate_manager_plots(
                plot_type='bar',
                race_index=race_index,
                races=None,
                race=race,
                dictionary=counts_dictionary,
                additional_parameters=counts_parameters
            )
            self._generate_manager_plots(
                plot_type='line',
                race_index=None,
                races=races,
                race=race,
                dictionary=counts_dictionary,
                additional_parameters=counts_parameters
            )

    def custom_league_stats(self,
                            race_index: int,
                            races: list,
                            race: str,
                            prize: str,
                            categories: list,
                            units: list,
                            statistics_dictionary: dict,
                            sort_top: int = 10) -> None:
        """
        Function Details
        ================
        Plot manager team statistics for custom prizes.

        Parameters
        ----------
        race_index: integer
            Index of races array for which to plot.
        races, counts: list
            List of completed_races. Team sheet list to count.
        race, prize: string
            Race name. Prize name.
        categories, units: list
            List of statistics dictionary keys to plot and corresponding units.
        counts_dictionary: dict
            Counts dictionary.

        Returns
        -------
        None.

        Notes
        -----
        Uses plot method.

        -----------------------------------------------------------------------
        Update History
        ==============

        24/03/2025
        ----------
        Created.

        """
        statistics_parameters = {
            "prize_bar": {
                "categories": categories,
                "units": units,
                "prize": prize,
                "sort_top": sort_top
            },
            "prize_line": {
                "categories": categories,
                "units": units,
                "prize": prize,
                "sort_top": sort_top
            }
        }
        for plot_type in ['bar', 'line']:
            self._generate_manager_plots(
                plot_type=plot_type,
                race_index=race_index if plot_type != 'line' else None,
                races=None if plot_type != 'line' else races,
                race=race,
                dictionary=statistics_dictionary,
                additional_parameters=statistics_parameters
            )

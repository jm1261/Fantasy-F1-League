import numpy as np
import src.dataIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot
import matplotlib.pyplot as plt

from pathlib import Path


def spot_prizes(manager_results : dict,
                max_races : list,
                min_races : list,
                prize_names: dict) -> dict:
    """
    Find the winners/losers at the races that are spot prizes.

    Find the maximum and minimum scores for the given races and assign the team
    and manager to the prize name.

    Parameters
    ----------
    manager_results, prize_names: dictionary
        Manager results showing manager, team and scores for all races. Prize
        names assigned by league owner with name of prize and the race.
    max_races, min_races: list
        List of maximum score and minimum score prize race names.

    Returns
    -------
    spot_prize_dict: dictionary
        Dictionary containing the prize names as keys, followed by an array
        of the race name, manager name, team name, and score that won the prize.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    """
    max_spot_results = {}
    min_spot_results = {}
    team_points = manager_results["Team Points"]
    for race in max_races:
        race_index = races.index(race)
        max_spot_results.update({race: ["Race", "Test", "Test", 0]})
        for manager, teams in team_points.items():
            for team, scores in teams.items():
                race_score = scores[race_index]
                if race_score > (max_spot_results[f'{race}'])[3]:
                    max_spot_results[f'{race}'] = [
                        f'{race}',
                        f'{manager}',
                        f'{team}',
                        race_score]
                elif race_score == (max_spot_results[f'{race}'])[3]:
                    print(f'{races[race_index]} Spot Problem')
                else:
                    pass
    for race in min_races:
        race_index = races.index(race)
        min_spot_results.update({race: ["Race", "Test", "Test", 1000]})
        for manager, teams in team_points.items():
            for team, scores in teams.items():
                race_score = scores[race_index]
                if race_score < (min_spot_results[f'{race}'])[3]:
                    min_spot_results[f'{race}'] = [
                        f'{race}',
                        f'{manager}',
                        f'{team}',
                        race_score]
                elif race_score == (min_spot_results[f'{race}'])[3]:
                    print(f'{races[race_index]} Spot Problem')
                else:
                    pass
    spot_prizes_dict = {}
    for race, prize in prize_names.items():
        if race in max_spot_results.keys():
            spot_prizes_dict.update({prize: max_spot_results[race]})
        if race in min_spot_results.keys():
            spot_prizes_dict.update({prize: min_spot_results[race]})
    return spot_prizes_dict


def prizes_bars(category_dict : dict,
                race_index : int,
                race : str,
                format_dir : str,
                out_path : str,
                title : str) -> None:
    """
    Plot top 10 and bottom 10 managers weekly.

    Plot top 10 and bottom 10 managers teams for specified races.

    Parameters
    ----------
    category_dictionary: dictionary
        Manager results dictionary.
    race_index: int
        Integer of races array for which to plot.
    race, format_dir, out_path, title: string
        Race name, path to format directory, path to save. Graph title.
    
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
    """
    out_file = Path(f'{out_path}/Prize_{race}_Bar.png')
    if out_file.is_file():
        pass
    else:
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
                colors = plot.plotting_colour(
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
            'Points [#]',
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
            f'{title}',
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


def sum_dict(dictionary : dict) -> dict:
    """
    Calculate the total (sum) points from a dictionary of scores.

    Also calculates average scores.

    Parameters
    ----------
    results_dict: dictionary
        Lineup results dictionary.
    
    Returns
    -------
    dictionary: dictionary
        Lineup total points and average points.
    
    See Also
    --------
    sum_values
    sum_points

    Notes
    -----
    None

    Example
    -------
    None

    """
    sum_points = {}
    average_points = {}
    for manager, teams in dictionary.items():
        manager_sum = {}
        manager_average = {}
        for team, all_points in teams.items():
            points = []
            avg_points = []
            for index, point in enumerate(all_points):
                if index == 0:
                    points.append(point)
                    avg_points.append(point)
                else:
                    points.append(point + points[index - 1])
                    avg_points.append(points[index] / (index + 1))
            manager_sum.update({f'{team}': points})
            manager_average.update({f'{team}': avg_points})
        sum_points.update({f'{manager}': manager_sum})
        average_points.update({f'{manager}': manager_average})
    dictionary = {
        'Sum Points': sum_points,
        'Average Points': average_points}
    return dictionary


def prize_lines(category_dict : dict,
                races : list,
                prize : str,
                format_dir : str,
                out_path : str) -> None:
    """
    Plot prizes statistics.

    Parameters
    ----------

    Returns
    -------
    None

    See Also
    --------
    plotting_color
    leagueteam_stat

    Notes
    -----
    None

    Example
    -------
    None

    """
    categories = ['Sum Points', 'Average Points']
    units = ['[#]', '[#]']
    for category, unit in zip(categories, units):
        out_file = Path(f'{out_path}/{prize}_{category}.png')
        if out_file.is_file():
            pass
        else:
            results_dict = category_dict[f'{category}']
            fig, ax = plt.subplots(
                nrows=1,
                ncols=1,
                figsize=[10, 7],
                dpi=600)
            sum_values = []
            x_values = []
            y_values = []
            colors = []
            markers = []
            names = []
            lines = []
            for manager, teams in results_dict.items():
                for team, values in teams.items():
                    x_values.append(races)
                    y_values.append([values[i] for i in range(len(races))])
                    sum_values.append(values[-1])
                    colours = plot.plotting_colour(
                        format_dir=format_dir,
                        manager_team=team)
                    colors.append(colours['bg_color'])
                    markers.append(colours['color'])
                    names.append(team)
                    lines.append(colours['linestyle'])
            zipped_lists = zip(
                sum_values,
                y_values,
                x_values,
                colors,
                markers,
                names,
                lines)
            sorted_pairs = sorted(zipped_lists)
            tuples = zip(*sorted_pairs[0: 10])
            _, top_y, top_x, top_c, top_m, top_n, top_l = [
                list(tuple) for tuple in tuples]
            tuples = zip(*sorted_pairs[-10:])
            _, bot_y, bot_x, bot_c, bot_m, bot_n, bot_l = [
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
                f'{prize} {category}',
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


def findmax(results_dict : dict) -> dict:
    """
    Find the maximum values of an array in a dictionary and sort into order.
    """
    y_values = []
    names = []
    for manager, teams in results_dict.items():
        for team, values in teams.items():
            y_values.append(values[-1])
            names.append(team)
    zipped_lists = zip(
        y_values,
        names)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    all_y, all_n = [list(tuple) for tuple in tuples]
    teams_orders = all_n[::-1]
    points_order = all_y[::-1]
    findmax_dict = {}
    for team, points in zip(teams_orders, points_order):
        findmax_dict.update({f'{team}': points})
    return findmax_dict


def findmax_manager(results_dict : dict) -> dict:
    """
    Find the maximum values of an array in a dictionary and sort into order.
    """
    y_values = []
    names = []
    for manager, values in results_dict.items():
        y_values.append(values[-1])
        names.append(manager)
    zipped_lists = zip(
        y_values,
        names)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    all_y, all_n = [list(tuple) for tuple in tuples]
    managers_orders = all_n[::-1]
    points_order = all_y[::-1]
    findmax_dict = {}
    for manager, points in zip(managers_orders, points_order):
        findmax_dict.update({f'{manager}': points})
    return findmax_dict


if __name__ == '__main__':
    year = 2023
    root = Path().absolute()
    info_path = Path(f'{root}/Info.json')
    data_path = Path(f'{root}/Data/{year}')
    format_dir = Path(f'{data_path}/Manager_Formats')
    manager_path = Path(f'{data_path}/Managers')

    info_dict = io.load_json(file_path=info_path)
    managers_dict = info_dict['Managers']
    lineup_dict = io.load_json(
            file_path=Path(f'{data_path}/Lineup/Results.json'))
    manager_results = io.load_json(
        file_path=Path(f'{manager_path}/Results.json'))
    manager_statistics = io.load_json(
        file_path=Path(f'{manager_path}/Statistics.json'))
    races_sofar, races = io.get_races_sofar(
        file_path=info_path,
        results_path=Path(f'{data_path}/Lineup'))

    """ Winners """
    league_scores = findmax(results_dict=manager_statistics['Team Sum Points'])

    """ Viking Comeback """
    scores = []
    names = []
    for manager, teams in team_points.items():
        for team, points in teams.items():
            scores.append(points[0])
            names.append(team)
    zipped_lists = zip(scores, names)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs[-5: ])
    scores, names = [list(tuple) for tuple in tuples]
    bahrain_scores = {}
    for score, name in zip(scores[::-1], names[::-1]):
        bahrain_scores.update({f'{name}': [score]})
    for manager, teams in manager_statistics['Team Sum Points'].items():
        for team, points in teams.items():
            if team in bahrain_scores.keys():
                bahrain_scores[team].append(points[-1])
    league_teams = league_scores.keys()
    for index, team in enumerate(league_teams):
        if team in bahrain_scores.keys():
            bahrain_scores[team].append(index + 1)

    """ Manager of the Year """
    manager_averages = manager_statistics['Manager Sum Average Points']
    max_managers_averages = findmax_manager(results_dict=manager_averages)

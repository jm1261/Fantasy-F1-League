import sys
import src.dataIO as io
import src.prizes as prize
import plotting as plot
# import src.old_plotting as plot

from pathlib import Path


def managers_prizes(root: str,
                    year: str) -> None:
    """
    Function Details
    ================
    Parameters
    ----------
    Returns
    -------
    See Also
    --------
    Notes
    -----
    Example
    -------

    ----------------------------------------------------------------------------
    Update History
    ==============

    02/04/2024
    ----------
    Created.

    """

    """ Config Files and Season Info """
    config = io.Configuration(
        root_directory=root,
        year=year)
    config.info_dictionary(file_name='Info.json')
    config.get_completed_races(races=config.info_dict['Races'])
    config.manager_results(file_name='Results.json')
    config.managers_statistics(file_name='Statistics.json')
    config.gets_prizes(file_name=f'{year}.json')

    """ Find Potential Prize Categories """
    prize_categories = config.prizes.keys()

    """ Spot Prizes """
    if "Spot" in prize_categories:
        spot_prize_winners = prize.spot_prizes(
            team_dictionary=config.manager_results["Team Points"],
            spot_prizes=config.prizes["Spot"],
            completed_races=config.completed_races)
        config.prizes["Spot"].update(
            {"Spot Winners": spot_prize_winners})
        comp_races = [
            race
            for race in
            config.prizes['Spot']['Spot Max'] +
            config.prizes['Spot']['Spot Min']
            if race in config.completed_races]
        comp_indices = [
            config.completed_races.index(race)
            for race in comp_races]
        prize_names = [
            config.prizes['Spot']['Spot Names'][f'{race}']
            for race in comp_races]
        for index, race, name in zip(comp_indices, comp_races, prize_names):
            manager_plotter = plot.Manager_Plots(
                out_path=Path(config.data_path, 'Figures', 'Prizes'),
                format_dir=config.format_path,
                year=year)
            manager_plotter.spotleagueprize(
                race_index=index,
                race=race,
                results_dictionary=config.manager_results,
                prize=name)

    """ Achievement Prizes """
    if "Achievements" in prize_categories:
        season_goals_dict = config.prizes["Achievements"]
        season_goals = season_goals_dict["Achievement Names"]
        if "Sprint" in season_goals.keys():
            sprint_races = season_goals_dict["Sprint Races"]
            exists = any(
                race in sprint_races for race in config.completed_races)
            if exists:
                sprint_dict = prize.short_season_result(
                    results=config.manager_results['Team Points'],
                    completed_races=config.completed_races,
                    specific_races=sprint_races)
                """ Plot manager stuff here """
                sprintking = prize.findmax(
                    results_dict=sprint_dict["Sum Points"])
                config.prizes["Achievements"].update(
                    {f'{season_goals["Sprint"]}': sprintking})
                for index, race in enumerate(sprint_races):
                    if race in config.completed_races:
                        races = sprint_races[0: index + 1]
                        manager_plotter = plot.Manager_Plots(
                            out_path=Path(
                                config.data_path, 'Figures', 'Prizes'),
                            format_dir=config.format_path,
                            year=year)
                        manager_plotter.achieve_prize_lines(
                            races=races,
                            race=race,
                            results_dictionary=sprint_dict,
                            prize=season_goals["Sprint"])
        if "World" in season_goals.keys():
            world_races = season_goals_dict["World Races"]
            exists = any(race in world_races for race in world_races)
            if exists:
                world_dict = prize.short_season_result(
                    results=config.manager_results['Team Points'],
                    completed_races=config.completed_races,
                    specific_races=world_races)
                """ Plot manager stuff here """
                champworld = prize.findmax(
                    results_dict=world_dict["Sum Points"])
                config.prizes["Achievements"].update(
                    {f'{season_goals["World"]}': champworld})
                for index, race in enumerate(world_races):
                    if race in config.completed_races:
                        races = world_races[0: index + 1]
                        manager_plotter = plot.Manager_Plots(
                            out_path=Path(
                                config.data_path, 'Figures', 'Prizes'),
                            format_dir=config.format_path,
                            year=year)
                        manager_plotter.achieve_prize_lines(
                            races=races,
                            race=race,
                            results_dictionary=world_dict,
                            prize=season_goals["World"])


    """ Championship """
    if len(config.completed_races) == len(config.info_dict["Races"]):

        """ Highest/Lowest """
        """ Highest Value """
        """ Manager of the Year """
        """ Transfers """
        """ League Totals """
    return config.prizes


if __name__ == '__main__':
    year = 2024
    # year = sys.argv[1]
    root = Path().absolute()
    prizes_dict = managers_prizes(
        root=root,
        year=year)
    io.save_json_dicts(
        out_path=Path(f'{root}/Prizes/{year}.json'),
        dictionary=prizes_dict)


    # """ End of Season Goals """
    # if len(completed_races) == len(info_dict["Races"]):

    #     """ Highest/Lowest Weekly """
    #     high_low_dict = higher_or_lower(
    #         results_dictionary=team_points,
    #         completed_races=completed_races)
    #     prizes_dict["Season Goals"].update({"Highest and Lowest": high_low_dict})
        
    #     """ Highest Value """
    #     max_value, ties = max_dicts_value(
    #         team_dictionary=manager_results["Team Values"],
    #         races=['Abu Dhabi'],
    #         completed_races=completed_races)
    #     prizes_dict["Season Goals"].update({"Highest Value": max_value[0]})

    #     """ Manager of the Year """
    #     top_five_managers = manager_of_the_year(
    #         manager_statistics=manager_statistics["Manager Sum Average Points"],
    #         info_dictionary=info_dict,
    #         number_of_teams_limit=0)
    #     prizes_dict["Season Goals"].update({"Manager of the Year": top_five_managers})

    #     """ Comeback """
    #     viking = viking_comeback(
    #         team_points=manager_statistics["Team Sum Points"],
    #         top_index=5)
    #     prizes_dict["Season Goals"].update({"Viking Comeback": viking})

    #     """ League Totals """
    #     league_winners = league_achievements(
    #         team_points=manager_statistics["Team Sum Points"],
    #         league_goals=prizes_dict["League Goals"])
    #     prizes_dict["League Goals"].update({'League Winners': league_winners})

    # io.save_json_dicts(
    #     out_path=Path(f'{prizes_path}/{year}.json'),
    #     dictionary=prizes_dict)

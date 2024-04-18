import sys
import src.dataIO as io
import src.prizes as prize
import src.plotting as plot

from pathlib import Path


def managers_prizes(root : str,
                    year : str) -> None:
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
    info_path = Path(f'{root}/Info.json')
    info_dict = (io.load_json(file_path=info_path))[f'{year}']
    managers_dict = info_dict["Managers"]
    data_path = Path(f'{root}/Data/{year}')
    lineup_dict = io.load_json(
        file_path=Path(f'{data_path}/Lineup/Results.json'))
    manager_path = Path(f'{data_path}/Managers')
    manager_results = io.load_json(
        file_path=Path(f'{manager_path}/Results.json'))
    team_points = manager_results["Team Points"]
    manager_statistics = io.load_json(
        file_path=Path(f'{manager_path}/Statistics.json'))
    format_path = Path(f'{root}/Config')
    results_path = Path(f'{data_path}/Lineup')
    prizes_path = Path(f'{root}/Prizes')
    prizes_dict = io.load_json(
        file_path=Path(f'{prizes_path}/{year}.json'))
    out_path = Path(f'{data_path}/Figures/Prizes')

    """ Check Complete Races """
    completed_races = io.get_completed_races(
        results_path=results_path,
        info_dictionary=info_dict)

    """ Find Potential Prize Categories """
    prize_categories = prizes_dict.keys()

    """ Spot Prizes """
    if "Spot" in prize_categories:
        spot_prize_winners = prize.spot_prizes(
            team_dictionary=manager_results["Team Points"],
            spot_prizes=prizes_dict["Spot"],
            completed_races=completed_races)
        prizes_dict["Spot"].update(
            {"Spot Winners": spot_prize_winners})
        for index, race in enumerate(completed_races):
            sp = prizes_dict["Spot"]
            if race in sp["Spot Max"] or race in sp["Spot Min"]:
                plot.prizes_bars(
                    category_dictionary=team_points,
                    race_index=index,
                    race=race,
                    year=year,
                    format_dir=format_path,
                    out_path=out_path,
                    title=(sp["Spot Names"])[f'{race}'])

    """ Achievement Prizes """
    if "Achievements" in prize_categories:
        season_goals_dict = prizes_dict["Achievements"]
        season_goals = season_goals_dict["Achievement Names"]
        if "Sprint" in season_goals.keys():
            sprint_races = season_goals_dict["Sprint Races"]
            exists = any(race in sprint_races for race in completed_races)
            if exists:
                sprint_dict = prize.short_season_result(
                    results=team_points,
                    completed_races=completed_races,
                    specific_races=sprint_races)
                """ Plot manager stuff here """
                sprintking = prize.findmax(
                    results_dict=sprint_dict["Sum Points"])
                prizes_dict["Achievements"].update(
                    {f'{season_goals["Sprint"]}': sprintking})
            for index, race in enumerate(sprint_races):
                if race in completed_races:
                    races = sprint_races[0: index + 1]
                    plot.prize_lines(
                        results_dictionary=sprint_dict,
                        race=race,
                        prize=season_goals["Sprint"],
                        races=races,
                        format_dir=format_path,
                        year=year,
                        out_path=out_path)
        if "World" in season_goals.keys():
            world_races = season_goals_dict["World Races"]
            exists = any(race in world_races for race in world_races)
            if exists:
                world_dict = prize.short_season_result(
                    results=team_points,
                    completed_races=completed_races,
                    specific_races=world_races)
                """ Plot manager stuff here """
                champworld = prize.findmax(
                    results_dict=world_dict["Sum Points"])
                prizes_dict["Achievements"].update(
                    {f'{season_goals["World"]}': champworld})
            for index, race in enumerate(world_races):
                if race in completed_races:
                    races = world_races[0: index + 1]
                    plot.prize_lines(
                        results_dictionary=world_dict,
                        race=race,
                        prize=season_goals["World"],
                        races=races,
                        format_dir=format_path,
                        year=year,
                        out_path=out_path)

    """ Championship """
    if len(completed_races) == len(info_dict["Races"]):

        """ Highest/Lowest """
        """ Highest Value """
        """ Manager of the Year """
        """ Transfers """
        """ League Totals """
    return prizes_dict


if __name__ == '__main__':
    #year = 2024
    year = sys.argv[1]
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

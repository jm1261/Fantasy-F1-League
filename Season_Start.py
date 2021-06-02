import os
import Functions.Organisation as org


def create_lineup(root, config):
    '''
    create_lineups creates 4 json dictionaries containing the teams and drivers
    for the current racing year, taken from an input config file. The input
    dictionary must contain a list of keys and array values with the driver/
    team names. The 4 created dictionaries are for driver/team points/values.
    Only use this function at the start of the season as it wipes all other
    files with the same name.
    Args:
        root: <string> directory path to output
        config: <dict> dictionary with keys and array values
    Returns:
        None: creates 4 dictionaries at root
    '''
    lineup = config.items()
    teams = [key for key, values in lineup]
    drivers = []
    for key, values in lineup:
        for value in values:
            drivers.append(value)
    team_points = {}
    team_values = {}
    [team_points.update({team: []}) for team in teams]
    [team_values.update({team: []}) for team in teams]
    driver_points = {}
    driver_values = {}
    [driver_points.update({driver: []}) for driver in drivers]
    [driver_values.update({driver: []}) for driver in drivers]
    org.dump_json(
        dictionary=team_points,
        out_path=os.path.join(
            root,
            'Team_Points.config'
        )
    )
    org.dump_json(
        dictionary=team_values,
        out_path=os.path.join(
            root,
            'Team_Values.config'
        )
    )
    org.dump_json(
        dictionary=driver_points,
        out_path=os.path.join(
            root,
            'Driver_Points.config'
        )
    )
    org.dump_json(
        dictionary=driver_values,
        out_path=os.path.join(
            root,
            'Driver_Values.config'
        )
    )


def create_teams(root, managers, info):
    '''
    create_teams creates the manager directories and corresponding team config
    files based on the information provided in manager and info config files.
    The function creates individual team config files with driver, team, turbo,
    mega, and penalty entries to match previous work with excel.
    Args:
        root: <string> path to root directory
        managers: <dict> manager dictionary
        info: <dict> season info dictionary
    Returns:
        None: creates manager directories and team config files
    '''
    team_dict = {}
    [team_dict.update({value: []}) for value in info['Team']]
    for key, values in managers.items():
        manager_dir = os.path.join(root, f'{key}')
        org.check_dir_exists(dir_path=manager_dir)
        for value in values:
            org.dump_json(
                dictionary=team_dict,
                out_path=os.path.join(
                    manager_dir,
                    f'{value}.config'
                )
            )


if __name__ == '__main__':

    ''' Select Year '''
    root = os.path.join(os.getcwd(), '2021')
    org.check_dir_exists(dir_path=root)

    ''' Load Driver and Team Lineup Files '''
    lineup = org.get_config(
        config_path=os.path.join(
            root,
            '..',
            'Lineup.config'
        )
    )
    lineup_dir = os.path.join(root, 'Lineup')
    org.check_dir_exists(dir_path=lineup_dir)
    create_lineup(root=lineup_dir, config=lineup)

    ''' Create Fantasy League Teams and Manager Directories '''
    season_info = org.get_config(
        config_path=os.path.join(
            root,
            '..',
            'Info.config'
        )
    )
    managers = org.get_config(
        config_path=os.path.join(
            root,
            '..',
            'Managers.config'
        )
    )
    create_teams(
        root=root,
        managers=managers,
        info=season_info
    )

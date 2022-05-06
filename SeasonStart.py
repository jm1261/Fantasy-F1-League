import os
import Functions.Organisation as org


def create_lineup(config):
    '''
    Creates 4 arrays containing the teams and drivers for current racing year,
    taken from an input config file. Input config must contain list of keys
    and array values with driver/team names.
    Args:
        config: <dict> dictionary with keys and array values
    Returns:
        configs: <arrau> array of team/driver points/values dictionaries
    '''
    lineup = config.items()
    teams = [key for key, values in lineup]
    drivers = []
    for key, values in lineup:
        [drivers.append(value) for value in values]
    team_points = {}
    team_values = {}
    [team_points.update(
        {team: []})
     for team in teams]
    [team_values.update(
        {team: []})
     for team in teams]
    driver_points = {}
    driver_values = {}
    [driver_points.update(
        {driver: []})
     for driver in drivers]
    [driver_values.update(
        {driver: []})
     for driver in drivers]
    configs = [
        team_points,
        team_values,
        driver_points,
        driver_values]
    return configs


def create_teams(root,
                 managers,
                 info):
    '''
    Create manager dictionaries corresponding to team, manager, and info config
    files. Creates individual team config files with team info from config.
    Args:
        root: <string> path to root directory
        managers: <dict> manager dictionary
        info: <dict> season info dictionary
    Returns:
        None: creates manager directories and team config files
    '''
    team_dict = {}
    [team_dict.update(
        {value: []}
     for value in info['Team'])]
    for key, values in managers.items():
        manager_dir = os.path.join(
            root,
            f'{key}')
        org.check_dir_exists(dir_path=manager_dir)
        [org.dump_json(
            dictionary=team_dict,
            out_path=os.path.join(
                manager_dir,
                f'{value}.config'))
         for value in values]


if __name__ == '__main__':

    ''' Organisation '''
    year = '2022'
    root = os.path.join(
        os.getcwd(),
        year)
    org.check_dir_exists(dir_path=root)

    ''' Load Driver and Team Lineup Configs '''
    lineupconfig = org.get_config(
        config_path=os.path.join(
            root,
            '..',
            'Lineup.config'))
    lineupdir = os.path.join(
        root,
        'Lineup')
    org.check_dir_exists(dir_path=lineupdir)
    configs = create_lineup(config=lineupconfig)
    configsnames = [
        'Team_Points',
        'Team_Values',
        'Driver_Points',
        'Driver_Values']
    [org.dump_json(
        dictionary=configs[i],
        out_path=os.path.join(
            lineupdir,
            f'{configsnames[i]}.config'))
     for i in range(len(configs))]

    ''' Create Fantasy Teams and Manager Directories '''
    seasosinfoconfig = org.get_config(
        config_path=os.path.join(
            root,
            '..',
            'Info.config'))
    managersconfig = org.get_config(
        config_path=os.path.join(
            root,
            '..',
            'Managers.config'))
    create_teams(
        root=root,
        managers=managersconfig,
        info=seasosinfoconfig)

    ''' Create Plot Directory '''
    plotdir = os.path.join(
        root,
        'Figures')
    org.check_dir_exists(dir_path=plotdir)

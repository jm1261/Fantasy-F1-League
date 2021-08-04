import os
import xlsxwriter as xlsx
import Functions.SeasonInfo as si
import Functions.Organisation as org

''' Organisation '''
year = '2021'
root = os.path.join(
    os.getcwd(),
    year)
lineup_dir = os.path.join(
    root,
    'Lineup')
format_dir = os.path.join(
    root,
    '..',
    'Formats')

''' Config Files '''
info = org.get_config(
    config_path=os.path.join(
        root,
        '..',
        'Info.config'
    )).items()
managers = org.get_config(
    config_path=os.path.join(
        root,
        '..',
        'Managers.config'
    )).items()
lineup = org.get_config(
    config_path=os.path.join(
        root,
        '..',
        'Lineup.config'
    )).items()
driver_points = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Individual_Driver_Points.config'
    ))
driver_values = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Driver_Values.config'
    ))
team_points = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Individual_Team_Points.config'
    ))
team_values = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Team_Values.config'
    ))

''' Count Races, Drivers, Teams, And Load Team Layout '''
season_length, races = si.season_length(dictionary=info)
teams, drivers, index = si.teams_drivers(dictionary=lineup)
stats = si.statistics(dictionary=info)
team_setup = si.team_setup(dictionary=info)
rsf = si.races_so_far(dictionary=driver_points)

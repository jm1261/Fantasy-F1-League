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
rsf = si.races_so_far(dictionary=driver_points.items())

''' Print Season Parameters '''
print(f'The season is {season_length} races long, the races are {races}.\n'
      f'There are {len(teams)} teams, who are {teams}.\n'
      f'There are {len(drivers)} drivers, who are {drivers}.\n'
      f'To date there have been {rsf} races, these are {races[0: rsf]}.')

''' Loop Managers '''
for manager, teams in managers:

    ''' More Organisation '''
    spreadsheet_name = f'{manager}_{year}.xlsx'
    dirpath = os.path.join(
        root,
        f'{manager}')
    org.check_dir_exists(dir_path=dirpath)
    filepath = os.path.join(
        dirpath,
        spreadsheet_name)

    ''' Create Spreadsheet '''
    workbook = xlsx.Workbook(filepath)

    ''' Create Cell Formats '''
    header_format = workbook.add_format(
        org.get_config(
            config_path=os.path.join(
                format_dir,
                'Header.config'
            )
        ).items())
    red_format = workbook.add_format(
        org.get_config(
            config_path=os.path.join(
                format_dir,
                'Red.config'
            )
        ).items())
    data_format = workbook.add_format(
        org.get_config(
            config_path=os.path.join(
                format_dir,
                'Data.config'
            )
        ).items())

    ''' Check Team Name Lengths '''
    team_names = [team[0: 31] if len(team) > 31 else team 
                  for team in teams]
    
    ''' Loop Teams '''
    for index, team in enumerate(teams):

        ''' Create Team Sheets '''
        team_sheet = workbook.add_worksheet(f'{team_names[index]}')

    ''' Close Workbook '''
    workbook.close()

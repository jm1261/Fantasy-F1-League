import os
import xlsxwriter as xlsx
from collections import Counter
import Functions.SeasonInfo as si
import Functions.Dictionary as dct
import Functions.Organisation as org
import matplotlib.pyplot as plt

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
raceteams, drivers, indix = si.teams_drivers(dictionary=lineup)
stats = si.statistics(dictionary=info)
team_setup = si.team_setup(dictionary=info)
rsf = si.races_so_far(dictionary=driver_points.items())

''' Print Season Parameters '''
print(f'The season is {season_length} races long, the races are {races}.\n'
      f'There are {len(raceteams)} teams, who are {raceteams}.\n'
      f'There are {len(drivers)} drivers, who are {drivers}.\n'
      f'To date there have been {rsf} races, these are {races[0: rsf]}.')

''' Statistics Configs '''
stats_dir = os.path.join(
    root,
    'Statistics')
org.check_dir_exists(dir_path=stats_dir)
score_dict = {}
value_dict = {}
driver_dict = {}
team_dict = {}
turbo_dict = {}
mega_dict = {}

''' Loop Managers '''
for manager, teams in managers:

    ''' Open Spreadsheet '''
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
                'Header.config')).items())
    red_format = workbook.add_format(
        org.get_config(
            config_path=os.path.join(
                format_dir,
                'Red.config')).items())
    data_format = workbook.add_format(
        org.get_config(
            config_path=os.path.join(
                format_dir,
                'Data.config')).items())

    ''' Check Team Name Lengths '''
    team_names = [
        team[0: 31] if len(team) > 31 else team
        for team in teams]

    ''' Output Config '''
    manager_score_dict = {}
    manager_value_dict = {}
    manager_driver_dict = {}
    manager_team_dict = {}
    manager_turbo_dict = {}
    manager_mega_dict = {}

    ''' Loop Teams '''
    for index, team in enumerate(teams):

        ''' Output Config '''
        team_driver_dict = {}
        team_team_dict = {}
        team_turbo_dict = {}
        team_mega_dict = {}

        ''' Create Team Sheet '''
        team_sheet = workbook.add_worksheet(f'{team_names[index]}')

        ''' Team Config File '''
        team_config = org.get_config(
            config_path=os.path.join(
                dirpath,
                f'{team}.config')).items()

        ''' Team Points and Values '''
        teampoints = dct.team_dict(
            team_name=team,
            team_dict=team_config,
            driver_points_dict=driver_points,
            team_points_dict=team_points)
        teamvalues = dct.team_dict(
            team_name=team,
            team_dict=team_config,
            driver_values_dict=driver_values,
            team_values_dict=team_values)

        ''' Team Statistics '''
        season_points = dct.team_points(
            manager_dict=teampoints.items(),
            races=rsf)
        season_values = dct.team_points(
            manager_dict=teamvalues.items(),
            races=rsf)
        drivercount, teamcount, turbocount, megacount = dct.team_counter(
            manager_dict=team_config)

        ''' Write Configs '''
        manager_score_dict.update({team: season_points})
        manager_value_dict.update({team: season_values})
        team_driver_dict.update(drivercount)
        team_team_dict.update(teamcount)
        team_turbo_dict.update(turbocount)
        team_mega_dict.update(megacount)
        score_dict.update({team: season_points})
        value_dict.update({team: season_values})
        for key, value in team_driver_dict.items():
            if key in manager_driver_dict:
                newvalue = value + manager_driver_dict[key]
                manager_driver_dict.update({key: newvalue})
            else:
                manager_driver_dict.update({key: value})
        for key, value in team_team_dict.items():
            if key in manager_team_dict:
                newvalue = value + manager_team_dict[key]
                manager_team_dict.update({key: newvalue})
            else:
                manager_team_dict.update({key: value})
        for key, value in team_turbo_dict.items():
            if key in manager_turbo_dict:
                newvalue = value + manager_turbo_dict[key]
                manager_turbo_dict.update({key: newvalue})
            else:
                manager_turbo_dict.update({key: value})
        for key, value in team_mega_dict.items():
            if key in manager_mega_dict:
                newvalue = value + manager_mega_dict[key]
                manager_mega_dict.update({key: newvalue})
            else:
                manager_mega_dict.update({key: value})
        for key, value in team_driver_dict.items():
            if key in driver_dict:
                newvalue = value + driver_dict[key]
                driver_dict.update({key: newvalue})
            else:
                driver_dict.update({key: value})
        for key, value in team_team_dict.items():
            if key in team_dict:
                newvalue = value + team_dict[key]
                team_dict.update({key: newvalue})
            else:
                team_dict.update({key: value})
        for key, value in team_turbo_dict.items():
            if key in turbo_dict:
                newvalue = value + turbo_dict[key]
                turbo_dict.update({key: newvalue})
            else:
                turbo_dict.update({key: value})
        for key, value in team_mega_dict.items():
            if key in mega_dict:
                newvalue = value + mega_dict[key]
                mega_dict.update({key: newvalue})
            else:
                mega_dict.update({key: value})

        ''' Wite Excel File '''

        ''' Names '''
        team_sheet.write(
            0,
            0,
            'Names',
            red_format)  # Identifier
        column = 0
        team_sheet.write_column(
            row=1,
            col=column,
            data=races,
            cell_format=header_format)  # Races
        column += 1
        team_sheet.write_row(
            row=0,
            col=column,
            data=team_setup,
            cell_format=header_format)  # Column Headers
        for key, values in team_config:
            team_sheet.write_column(
                row=1,
                col=column,
                data=values,
                cell_format=data_format)  # Driver Selection
            column += 1
        
        for i in range(0, len(drivers)):
            cell_format = workbook.add_format(
                org.get_config(
                    config_path=os.path.join(
                        format_dir,
                        f'{indix[i]}.config')).items())
            team_sheet.write(
                1 + i,
                column,
                f'{drivers[i]}',
                cell_format)
            team_sheet.write(
                0,
                column + 1,
                'Driver Usage',
                red_format)  # Identifier
            if f'{drivers[i]}' in team_driver_dict:
                team_sheet.write(
                    1 + i,
                    column + 1,
                    team_driver_dict[f'{drivers[i]}'],
                    data_format)
            else:
                pass
            team_sheet.write(
                0,
                column + 2,
                'Turbo Usage',
                red_format)  # Identifier
            if f'{drivers[i]}' in team_turbo_dict:
                team_sheet.write(
                    1 + i,
                    column + 2,
                    team_turbo_dict[f'{drivers[i]}'],
                    data_format)
            else:
                pass
            team_sheet.write(
                0,
                column + 3,
                'Mega Usage',
                red_format)  # Identifier
            if f'{drivers[i]}' in team_mega_dict:
                team_sheet.write(
                    1 + i,
                    column + 3,
                    team_mega_dict[f'{drivers[i]}'],
                    data_format)
            else:
                pass
        column += 4
        for i in range(0, len(raceteams)):
            cell_format = workbook.add_format(
                org.get_config(
                    config_path=os.path.join(
                        format_dir,
                        f'{raceteams[i]}.config')).items())
            team_sheet.write(
                1 + (2 * i),
                column,
                f'{raceteams[i]}',
                cell_format)
            team_sheet.write(
                0,
                column + 1,
                'Team Usage',
                red_format)  # Identifier
            if f'{raceteams[i]}' in team_team_dict:
                team_sheet.write(
                    1 + (2 * i),
                    column + 1,
                    team_team_dict[f'{raceteams[i]}'],
                    data_format)
            else:
                pass

        ''' Dump Configs '''

    ''' Close Workbook '''
    workbook.close()

import os
import xlsxwriter as xlsx
import Functions.Maths as maths
import Functions.SeasonInfo as si
import Functions.Organisation as org

''' Organisation '''
year = '2021'
root = os.path.join(
    os.getcwd(),
    year)
spreadsheet_name = f'Fantasy F1 {year}.xlsx'
filepath = os.path.join(
    root,
    spreadsheet_name)
lineup_dir = os.path.join(
    root,
    'Lineup')
format_dir = os.path.join(
    root,
    '..',
    'Formats')
plot_dir = os.path.join(
    root,
    'Figures')
org.check_dir_exists(dir_path=plot_dir)

''' Config Files '''
info = org.get_config(
    config_path=os.path.join(
        root,
        '..',
        'Info.config'
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
        'Driver_Points.config'
    )).items()
driver_values = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Driver_Values.config'
    )).items()
team_points = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Team_Points.config'
    )).items()
team_values = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Team_Values.config'
    )).items()

''' Correct Driver and Team Points '''
maths.correct_points(
    points_dict=driver_points,
    out_path=os.path.join(
        lineup_dir,
        'Individual_Driver_Points.config'))
maths.correct_points(
    points_dict=team_points,
    out_path=os.path.join(
        lineup_dir,
        'Individual_Team_Points.config'))
driver_points = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Individual_Driver_Points.config'
    )).items()
team_points = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Individual_Team_Points.config'
    )).items()

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

''' Create Sheets '''
driver_sheet = workbook.add_worksheet('Drivers')
team_sheet = workbook.add_worksheet('Teams')

''' Count Races, Drivers, and Teams '''
season_length, races = si.season_length(dictionary=info)
teams, drivers, index = si.teams_drivers(dictionary=lineup)
stats = si.statistics(dictionary=info)
rsf = si.races_so_far(dictionary=driver_points)

''' Print Season Parameters '''
print(f'The season is {season_length} races long, the races are {races}.\n'
      f'There are {len(teams)} teams, who are {teams}.\n'
      f'There are {len(drivers)} drivers, who are {drivers}.\n'
      f'To date there have been {rsf} races, these races are {races[0: rsf]}.')

''' Add Races Row Headers '''
driver_sheet.write_column(
    row=1,
    col=0,
    data=races,
    cell_format=header_format)  # Points
driver_sheet.write_column(
    row=1,
    col=2 + len(drivers),
    data=races,
    cell_format=header_format)  # Values
team_sheet.write_column(
    row=1,
    col=0,
    data=races,
    cell_format=header_format)  # Points
team_sheet.write_column(
    row=1,
    col=2 + len(teams),
    data=races,
    cell_format=header_format)  # Values

''' Update Data From Config '''
driver_sheet.write(
    0,
    0,
    'Points',
    red_format)
column = 1
for driver, points in driver_points:
    driver_sheet.write_column(
        row=1,
        col=column,
        data=points,
        cell_format=data_format)
    column += 1
column += 1
driver_sheet.write(
    0,
    column,
    'Values',
    red_format)
column += 1
for driver, values in driver_values:
    driver_sheet.write_column(
        row=1,
        col=column,
        data=values,
        cell_format=data_format)
    column += 1
team_sheet.write(
    0,
    0,
    'Points',
    red_format)
column = 1
for team, points in team_points:
    team_sheet.write_column(
        row=1,
        col=column,
        data=points,
        cell_format=data_format)
    column += 1
column += 1
team_sheet.write(
    0,
    column,
    'Values',
    red_format)
column += 1
for team, values in team_values:
    team_sheet.write_column(
        row=1,
        col=column,
        data=values,
        cell_format=data_format)
    column += 1

''' Write Names With Colours '''
for i in range(0, len(drivers)):
    cell_format = workbook.add_format(
        org.get_config(
            config_path=os.path.join(
                format_dir,
                f'{index[i]}.config'
                )
        ).items())
    driver_sheet.write(
        0,
        1 + i,
        f'{drivers[i]}',
        cell_format)
    driver_sheet.write(
        0,
        3 + len(drivers) + i,
        f'{drivers[i]}',
        cell_format)
for i in range(0, len(teams)):
    cell_format = workbook.add_format(
        org.get_config(
            config_path=os.path.join(
                format_dir,
                f'{teams[i]}.config'
            )
        ).items())
    team_sheet.write(
        0,
        1 + i,
        f'{teams[i]}',
        cell_format)
    team_sheet.write(
        0,
        3 + len(teams) + i,
        f'{teams[i]}',
        cell_format)

''' Close Workbook '''
workbook.close()

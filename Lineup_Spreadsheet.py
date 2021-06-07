import os
import xlsxwriter as xlsx
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

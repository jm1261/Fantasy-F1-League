import src.dataIO as io

from pathlib import Path

root = Path().absolute()
year = 2019

info_path = Path(f'{root}/Info.json')
info_dict = (io.load_json(file_path=info_path))[f'{year}']
data_path = Path(f'{root}/Data/{year}')
results_path = Path(f'{root}/Data/{year}/Lineup')
format_path = Path(f'{root}/Config')

lineup_results = io.load_json(file_path=Path(f'{results_path}/Results.json'))

races = info_dict["Races"]

lineup_weekly = io.load_json(file_path=Path(f'{data_path}/Lineup_Weekly.json'))

driver_points = lineup_results["Driver Points"]
driver_values = lineup_results["Driver Values"]
team_points = lineup_results["Team Points"]
team_values = lineup_results["Team Values"]

drivers = [key for key, values in driver_points.items()]
teams = [key for key, values in team_points.items()]

for index, race in enumerate(races):
    race_results = lineup_weekly
    race_results.update({"Race": [f'{race}']})
    for driver in drivers:
        race_results.update({f'{driver}': [
            (driver_points[f'{driver}'])[index],
            (driver_values[f'{driver}'])[index]]})
    for team in teams:
        race_results.update({f'{driver}': [
            (team_points[f'{team}'])[index],
            (team_values[f'{team}'])[index]]})
    io.save_json_dicts(
        out_path=Path(f'{results_path}/{race}_Results.json'),
        dictionary=race_results)
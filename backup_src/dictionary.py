import os
import src.dataIO as io
import src.filepaths as fp

from pathlib import Path


root = Path().absolute()
year = '2023'

data_path = Path(f'{root}/Data/{year}')
info_path = Path(f'{root}/Info.json')
info_dict = io.load_json(file_path=info_path)

manager_dict = info_dict['Managers']

results_path = Path(f'{root}/Data/{year}/Lineup')
format_path = Path(f'{root}/Data/{year}/Lineup_Formats')
races_sofar, races = io.get_races_sofar(
    file_path=info_path,
    results_path=results_path)

for manager, teams in manager_dict.items():
    for team in teams:
        team_dict = {}
        for race in races:
            teamsheet = io.load_json(file_path=Path(f'{data_path}/{manager}/{race}_{team}.json'))
            new_teamsheet = {}
            for position, name in teamsheet.items():
                if position == 'Position' or position == 'Race':
                    pass
                elif position == 'Team Name':
                    pass
                else:
                    new_teamsheet.update({f'{position}': name[0]})
            team_dict.update({f'{race}': new_teamsheet})
            os.remove(Path(f'{data_path}/{manager}/{race}_{team}.json'))
        io.save_json_dicts(
            out_path=Path(f'{data_path}/{manager}/{team}.json'),
            dictionary=team_dict)
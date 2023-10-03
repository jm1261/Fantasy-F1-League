import src.dataIO as io
import src.filepaths as fp
import src.formats as form

from pathlib import Path


def season_launches(root,
                    year):
    '''
    Launch a new season.
    Args:
        root: <string> path to root file
        year: <string> year as a string
    Returns:
        None
    '''
    year_path = Path(f'{root}/Data/{year}')
    fp.check_dir_exists(dir_path=year_path)
    lineup_path = Path(f'{year_path}/Lineup_Formats')
    info_path = Path(f'{root}/Info.json')
    info = io.load_json(file_path=info_path)
    fp.season_dirs(
        dir_path=year_path,
        managers=info['Managers'])
    form.generate_manager_colors(
        info_dict=info,
        format_dir=Path(f'{year_path}/Manager_Formats'))
    lineup_dict = io.create_lineup(lineup_path=lineup_path)
    statistics_dict = io.create_statistics(lineup_path=lineup_path)
    lineup_weekly_dict = io.create_lineup_weekly(lineup_path=lineup_path)
    lineup_outfile = Path(f'{year_path}/Lineup/Results.json')
    if lineup_outfile.is_file():
        pass
    else:
        io.save_json_dicts(
            out_path=lineup_outfile,
            dictionary=lineup_dict)
    statistics_outfile = Path(f'{year_path}/Lineup/Statistics.json')
    if statistics_outfile.is_file():
        pass
    else:
        io.save_json_dicts(
            out_path=statistics_outfile,
            dictionary=statistics_dict)
    io.save_json_dicts(
        out_path=Path(f'{year_path}/Lineup_Weekly.json'),
        dictionary=lineup_weekly_dict)


if __name__ == '__main__':
    year = 2023
    root = Path().absolute()
    season_launches(
        root=root,
        year=2023)
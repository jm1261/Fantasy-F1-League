import src.dataIO as io
import src.filepaths as fp
import src.formats as form

from pathlib import Path


def launches_new_season(root : str,
                        year : str) -> None:
    """
    Function Details
    ================
    Function to begin a new season.

    Begin a new season with only the root directory and the given year. Creates
    all the required directory paths and files to begin a new fantasy league
    season.

    Parameters
    ----------
    root, year: string
        Path to root directory, year for data storage.

    Returns
    -------
    None

    See Also
    --------
    load_json
    season_dirs
    check_manager_exist
    get_used_colors
    generate_manager_colors
    adds_managers_teams
    create_lineup
    create_statistics
    create_lineup_weekly
    save_json_dicts

    Notes
    -----
    Creates the data path to the year for which a new season is created. Then
    creates the required directory paths. Checks to see if there are any new
    managers this season. If there are, it will create some. Add manager teams
    to the format dictionaries if they don't exist. Finish by setting up the
    weekly lineup, results, and statistics dictionaries if they don't exist.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ============

    07/02/2024
    ----------
    Updated to split the function into further segments for a clearer
    understanding to the reader going forward. The format dictionaries have
    been updated for the teams and drivers to allow multiple years of data to be
    stored in one individual file in the .config directory. As such, some of the
    driver and team results/statistics functions have been updated, as well as
    the lineup_format_path. Update to function names for PEP8. This update was
    created by J.Male.

    14/02/2024
    ----------
    Added a year key to the info_dict, changed in this function to pull the
    yearly info dictionary in automatically. This update was created by J.Male.

    15/02/2024
    ----------
    Checked to ensure the lineup results and statistics dictionaries were all
    working properly. They are. This function works as intended as of this date.

    """

    """ Create Year Path """
    year_path = Path(f'{root}/Data/{year}')
    fp.check_dir_exists(dir_path=year_path)

    """ Config Files and Season Info """
    lineup_format_path = Path(f'{root}/Config/Lineup_Formats')
    manager_format_path = Path(f'{root}/Config/Manager_Formats')
    info_path = Path(f'{root}/Info.json')
    info_dict = (io.load_json(file_path=info_path))[f'{year}']

    """ Create Manager Folders """
    managers = info_dict['Managers'].keys()
    fp.season_dirs(
        dir_path=year_path,
        managers=managers)
    new_managers = fp.check_manager_exist(
        dir_path=manager_format_path,
        managers=managers)
    used_colors = io.get_used_colors(dir_path=manager_format_path)
    form.generate_manager_colors(
        new_managers=new_managers,
        used_colors=used_colors,
        dir_path=manager_format_path)
    io.adds_managers_teams(
        dir_path=manager_format_path,
        manager_dict=info_dict['Managers'])
    
    """ Create Lineup Files for Results, Statistics, and Weekly Submission """
    lineup_dict = io.creates_driver_team_results(
        lineup_path=lineup_format_path,
        year=year)
    print(lineup_dict)
    lineup_outfile = Path(f'{year_path}/Lineup/Results.json')
    if lineup_outfile.is_file():
        pass
    else:
        io.save_json_dicts(
            out_path=lineup_outfile,
            dictionary=lineup_dict)
    statistics_dict = io.create_drivers_teams_statistics(
        lineup_path=lineup_format_path,
        year=year)
    statistics_outfile = Path(f'{year_path}/Lineup/Statistics.json')
    if statistics_outfile.is_file():
        pass
    else:
        io.save_json_dicts(
            out_path=statistics_outfile,
            dictionary=statistics_dict)
    lineup_weekly_dict = io.create_drivers_teams_weekly(
        lineup_path=lineup_format_path,
        year=year)
    io.save_json_dicts(
        out_path=Path(f'{year_path}/Lineup_Weekly.json'),
        dictionary=lineup_weekly_dict)
    
    """ Create manager team sheet dictionaries """
    io.managers_weekly(
        info_dictionary=info_dict,
        data_path=year_path,
        race_index=0)


if __name__ == '__main__':
    year = 2024
    root = Path().absolute()
    launches_new_season(
        root=root,
        year=f'{year}')

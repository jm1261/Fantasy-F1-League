import os
import xlsxwriter as xlsx
import Functions.Organisation as org


def driver_team_spreadsheet(file_path,
                            format_dir,
                            races,
                            drivers,
                            teams,
                            index,
                            driver_points,
                            driver_values,
                            team_points,
                            team_values,
                            driver_points_stats,
                            driver_values_stats,
                            team_points_stats,
                            team_values_stats):
    '''
    Create driver/team points/values spreadsheet. Strict layout design, could
    be changed in function.
    Args:
        file_path: <string> path to spreadsheet file
        format_dir: <string> path to config files
        races: <array> races array
        drivers: <array> list of driver names
        teams: <array> list of team names
        index: <array> team/driver colours index
        driver_points: <dict> driver points dictionary
        driver_values: <dict> driver values dictionary
        team_points: <dict> team points dictionary
        team_values: <dict> team values dictionary
        driver_points_stats: <array> driver points statistics array
        driver_values_stats: <arrau> driver values statistics array
        team_points_stats: <array> team points statistics array
        team_values_stats: <array> team values statistics array
    Returns:
        None
    '''
    ''' Create Spreadsheet '''
    workbook = xlsx.Workbook(file_path)
    ''' Cell Formats '''
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
    ''' Create Sheets '''
    driver_sheet = workbook.add_worksheet('Drivers')
    team_sheet = workbook.add_worksheet('Teams')
    ''' Add Races Row Headers '''
    driver_sheet.write_column(
        row=1,
        col=0,
        data=races,
        cell_format=header_format)  # points
    driver_sheet.write_column(
        row=1,
        col=2 + len(drivers),
        data=races,
        cell_format=header_format)  # values
    team_sheet.write_column(
        row=1,
        col=0,
        data=races,
        cell_format=header_format)  # points
    team_sheet.write_column(
        row=1,
        col=2 + len(teams),
        data=races,
        cell_format=header_format)  # values
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
    for i in range(len(drivers)):
        cell_format = workbook.add_format(
            org.get_config(
                config_path=os.path.join(
                    format_dir,
                    f'{index[i]}.config')).items())
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
    for i in range(len(teams)):
        cell_format = workbook.add_format(
            org.get_config(
                config_path=os.path.join(
                    format_dir,
                    f'{teams[i]}.config')).items())
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
    ''' Write Statistics To Sheet '''
    for i in range(len(driver_points_stats)):
        driver_sheet.write_row(
            2 + i + len(races),
            1,
            driver_points_stats[i],
            data_format)
        driver_sheet.write_row(
            2 + i + len(races),
            3 + len(drivers),
            driver_values_stats[i],
            data_format)
        team_sheet.write_row(
            2 + i + len(races),
            1,
            team_points_stats[i],
            data_format)
        team_sheet.write_row(
            2 + i + len(races),
            3 + len(teams),
            team_values_stats[i],
            data_format)
    ''' Close Workbook '''
    workbook.close()

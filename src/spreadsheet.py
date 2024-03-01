import xlsxwriter as xlsx

from src.formats import drivers_formats, team_format


def line_up_spreadsheet(file_path : str,
                        format_dir : str,
                        races : list,
                        results : dict,
                        statistics : dict) -> None:
    """
    Function Details
    ================
    Create the team and driver spreadsheet for points, values, and statistics.

    Creates a two-sheet excel spreadsheet containing the driver and team points,
    values, and statistics for each race weekend.

    Parameters
    ----------
    file_path, format_dir : string
        Path to save spreadsheet and path to formats directory.
    races : list
        List of strings containing all races in calendar year.
    results, statistics : dictionary
        Driver and team results and statistics dictionaries.
    
    Returns
    -------
    None

    See Also
    --------
    driver_formats
    team_format

    Notes
    -----
    Create a spreadsheet containing the driver points and values, and team
    points and values, as well as the statistics.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    01/03/2024
    ----------
    Documentation update.

    """
    workbook = xlsx.Workbook(file_path)
    header_format = workbook.add_format(
        {
            "bold": "True",
            "size": 12,
            "align": "centre",
            "font": "Calibri"})
    data_format = workbook.add_format(
        {
            "size": 10,
            "align": "centre",
            "font": "Calibri"})
    red_format = workbook.add_format(
        {
            "bold": "True",
            "size": 12,
            "align": "centre",
            "color": "red",
            "font": "Calibri"})
    categories = ['Driver', 'Team']
    for category in categories:
        category_sheet = workbook.add_worksheet(f'{category}s')
        tables = ['Points', 'Values',]
        column_index = 0
        row_index = 0
        for table in tables:
            category_sheet.write(
                row_index,
                column_index,
                f'{table}',
                red_format)
            category_sheet.write_row(
                row=row_index,
                col=column_index + 1,
                data=races,
                cell_format=header_format)
            row_index += 1
            for key, values in results[f'{category} {table}'].items():
                if category == 'Driver':
                    format_choice = drivers_formats(
                        format_dir=format_dir,
                        driver=key).items()
                elif category == 'Team':
                    format_choice = team_format(
                        format_dir=format_dir,
                        team=key).items()
                cell_format = workbook.add_format(format_choice)
                category_sheet.write(
                    row_index,
                    column_index,
                    f'{key}',
                    cell_format)
                category_sheet.write_row(
                    row=row_index,
                    col=column_index + 1,
                    data=values,
                    cell_format=data_format)
                row_index += 1
            row_index += 1
        tables = [
            'Sum Points', 'Sum Values',
            'Average Points', 'Average Values',
            'Points Per Value', 'Average Points Per Value']
        for table in tables:
            category_sheet.write(
                row_index,
                column_index,
                f'{table}',
                red_format)
            category_sheet.write_row(
                row=row_index,
                col=column_index + 1,
                data=races,
                cell_format=header_format)
            row_index += 1
            for key, values in statistics[f'{category} {table}'].items():
                if category == 'Driver':
                    format_choice = drivers_formats(
                        format_dir=format_dir,
                        driver=key).items()
                elif category == 'Team':
                    format_choice = team_format(
                        format_dir=format_dir,
                        team=key).items()
                cell_format = workbook.add_format(format_choice)
                category_sheet.write(
                    row_index,
                    column_index,
                    f'{key}',
                    cell_format)
                category_sheet.write_row(
                    row=row_index,
                    col=column_index + 1,
                    data=values,
                    cell_format=data_format)
                row_index += 1
            row_index += 1
    workbook.close()

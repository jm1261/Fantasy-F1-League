import os
import xlsxwriter as xlsx
import Functions.Organisation as org

''' Organisation '''
root = os.path.join(
    os.getcwd(),
    '2021')
spreadsheet_name = 'Fantasy F1 2021.xlsx'
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

''' Create Spreadsheet '''
workbook = xlsx.Workbook(filepath)

''' Config Files '''
info = org.get_config(
    config_path=os.path.join(
        root,
        '..',
        'Info.config')
    ).items()

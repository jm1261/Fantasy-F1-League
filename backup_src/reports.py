import requests
import pandas as pd

from bs4 import BeautifulSoup


def create_lineup_report(test):
    return 0


def get_table(address):
    '''
    Pull table data from F1 results website.
    Args:
        address: <string> web page address
    Returns:
        table: <array> list of table entries
    '''
    page = requests.get(address)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.select('table')[0].text.split('\n\n\n\n')
    return table


def create_grid_dict(table_data):
    '''
    Create starting grid dictionary.
    Args:
        table_data: <array> list of table entries
    Returns:
        grid_dict: <dictionary> starting grid dictionary
    '''
    grid_dict = {}
    keys = ['Pos', 'Num', 'Name', 'Surname', 'Abbrev', 'Car', 'Time']
    for index, line in enumerate(table_data[1:]):
        line_elements = line.split('\n')
        if index == 0:
            pass
        else:
            none_blank_elements = [
                element
                for element in line_elements
                if element != '']
            for i, element in enumerate(none_blank_elements):
                if keys[i] in grid_dict.keys():
                    grid_dict[keys[i]].append(element)
                else:
                    grid_dict.update({keys[i]: [element]})
    return grid_dict


def create_race_dict(table_data):
    '''
    Create starting grid dictionary.
    Args:
        table_data: <array> list of table entries
    Returns:
        race_dict: <dictionary> finishing race dictionary
    '''
    race_dict = {}
    keys = ['Pos', 'Num', 'Name', 'Surname',
            'Abbrev', 'Car', 'Laps', 'Time', 'Points']
    for index, line in enumerate(table_data[1:]):
        line_elements = line.split('\n')
        if index == 0:
            pass
        else:
            none_blank_elements = [
                element
                for element in line_elements
                if element != '']
            print(none_blank_elements)
            for i, element in enumerate(none_blank_elements):
                if keys[i] in race_dict.keys():
                    race_dict[keys[i]].append(element)
                else:
                    race_dict.update({keys[i]: [element]})


if __name__ == '__main__':
    year = 2023
    race_index = 1141
    race = 'Bahrain'
    grid_address = f'https://www.formula1.com/en/results.html/{year}/races/{race_index}/{race}/starting-grid.html'
    race_address = f'https://www.formula1.com/en/results.html/{year}/races/{race_index}/{race}/race-result.html'
    grid_table = get_table(address=grid_address)
    race_table = get_table(address=race_address)

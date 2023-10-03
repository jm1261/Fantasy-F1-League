import requests

from bs4 import BeautifulSoup


def get_table_data(year):
    '''
    Get all table data from web page.
    Args:
        year: <string> year as string, e.g., "2020"
    Returns:
        table_data: <array> driver standings table
    '''
    address = f'https://www.formula1.com/en/results.html/{year}/drivers.html'
    page = requests.get(address)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_data = soup.select('.table-wrap')[0].text.split('\n\n\n\n\n')
    return table_data


def get_drivers_teams(table_data):
    '''
    Get driver list and team list from table data.
    Args:
        table_data: <array> driver standings table
    Returns:
        drivers: <array> list of drivers
        teams: <array> list of teams
    '''
    drivers = []
    teams = []
    for line in table_data[1:]:
        elements = line.split('\n')
        temp = []
        for e in elements:
            if e != '':
                temp.append(e)
        if len(temp) > 4:
            drivers.append(f'{temp[1]} {temp[2]}')
            teams.append(f'{temp[5]}')
    return drivers, teams


def make_teams_dict(drivers,
                    teams):
    '''
    Make team dictionary from drivers and teams arrays.
    Args:
        drivers: <array> driver list
        teams: <array> team list (same length)
    Returns:
        teams_dictionary: <dictionary>
            team_name: [driver_1, driver_2]
    '''
    teams_dictionary = {}
    for index, team in enumerate(teams):
        if team in teams_dictionary:
            teams_dictionary[f'{team}'].append(drivers[index])
        else:
            teams_dictionary.update({f'{team}': [f'{drivers[index]}']})
    return teams_dictionary


def get_team_dictionary(year):
    '''
    Create teams and drivers dictionary.
    Args:
        year: <string> year as string, e.g., "2020"
    Returns:
        teams_dictionary: <dictionary>
            team_name: [driver_1, driver_2]
    '''
    table_data = get_table_data(year=year)
    drivers, teams = get_drivers_teams(table_data=table_data)
    teams_dictionary = make_teams_dict(
        drivers=drivers,
        teams=teams)
    return teams_dictionary



if __name__ == '__main__':
    year = 2022
    teams_dictionary = get_team_dictionary(year=f'{year}')
    #print(teams_dictionary)
    address = "https://www.f1fantasytracker.com/standings.html"
    page = requests.get(address)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.select('results.data')
    print(table)
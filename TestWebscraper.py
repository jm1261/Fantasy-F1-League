import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import time


def GetTableData(address):
    '''
    '''
    page = requests.get(address)
    soup = BeautifulSoup(page.content, 'html.parser')
    tabledata = soup.select('.table-wrap')[0].text.split('\n\n\n\n\n')
    return tabledata


def GetDrivers(data):
    '''
    '''
    drivers = []
    teams = []
    for line in data[1: ]:
        elements = line.split('\n')
        temp = []
        for e in elements:
            if e != '':
                temp.append(e)
        if len(temp) > 4:
            drivers.append(f'{temp[1]} {temp[2]}')
            teams.append(f'{temp[5]}')
    return drivers, teams


def GetTeams(data):
    '''
    '''
    teams = []
    for line in data[1: ]:
        elements = line.split('\n')
        temp = []
        for e in elements:
            if e != '':
                temp.append(e)
        if len(temp) > 2:
            teams.append(f'{temp[1]}')
    return teams


def TeamsDictionary(drivers,
                    teams):
    '''
    '''
    teamdict = {}
    for index, team in enumerate(teams):
        if team in teamdict:
            teamdict[f'{team}'].append(drivers[index])
        else:
            teamdict.update({f'{team}': [f'{drivers[index]}']})
    return teamdict



if __name__ == '__main__':
    year = 2022
    address = f'https://www.formula1.com/en/results.html/{year}/drivers.html'
    drivers, allteams = GetDrivers(
        data=GetTableData(
            address=(
                f'https://www.formula1.com/en/results.html'
                f'/{year}/drivers.html')))
    teams = GetTeams(
        data=GetTableData(
            address=(
                f'https://www.formula1.com/en/results.html'
                f'/{year}/team.html')))
    teamdict = TeamsDictionary(
        drivers=drivers,
        teams=allteams)
    print(f'\n{drivers}')
    print(f'\n{allteams}')
    print(f'\n{teams}')
    print(f'\n{teamdict}')

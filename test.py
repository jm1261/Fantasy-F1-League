import requests
import json
import os
from bs4 import BeautifulSoup


def convertpagetodict(url):
    '''
    '''
    page = requests.get(url)
    data = page.json()
    return data

def saveoutdict(out_path,
                dictionary):
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2)

login = {
    'Login': 'josh.simon.male@gmail.com',
    'Password': 'FKaz11994'}

''' Teams and Drivers Info No Login '''
teamsurl = 'https://fantasy-api.formula1.com/f1/2022/teams'
driversurl = 'https://fantasy-api.formula1.com/f1/2022/players'

''' Login Stuff '''
fixturesurl = 'https://fantasy-api.formula1.com/f1/2022'

with requests.Session() as session:
    logindetails = session.post(
        ('https://account.formula1.com/#/en/login?lead_source=web_fantasy&redirect=https%3A%2F%2Ffantasy.formula1.com%2Fapp%2F%23%2F'),
        data=login)
    r = session.get(fixturesurl)
    print(r.text)

    data = convertpagetodict(url=fixturesurl)
    saveoutdict(
        out_path=os.path.join(
            os.getcwd(),
            'Test.json'),
        dictionary=data)

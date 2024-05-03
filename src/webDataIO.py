import requests

from bs4 import BeautifulSoup
from src.dataIO import output_string


def get_response(url : str | bytes):
    """
    Function Details
    ================

    Ping url for response.

    Parameters
    ----------
    url: string
        Website address or bytes.

    Returns
    -------
    Response

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    11/03/2024
    ----------
    Created.

    """
    response = requests.get(url)
    return response


def get_the_soup(url : str | bytes) -> BeautifulSoup | list:
    """
    Function Details
    ================
    Get the soup from a given url.

    Parameters
    ----------
    url: string/bytes
        Link to website

    Returns
    -------
    soup: BeautifulSoup/list
        Website content. Blank if no response.

    See Also
    --------
    get_response

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    12/03/2024
    ----------
    Created.

    """
    response = get_response(url=url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_season_urls(url : str | bytes) -> tuple[list, list]:
    """
    Function Details
    ================
    Get the season races and their results page links.

    Parameters
    ----------
    url: string/byte
        Website address.

    Returns
    -------
    races, urls: tuple[list, list]
        List of races for which data exists, urls for their results pages.

    See Also
    --------
    get_response
    get_the_soup

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    12/03/2024
    ----------
    Created.

    """
    soup = get_the_soup(url=url)
    urls = []
    races = []
    td_tags = soup.find_all('td', class_='dark bold')
    for tag in td_tags:
        anchor_tag = tag.find('a')
        if anchor_tag:
            urls.append(anchor_tag.get('href'))
            races.append(anchor_tag.text.strip())
        else:
            pass
    return races, urls


def results_archive_table(soup : BeautifulSoup) -> list:
    """
    Function Details
    ================
    Pull results table from website into list.

    Parameters
    ----------
    soup: BeautifulSoup
        bs4 soup.

    Returns
    -------
    table_data: list
        html table data as a lit.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    12/03/2024
    ----------
    Created.

    """
    table_data = []
    table = soup.find('table', class_='resultsarchive-table')
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all(['th', 'td'])
        table_data.append(
            [column.text.replace('\n', ' ').strip() for column in columns])
    return table_data


def get_qualifying_result(url : str | bytes):
    """
    Function Details
    ================
    Turn qualifying results table into a markdown table string.

    Parameters
    ----------
    url: string/bytes
        Website address.

    Returns
    -------
    markdown_table: string
        Qualifying results table as a markdown string.

    See Also
    --------
    get_the_soup
    results_archive_table

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    13/03/2024
    ----------
    Created.

    """
    soup = get_the_soup(url=url)
    table_data = results_archive_table(soup=soup)
    markdown_table = ""
    for index, data_row in enumerate(table_data):
        markdown_table += f'| {" | ".join(data_row[1: -1])} |\n'
        if index == 0:
            markdown_table += (
                '| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |\n')
    return markdown_table


def get_fastest_laps(url : str | bytes):
    """
    Function Details
    ================
    Turn fastest laps results table into a markdown table string.

    Parameters
    ----------
    url: string/bytes
        Website address.

    Returns
    -------
    markdown_table: string
        Fastest laps results table as a markdown string.

    See Also
    --------
    get_the_soup
    results_archive_table

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    13/03/2024
    ----------
    Created.

    """
    soup = get_the_soup(url=url)
    table_data = results_archive_table(soup=soup)
    markdown_table = ""
    for index, data_row in enumerate(table_data):
        markdown_table += f'| {" | ".join(data_row[1: -1])} |\n'
        if index == 0:
            markdown_table += (
                '| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |\n')
    return markdown_table


def get_race_results(url : str | bytes):
    """
    Function Details
    ================
    Turn race results table into a markdown table string.

    Parameters
    ----------
    url: string/bytes
        Website address.

    Returns
    -------
    markdown_table: string
        Race results table as a markdown string.

    See Also
    --------
    get_the_soup
    results_archive_table

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    13/03/2024
    ----------
    Created.

    """
    soup = get_the_soup(url=url)
    table_data = results_archive_table(soup=soup)
    markdown_table = ""
    for index, data_row in enumerate(table_data):
        markdown_table += f'| {" | ".join(data_row[1: -1])} |\n'
        if index == 0:
            markdown_table += (
                '| :-: | :-: | :-: | :-: | :-: | :-: | :-: |\n')
    return markdown_table


def outputs_qualifying_data(year : str,
                            race : str) -> None:
    """
    Function Details
    ================
    Pulls race qualifying results and outputs as a markdown table.

    Parameters
    ----------
    year, race: string
        Year and race to process.

    Returns
    -------
    None

    See Also
    --------
    get_season_urls
    get_qualifying_result

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    13/03/2024
    ----------
    Created.

    """
    base_url = 'https://www.formula1.com'
    url = f'{base_url}/en/results.html/{year}/races.html'
    races, urls = get_season_urls(url=url)
    if race in races:
        base_url += urls[races.index(race)]
        url_split = base_url.split('/')
        url_split[-1] = 'qualifying.html'
        qualifying_url = '/'.join(url_split)
        table = get_qualifying_result(url=qualifying_url)
        output_string(string=table)


def outputs_sq_data(year : str,
                    race : str) -> None:
    """
    Function Details
    ================
    Pulls sprint qualifying results and outputs as a markdown table.

    Parameters
    ----------
    year, race: string
        Year and race to process.

    Returns
    -------
    None

    See Also
    --------
    get_season_urls
    get_qualifying_result

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    23/04/2024
    ----------
    Created.

    """
    base_url = 'https://www.formula1.com'
    url = f'{base_url}/en/results.html/{year}/races.html'
    races, urls = get_season_urls(url=url)
    if race in races:
        base_url += urls[races.index(race)]
        url_split = base_url.split('/')
        url_split[-1] = 'sprint-qualifying.html'
        qualifying_url = '/'.join(url_split)
        table = get_qualifying_result(url=qualifying_url)
        output_string(string=table)


def outputs_fastest_lap(year : str,
                        race : str) -> None:
    """
    Function Details
    ================
    Pulls race fastest lap results and outputs as a markdown table.

    Parameters
    ----------
    year, race: string
        Year and race to process.

    Returns
    -------
    None

    See Also
    --------
    get_season_urls
    get_fastest_laps

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    13/03/2024
    ----------
    Created.

    """
    base_url = 'https://www.formula1.com'
    url = f'{base_url}/en/results.html/{year}/races.html'
    races, urls = get_season_urls(url=url)
    if race in races:
        base_url += urls[races.index(race)]
        url_split = base_url.split('/')
        url_split[-1] = 'fastest-laps.html'
        fastest_laps_url = '/'.join(url_split)
        table = get_fastest_laps(url=fastest_laps_url)
        output_string(string=table)


def outputs_race_result(year : str,
                        race : str) -> None:
    """
    Function Details
    ================
    Pulls race results and outputs as a markdown table.

    Parameters
    ----------
    year, race: string
        Year and race to process.

    Returns
    -------
    None

    See Also
    --------
    get_season_urls
    get_race_results

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    13/03/2024
    ----------
    Created.

    """
    base_url = 'https://www.formula1.com'
    url = f'{base_url}/en/results.html/{year}/races.html'
    races, urls = get_season_urls(url=url)
    if race in races:
        base_url += urls[races.index(race)]
        table = get_race_results(url=base_url)
        output_string(string=table)


def outputs_sprint_data(year : str,
                        race : str) -> None:
    """
    Function Details
    ================
    Pulls sprint race results and outputs as a markdown table.

    Parameters
    ----------
    year, race: string
        Year and race to process.

    Returns
    -------
    None

    See Also
    --------
    get_season_urls
    get_race_results

    Notes
    -----
    None

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    23/04/2024
    ----------
    Created.

    """
    base_url = 'https://www.formula1.com'
    url = f'{base_url}/en/results.html/{year}/races.html'
    races, urls = get_season_urls(url=url)
    if race in races:
        print(race)
        base_url += urls[races.index(race)]
        url_split = base_url.split('/')
        url_split[-1] = 'sprint-results.html'
        sprint_url = '/'.join(url_split)
        table = get_race_results(url=sprint_url)
        output_string(string=table)

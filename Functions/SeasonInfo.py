def season_length(dictionary):
    '''
    season_length reads in a user created dictionary containing all the races
    in a season and returns the length of the season for indexing purposes.
    Args:
        dictionary: <dict> unpacked dict containing at least one key that is
                    the season races
    Returns:
        season_length: <int> number of races
        races: <array> array of race names
    '''
    season_length = 0
    races = []
    for key, values in dictionary:
        if key == 'Races':
            season_length = len(values)
            for value in values:
                races.append(value)
        else:
            pass
    return season_length, races


def teams_drivers(dictionary):
    '''
    teams_drivers reads in the lineup for the season and returns the number of
    teams, drivers, and an indexing array for colour formatting reasons.
    Args:
        dictionary: <dict> unpacked lineup dictionary
    Returns:
        teams: <array> the team names in order
        drivers: <array> the driver names in order
        index: <array> an array for indexing colours
    '''
    teams = []
    drivers = []
    index = []
    for key, values in dictionary:
        teams.append(key)
        index.append(key)
        index.append(key)
        for value in values:
            drivers.append(value)
    return teams, drivers, index


def statistics(dictionary):
    '''
    statistics works in the same way as season length in that it looks at the
    same dictionary for the statistics we care about and pulls the names out.
    Args:
        dictionary: <dict> unpacked dictionary
    Returns:
        statistics: <array> array of statistics values
    '''
    statistics = []
    for key, values in dictionary:
        if key == 'Statistics':
            for value in values:
                statistics.append(value)
        else:
            pass
    return statistics


def team_setup(dictionary):
    '''
    team_setup looks at the fantasy team positions and places them into an
    array. It looks for these parameters in the info config file.
    Args:
        dictionary: <dict> unpacked dictionary
    Returns:
        team_setup: <array> array of fantasy league positions
    '''
    team_setup = []
    for key, values in dictionary:
        if key == 'Team':
            for value in values:
                team_setup.append(value)
        else:
            pass
    return team_setup


def races_so_far(dictionary):
    '''
    races_so_far counts the number of filled array values in a points
    dictionary and returns the number of races that have currently been
    completed.
    Args:
        dictionary: <dict> unpacked dictionary
    Returns:
        races so far: <int> number of races completed
    '''
    races_so_far = [len(points) for key, points in dictionary][0]
    return races_so_far

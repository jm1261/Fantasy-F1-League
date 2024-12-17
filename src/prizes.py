def viking_comeback(team_points : dict,
                    top_index : int) -> dict:
    """
    Function Details
    ================
    Top scorers in the first race as a function of finishing position at the
    end of the season.

    Parameters
    ----------
    team_points: dictionary
        Team summed points.
    top_index: int
        How many teams to include in the output.

    Returns
    -------
    comeback_scores: dictionary
        Top teams from the first race and their final scores.

    See Also
    --------
    None

    Notes
    -----
    Finds the top {index} number of teams from the first race and returns their
    final scores.

    Example
    -------
    None

    ----------------------------------------------------------------------------
    Update History
    ==============

    27/03/2024
    ----------
    Created.

    """
    scores = []
    names = []
    for manager, teams in team_points.items():
        for team, points in teams.items():
            scores.append(points[0])
            names.append(team)
    zipped_lists = zip(scores, names)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs[-top_index: ])
    scores, names = [list(tuple) for tuple in tuples]
    comeback_scores = {}
    for score, name in zip(scores[::-1], names[::-1]):
        comeback_scores.update({f'{name}': [score]})
    for manager, teams in team_points.items():
        for team, points in teams.items():
            if team in comeback_scores.keys():
                comeback_scores[team].append(points[-1])
    return comeback_scores

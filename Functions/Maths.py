import Functions.Organisation as org


def correct_points(points_dict,
                   out_path):
    '''
    correct_points takes the input points dictionaries, which are total points
    at after each race, and calculates the individual points scored for each
    race. In other words, it subtracts the race total from the previous total
    to calculate the difference.
    Args:
        points_dict: <dict> dictionary containing teams or drivers and their
                     total points
        out_path: <string> path to save
    Returns:
        None
    '''
    individual_points = {}
    for key, points in points_dict:
        indiv_points = [points[i] if i == 0 else points[i] - points[i - 1]
                        for i in range(0, len(points))]
        individual_points.update({key: indiv_points})
    org.dump_json(
        out_path=out_path,
        dictionary=individual_points)

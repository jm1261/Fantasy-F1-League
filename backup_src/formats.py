import os
import random

from pathlib import Path
from src.dataIO import load_json, save_json_dicts


def drivers_formats(format_dir,
                    driver):
    '''
    Find driver cell formats, from team colors.
    Args:
        format_dir: <string> path to team format files
        driver: <string> driver name
    Returns:
        cell_format: <dict> cell format dictionary
    '''
    team_formats = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if 'Perks.json' not in file]
    format_dict = {}
    for team_path in team_formats:
        team_format = load_json(file_path=team_path)
        if driver in team_format['drivers']:
            for key, value in team_format.items():
                if key == 'drivers':
                    pass
                else:
                    format_dict.update({key: value})
    return format_dict


def drivers_colours(format_dir,
                    driver):
    '''
    Find driver graph formats, from team colors.
    Args:
        format_dir: <string> path to team format files
        driver: <string> driver name
    Returns:
        format_dict: <dict> cell format dictionary
    '''
    team_formats = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if 'Perks.json' not in file]
    format_dict = {}
    for team_path in team_formats:
        team_format = load_json(file_path=team_path)
        if driver in team_format['drivers']:
            for key, value in team_format.items():
                format_dict.update({key: value})
    return format_dict


def team_format(format_dir,
                team):
    '''
    Find team cell format, from team colors.
    Args:
        format_dir: <string> path to team format files
        team: <string> team name
    Returns:
        cell_format: <dict> format dictionary
    '''
    paths = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if '.json' in file]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    format_dict = {}
    for index, path in enumerate(paths):
        team_format = load_json(file_path=path)
        if team == teams[index]:
            for key, value in team_format.items():
                if key == 'drivers':
                    pass
                else:
                    format_dict.update({key: value})
    return format_dict


def team_colour(format_dir,
                team):
    '''
    Find team graph format, from team colors.
    Args:
        format_dir: <string> path to team format files
        team: <string> team name
    Returns:
        format_dict: <dict> format dictionary
    '''
    paths = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if '.json' in file]
    teams = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    format_dict = {}
    for index, path in enumerate(paths):
        team_format = load_json(file_path=path)
        if team == teams[index]:
            for key, value in team_format.items():
                format_dict.update({key: value})
    return format_dict


def perk_colour(format_dir,
                perk):
    '''
    Find perk graph format from color dictionary.
    Args:
        format_dir: <string> path to team format files
        perk: <string> perk name
    Returns:
        format_dict: <dict> format dictionary
    '''
    path = Path(f'{format_dir}/Perks.json')
    perk_formats = load_json(file_path=path)
    all_perks = perk_formats['perks']
    all_colours = perk_formats['bg_color']
    format_dict = {}
    for key, value in perk_formats.items():
        format_dict.update({key: value})
    for p, c in zip(all_perks, all_colours):
        if p == perk:
            format_dict.update({'bg_color': c})
    return format_dict


def manager_team_colour(format_dir,
                        team):
    '''
    Find team graph format, from manager colors.
    Args:
        format_dir: <string> path to manager format files
        team: <string> team name
    Returns:
        format_dict: <dict> format dictionary
    '''
    paths = [
        Path(f'{format_dir}/{file}')
        for file in os.listdir(format_dir)
        if '.json' in file]
    managers = [os.path.splitext(os.path.basename(path))[0] for path in paths]
    format_dict = {}
    for index, path in enumerate(paths):
        manager_format = load_json(file_path=path)
        if team in manager_format['teams']:
            for key, value in manager_format.items():
                format_dict.update({key: value})
    return format_dict


def managers_colour(format_dir,
                    manager):
    '''
    Find manager graph format, from manager colors.
    Args:
        format_dir: <string> path to manager format files
        manager: <string> manager name
    Returns:
        format_dict: <dict> format dictionary
    '''
    format_dict = load_json(
        file_path=Path(f'{format_dir}/{manager}.json'))
    return format_dict



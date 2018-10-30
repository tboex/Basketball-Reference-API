import difflib
import lib.data_harvest as data_harvest


def get_diff(inp):
    data_inp = data_harvest.get_data()

    players = data_inp[0]
    teams = data_inp[1]

    data = players + teams
    diff = difflib.get_close_matches(inp, data)
    return diff


def get_diff_teams(inp):
    data_inp = data_harvest.get_data()

    teams = data_inp[1]

    data = teams
    diff = difflib.get_close_matches(inp, data)
    return diff


def get_diff_players(inp):
    data_inp = data_harvest.get_data()

    players = data_inp[0]

    data = players
    diff = difflib.get_close_matches(inp, data)
    return diff

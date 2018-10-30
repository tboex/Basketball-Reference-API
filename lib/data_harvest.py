import requests
from bs4 import BeautifulSoup
import urllib.request
import datetime

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
players = []
teams = []


def get_data():
    players = get_players()
    teams = get_teams()
    return [players, teams]


def get_players():
    file = None
    try:
        filename = "saved/localcache/players_" + \
            str(datetime.datetime.now().date()) + ".txt"
        file = open(filename, "r")
        for line in file.readlines():
            players.append(line.replace('\n', ''))
    except:
        print("\nLocal Data for Players was not found.")
        print(" - Fetching Players")
        for letter in alphabet:
            URL = "https://www.basketball-reference.com/players/"
            URL = f"{URL}{letter}/"
            r = requests.get(URL)
            strip_data(r.text, "players")
        write_to_file(players, "players")

    return players


def get_teams():
    try:
        filename = "saved/localcache/teams_" + \
            str(datetime.datetime.now().date()) + ".txt"
        file = open(filename, "r")
        for line in file.readlines():
            teams.append(line.replace('\n', ''))
    except:
        print("\nLocal Data for Teams was not found.")
        print(" - Fetching Teams")
        URL = 'https://www.basketball-reference.com/teams/'
        r = requests.get(URL)
        strip_data(r.text, "teams")
        write_to_file(teams, "teams")
    return teams


def strip_data(html, type):
    soup = BeautifulSoup(html, 'html.parser')
    if type == "players":
        table = soup.find('table')
        tbody = table.find('tbody')
        for row in tbody.find_all('tr'):
            player_name = row.find('th')
            players.append(player_name.text.strip())
    if type == "teams":
        table = soup.find('table')
        tbody = table.find('tbody')
        for row in tbody.find_all('tr'):
            team_name = row.find('th')
            teams.append(team_name.text.strip())


def write_to_file(data, type):
    print("Writing " + type + " to File")
    data = sorted(set(data))
    filename = f"saved/localcache/{type}_" + str(datetime.datetime.now().date()) + ".txt"
    with open(filename, 'w') as f:
        for item in data:
            f.write("%s\n" % item.replace('*', ''))

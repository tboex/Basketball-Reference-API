import requests
from bs4 import BeautifulSoup
import urllib.request
import datetime
import pickle
import os.path


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
players = []
players_dict = {}
teams = []


def get_data():
    players, players_dict = get_players()
    teams = get_teams()
    return [players, teams], players_dict


def get_players():
    file = None
    filename = "saved/localcache/players_" + \
            str(datetime.datetime.now().date()) + ".txt"
    if os.path.exists(filename):
        file = open(filename, "r")
        for line in file.readlines():
            players.append(line.replace('\n', ''))
        return players, load_obj("players")
    else:
        print("\nLocal Data for Players was not found.")
        print(" - Fetching Players")
        obj = {}
        for letter in alphabet:
            URL = "https://www.basketball-reference.com/players/"
            URL = f"{URL}{letter}/"
            r = requests.get(URL)
            obj.update(strip_data(r.text, "players"))
        write_to_file(players, "players")
        save_obj(obj, "players")
        return players, obj


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
        players_dict = {}
        for row in tbody.find_all('tr'):
            player_name = row.find('th')
            link = player_name.find('a')
            players.append(player_name.text.strip())
            players_dict[player_name.text.strip()] = link['href']
        return players_dict
    if type == "teams":
        table = soup.find('table')
        tbody = table.find('tbody')
        for row in tbody.find_all('tr'):
            team_name = row.find('th')
            link = team_name.find('a')
            teams.append(team_name.text.strip())


def write_to_file(data, type):
    print("Writing " + type + " to File")
    data = sorted(set(data))
    filename = f"saved/localcache/{type}_" + str(datetime.datetime.now().date()) + ".txt"
    with open(filename, 'w') as f:
        for item in data:
            f.write("%s\n" % item.replace('*', ''))

def save_obj(obj, type):
    filename = f"saved/localcache/{type}_" + str(datetime.datetime.now().date()) + ".pkl"
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    

def load_obj(type):
    filename = f"saved/localcache/{type}_" + str(datetime.datetime.now().date()) + ".pkl"
    with open(filename, 'rb') as f:
        return pickle.load(f)
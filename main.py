import lib.players as players
import lib.teams as teams
import lib.search as search
import lib.data_harvest as data_harvest
import lib.settings as settings
import lib.data_magic_player as dmp

from tqdm import tqdm
import pprint
import argparse
import lib.menu as menu
import shutil
import os
from colorama import Fore, Back, Style
import datetime
from pyfiglet import Figlet


def main():
    settings.load_settings()
    date = datetime.datetime.now()
    str_date = str(date.year) + "-" + str(date.month)
    make_folders("saved/")
    make_folders("saved/localcache/")
    make_folders("saved/sqlite/")
    make_folders("saved/players/cache/")
    make_folders("saved/players/json/" + str_date + "/")
    make_folders("saved/players/cache/" + str_date + "/")
    make_folders("saved/teams/")
    make_folders("saved/teams/history/json/" + str_date + "/")
    make_folders("saved/teams/history/cache/")
    make_folders("saved/teams/specific/cache/")
    make_folders("saved/teams/specific/json/" + str_date + "/")

    bigWord()

    parser = argparse.ArgumentParser(
        description='Find out the information of anything in the Basketball world')
    parser.add_argument(
        'search', nargs='*', help="Enter the value that you wish to search. Without any flags it will search all of the possible endpoints")
    parser.add_argument('-p', nargs='*',
                        help='Player')
    parser.add_argument('-t', nargs='*',
                        help='Team')
    parser.add_argument('-c', action='store_true',
                        help='Compare'),
    parser.add_argument('-p2', nargs='*',
                        help='Second Player (Only use with the -c flag).  Example: -p Donovan Mitchell -p2 Kyrie Irving -c')

    args = parser.parse_args()
    name_inp = ' '.join(args.search)

    if name_inp:
        search_through_both(name_inp)
    elif args.p and args.p2:
        do_compare(args.p, args.p2)
    elif args.p:
        search_for_player(' '.join(args.p))
    elif args.t:
        search_for_team(' '.join(args.t))
    elif args.c:
        do_compare(None, None)
    else:
        mainmenu()


def bigWord():
    f = Figlet(font='slant')
    print(f.renderText('Rebound'))
    print('-' * 50)

def search_through_database(args, name):
    if args.p:
        search_for_player(name)
    elif args.t:
        search_for_team(name)
    else:
        search_through_both(name)


def search_through_both(name):
    get_diff_players(name)
    # try:
    #     get_diff_players(name)
    # except:
    #     get_diff_teams(name)


def search_for_player(name):
    player = players.Player(name)
    player.fetch_player()
    player.pretty_print_player()
    if settings.get_Local() == "True":
        player.to_file()
    if settings.get_JSON() == "True":
        player.to_json()


def search_for_team(name):
    choice = menu.hist_or_spec_team()
    team = teams.TeamHistory(name)
    team.fetch_team()
    if choice == "h":
        team.fetch_team()
        team.pretty_print()
        if settings.get_Local() == "True":
            team.to_file("history")
        if settings.get_JSON() == "True":
            team.to_json()
    elif choice == "s":
        year = menu.get_year()
        team_year_links = team.get_team_links()
        specific_team = teams.TeamSpecific(name, year, team_year_links)
        specific_team.fetch_team_specifics()
        specific_team.pretty_print()

        if settings.get_Local() == "True":
            team.to_file("specific")
        if settings.get_JSON() == "True":
            team.to_json()


def check_diff(name):
    diff_arr = search.get_diff(name)
    if name in diff_arr:
        return None
    else:
        return diff_arr


def check_diff_players(name):
    diff_arr = search.get_diff_players(name)
    if name in diff_arr:
        return None
    else:
        return diff_arr

def get_diff_players(name):
    diff_arr = check_diff_players(name)
    if diff_arr == []:
        print(" - No player named {} found".format(name))
    elif diff_arr == None:
        search_for_player(name)
    else:
        player = menu.diff_menu(diff_arr)
        search_for_player(player)


def check_diff_teams(name):
    diff_arr = search.get_diff_teams(name)
    if name in diff_arr:
        return None
    else:
        return diff_arr


def get_diff_teams(name):
    diff_arr = check_diff_teams(name)
    if diff_arr == None or diff_arr == []:
        search_for_team(name)
    else:
        team = menu.diff_menu(diff_arr)
        search_for_team(team)


def download_players():
    player_list, p_dict = data_harvest.get_players()
    averages = dmp.DM_Player()
    print("Downloading All Players: (Go Shoot some baskets while you wait)")
    print("------------------------")

    player_amount = len(player_list)
    pbar = tqdm(total=player_amount)
    for index, item in enumerate(player_list, start=0):
        player = players.Player(item.replace('.', ''))
        player.fetch_url(True)
        player.to_file()
        player.to_json()
        averages.set_all(player)
        if index < player_amount:
            pbar.update(1)
        if index > player_amount:
            break
    pbar.close()

    print("Getting Current Averages")
    print("------------------------")
    avg_obj = averages.get_averages()
    averages.to_file()


def download_teams():
    notfound = []
    team_list = data_harvest.get_teams()
    print("Downloading All Teams History:")
    print("------------------------")
    pbar = tqdm(total=(len(team_list)))
    for index, item in enumerate(team_list):
        if index % 10:
            pbar.update(index)
        team = teams.Team(item.replace('.', ''))
        try:
            team.get_team_history()
        except:
            notfound.append(item)

        print("Downloading Specifics for " + team.name)
        print("------------------------")
        for itemx in team.team_links:
            team.get_specific_year(str(itemx))
    pbar.close()


def make_folders(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def delete_folder(folder):
    shutil.rmtree(folder)


def do_compare(name1, name2):
    if name1 == None or name2 == None:
        inp = menu.get_name("Player").title()
    else:
        player1 = ' '.join(name1)
        inp = player1
    diff_arr = check_diff_players(inp)
    if diff_arr == None or diff_arr == []:
        player1 = players.Player(inp)
        player1.fetch_url(False)
    else:
        name = menu.diff_menu(diff_arr)
        player1 = players.Player(name)
        player1.fetch_url(False)

    # ---------------------------
    if name1 == None or name2 == None:
        inp = menu.get_name("Player2").title()
    else:
        player2 = ' '.join(name2)
        inp = player2
    diff_arr = check_diff_players(inp)
    if diff_arr == None or diff_arr == []:
        player2 = players.Player(inp)
        player2.fetch_url(False)
    else:
        name = menu.diff_menu(diff_arr)
        player2 = players.Player(name)
        player2.fetch_url(False)

    player1.compare(player2)


def mainmenu():
    choice = menu.main_menu()
    if choice == "p":
        get_diff_players(menu.get_name("Player").title())
    elif choice == "t":
        get_diff_teams(menu.get_name("Team").title())
    elif choice == "c":
        do_compare(None, None)
    elif choice == "s":
        inp = menu.settings_menu()
        if inp == "c":
            if menu.verify():
                print("Deleting all cached data")
                delete_folder("saved/localcache/")
                delete_folder("saved/players/cache")
                delete_folder("saved/teams/history/cache/")
                delete_folder("saved/teams/specific/cache/")
                print("All Cached data deleted")
        elif inp == "b":
            mainmenu()
        elif inp == "j":
            if settings.get_JSON() == "True":
                settings.set_JSON("False")
            else:
                settings.set_JSON("True")
            mainmenu()
        elif inp == "l":
            if settings.get_Local() == "True":
                settings.set_Local("False")
            else:
                settings.set_Local("True")
            mainmenu()
        elif inp == "d":
            down_inp = menu.downloads_menu()
            if down_inp == "n":
                check_diff_teams(down_inp)
            elif down_inp == "dp":
                if menu.y_n_download():
                    download_players()
            elif down_inp == "dt":
                if menu.y_n_download():
                    download_teams()


# ---- main ---
if __name__ == "__main__":
    main()


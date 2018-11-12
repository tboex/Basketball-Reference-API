import lib.players as players
import lib.teams as teams
import lib.search as search
import lib.data_harvest as data_harvest
import lib.settings as settings
import lib.data_visualization.player_visualization as player_visualization
import progressbar
import pprint
import argparse
import lib.menu as menu
import shutil
import os
from colorama import Fore, Back, Style
import datetime
import shutil


def main():
    settings.load_settings()
    date = datetime.datetime.now()
    str_date = str(date.year) + "-" + str(date.month)
    make_folders("saved/")
    make_folders("saved/localcache/")
    make_folders("saved/players/cache/")
    make_folders("saved/players/json/" + str_date + "/")
    make_folders("saved/players/cache/" + str_date + "/")
    make_folders("saved/teams/")
    make_folders("saved/teams/history/json/" + str_date + "/")
    make_folders("saved/teams/history/cache/")
    make_folders("saved/teams/specific/cache/")
    make_folders("saved/teams/specific/json/" + str_date + "/")

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


def search_through_database(args, name):
    if args.p:
        search_for_player(name)
    elif args.t:
        search_for_team(name)
    else:
        search_through_both(name)


def search_through_both(name):
    try:
        search_for_player(name)
    except:
        try:
            search_for_team(name)
        except:
            print("\n" + Fore.BLUE + ''.join(name) + Style.RESET_ALL +
                  " was not found as either a player or team")
            input("\nPress Enter to Continue...")
            mainmenu()


def search_for_player(name):
    player = players.Player(name)
    player.fetch_url(True)
    player.pretty_print_player()
    if settings.get_Local() == "True":
        player.to_file()
    if settings.get_JSON() == "True":
        player.to_json()
    if settings.get_Visual() == "True":
        print(settings.get_Visual())
        visualize(player, None)


def search_for_team(name):
    team = teams.Team(name)
    choice = menu.hist_or_spec_team()
    if choice == "h":
        try:
            team.get_team_history()
            team.pretty_print_team_history()
            if settings.get_Local() == "True":
                team.to_file("history")
            if settings.get_JSON() == "True":
                team.to_json_history()
        except:
            print("\n" + Fore.BLUE + name +
                  Style.RESET_ALL + "was not found as a team")
            input("\nPress Enter to Continue...")
            mainmenu()
    elif choice == "s":
        year = menu.get_year()
        try:
            team.get_team_history()
            team.get_specific_year(year)
            team.pretty_print_specific_team()
            if settings.get_Local() == "True":
                team.to_file("specific")
            if settings.get_JSON() == "True":
                team.to_json_specific()
        except:
            print("\n" + Fore.BLUE + name +
                  Style.RESET_ALL + "was not found as a team")
            input("\nPress Enter to Continue...")
            mainmenu()


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


def check_diff_teams(name):
    diff_arr = search.get_diff_teams(name)
    if name in diff_arr:
        return None
    else:
        return diff_arr


def download_players():
    notfound = []
    player_list, p_dict = data_harvest.get_players()
    print("Downloading All Players:")
    print("------------------------")
    with progressbar.ProgressBar(max_value=(len(player_list))) as bar:
        for index, item in enumerate(player_list):
            if index % 10:
                bar.update(index)
            player = players.Player(item.replace('.', ''))
            try:
                player.fetch_url(True)
            except:
                notfound.append(item)


def download_teams():
    notfound = []
    team_list = data_harvest.get_teams()
    print("Downloading All Teams History:")
    print("------------------------")
    with progressbar.ProgressBar(max_value=(len(team_list))) as bar:
        for index, item in enumerate(team_list):
            if index % 10:
                bar.update(index)
            team = teams.Team(item.replace('.', ''))
            try:
                team.get_team_history()
            except:
                notfound.append(item)
            print("Downloading Specifics for " + team.name)
            print("------------------------")
            for itemx in team.team_links:
                team.get_specific_year(str(itemx))


def visualize(player, team):
    if player:
        vis = menu.player_visualize_menu()
        if vis == "s":
            option = menu.player_visualize_menu_single()
            player_visualization.graph_player_stat(player, option)
        #player_visualization.graph_player_stat_comparison(player, "FG", "FGA")


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
        inp = menu.get_name("Player").title()
        diff_arr = check_diff_players(inp)
        if diff_arr == None or diff_arr == []:
            search_for_player(inp)
        else:
            player = menu.diff_menu(diff_arr)
            search_for_player(player)
    elif choice == "t":
        inp = menu.get_name("Team").title()
        diff_arr = check_diff_teams(inp)
        if diff_arr == None or diff_arr == []:
            search_for_team(inp)
        else:
            team = menu.diff_menu(diff_arr)
            search_for_team(team)
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
        elif inp == "v":
            if settings.get_Visual() == "True":
                settings.set_Visual("False")
            else:
                settings.set_Visual("True")
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


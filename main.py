import lib.players as players
import lib.teams as teams
import lib.search as search
import lib.data_harvest as data_harvest
import progressbar
import pprint
import argparse
import lib.menu as menu
import shutil
import os


def main():
    make_folders("saved/")
    make_folders("saved/localcache/")
    make_folders("saved/players/cache")
    make_folders("saved/teams/")
    make_folders("saved/teams/history/cache")
    make_folders("saved/teams/specific/cache")

    parser = argparse.ArgumentParser(description='Find out the information of anything in the Basketball world')
    parser.add_argument('search', nargs='*', help="Enter the value that you wish to search. Without any flags it will search all of the possible endpoints")
    parser.add_argument('-p', nargs='*',
                            help='Player')
    parser.add_argument('-t', nargs='*',
                            help='Team')
    parser.add_argument('-c', action='store_true',
                            help='Compare'),
    parser.add_argument('-p2', nargs='*',
                            help='Second Player (Only use with the -c flag).  Example: -p Donovan Mitchell -p2 Kyrie Irving -c'),
    parser.add_argument('-t2', nargs='*',
                            help='Second Team (Only use with the -c flag).  Example: -t Utah Jazz -t2 Chicago Bulls -c')                       

    args = parser.parse_args()
    name_inp = ' '.join(args.search)

    if name_inp:
        search_through_both(name_inp)
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
            print(''.join(name) + " was not found as either a player or team")
            input("Press Enter to Continue...")
            mainmenu()

def search_for_player(name):
    player = players.Player(name)
    player.fetch_url(True)
    player.pretty_print_player()

def search_for_team(name):
    team = teams.Team(name)
    team.get_team_history()
    choice = menu.hist_or_spec_team()
    if choice == "h":
        team.pretty_print_team_history()
    elif choice == "s":
        year = menu.get_year()
        team.get_team_history()
        team.get_specific_year(year)
        team.pretty_print_specific_team()

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

def make_folders(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def delete_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

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
        player1, player2 = None, None

        inp = menu.get_name("Player").title()
        diff_arr = check_diff_players(inp)
        if diff_arr == None or diff_arr == []:
            player1 = players.Player(inp)
            player1.fetch_url(False)
        else:
            name = menu.diff_menu(diff_arr)
            player1 = players.Player(name)
            player1.fetch_url(False)

        inp = menu.get_name("Player 2").title()
        diff_arr = check_diff_players(inp)
        if diff_arr == None or diff_arr == []:
            player2 = players.Player(inp)
            player2.fetch_url(False)
        else:
            name = menu.diff_menu(diff_arr)
            player2 = players.Player(name)
            player2.fetch_url(False)

        player1.compare(player2)
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
        elif inp == "p":
            check_diff_teams(inp)
        elif inp == "dp":
            if menu.y_n_download():
                notfound = []
                player_list = data_harvest.get_players()
                print("Downloading All Players:")
                print("------------------------")
                with progressbar.ProgressBar(max_value=(len(player_list))) as bar:
                    for index, item in enumerate(player_list):
                        if index % 10:
                            bar.update(index)
                        player = players.Player(item.replace('.',''))
                        try:
                            player.fetch_url(True)
                        except:
                            notfound.append(item)
        elif inp == "dt":
            if menu.y_n_download():
                notfound = []
                team_list = data_harvest.get_teams()
                print("Downloading All Teams History:")
                print("------------------------")
                with progressbar.ProgressBar(max_value=(len(team_list))) as bar:
                    for index, item in enumerate(team_list):
                        if index % 10:
                            bar.update(index)
                        team = teams.Team(item.replace('.',''))
                        try:
                            team.get_team_history()
                        except:
                            notfound.append(item)
                        print("Downloading Specifics for " + team.name)
                        print("------------------------")
                        for itemx in team.team_links:
                            team.get_specific_year(str(itemx))

# ---- main ---
if __name__ == "__main__":
    main()
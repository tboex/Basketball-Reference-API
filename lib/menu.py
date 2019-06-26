import qprompt
import re
from colorama import Fore, Back, Style
import lib.settings as settings

STAT_HEADERS = ['G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']


def main_menu():
    menu = qprompt.Menu()
    menu.add("p", f"{Fore.RED}Player{Style.RESET_ALL}")
    menu.add("t", f"{Fore.RED}Team{Style.RESET_ALL}")
    menu.add("c", f"{Fore.RED}Compare{Style.RESET_ALL}")
    menu.add("s", f"{Fore.RED}Settings{Style.RESET_ALL}")
    menu.add("q", "Quit")
    return menu.show()


def diff_menu(diff_arr):
    menu = qprompt.Menu()
    for index, item in enumerate(diff_arr):
        menu.add(str(index), item)
    return menu.show(returns="desc")


def hist_or_spec_team():
    menu = qprompt.Menu()
    menu.add("h", f"{Fore.RED}History{Style.RESET_ALL}")
    menu.add("s", f"{Fore.RED}Specific{Style.RESET_ALL}")
    return menu.show()


def settings_menu():
    menu = qprompt.Menu()
    menu.add("d", f"{Fore.RED}Downloades{Style.RESET_ALL}")
    menu.add("c", f"{Fore.RED}Clear Cache{Style.RESET_ALL}")
    menu.add("j", f"{Fore.RED}Download Searches as JSON{Style.RESET_ALL} - Currently " + settings.get_JSON())
    menu.add("l", f"{Fore.RED}Download Searches Locally{Style.RESET_ALL} - Currently " + settings.get_Local())
    menu.add("l", f"{Fore.RED}Download Searches to SQL{Style.RESET_ALL} - Currently " + settings.get_SQL())
    menu.add("v", f"{Fore.RED}Visualize Searches{Style.RESET_ALL} - Currently " + settings.get_Visual())
    menu.add("b", "Back")
    menu.add("q", "Quit")
    return menu.show()


def downloads_menu():
    menu = qprompt.Menu()
    menu.add("n", f"{Fore.RED}Download Names{Style.RESET_ALL}")
    menu.add("dp", f"{Fore.RED}Download All Players{Style.RESET_ALL}")
    menu.add("dt", f"{Fore.RED}Download All Teams{Style.RESET_ALL}")
    return menu.show()


def get_name(type):
    return qprompt.ask_str(f"{Fore.RED}{type}{Style.RESET_ALL} - Enter their name")


def get_year():
    return qprompt.ask_str("Enter a year span", valid=lambda x: bool(re.search('[0-9]{4}-[0-9]{2}', x)))


def y_n_download():
    return qprompt.ask_yesno("This may take around 10 mins, do you want to continue?")


def verify():
    sicher = qprompt.ask_yesno("Are you sure?")
    if sicher:
        cap = qprompt.ask_captcha(length=6)
        if cap == None:
            return True
    else:
        return False

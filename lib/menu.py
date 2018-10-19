import qprompt
import re
from colorama import Fore, Back, Style

def main_menu():
    menu = qprompt.Menu()
    menu.add("p", Fore.RED + "Player" + Style.RESET_ALL)
    menu.add("t", Fore.RED + "Team" + Style.RESET_ALL)
    menu.add("c", Fore.RED + "Compare" + Style.RESET_ALL)
    menu.add("s", Fore.RED + "Settings" + Style.RESET_ALL)
    menu.add("q", "Quit" )
    return menu.show()

def diff_menu(diff_arr):
    menu = qprompt.Menu()
    for index, item in enumerate(diff_arr):
        menu.add(str(index), item)
    return menu.show(returns="desc")

def hist_or_spec_team():
    menu = qprompt.Menu()
    menu.add("h", Fore.RED + "History" + Style.RESET_ALL)
    menu.add("s", Fore.RED + "Specific" + Style.RESET_ALL)
    return menu.show()

def settings_menu():
    menu = qprompt.Menu()
    menu.add("p", Fore.RED + "Download Names" + Style.RESET_ALL)
    menu.add("dp", Fore.RED + "Download All Players" + Style.RESET_ALL)
    menu.add("dt", Fore.RED + "Download All Teams" + Style.RESET_ALL)
    menu.add("c", Fore.RED + "Clear Cache" + Style.RESET_ALL)
    menu.add("b", "Back")
    menu.add("q", "Quit")
    return menu.show()

def get_name(type):
    return qprompt.ask_str(Fore.RED + type + Style.RESET_ALL + " - Enter their name")

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

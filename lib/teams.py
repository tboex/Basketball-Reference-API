import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
import urllib.request
import pickle
from colorama import Fore, Style
import json
import datetime


position_conv = {
    "Shooting": "SG",
    "Point": "PG",
    "Center": "C",
    "Small": "SF",
    "Power": "PF",
}
team_list = {
    "hawks": "/teams/ATL/",
    "celtics": "/teams/BOS/",
    "nets": "/teams/NJN/",
    "hornets": "/teams/CHA/",
    "bulls": "/teams/CHI/",
    "cavaliers": "/teams/CLE/",
    "mavericks": "/teams/DAL/",
    "nuggets": "/teams/DEN/",
    "pistons": "/teams/DET/",
    "warriors": "/teams/GSW/",
    "rockets": "/teams/HOU/",
    "pacers": "/teams/IND/",
    "clippers": "/teams/LAC/",
    "lakers": "/teams/LAL/",
    "grizzlies": "/teams/MEM/",
    "heat": "/teams/MIA/",
    "bucks": "/teams/MIL/",
    "timberwolves": "/teams/MIN/",
    "pelicans": "/teams/NOH/",
    "knicks": "/teams/NYK/",
    "thunder": "/teams/OKC/",
    "magic": "/teams/ORL/",
    "76ers": "/teams/PHI/",
    "suns": "/teams/PHO/",
    "blazers": "/teams/POR/",
    "trailblazers": "/teams/POR/",
    "kings": "/teams/SAC/",
    "spurs": "/teams/SAS/",
    "raptors": "/teams/TOR/",
    "jazz": "/teams/UTA/",
    "wizards": "/teams/WAS/",
}


class Team:
    def __init__(self, name):
        self.name = name
        self.team_headers = []
        self.team_stats = []
        self.team_links = {}

        self.specific_year = ""
        self.roster = []
        self.roster_headers = []
        self.roster_links = {}

        self.assistant_staff_links = {}
        self.assistant_staff = []

        self.specific_year_record = ""
        self.specific_year_lg = ""
        self.specific_year_coach = ""
        self.specific_year_executive = ""
        self.specific_year_pts_g = ""
        self.specific_year_opp_pts_g = ""
        self.specific_year_srs = ""
        self.specific_year_pace = ""
        self.specific_year_off_rtg = ""
        self.specific_year_def_rtg = ""
        self.specific_year_expected_wl = ""
        self.specific_year_arena = ""
        self.specific_year_playoffs = ""

        self.total_headers = []
        self.total_stats = []

    def get_team_history(self):
        def fetch_url(self):
            if self.from_file("history") == False:
                URL = "https://www.basketball-reference.com"
                URL = URL + team_list[self.name.split()[-1].lower()]
                html = ""
                try:
                    with urllib.request.urlopen(URL) as response:
                        # use whatever encoding as per the webpage
                        html = response.read().decode('utf-8')
                except urllib.request.HTTPError as e:
                    if e.code == 404:
                        print(f"{URL} is not found")
                    elif e.code == 503:
                        print(f'{URL} base webservices are not available')
                        # can add authentication here
                    else:
                        print('http error', e)
                clean_team_url(self, html)
                return True
            else:
                print(Fore.GREEN + " - Data Loaded from File - " + Style.RESET_ALL)

        def clean_team_url(self, html):
            soup = BeautifulSoup(html, 'html.parser')
            history = soup.find('div', attrs={"class": "overthrow"})
            get_team_history_info(self, history)

        def get_team_history_info(self, history):
            table = history.find('table')
            thead = table.find('thead')
            headers = thead.find_all('th')
            for header in headers:
                self.team_headers.append(header.text.strip())
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            for row in rows:
                temp = []
                header = row.find('th')
                if header.a:
                    self.team_links[header.text.strip()] = header.a.get('href')
                temp.append(header.text.strip())
                tds = row.find_all('td')
                [temp.append(td.text.strip()) for td in tds]
                self.team_stats.append(temp)

        fetch_url(self)

    def get_specific_year(self, year):
        def fetch_url(self, year):
            self.specific_year = year
            is_specific = self.from_file("specific")
            if is_specific == False:
                URL = "https://www.basketball-reference.com"
                URL = URL + self.team_links[year]
                html = ""
                try:
                    with urllib.request.urlopen(URL) as response:
                        # use whatever encoding as per the webpage
                        html = response.read().decode('utf-8')
                except urllib.request.HTTPError as e:
                    if e.code == 404:
                        print(f"{URL} is not found")
                    elif e.code == 503:
                        print(f'{URL} base webservices are not available')
                    else:
                        print('http error', e)
                clean_team_url(self, html)
            else:
                print(" - Data Loaded from File - ")

        def clean_team_url(self, html):
            soup = BeautifulSoup(html, 'html.parser')
            roster = soup.find('table', attrs={'id': 'roster'})
            info = soup.find('div', attrs={'id': 'info'})
            totals = soup.find('div', attrs={'id': 'all_totals'})
            staff = soup.find('div', attrs={'id': 'all_assistant_coaches'})
            try:
                get_roster(self, roster)
            except:
                print("No Roster found")
            try:
                get_totals(self, totals)
            except:
                print("No Totals Found")
            try:
                get_info_for_year(self, info)
            except:
                print("No info for year")
            try:
                get_assistant_staff(self, staff)
            except:
                print("No Assistant Staff")
            self.to_file("specific")

        def get_roster(self, roster):
            thead = roster.find('thead')
            self.roster_headers = thead.text.strip().replace(' ', ' CountryofOrigin').split()
            tbody = roster.find('tbody')
            rows = tbody.find_all('tr')
            for row in rows:
                temp = []
                temp.append(row.find('th').text.strip())
                tds = row.find_all('td')
                for td in tds:
                    temp.append(td.text.strip())
                self.roster.append(temp)

        def get_assistant_staff(self, staff):
            soup = BeautifulSoup(str(staff).replace(
                '-->', '').replace('<!--', ''), 'html.parser')
            table = soup.find('table')
            for row in table.find_all('tr'):
                if row.a:
                    self.assistant_staff_links[row.a.text] = row.a.get('href')
                for td in row.find_all('td'):
                    self.assistant_staff.append(td.text.strip())
                # self.assistant_staff[temp[0] = temp[1]

        def get_totals(self, totals):
            soup = BeautifulSoup(str(totals).replace(
                '-->', '').replace('<!--', ''), 'html.parser')
            table = soup.find('table', attrs={'id': 'totals'})
            thead = table.find('thead')
            self.total_headers = thead.text.strip().split()
            tbody = table.find('tbody')
            for row in tbody.find_all('tr'):
                temp = []
                temp.append(row.find('th').text.strip())
                tds = row.find_all('td')
                for td in tds:
                    temp.append(td.text.strip())
                self.total_stats.append(temp)

        def get_info_for_year(self, info):
            div = info.find('div', attrs={'id': 'meta'})
            for p in div.find_all('p'):
                arr = p.text.strip().split()
                if 'Record:' in arr:
                    self.specific_year_record = ' '.join(arr[1:])
                if 'Game:' in arr:
                    self.specific_year_lg = ' '.join(arr[2:])
                if 'Coach:' in arr:
                    self.specific_year_coach = ' '.join(arr[1:])
                if 'Executive:' in arr:
                    self.specific_year_executive = ' '.join(arr[1:])
                if 'PTS/G:' in arr:
                    self.specific_year_pts_g = ' '.join(arr[1:arr.index("Opp")])
                    self.specific_year_opp_pts_g = ' '.join(arr[arr.index("Opp")+2:])
                if 'SRS:' in arr:
                    self.specific_year_srs = ' '.join(arr[1:arr.index("Pace:")])
                if 'Pace:' in arr:
                    self.specific_year_pace = ' '.join(arr[arr.index("Pace:")+1:])
                if 'Rtg:' in arr:
                    self.specific_year_off_rtg = ' '.join(arr[2:arr.index("Def")])
                    self.specific_year_def_rtg = ' '.join(arr[arr.index("Def")+2:])
                if 'W-L:' in arr:
                    self.specific_year_expected_wl = ' '.join(arr[2:])
                if 'Arena:' in arr:
                    self.specific_year_arena = ' '.join(arr[1:])
                if 'Playoffs:' in arr:
                    self.specific_year_playoffs = ' '.join(arr[3:])

        fetch_url(self, year)

    def pretty_print_team_history(self):

        print('\n\033[1m\033[96mTeam History:\033[0m')
        print("-" * 40)
        print(tabulate(self.team_stats,
                       headers=self.team_headers, tablefmt='fancy_grid'))

    def pretty_print_specific_team(self):
        print("\033[1m\033[91m\n" + self.name +
              "  " + self.specific_year + '\033[0m')
        print("-" * 40)

        if self.specific_year_record:
            print("\033[1m\033[96m " + "Record: " +
                  '\033[0m' + self.specific_year_record)
            print("\033[1m\033[96m " + "Last Game: " +
                  '\033[0m' + self.specific_year_lg)
            print("\033[1m\033[96m " + "Coach: " +
                  '\033[0m' + self.specific_year_coach)
            print("\033[1m\033[96m " + "Executive: " +
                  '\033[0m' + self.specific_year_executive)
            print("\033[1m\033[96m " + "PTS/G: " +
                  '\033[0m' + self.specific_year_pts_g)
            print("\033[1m\033[96m " + "Opp PTS/G: " +
                  '\033[0m' + self.specific_year_opp_pts_g)
            print("\033[1m\033[96m " + "SRS: " +
                  '\033[0m' + self.specific_year_srs)
            print("\033[1m\033[96m " + "Pace: " +
                  '\033[0m' + self.specific_year_pace)
            print("\033[1m\033[96m " + "Off Rtg: " +
                  '\033[0m' + self.specific_year_off_rtg)
            print("\033[1m\033[96m " + "Def Rtg: " +
                  '\033[0m' + self.specific_year_def_rtg)
            print("\033[1m\033[96m " + "W/L: " + '\033[0m' +
                  self.specific_year_expected_wl)
            print("\033[1m\033[96m " + "Arena: " +
                  '\033[0m' + self.specific_year_arena)
            print("\033[1m\033[96m " + "Playoffs: " +
                  '\033[0m' + self.specific_year_playoffs)

        if self.assistant_staff:
            print("\n\033[1m\033[91mAssistant Staff:" + '\033[0m')
            print("-" * 40)
            for index in range(int(len(self.assistant_staff)/2)):
                print("\033[1m\033[96m" + self.assistant_staff[index] +
                      '\033[0m -  ' + self.assistant_staff[index+1])

        if self.roster_headers:
            print("\n\033[1m\033[91m\033[4mRoster:" + '\033[0m')
            print("-" * 40)
            print(tabulate(self.roster, headers=self.roster_headers,
                           tablefmt='fancy_grid'))

        if self.total_headers:
            print("\n\033[1m\033[91m\033[4mTotals:" + '\033[0m')
            print("-" * 40)
            print(tabulate(self.total_stats,
                           headers=self.total_headers, tablefmt='fancy_grid'))

    def to_file(self, name):
        filename = "saved/teams/" + name + "/cache/" + \
            self.name.replace(" ", "_") + self.specific_year + ".pkl"
        output = open(filename, 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(vars(self), output)

        output.close()


    def from_file(self, name):
        filename = "saved/teams/" + name + "/cache/" + \
            self.name.replace(" ", "_") + self.specific_year + ".pkl"
        try:
            pkl_file = open(filename, 'rb')
            data = pickle.load(pkl_file)
            for key in data:
                setattr(self, key, data[key])
            pkl_file.close()
            return True
        except:
            return False


    def to_json_history(self):
        date = datetime.datetime.now()
        str_date = str(date.year) + "-" + str(date.month)
        filename = "saved/teams/history/json/{}/{}.json".format(
            str_date, self.name.replace(" ", "_"))
        obj = {}
        obj['Team_Stats'] = {}
        for row in self.team_stats:
            obj['Team_Stats'][row[0]] = {}
            for index, item in enumerate(row):
                obj['Team_Stats'][row[0]][str(self.team_headers[index])] = item

        with open(filename, 'w') as outfile:
            json.dump(obj, outfile)

    
    def to_json_specific(self):
        date = datetime.datetime.now()
        str_date = str(date.year) + "-" + str(date.month)
        filename = "saved/teams/specific/json/{}/{}{}.json".format(
            str_date, self.name.replace(" ", "_"), self.specific_year)
        obj = {}
        obj['Record'] = self.specific_year_record
        obj['Last_Game'] = self.specific_year_lg
        obj['Coach'] = self.specific_year_coach
        obj['Executive'] = self.specific_year_executive
        obj['Points_Per_Game'] = self.specific_year_pts_g
        obj['Simple_Rating_System'] = self.specific_year_srs
        obj['Pace'] = self.specific_year_pace
        obj['Offensive_Rating'] = self.specific_year_off_rtg
        obj['Defensive_Rating'] = self.specific_year_def_rtg
        obj['Win_Loss'] = self.specific_year_expected_wl
        obj['Arena'] = self.specific_year_arena
        obj['Playoffs'] = self.specific_year_playoffs

        obj['Roster'] = {}
        for row in self.roster:
            obj['Roster'][row[1]] = {}
            for index, item in enumerate(row):
                obj['Roster'][row[1]][self.roster_headers[index]] = item

        obj['Totals'] = {}
        for row in self.total_stats:
            obj['Totals'][row[1]] = {}
            for index, item in enumerate(row):
                if index > 0:
                    obj['Totals'][row[1]][self.total_headers[index-1]] = item
        with open(filename, 'w') as outfile:
            json.dump(obj, outfile)
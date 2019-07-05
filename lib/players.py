import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
import pickle
import pprint
import datetime
import json

import lib.settings as settings
import lib.data_harvest
import lib.data_magic_player as dmp
import lib.sql_lib.sqlizer as sqlizer
from lib.data_structures import Field

position_conv = {
    "Shooting": "SG",
    "Point": "PG",
    "Center": "C",
    "Small": "SF",
    "Power": "PF",
}

class Player:
    def __init__(self, name):
        self.name = name
        self.profile_link = ""
        self.height = ""
        self.weight = ""
        self.position = []
        self.shoots = ""
        self.team = ""
        self.team_colors = None
        self.born = ""
        self.college = ""
        self.high_school = ""
        self.recruiting_rank = ""
        self.draft = ""
        self.nba_debut = ""
        self.experience = ""
        self.awards = []
        self.age = ""

        self.stat_headers = []
        self.stats = []

        self.pbp_headers = []
        self.pbp_stats = []

        self.similarities_carrer_headers = []
        self.similarities_carrer = []

        self.transactions = []

        self.projection_year = ""
        self.projections_headers = []
        self.projections = []

        self.salaries_headers = []
        self.salaries = []
        self.contract_headers = []
        self.contract = []

        self.current_stats = {}
        self.current_year = self.set_current_year(datetime.datetime.today().year)

        self.percentiles = {}
        self.percentiles_arr = []
        self.percentiles_headers = []
        
    def fetch_player(self, full=True):
        player_data = self.fetch_url()
        if player_data:
            cleaned_player_data = self.clean_player_url(player_data)
            data_points = self.get_data_points(cleaned_player_data)
            self.get_info_from_data_points(data_points)

    def set_current_year(self, year):
        future_opener = datetime.date(year, 11, 16)

        if datetime.date.today() < future_opener:
            year = year - 1
        appendage = year%100 + 1
        return str(str(year) + "-" + str(appendage))

    def fetch_url(self):
        player_name = self.name.split()
        is_file = self.from_file()
        if is_file == False:
            players_dict = lib.data_harvest.get_players()[1]
            URL = "https://www.basketball-reference.com"
            if self.name in players_dict:
                URL = URL + players_dict[self.name]
            else:
                first_name = list(player_name[0])
                last_name = list(''.join(player_name[1:]))
                last_name_index = last_name[0]

                if len(last_name) > 5:
                    last_name = last_name[:5]
                if len(first_name) > 2:
                    first_name = first_name[:2]

                URL = URL + '/players/' + last_name_index.lower() + '/' + ''.join(last_name).lower() + \
                    ''.join(first_name).lower() + '01.html'
            r = requests.get(URL)
            return (r.text)
        else:
            return None

    def clean_player_url(self, html):
        return BeautifulSoup(html, 'html.parser')

    def get_data_points(self, soup):
        return {
            "info": soup.find('div', attrs={'id': 'info'}),
            "basic_info": Field(soup.find('div', attrs={'itemtype': 'https://schema.org/Person'}), Player.get_basic_info),
            "bling": Field(soup.find('ul', attrs={"id": "bling"}), Player.get_bling),
            "stats": Field(soup.find('div', attrs={'class': 'stats_pullout'}), Player.get_summary_stats),
            "full_stats": Field(soup.find('table', attrs={'id': 'per_game'}), Player.get_full_stats),
            "similarity_carrer": Field(soup.find('div', attrs={'id': 'all_sim_career'}), Player.get_similarities),
            "transactions": Field(soup.find('div', attrs={'id': 'all_transactions'}), Player.get_transactions),
            "projections": Field(soup.find('div', attrs={'id': 'all_projection'}), Player.get_projections),
            "salaries": Field(soup.find('div', attrs={'id': 'all_all_salaries'}), Player.get_salaries),
            "contract": Field(soup.find('div', attrs={'id': 'all_contracts_bos'}), Player.get_contract),
            "play_by_play": Field(soup.find('div', attrs={'id': 'all_pbp'}), Player.get_play_by_play),
        }
        
    def get_info_from_data_points(self, data_points):
        for key in data_points:
            field = data_points[key]
            if field.data and isinstance(field, Field):
                field.transform_func(self, field.data)
        
        self.profile_link = data_points.get('info').find('img')['src']
        self.team_colors = self.team_to_colors()

    def get_basic_info(self, basic_info):
        try:
            info_arr = []
            self.name = basic_info.find(
                'h1', attrs={'itemprop': 'name'}).text.strip()
            for p in basic_info.find_all('p'):
                info_arr.append(p.text.strip().split())
            for index, info in enumerate(info_arr):
                if "Position:" in info:
                    position = info[(info.index("Position:") + 1): (info.index("Shoots:") - 1)]
                    for pos in position:
                        if pos in position_conv:
                            self.position.append(position_conv[pos])
                    bio_arr = info_arr[index + 1]
                    self.height, self.weight = bio_arr[0].replace(
                        ',', ''), bio_arr[1].replace(',', '')
                if "Shoots:" in info:
                    self.shoots = info[info.index("Shoots:") + 1]
                if "Team:" in info:
                    self.team = ' '.join(info[info.index("Team:") + 1:])
                if "Born:" in info:
                    self.born = ' '.join(
                        info[info.index("Born:")+1:]).replace(',', '')
                if "College:" in info:
                    self.college = ' '.join(info[info.index("College:")+1:])
                if "School:" in info:
                    self.high_school = ' '.join(
                        info[info.index("School:")+1:]).replace(',', '')
                if "Rank:" in info:
                    self.recruiting_rank = ' '.join(
                        info[info.index("Rank:")+1:]).replace('(', '').replace(')', '')
                if "Debut:" in info:
                    self.nba_debut = ' '.join(
                        info[info.index("Debut:")+1:]).replace(',', '')
                if "Experience:" in info:
                    self.experience = ' '.join(info[info.index("Experience:")+1:])
                if "Draft:" in info:
                    self.draft = ' '.join(
                        info[info.index("Draft:")+1:]).replace(',', '')
        except Exception as e:
            print("{} Error : with {}".format(e, self.name))

    def get_bling(self, bling):
        try:
            for li in bling.find_all('li'):
                self.awards.append(li.text.strip())
        except:
            self.awards = []

    def get_summary_stats(self, html):
        headers = html.find_all('h4')
        for header in headers:
            self.stat_headers.append(header.text.strip())
        stats = html.find_all('p')
        temp = []
        for stat in stats:
            temp.append(stat.text.strip())

        current = []
        carrer = []
        for index, item in enumerate(temp):
            if index == 0 or index % 2 == 0:
                current.append(item)
            else:
                carrer.append(item)
        self.stats.append(current)
        self.stats.append(carrer)

    def get_full_stats(self, html):
        summary = html.find('thead')
        table = html.find('tbody')
        stats = table.find_all('tr')
        for row in stats:
            temp = []
            season = row.find('th')
            if season:
                temp.append(season.text.strip())
            for info in row.find_all('td'):
                temp.append(info.text.strip())
            self.stats.append(temp)
            if self.current_year in temp:
                self.set_current_stats(temp)
                

        [self.stat_headers.append(item) for item in summary.text.strip().split()]
        footer = html.find('tfoot')
        rows = footer.find_all('tr')
        for row in rows:
            temp = []
            season = row.find('th')
            temp.append(season.text.strip())
            for info in row.find_all('td'):
                temp.append(info.text.strip())
            self.stats.append(temp)

    def set_current_stats(self, arr):
        self.current_stats['age'] = arr[1]
        self.current_stats['position'] = arr[4]
        self.current_stats['games'] = arr[5]
        self.current_stats['minutes_played'] = arr[7]
        self.current_stats['fg'] = arr[8]
        self.current_stats['fga'] = arr[9]
        self.current_stats['fg_per'] = arr[10]
        self.current_stats['3fg'] = arr[11]
        self.current_stats['3fga'] = arr[12]
        self.current_stats['3fg_per'] = arr[13]
        self.current_stats['efg_per'] = arr[17]
        self.current_stats['ft'] = arr[18]
        self.current_stats['fta'] = arr[19]
        self.current_stats['ft_per'] = arr[20]
        self.current_stats['orb'] = arr[21]
        self.current_stats['drb'] = arr[22]
        self.current_stats['trb'] = arr[23]
        self.current_stats['ast'] = arr[24]
        self.current_stats['stl'] = arr[25]
        self.current_stats['blk'] = arr[26]
        self.current_stats['tov'] = arr[27]
        self.current_stats['pf'] = arr[28]
        self.current_stats['pts'] = arr[29]

    def team_to_colors(self):
        color_dict = {
            "Atlanta Hawks": ('#e03a3e', '#C1D32F', '#26282A'),
            "Boston Celtics": ('#007A33', '#BA9653', '#963821'),
            "Brooklyn Nets": ('#000000', '#FFFFFF'),
            "Charlotte Hornets": ('#1d1160', '#00788C', '#A1A1A4'),
            "Chicago Bulls": ('#CE1141', '#000000'),
            "Cleveland Cavaliers": ('#6F263D', '#041E42', '#FFB81C'),
            "Dallas Mavericks": ('#00538C', '#002B5e', '#B8C4CA'),
            "Denver Nuggets": ('#0E2240', '#FEC524', '#8B2131'),
            "Detroit Pistons": ('#C8102E', '#006BB6', '#bec0c2'),
            "Golden State Warriors": ('#006BB6', '#FDB927', '#26282A'),
            "Houston Rockets": ('#CE1141', '#000000', '#C4CED4'),
            "Indiana Pacers": ('#002D62', '#FDBB30', '#BEC0C2'),
            "Los Angeles Clippers": ('#c8102E', '#1d42ba', '#BEC0C2'),
            "Los Angeles Lakers": ('#552583', '#FDB927', '#000000'),
            "Memphis Grizzlies": ('#5D76A9', '#12173F', '#F5B112'),
            "Miami Heat": ('#98002E', '#F9A01B', '#000000'),
            'Milwaukee Bucks': ('#00471B', '#EEE1C6', '#000000'),
            'Minnesota Timberwolves': ('#0C2340', '#236192', '#78BE20'),
            'New Orleans Pelicans': ('#0C2340', '#C8102E', '#85714D'),
            'New York Knicks': ('#006BB6', '#F58426', '#BEC0C2'),
            'Oklahoma City Thunder': ('#007ac1', '#ef3b24', '#002D62'),
            'Orlando Magic': ('#0077c0', '#C4ced4', '#000000'),
            'Philadelphia 76ers': ('#006bb6', '#ed174c', '#002B5C'),
            'Phoenix Suns': ('#1d1160', '#e56020', '#000000'),
            'Portland Trail Blazers': ('#E03A3E', '#000000'),
            'Sacramento Kings': ('#5a2d81', '#63727A', '#000000'),
            'San Antonio Spurs': ('#c4ced4', '#000000'),
            'Toronto Raptors': ('#ce1141', '#000000', '#A1A1A4'),
            'Utah Jazz': ('#002B5C', '#00471B', '#F9A01B'),
            'Washington Wizards': ('#002B5C', '#e31837', '#C4CED4')
        }
        if self.team in color_dict:
            return color_dict[self.team]
        else:
            return None

    def get_play_by_play(self, html):
        soup = BeautifulSoup(str(html).replace(
            '-->', '').replace('<!--', ''), 'html.parser')
        table = soup.find('table', attrs={'id': 'pbp'})
        summary = table.find('thead')
        tbody = table.find('tbody')

        self.pbp_headers = summary.text.strip().split()
        self.pbp_headers = self.pbp_headers[self.pbp_headers.index("Season"):]
        for row in tbody.find_all('tr'):
            temp = []
            season = row.find('th')
            if season:
                temp.append(season.text.strip())
            for info in row.find_all('td'):
                temp.append(info.text.strip())
            if self.current_year in temp:
                self.age = temp[1]
            self.pbp_stats.append(temp)
        
        footer = table.find('tfoot')
        rows = footer.find_all('tr')
        for row in rows:
            temp = []
            season = row.find('th')
            temp.append(season.text.strip())
            for info in row.find_all('td'):
                temp.append(info.text.strip())
            self.pbp_stats.append(temp)

    def get_similarities(self, similarity):
        soup = BeautifulSoup(str(similarity).replace(
            '-->', '').replace('<!--', ''), 'html.parser')
        table = soup.find('table')
        thead = table.find('thead')
        self.similarities_carrer_headers = thead.text.strip().split()
        tbody = table.find('tbody')
        for row in tbody.find_all('tr'):
            temp = []
            temp.append(row.find('th').text.strip())
            tds = row.find_all('td')
            for td in tds:
                temp.append(td.text.strip())
            self.similarities_carrer.append(temp)
        self.similarities_carrer_headers = self.similarities_carrer_headers[6:]
        self.similarities_carrer_headers[1] = "Sim | Win Shares (Best to Worst)"

    def get_transactions(self, transactions):
        soup = BeautifulSoup(str(transactions).replace(
            '-->', '').replace('<!--', ''), 'html.parser')
        div = soup.find('div', attrs={'id': 'div_transactions'})
        for p in div.find_all('p'):
            self.transactions.append(p.text.strip())

    def compare_to_averages(self):
        if self.current_stats:
            average_engine = dmp.DM_Player()
            if average_engine.from_file():
                self.percentiles = average_engine.get_percentiles(self)

                for key in self.percentiles:
                    self.percentiles_arr.append(self.percentiles[key])
                    self.percentiles_headers.append(key)

    def get_projections(self, html):
        html = html.find('table')
        thead = html.find('thead')
        headers = thead.find_all('th', attrs={'class': 'poptip'})
        for header in headers:
            self.projections_headers.append(header.text.strip())
        self.projections_headers.remove('Season')

        tbody = html.find('tbody')
        self.projection_year = tbody.find('th').text.strip()
        stats = tbody.find_all('td')

        for stat in stats:
            temp = stat.text.strip()
            self.projections.append(str(temp))
    
    def get_contract(self, html):
        soup = BeautifulSoup(str(html).replace(
            '-->', '').replace('<!--', ''), 'html.parser')
        table = soup.find('table')
        h_rows = table.find_all('th')

        for item in h_rows:
            self.contract_headers.append(item.text.strip())
        for row in table.find_all('tr'):
            temp = []
            for item in row.find_all('td'):
                temp.append(item.text.strip())
            if temp:
                self.contract.append(temp)

    def get_salaries(self, html):
        soup = BeautifulSoup(str(html).replace(
            '-->', '').replace('<!--', ''), 'html.parser')
        html = soup.find('div', attrs={'class', 'table_outer_container'})
        html = html.find('table')
        thead = html.find('thead')
        headers = thead.find_all('th', attrs={'class': 'poptip'})
        for header in headers:
            self.salaries_headers.append(header.text.strip())
        

        tbody = html.find('tbody')
        stats = tbody.find_all('tr')

        for stat in stats:
            temp = []
            temp.append(stat.find('th').text.strip())
            for info in stat.find_all('td'):
                temp.append(info.text.strip())
            self.salaries.append(temp)

    def pretty_print_player(self):
        print("\033[1m\033[91m\n{}\n\033[0m".format(self.name))
        print("\033[1m\033[96m{}\033[0m".format("Info:"))
        print("-" * 40)
        print("\033[1m\033[96m {}\033[0m {}".format("Age:", self.age))
        print("\033[1m\033[96m {}:\033[0m{} at {}".format(
            "Build", self.height, self.weight))
        print("\033[1m\033[96m {}\033[0m {}".format("Positions:", ', '.join(self.position)))
        print("\033[1m\033[96m {}\033[0m{}".format("Shoots:", self.shoots))
        print("\033[1m\033[96m {}\033[0m{}".format("Team:", self.team))
        print("\033[1m\033[96m {}\033[0m{}".format("Born:", self.born))

        if self.college:
            print("\033[1m\033[96m {}\033[0m{}".format(
                "College: ", self.college))
        if self.high_school:
            print("\033[1m\033[96m {}\033[0m{}".format(
                "High School: ", self.high_school))
        if self.recruiting_rank:
            print("\033[1m\033[96m {}\033[0m{}".format(
                "Recruiting Rank: ", self.recruiting_rank))
        if self.draft:
            print("\033[1m\033[96m {}\033[0m{}".format("Draft: ", self.draft))
        if self.nba_debut:
            print("\033[1m\033[96m {}\033[0m{}".format(
                "NBA Debut: ", self.nba_debut))
        if self.experience:
            print("\033[1m\033[96m {}\033[0m{}".format(
                "Experience: ", self.experience))
        if self.awards:
            print("\n\033[1m\033[96mAwards:\033[0m")
            print("-" * 40)
            for award in self.awards:
                print("  - {}".format(award))
        if self.transactions:
            print("\n\033[1m\033[96mTransactions:\033[0m")
            print("-" * 40)
            for transaction in self.transactions:
                print("  - {}".format(transaction))
        if self.projections:
            self.pretty_print_array((self.projection_year + " Projections"), [self.projections], self.projections_headers)
        if self.contract:
            self.pretty_print_array(("Contract"), self.contract, self.contract_headers)
        if self.salaries:
            self.pretty_print_array(("Salaries"), self.salaries, self.salaries_headers)
        if self.stats:
            self.pretty_print_array(("Stats"), self.stats, self.stat_headers)
        if self.pbp_stats:
            self.pretty_print_array(("Play-by-Play Stats"), self.pbp_stats, self.pbp_headers)
        if self.percentiles:
            self.pretty_print_array(("Percentiles"), [self.percentiles_arr], self.percentiles_headers)
        if self.similarities_carrer_headers:
            self.pretty_print_array(("Simularities"), self.similarities_carrer, self.similarities_carrer_headers)

    def pretty_print_array(self, title, data_arr, header_arr):
        print("\n\033[1m\033[96m{}:\033[0m".format(title))
        print("-" * 40)
        print(tabulate(data_arr, headers=header_arr, tablefmt='fancy_grid'))

    def compare(self, altPlayer):
        headers_comparison = [" "]
        headers_comparison.append(self.name)
        headers_comparison.append(altPlayer.name)

        info = []
        info.append(["Height", self.height, altPlayer.height])
        info.append(["Position", ", ".join(self.position),
                     ", ".join(altPlayer.position)])
        info.append(["Shooting Hand", self.shoots, altPlayer.shoots])
        info.append(["Team", self.team, altPlayer.team])
        info.append(["Born", self.born, altPlayer.born])
        info.append(["College", self.college, altPlayer.college])
        info.append(["High School", self.high_school, altPlayer.high_school])
        info.append(["Recruiting Rank", self.recruiting_rank.replace(
            " ", '-'), altPlayer.recruiting_rank.replace(" ", '-')])
        info.append(["Draft", self.draft, altPlayer.draft])
        info.append(["NBA Debut", self.nba_debut.replace(
            " ", ','), altPlayer.nba_debut.replace(" ", ',')])
        info.append(["Experience", self.experience, altPlayer.experience])
        info.append(["Awards", ", ".join(self.awards),
                     ", ".join(altPlayer.awards)])

        print(tabulate(info, headers=headers_comparison, tablefmt='fancy_grid'))

        headers_comparison.insert(2, " ")
        stats = []
        for index, item in enumerate(self.stats[0]):
            temp = []
            curr1 = self.stats[0][index]
            carr1 = self.stats[1][index]
            curr2 = altPlayer.stats[0][index]
            carr2 = altPlayer.stats[1][index]

            if index > 0 and curr1 and curr2 and float(curr1) and float(curr2):
                curr1 = curr1.replace("-", "0")
                carr1 = carr1.replace("-", "0")
                curr2 = curr2.replace("-", "0")
                carr2 = carr2.replace("-", "0")
                if float(curr1) > float(curr2):
                    curr1 = "\033[1;31m{}\033[0m".format(str(curr1))
                elif float(curr2) > float(curr1):
                    curr2 = "\033[1;31m{}\033[0m".format(str(curr2))
                if float(carr1) > float(carr2):
                    carr1 = "\033[1;31m{}\033[0m".format(str(carr1))
                elif float(carr2) > float(carr1):
                    carr2 = "\033[1;31m{}\033[0m".format(str(carr2))
            temp.append(self.stat_headers[index])
            temp.append(curr1)
            temp.append(carr1)
            temp.append(curr2)
            temp.append(carr2)
            stats.append(temp)
        print("\n\033[1m\033[96m\033[4mStats Comparison:\033[0m")
        print(tabulate(stats, headers=headers_comparison, tablefmt='fancy_grid'))

    def to_file(self):
        date = datetime.datetime.now()
        str_date = str(date.year) + "-" + str(date.month)
        filename = "saved/players/cache/{}/{}.pkl".format(
            str_date, self.name.replace(" ", "_"))

        output = open(filename, 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(vars(self), output)

        output.close()

    def from_file(self):
        date = datetime.datetime.now()
        str_date = str(date.year) + "-" + str(date.month)
        filename = "saved/players/cache/{}/{}.pkl".format(
            str_date, self.name.replace(" ", "_"))
        try:
            pkl_file = open(filename, 'rb')
            data = pickle.load(pkl_file)
            for key in data:
                setattr(self, key, data[key])
            pkl_file.close()
            return True
        except:
            return False

    def to_json(self):
        date = datetime.datetime.now()
        str_date = str(date.year) + "-" + str(date.month)
        filename = "saved/players/json/{}/{}.json".format(
            str_date, self.name.replace(" ", "_"))
        obj = {}
        obj['Weight'] = self.weight

        obj['Age'] = self.age

        obj['Current_Year'] = self.current_year

        obj['Current_Stats'] = self.current_stats

        obj['Profile_Pic'] = self.profile_link

        obj['Transactions'] = {}
        for index, transaction in enumerate(self.transactions):
            obj['Transactions'][index] = transaction 

        obj['Team'] = self.team

        obj['Team_Colors'] = self.team_colors

        obj['Stats'] = {}
        for stat_row in self.stats:
            if stat_row[0]:
                obj['Stats'][stat_row[0]] = {}
                for index, item in enumerate(stat_row):
                    obj['Stats'][stat_row[0]][self.stat_headers[index]] = stat_row[index]

        obj['Shoots'] = self.shoots

        obj['Salaries'] = {}
        for salary in self.salaries:
            obj['Salaries'][salary[0]] = {}
            obj['Salaries'][salary[0]]['Team'] = salary[1]
            obj['Salaries'][salary[0]]['League'] = salary[2]
            obj['Salaries'][salary[0]]['Salary'] = salary[3]

        year_rank = self.recruiting_rank.split()
        obj['Recruiting_Rank'] = {}
        if year_rank:
            obj['Recruiting_Rank'][year_rank[0]] = year_rank[1]

        obj['Positions'] = {}
        for index, pos in enumerate(self.position):
            obj['Positions'][index] = pos

        obj['NBA_Debut'] = self.nba_debut
        obj['Name'] = self.name
        obj['High_School'] = self.high_school
        obj['Height'] = self.height
        obj['Experience'] = self.experience
        obj['Draft'] = self.draft
        obj['Contract'] = {}

        obj['Percentiles'] = self.percentiles

        for index, contract in enumerate(self.contract):
            if contract:
                obj['Contract'][index] = {}
                for jndex, item in enumerate(contract):
                    obj['Contract'][index][self.contract_headers[jndex]] = item

        obj['College'] = self.college
        obj['Born'] = self.born
        obj['Awards'] = {}
        for index, award in enumerate(self.awards):
            obj['Awards'][index] = award
        with open(filename, 'w') as outfile:
            json.dump(obj, outfile)        

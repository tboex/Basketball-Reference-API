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
        self.height = ""
        self.weight = ""
        self.position = []
        self.shoots = ""
        self.team = ""
        self.born = ""
        self.college = ""
        self.high_school = ""
        self.recruiting_rank = ""
        self.draft = ""
        self.nba_debut = ""
        self.experience = ""
        self.awards = []

        self.stat_headers = []
        self.stats = []

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

    def fetch_url(self, full):
        player_name = self.name.split()
        is_file = self.from_file()
        if is_file == False:
            print("No local data found, downloading now...")
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

                URL = URL + '/players' + last_name_index.lower() + '/' + ''.join(last_name).lower() + \
                    ''.join(first_name).lower() + '01.html'
            r = requests.get(URL)

            self.clean_player_url(r.text, full)
        else:
            print("\n - Local data found - ")

    def clean_player_url(self, html, full):
        soup = BeautifulSoup(html, 'html.parser')
        basic_info = soup.find(
            'div', attrs={'itemtype': 'https://schema.org/Person'})
        bling = soup.find(
            'ul', attrs={"id": "bling"})
        stats = soup.find(
            'div', attrs={'class': 'stats_pullout'})
        full_stats = soup.find(
            'table', attrs={'id': 'per_game'})
        similarity_carrer = soup.find(
            'div', attrs={'id': 'all_sim_career'})
        transactions = soup.find(
            'div', attrs={'id': 'all_transactions'})
        projections = soup.find(
            'div', attrs={'id': 'all_projection'})
        salaries = soup.find(
            'div', attrs={'id': 'all_all_salaries'})
        contract = soup.find(
            'div', attrs={'id': 'all_contracts_bos'})
        self.get_basic_info(basic_info)

        if bling:
            self.get_bling(bling)
        if full_stats and full:
            self.get_full_stats(full_stats)
        elif stats:
            self.get_summary_stats(stats)
        if similarity_carrer:
            self.get_similarities(similarity_carrer)
        if transactions:
            self.get_transactions(transactions)
        if projections:
            self.get_projections(projections)
        if contract:
            self.get_contract(contract)
        if salaries:
            self.get_salaries(salaries)


    def get_basic_info(self, basic_info):
        info_arr = []
        self.name = basic_info.find(
            'h1', attrs={'itemprop': 'name'}).text.strip()
        for p in basic_info.find_all('p'):
            info_arr.append(p.text.strip().split())
        for index, info in enumerate(info_arr):
            if "Position:" in info:
                position = info[info.index(
                    "Position:") + 1:info.index("Shoots:")-1]
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
        [self.stat_headers.append(item)
         for item in summary.text.strip().split()]
        footer = html.find('tfoot')
        rows = footer.find_all('tr')
        for row in rows:
            temp = []
            season = row.find('th')
            temp.append(season.text.strip())
            for info in row.find_all('td'):
                temp.append(info.text.strip())
            self.stats.append(temp)

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
        print("\033[1m\033[91m{}\n\033[0m".format(self.name))
        print("-" * 20)
        print("\033[1m\033[96m{}:\033[0m{} at {}".format(
            "Build", self.height, self.weight))
        print("\033[1m\033[96m{}\033[0m {}".format("Positions:", ', '.join(self.position)))
        print("\033[1m\033[96m{}\033[0m{}".format("Shoots:", self.shoots))
        print("\033[1m\033[96m{}\033[0m{}".format("Team:", self.team))
        print("\033[1m\033[96m{}\033[0m{}".format("Born:", self.born))

        if self.college:
            print("\033[1m\033[96m{}\033[0m{}".format(
                "College: ", self.college))
        if self.high_school:
            print("\033[1m\033[96m{}\033[0m{}".format(
                "High School: ", self.high_school))
        if self.recruiting_rank:
            print("\033[1m\033[96m{}\033[0m{}".format(
                "Recruiting Rank: ", self.recruiting_rank))
        if self.draft:
            print("\033[1m\033[96m{}\033[0m{}".format("Draft: ", self.draft))
        if self.nba_debut:
            print("\033[1m\033[96m{}\033[0m{}".format(
                "NBA Debut: ", self.nba_debut))
        if self.experience:
            print("\033[1m\033[96m{}\033[0m{}".format(
                "Experience: ", self.experience))
        if self.awards:
            print("\n\033[1m\033[96m\033[4mAwards:\033[0m")
            for award in self.awards:
                print("  - {}".format(award))
        if self.transactions:
            print("\n\033[1m\033[96m\033[4mTransactions:\033[0m")
            for transaction in self.transactions:
                print("  - {}".format(transaction))
        if self.projections:
            print("\n\033[1m\033[96m\033[4m{} {}\033[0m".format(
                self.projection_year, "Projections:"))
            print(tabulate(
                [self.projections], headers=self.projections_headers, tablefmt='fancy_grid'))
        if self.contract:
            print("\n\033[1m\033[96m\033[4mContract:\033[0m")
            print(tabulate(self.contract, headers=self.contract_headers, tablefmt='fancy_grid'))
        if self.salaries:
            print("\n\033[1m\033[96m\033[4mSalaries:\033[0m")
            print(tabulate(
                self.salaries, headers=self.salaries_headers, tablefmt='fancy_grid'))
        if self.stats:
            print("\n\033[1m\033[96m\033[4mStats:\033[0m")
            print(tabulate(self.stats, headers=self.stat_headers, tablefmt='fancy_grid'))
        if self.similarities_carrer_headers:
            print("\n\033[1m\033[96m\033[4mSimularities:\033[0m")
            print(tabulate(self.similarities_carrer,
                           headers=self.similarities_carrer_headers, tablefmt='fancy_grid'))

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

        obj['Transactions'] = {}
        for index, transaction in enumerate(self.transactions):
            obj['Transactions'][index] = transaction 

        obj['Team'] = self.team

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
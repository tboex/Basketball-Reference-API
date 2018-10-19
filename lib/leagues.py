import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
import urllib.request 

team_list ={
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

class League:
    def __init__(self):
        self.headers = []

    def fetch_url(self):
        URL = "https://www.basketball-reference.com/leagues/"

        html = ""
        try:
            with urllib.request.urlopen(URL) as response:
                html = response.read().decode('utf-8')#use whatever encoding as per the webpage
        except urllib.request.HTTPError as e:
            if e.code==404:
                print(f"{URL} is not found")
            elif e.code==503:
                print(f'{URL} base webservices are not available')
                ## can add authentication here 
            else:
                print('http error',e)
        self.clean_league_url(html)
    
    def clean_league_url(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        self.get_league_winners(table)
        
    def get_league_winners(self, table):
        rows = table.find_all('tr')
        headers = table.find_all('tr', attrs={'class': 'thead'})
        for header in headers:
           self.headers.append(header.text.strip())
        print(self.headers)
        self.headers = self.headers[2:]
        
        # for row in rows:
        #     print(row.text.strip())
        # print(self.headers)

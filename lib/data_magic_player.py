import lib.players as players
from statistics import mean
import pickle
import datetime
import json
from scipy import stats

class DM_Player:
    def __init__(self):
        self.ages = []
        self.heights = []
        self.weights = []
        self.draft_positions = []

        self.effective_shootings = []
        self.fg_pers = []
        self.three_pers = []
        self.ft_pers = []

        self.ppgs = []
        self.apgs = []
        self.bpgs = []
        self.spgs = []
        self.trpgs = []
        self.minutes_playeds = []
        self.ptss = []
        self.tovs = []

        self.averages = {}

    def set_all(self, Player):
        if Player.current_stats:
            if Player.current_stats['age']:
                self.set_age(Player)
            if Player.height:
                self.set_height(Player)
            if Player.weight:    
                self.set_weight(Player)
            if Player.current_stats['efg_per']:    
                self.set_effective_shooting(Player)
            if Player.current_stats['fg_per']:    
                self.set_fg_per(Player)
            if Player.current_stats['ft_per']:    
                self.set_ft_per(Player)
            if Player.current_stats['3fg_per']:    
                self.set_three_per(Player)
            if Player.current_stats['pts']:    
                self.set_ppg(Player)
            if Player.current_stats['ast']:    
                self.set_apg(Player)
            if Player.current_stats['blk']:    
                self.set_bpg(Player)
            if Player.current_stats['stl']:    
                self.set_spg(Player)
            if Player.current_stats['trb']:    
                self.set_trpg(Player) 
            if Player.current_stats['minutes_played']:
                self.set_minutes_played(Player)
            if Player.current_stats['tov']:
                self.set_tov(Player)
            if Player.current_stats['pts']:
                self.set_pts(Player)

    def get_averages(self):
        if not self.from_file():
            self.averages['age'] = round(mean(self.ages), 2)
            self.averages['heights'] = round(mean(self.heights), 2)
            self.averages['weights'] = round(mean(self.weights), 2)
            self.averages['effective_shootings'] = round(mean(self.effective_shootings), 2)
            self.averages['fg_pers'] = round(mean(self.fg_pers), 2)
            self.averages['ft_pers'] = round(mean(self.ft_pers), 2)
            self.averages['three_pers'] = round(mean(self.three_pers), 2)
            self.averages['ppgs'] = round(mean(self.ppgs), 2)
            self.averages['apgs'] = round(mean(self.apgs), 2)
            self.averages['bpgs'] = round(mean(self.bpgs), 2)
            self.averages['spgs'] = round(mean(self.spgs), 2)
            self.averages['trpgs'] = round(mean(self.trpgs), 2)
            self.averages['minutes_played'] = round(mean(self.minutes_playeds), 2)
            self.averages['tov'] = round(mean(self.tovs), 2)
            self.averages['pts'] = round(mean(self.ptss), 2)
        return self.averages

    def set_height(self, Player):
        height = Player.height.split('-')
        self.heights.append((int(height[0])*12) + int(height[1]))

    def set_weight(self, Player):
        weight = ''.join(x for x in Player.weight if x.isdigit())
        self.weights.append(int(weight))
    
    def set_age(self, Player):
        self.ages.append(int(Player.current_stats['age']))

    def set_draft_position(self):
        #TODO think about this one
        return

    def set_effective_shooting(self, Player):
        self.effective_shootings.append(float(Player.current_stats['efg_per']))

    def set_fg_per(self, Player):
        self.fg_pers.append(float(Player.current_stats['fg_per']))

    def set_ft_per(self, Player):
        self.ft_pers.append(float(Player.current_stats['ft_per']))

    def set_three_per(self, Player):
        self.three_pers.append(float(Player.current_stats['3fg_per']))

    def set_ppg(self, Player):
        self.ppgs.append(float(Player.current_stats['pts']))

    def set_apg(self, Player):
        self.apgs.append(float(Player.current_stats['ast']))

    def set_bpg(self, Player):
        self.bpgs.append(float(Player.current_stats['blk']))

    def set_spg(self, Player):
        self.spgs.append(float(Player.current_stats['stl']))

    def set_trpg(self, Player):
        self.trpgs.append(float(Player.current_stats['trb']))

    def set_minutes_played(self, Player):
        self.minutes_playeds.append(float(Player.current_stats['minutes_played']))

    def set_tov(self, Player):
        self.tovs.append(float(Player.current_stats['tov']))
    
    def set_pts(self, Player):
        self.ptss.append(float(Player.current_stats['pts']))

    def get_percentiles(self, Player):
        percentiles = {}

        height = Player.height.split("-")
        height = (int((int(height[0]) * 12 )) + int(height[1]))
        weight = int(''.join(x for x in Player.weight if x.isdigit()))
        if Player.current_stats['efg_per']:
            efg = float(Player.current_stats['efg_per'])
            percentiles['efg'] = round(stats.percentileofscore(self.effective_shootings, efg), 2)
        if Player.current_stats['ft_per']:
            ft_per = float(Player.current_stats['ft_per'])
            percentiles['ft_per'] = round(stats.percentileofscore(self.ft_pers, ft_per), 2)
        if Player.current_stats['fg_per']:
            fg = float(Player.current_stats['fg_per'])
            percentiles['fg'] = round(stats.percentileofscore(self.fg_pers, fg), 2)
        if Player.current_stats['3fg_per']:
            fg_three = float(Player.current_stats['3fg_per'])
            percentiles['fg_three'] = round(stats.percentileofscore(self.three_pers, fg_three), 2)
        if Player.current_stats['pts']:
            ppg = float(Player.current_stats['pts'])
            percentiles['ppg'] = round(stats.percentileofscore(self.ppgs, ppg), 2)
        if Player.current_stats['ast']:
            apg = float(Player.current_stats['ast'])
            percentiles['apg'] = round(stats.percentileofscore(self.apgs, apg), 2)
        if Player.current_stats['blk']:
            bpg = float(Player.current_stats['blk'])
            percentiles['bpg'] = round(stats.percentileofscore(self.bpgs, bpg), 2)
        if Player.current_stats['stl']:
            spg = float(Player.current_stats['stl'])
            percentiles['spg'] = round(stats.percentileofscore(self.spgs, spg), 2)
        if Player.current_stats['trb']:
            trpg = float(Player.current_stats['trb'])
            percentiles['trpg'] = round(stats.percentileofscore(self.trpgs, trpg), 2)
        if Player.current_stats['minutes_played']:
            minutes_played = float(Player.current_stats['minutes_played'])
            percentiles['minutes_played'] = round(stats.percentileofscore(self.minutes_playeds, minutes_played), 2)
        if Player.current_stats['pts']:
            pts = float(Player.current_stats['pts'])
            percentiles['pts'] = round(stats.percentileofscore(self.ptss, pts), 2)
        if Player.current_stats['tov']:
            tov = float(Player.current_stats['tov'])
            percentiles['tov'] = round(stats.percentileofscore(self.tovs, tov), 2)
        if Player.current_stats['age']:
            age = float(Player.current_stats['age'])
            percentiles['age'] = round(stats.percentileofscore(self.ages, age), 2)

        percentiles['Height'] = round(stats.percentileofscore(self.heights, height), 2)
        percentiles['Weight'] = round(stats.percentileofscore(self.weights, weight), 2)
        return percentiles

    def to_file(self):
        date = datetime.datetime.now()
        str_date = str(date.year) + "-" + str(date.month)
        filename = "saved/averages" + str_date + ".pkl"

        output = open(filename, 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(vars(self), output)

        output.close()
        self.to_json()

    def from_file(self):
        date = datetime.datetime.now()
        str_date = str(date.year) + "-" + str(date.month)
        filename = "saved/averages" + str_date + ".pkl"
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
        filename = "saved/averages" + str_date + ".json"
        with open(filename, 'w') as outfile:
            json.dump(self.averages, outfile)
import lib.players as players
from statistics import mean
import pickle
import datetime
import json

class DM_Player:
    def __init__(self):
        self.heights = []
        self.weights = []
        self.draft_positions = []

        self.effective_shootings = []
        self.fg_pers = []
        self.three_pers = []

        self.ppgs = []
        self.apgs = []
        self.bpgs = []
        self.spgs = []
        self.trpgs = []

        self.averages = {}

    def set_all(self, Player):
        self.set_height(Player)
        self.set_weight(Player)
        self.set_effective_shooting(Player)
        self.set_fg_per(Player)
        self.set_three_per(Player)
        self.set_ppg(Player)
        self.set_apg(Player)
        self.set_bpg(Player)
        self.set_spg(Player)
        self.set_trpg(Player)

    def get_averages(self):
        self.averages['heights'] = round(mean(self.heights), 3)
        self.averages['weights'] = round(mean(self.weights), 3)
        self.averages['effective_shootings'] = round(mean(self.effective_shootings), 3)
        self.averages['fg_pers'] = round(mean(self.fg_pers), 3)
        self.averages['three_pers'] = round(mean(self.three_pers), 3)
        self.averages['ppgs'] = round(mean(self.ppgs), 3)
        self.averages['apgs'] = round(mean(self.apgs), 3)
        self.averages['bpgs'] = round(mean(self.bpgs), 3)
        self.averages['spgs'] = round(mean(self.spgs), 3)
        self.averages['trpgs'] = round(mean(self.trpgs), 3)
        self.to_file()
        self.to_json()
        return self.averages

    def set_height(self, Player):
        height = Player.height.split('-')
        self.heights.append((int(height[0])*12) + int(height[1]))

    def set_weight(self, Player):
        weight = ''.join(x for x in Player.weight if x.isdigit())
        self.weights.append(int(weight))

    def set_draft_position(self):
        #TODO think about this one
        return

    def set_effective_shooting(self, Player):
        self.effective_shootings.append(float(Player.current_stats['efg_per']))

    def set_fg_per(self, Player):
        self.fg_pers.append(float(Player.current_stats['fg_per']))

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

    def to_file(self):
        date = datetime.datetime.now()
        str_date = str(date.year) + "-" + str(date.month)
        filename = "saved/averages" + str_date + ".json"

        output = open(filename, 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(vars(self), output)

        output.close()

    def from_file(self):
        date = datetime.datetime.now()
        str_date = str(date.year) + "-" + str(date.month)
        filename = "saved/averages" + str_date + ".json"
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
        with open(filename, 'wb') as outfile:
            json.dump(self.averages, outfile)
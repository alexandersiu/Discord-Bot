import os

from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv

load_dotenv()
RIOT_TOKEN = os.getenv('RIOT_TOKEN')

class League:
    def __init__(self, username):
        self.lol_watcher = LolWatcher(RIOT_TOKEN)
        self.region = 'na1'

        self.username_lower = username.lower()

        self.user_data = self.lol_watcher.summoner.by_name(self.region, username)

        self.ranked_stats = self.lol_watcher.league.by_summoner(self.region, self.user_data['id'])
        self.patch = self.lol_watcher.data_dragon.versions_for_region(self.region)['n']['champion']
        self.puuid = self.user_data.get('puuid')
        self.my_matches = self.lol_watcher.match.matchlist_by_puuid(self.region, self.puuid)
        self.static_champ_list = self.lol_watcher.data_dragon.champions(self.patch, False, 'en_US')
        
        self.run()
        
    def current_rank(self):
        self.tier_rank = []

        for i in range(len(self.ranked_stats)):
            self.gamemode = self.ranked_stats[i]['queueType']
            if self.gamemode == 'RANKED_SOLO_5x5':
                self.queue = '**Ranked Solo/Duo:** '
                self.tier = self.ranked_stats[i]['tier']
                self.rank = self.ranked_stats[i]['rank']
                self.lp = self.ranked_stats[i]['leaguePoints']
                self.tier_rank.append(self.queue + ' ' + self.tier + ' ' + self.rank+ ' ' + str(self.lp) + ' LP')
            elif self.gamemode == 'RANKED_FLEX_SR':
                self.queue = '**Ranked Flex:** '
                self.tier = self.ranked_stats[i]['tier']
                self.rank = self.ranked_stats[i]['rank']
                self.lp = self.ranked_stats[i]['leaguePoints']
                self.tier_rank.append(self.queue + ' ' + self.tier + ' ' + self.rank + ' ' + str(self.lp) + ' LP')
        
        for i in range(len(self.tier_rank)):
            ranks = ' '.join(self.tier_rank)
        
        return ranks

    def last_ten_matches(self):
        self.matches = []
        self.win_lost = []

        try:
            for i in range(10):
                self.last_match = self.my_matches[i]
                self.matches.append(self.lol_watcher.match.by_id(self.region, self.last_match))
        except IndexError:
            return False

        for i in range(10):
            self.match_detail = self.matches[i]
            for key in self.match_detail['info']['participants']:
                self.key_lower = key['summonerName'].lower()
                if self.key_lower == self.username_lower:
                    if key['win'] == False:
                        self.win_lost.append(':red_square:')
                    else:
                        self.win_lost.append(':green_square:')
                    break
        self.win_streak = ''.join(self.win_lost)
        return self.win_streak
    
    def champ_index(self):
        self.champ_dict = {}
        for key in self.static_champ_list['data']:
            self.row = self.static_champ_list['data'][key]
            self.champ_dict[self.row['key']] = self.row['id']

    def last_match_champ_kda(self):
        for champ in self.matches[0]['info']['participants']:
            if champ['summonerName'].lower() == self.username_lower:
                self.championId = champ['championId']
                self.kills = champ['kills']
                self.deaths = champ['deaths']
                self.assists = champ['assists']
        if str(self.championId) in self.champ_dict:
            self.champ_played = self.champ_dict[str(self.championId)]

        self.kda = str(self.kills) + '/' + str(self.deaths) + '/' + str(self.assists)
        self.latest_match = self.champ_played + ' ' + self.kda
        return self.latest_match

    def champ_img(self):
        self.champ_img_url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + self.champ_played +'_0.jpg'
        return self.champ_img_url
    
    def run(self):
        self.current_rank()
        self.last_ten_matches()
        self.champ_index()
        self.last_match_champ_kda()
        self.champ_img()

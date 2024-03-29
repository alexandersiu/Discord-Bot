import os

from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv

#loads information from .env file
load_dotenv()
RIOT_TOKEN = os.getenv('RIOT_TOKEN')

class League:
    def __init__(self, username):
        self.lol_watcher = LolWatcher(RIOT_TOKEN) #uses class from riotwatcher 
        self.region = 'na1' #you are able to change your region here

        self.username_lower = username.lower()

        self.user_data = self.lol_watcher.summoner.by_name(self.region, username) #provides user data from the username
        self.ranked_stats = self.lol_watcher.league.by_summoner(self.region, self.user_data['id']) #provides ranked stats from the username
        self.patch = self.lol_watcher.data_dragon.versions_for_region(self.region)['n']['champion'] #provides data from the current patch
        self.puuid = self.user_data.get('puuid') #provides the puuid from the user data
        self.my_matches = self.lol_watcher.match.matchlist_by_puuid(self.region, self.puuid) #provides the match data from the puuid
        self.static_champ_list = self.lol_watcher.data_dragon.champions(self.patch, False, 'en_US') #provides the champ list
        
        self.run()
        
    #this function finds the current ranks (Solo/Duo and Flex) of the user
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
            self.ranks = ' '.join(self.tier_rank)
        
        try: 
            return self.ranks
        except:
            return 'No current rank'

    #this function shows a win or a lost in the users last 10 matches
    def last_ten_matches(self):
        self.matches = []
        self.win_lost = []

        try:
            for i in range(10):
                self.last_match = self.my_matches[i]
                self.matches.append(self.lol_watcher.match.by_id(self.region, self.last_match))
        except IndexError:
            return 'No matches played'

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
    
    #this function provides the all of the champions based on their number id
    def champ_index(self):
        self.champ_dict = {}
        for key in self.static_champ_list['data']:
            self.row = self.static_champ_list['data'][key]
            self.champ_dict[self.row['key']] = self.row['id']

    #this function will find the K/D/A from the user's last match
    def last_match_champ_kda(self):
        try:
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
        except:
            return 'No matches played'

    #this functions the champion image from the last champion played by the user
    def champ_img(self):
        try:
            self.champ_img_url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + self.champ_played +'_0.jpg'

            return self.champ_img_url
        except:
            return 'https://cdn.discordapp.com/attachments/765556266667868173/998662901604814950/58e8ff52eb97430e819064cf.png'
    
    #this functions runs all of the functions
    def run(self):
        self.current_rank()
        self.last_ten_matches()
        self.champ_index()
        self.last_match_champ_kda()
        self.champ_img()

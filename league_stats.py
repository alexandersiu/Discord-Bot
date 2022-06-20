#using riotwatcher library to read Riot API
from riotwatcher import LolWatcher, ApiError
from soupsieve import match

import os
from dotenv import load_dotenv

load_dotenv()

RIOT_TOKEN = os.getenv('RIOT_TOKEN')

def get_rank(username):

    watcher = LolWatcher(RIOT_TOKEN)
    region = 'na1' 

    user_lower = username.lower()
    try:
        user_data = watcher.summoner.by_name(region, user_lower) 

    except ApiError as err:
        if err.response.status_code == 404:
            return False
            
    ranked_stats = watcher.league.by_summoner(region, user_data['id']) 
    patch = watcher.data_dragon.versions_for_region(region)['n']['champion']

    tier_rank = []
    for i in range(len(ranked_stats)):
        gamemode = ranked_stats[i]['queueType']
        if gamemode == 'RANKED_SOLO_5x5':
            queue = '**Ranked Solo/Duo:** '
            tier = ranked_stats[i]['tier']
            rank = ranked_stats[i]['rank']
            lp = ranked_stats[i]['leaguePoints']
            tier_rank.append(queue + ' ' + tier + ' ' + rank+ ' ' + str(lp) + ' LP')
        elif gamemode == 'RANKED_FLEX_SR':
            queue = '**Ranked Flex:** '
            tier = ranked_stats[i]['tier']
            rank = ranked_stats[i]['rank']
            lp = ranked_stats[i]['leaguePoints']
            tier_rank.append(queue + ' ' + tier + ' ' + rank + ' ' + str(lp) + ' LP')
    
    for i in range(len(tier_rank)):
        ranks = ' '.join(tier_rank)

    puuid = user_data.get('puuid')
    my_matches = watcher.match.matchlist_by_puuid(region, puuid)

    matches = []

    try: 
        for i in range(10):
            last_match = my_matches[i]
            matches.append(watcher.match.by_id(region, last_match))
    except IndexError:
        return False

    win_lost = []

    for i in range(10):
        match_detail = matches[i]
        target = ''
        for key in match_detail['info']['participants']:
            key_lower = key['summonerName'].lower()
            if key_lower == user_lower:
                target = key
                if key['win'] == False:
                    win_lost.append('🟥')
                else:
                    win_lost.append('🟩')
                break
    win_streak = ''.join(win_lost)

    static_champ_list = watcher.data_dragon.champions(patch, False, 'en_US')
    champ_dict = {}

    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']
    for champ in matches[0]['info']['participants']:
        if champ['summonerName'].lower() == user_lower:
            championId = champ['championId']
            kills = champ['kills']
            deaths = champ['deaths']
            assists = champ['assists']
    if str(championId) in champ_dict:
        champ_played = champ_dict[str(championId)]
    
    kda = str(kills) + '/' + str(deaths) + '/' + str(assists)

    latest_match = champ_played + ' ' + kda

    champ_img_url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + champ_played +'_0.jpg'

    output = [username, ranks, win_streak, latest_match, champ_img_url]
    return output
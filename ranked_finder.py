#using riotwatcher library to read Riot API
from riotwatcher import LolWatcher, ApiError
from soupsieve import match

#this function receives a riot username (not case-sensitize) and outputs the ranked solo/duo rank and last 10 wins/lost
def get_rank(username):
    api_key = 'RGAPI-ca0efcb4-b8d5-4a86-9408-c81d86788066' #api developer key given by Riot
    watcher = LolWatcher(api_key) #uses the API key to access data from Riot
    region = 'na1' 

    user_lower = username.lower()
    user_data = watcher.summoner.by_name(region, user_lower) #gets basic data about the user

    ranked_stats = watcher.league.by_summoner(region, user_data['id']) #gets the ranked stats of the user 

    #gets the ranked solo/duo tier and rank of the user
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
    my_matches = watcher.match.matchlist_by_puuid(region, puuid) #receives the last 20 match IDs of the user

    matches = []

    #pre-loads the match information about each of the 10 matches and appends them into a list (we do this to decrease time)
    for i in range(10):
        last_match = my_matches[i]
        matches.append(watcher.match.by_id(region, last_match))

    win_lost = []

    #uses the pre-loaded data about the matches and prints a red or green square based on of the user won or lost the game for the last 10 games
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
    output = [username, ranks, win_streak]
    return output

from bs4 import BeautifulSoup
import requests

def val_stats(username):
    user = username[:username.rfind("#")]
    tag = username[username.rfind("#"):][1:]
    url = 'https://tracker.gg/valorant/profile/riot/' + user + '%23' + tag + '/overview'
    
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    current_rank = soup.find_all('div', {'class': 'stat'})
    for stat in current_rank:
        stat_type = stat.find('span', {'class': 'stat__label'})
        if stat_type.text == 'Rating':
            rank = stat.find('span', {'class': 'stat__value'})
            break

    try: rank
    except UnboundLocalError: rank = None

    if rank is None:
        return False
    else:
        rank_output = rank.text
    
    def stats(type_of_stat):
        all_stats = soup.find_all('div', {'class': 'numbers'})
        for statter in all_stats:
            stat_type = statter.find('span', {'class': 'name'})
            if stat_type.text == type_of_stat:
                stat_val = statter.find('span', {'class': 'value'})
                break
        stat_val_output = stat_val.text
        return stat_val_output

    kd = stats('K/D Ratio')
    hs = stats('Headshot%')
    wr = stats('Win %')

    #agent_list = ['Brimstone', 'Cypher', 'Jett', 'Omen', 'Phoenix', 'Raze', 'Sage', 'Sova', 'Viper', 'Skye', 'Astra', 'Chamber', 'KAY/O', 'Neon', 'Reyna', 'Breach', 'Yoru', 'Killjoy']

    output = [username, rank_output, kd, hs, wr]
    return output
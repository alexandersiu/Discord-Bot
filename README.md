# Discord-Bot

> This Discord bot allows for users to type in discord chat to see their League of Legends or their Valorant stats. 

The League of Legends data is supported by the Riot API, using their updated datasets to display the stats the bot outputs. This is seen in the ranked_finder.py file.

The Valorant data is obtained through webscrapping, using the BeautifulSoup library. The website the data was scrapped from is Valorant Tracker. This is seen in the valorant_stats.py file.

- `$league <username>` : outputs the users solo/duo rank, ranked flex rank, latest game champion and KDA, and wins/losts of their last 10 games

![image](https://user-images.githubusercontent.com/105384095/174151656-4be7faa3-5693-4445-9eb0-baf3eb4015dc.png)
- `$val <username#tag>` : outputs the users rank, K/D ratio, headshot percentage, and winrate

![image](https://user-images.githubusercontent.com/105384095/173692561-5305259f-9750-4650-8b2f-11f8c809cbb7.png)

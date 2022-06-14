# Discord-Bot

> This Discord bot allows for users to type in discord chat to see their League of Legends or their Valorant stats. 

The League of Legends data is supported by the Riot API, using their updated datasets to display the stats the bot outputs. This is seen in the ranked_finder.py file.

The Valorant data is obtained through webscrapping, using the BeautifulSoup library. The website the data was scrapped from is Valorant Tracker. This is seen in the valorant_stats.py file.

- `$league <username>` : outputs the users solo/duo rank, ranked flex rank, latest game champion and KDA, and wins/losts of their last 10 games

![image](https://user-images.githubusercontent.com/105384095/172506682-b4a20dfd-b776-46e7-83c2-16d40123f2e5.png)
- `$val <username#tag>` : outputs the users rank, K/D ratio, headshot percentage, and winrate
![image](https://user-images.githubusercontent.com/105384095/172506668-4795ca42-fd7c-464f-bcbd-13147694db81.png)

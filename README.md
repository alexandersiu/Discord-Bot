# Discord-Bot

> This Discord bot allows for users to type in discord chat to see their League of Legends statistics, along side with some other fun commands I wanted to add. 

The bot usually takes a few seconds (5-10 seconds) to load. 

For users to implement the bot themselves, you first need to create a `.env` file that contains a your Discord bot token (useful source: https://realpython.com/how-to-make-a-discord-bot-python/). Next, you would have to load your own Riot development API key (https://developer.riotgames.com/docs/portal#_getting_started)._ This key expires every 24 hours, unless you apply for the Personal API key. You would also put this key into the `.env` file.

The League of Legends data is supported by the Riot API, using their updated datasets to display the stats the bot outputs. This is seen in the league.py file.


- `$league <username>` : outputs the users solo/duo rank, ranked flex rank, latest game champion and KDA, and wins/losts of their last 10 games

![image](https://user-images.githubusercontent.com/105384095/174151656-4be7faa3-5693-4445-9eb0-baf3eb4015dc.png)

- `$webtoon` or `$wt`: outputs a random webtoon with its title, cover art, rating, and a summary of the plot

![image](https://user-images.githubusercontent.com/105384095/175999398-eb45e4db-ba57-46c8-a3a5-3ad7bcad093e.png)

- `$anime`: outputs a random anime from the top 1500 animes on MyAnimeList with the title, thumbnail, rating, and summary

![image](https://user-images.githubusercontent.com/105384095/178405845-9934425c-6801-4df6-b2ab-bc57279e7706.png)

- `$search <anime>`: outputs information about the anime you inqueried about

![image](https://user-images.githubusercontent.com/105384095/179610109-c9f27882-3e94-418e-bfa3-c16a02a6d48a.png)

- `$rap`: outputs a random rap video from a YouTube playlist (this command is adaptable with other YouTube playlists)

![image](https://user-images.githubusercontent.com/105384095/178405981-dc6f2757-6f1c-42c4-81d9-b0c7c7097bc9.png)

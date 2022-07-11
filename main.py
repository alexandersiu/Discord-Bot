import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

from random_playlist_video import RandomPlaylistVideo
from league import League
from webtoon import Webtoon

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Connected.')

@bot.command()
async def korean(ctx):
    video = RandomPlaylistVideo('https://www.youtube.com/playlist?list=PLZOm6GjV8TWLafFrBzmfl4KCmInWGPX5G')
    url = video.run()
    await ctx.send(url)

@bot.command()
async def rap(ctx):
    video = RandomPlaylistVideo('https://www.youtube.com/watch?v=M-w9tg80ZQk&list=PLxA687tYuMWjuNRTGvDuLQZjHaLQv3wYL')
    url = video.run()
    await ctx.send(url)
    
@bot.command()
async def league(ctx, *, arg):
    league_stats = League(arg)
    embed = discord.Embed(title=arg, description= arg + '\'s League of Legends statistics.')
    embed.add_field(name='Rank:', value=league_stats.current_rank(), inline=False)
    embed.add_field(name='Latest Match:', value=league_stats.last_match_champ_kda(), inline=False)
    embed.add_field(name='Recent 10 Games:', value=league_stats.last_ten_matches(), inline=False)
    embed.set_thumbnail(url=league_stats.champ_img())
    await ctx.send(embed=embed)

@bot.command(aliases=['wt'])
async def webtoon(ctx):
    webtoon_info = Webtoon()
    embed = discord.Embed(title=webtoon_info.webtoon_title(), url=webtoon_info.webtoon_url())
    embed.set_thumbnail(url=webtoon_info.webtoon_img())
    embed.add_field(name='Rating:', value=webtoon_info.webtoon_rating() + ' / 5')
    embed.add_field(name='Summary:', value=webtoon_info.webtoon_summary())
    await ctx.send(embed=embed)

bot.run(TOKEN)
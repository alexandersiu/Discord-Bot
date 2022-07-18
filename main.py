import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

from random_playlist_video import RandomPlaylistVideo
from league import League
from webtoon import Webtoon
from anime import RandomAnime, AnimeByName

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Connected.')

#@bot.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.CommandNotFound):
#        await ctx.send("Unknown command")

@bot.command()
async def korean(ctx):
    video = RandomPlaylistVideo('https://www.youtube.com/playlist?list=PLZOm6GjV8TWLafFrBzmfl4KCmInWGPX5G')
    url = video.run()
    await ctx.send(url)

@bot.command()
async def rap(ctx):
    video = RandomPlaylistVideo('https://www.youtube.com/watch?v=UceaB4D0jpo&list=PLplXQ2cg9B_pdAfL7DA4N2n-SuXm2G0RA')
    url = video.run()
    await ctx.send(url)
    
@bot.command()
async def league(ctx, *, arg):
    try:
        league_stats = League(arg)
        embed = discord.Embed(title=arg, description= arg + '\'s League of Legends statistics.')
        embed.add_field(name='Rank:', value=league_stats.current_rank(), inline=False)
        embed.add_field(name='Latest Match:', value=league_stats.last_match_champ_kda(), inline=False)
        embed.add_field(name='Recent 10 Games:', value=league_stats.last_ten_matches(), inline=False)
        embed.set_thumbnail(url=league_stats.champ_img())
        await ctx.send(embed=embed)
    except:
        await ctx.send('Not a valid username')


@bot.command(aliases=['wt'])
async def webtoon(ctx):
    webtoon_info = Webtoon()
    embed = discord.Embed(title=webtoon_info.webtoon_title(), url=webtoon_info.webtoon_url())
    embed.set_thumbnail(url=webtoon_info.webtoon_img())
    embed.add_field(name='Rating:', value=webtoon_info.webtoon_rating() + ' / 5')
    embed.add_field(name='Summary:', value=webtoon_info.webtoon_summary())
    await ctx.send(embed=embed)

@bot.command()
async def anime(ctx):
    anime_info = RandomAnime()
    if anime_info.anime_title_eng() == False:
        embed = discord.Embed(title=anime_info.anime_title(), url=anime_info.get_anime())
    else:
        embed = discord.Embed(title=anime_info.anime_title(), url=anime_info.get_anime(), description=anime_info.anime_title_eng())
    embed.set_thumbnail(url=anime_info.anime_thumbnail())
    embed.add_field(name='**MyAnimeList Rank**', value=anime_info.anime_rating())
    embed.add_field(name='**MyAnimeList Popularity**', value=anime_info.anime_popularity())
    embed.add_field(name='**Synopsis**', value=anime_info.anime_synopsis(), inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('🐐')
    await msg.add_reaction('🗑️')

@bot.command()
async def search(ctx, *, arg):
    anime = AnimeByName(arg)
    embed = discord.Embed(title=arg, description='**Japanese Name:** ' + anime.anime_name_jp + '\n**English Name:** ' + anime.anime_name_eng)
    embed.set_thumbnail(url=anime.anime_cover_art)
    embed.add_field(name='**Score:** ', value=anime.anime_score)
    try:
        embed.add_field(name='**Genres:**', value=anime.anime_genres)
    except:
        embed.add_field(name='**Genres:**', value='None')
    embed.add_field(name='**Description:**', value=anime.anime_description, inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)
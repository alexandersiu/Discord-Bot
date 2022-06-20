import discord
import os
import random
from dotenv import load_dotenv

from league_stats import get_rank
from valorant_stats import val_stats
from fancam import get_Fancam

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client() #gets connect to Discord

@client.event #is used to register an event
async def on_ready(): #is called when the bot is ready to start being used
    print('We have logged in as {0.user}'.format(client)) 

nickname_dict = {}
@client.event
async def on_message(message): #event triggers each time a message is received
    if message.author == client.user:
        return
    if message.content.startswith('$league'): #sees if the beginning of the message starts with '$league' to trigger the command
        username = message.content[8:] #concatenates the beginning of the message to only get the username
        league_stats = get_rank(username) 
        if league_stats == False:
            await message.channel.send('User not found')
        else:
            embed = discord.Embed(title=username, description=username + '\'s League of Legends stats.', color = 0x00ff00)
            embed.add_field(name='Rank:', value=league_stats[1], inline=False)
            embed.add_field(name='Latest Match:', value=league_stats[3], inline=False)
            embed.add_field(name='Recent 10 Games:', value=league_stats[2], inline=False)
            embed.set_thumbnail(url=league_stats[4])
            await message.channel.send(embed=embed)
    if message.content.startswith('$val'):
        username = message.content[5:]
        valorant_stats = val_stats(username)
        if valorant_stats == False:
            await message.channel.send('User not found')
        else:
            embed = discord.Embed(title=username, description=username + '\'s Valorant stats.', color = 0x00ff00)
            embed.add_field(name='Rank', value=valorant_stats[1], inline=False)
            embed.add_field(name='K/D Ratio', value=valorant_stats[2], inline=False)
            embed.add_field(name='Headshot%', value=valorant_stats[3], inline=False)
            embed.add_field(name='Win %', value=valorant_stats[4], inline=False)
            #embed.add_field(name='Most Played Agent', value=valorant_stats[5], inline=False)
            embed.set_thumbnail(url='https://preview.redd.it/tch01tr0edn51.png?width=1700&format=png&auto=webp&s=f478ab468ffd393d83d690b6b0797b682325d8ed')
            await message.channel.send(embed=embed)
    if message.content.startswith('$love'):
        string = message.content[6:]
        target1 = string.split(', ')[0]
        target2 = string.split(', ')[1]
        loveAmount = random.randint(0, 100)
        embed = discord.Embed(title = 'Lover Meter', color = 0x00ff00)
        embed.add_field(name = target1 + ' loves ' + target2, value = str(loveAmount) + '%', inline = False)
        embed.set_thumbnail(url='https://thumbs.dreamstime.com/z/love-meter-heart-indicator-day-full-test-valentine-background-card-progress-171670379.jpg')
        await message.channel.send(embed=embed)
    if message.content.startswith('$fancam'):
        idol = message.content[8:]
        video_Info = get_Fancam(idol)
        await message.channel.send(video_Info[0])



client.run(TOKEN)


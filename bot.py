import discord
from discord.ext import commands
import configparser
config = configparser.ConfigParser()
config.read("./docs/.config.ini")
token = config['auth']['discord_token']
client = commands.Bot(command_prefix='-')

@client.event
async def on_ready():
    print("Bot is ready, my dude.")

client.run(token)


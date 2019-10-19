import discord
from discord.ext import commands
import configparser
import os


config = configparser.ConfigParser()
config.read("./docs/.config.ini")
token = config['auth']['discord_token']
client = commands.Bot(command_prefix='-')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


try:
    for filename in os.listdir('./cogs'):

        if filename.endswith('.py'):

            client.load_extension(f'cogs.{filename[:-3]}')

    client.run(token)

except Exception as e:
    print(e)


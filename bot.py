import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
import configparser
import os


config = configparser.ConfigParser()
config.read("./docs/.config.ini")
token = config['auth']['discord_token']

Client = discord.Client()
client = commands.Bot(command_prefix='-')


#events
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there!'))
    print('Bot is online.')

#commands
@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")



@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send(f"Can't leave channel if not connect to a channel.")

@client.command(pass_context=True)
async def play(ctx, url: str):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete file song file, but it's current in use")
        await ctx.send("Error: Music is playing")
        return
    await ctx.send("Attempting to play youtube songerino now")
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading song now")
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f'Renamed file: {file}\n')
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f'{name} has finsished playing'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.30

    nname = name.rsplit("-", 2)
    await ctx.send(f'Playing: {nname}')
    print("Playing")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

client.command()
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


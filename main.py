import discord
import os
import requests
import json
from apikeys import TOKEN
from discord import FFmpegPCMAudio
#from replit import db
from discord.ext import commands
#from discord.utils import get
import youtube_dl
#from discord.ext.commands import Bot
#from keep_alive import keep_alive

#intents = discord.Intents.default()
#intents.members = True
activity = discord.Activity(type=discord.ActivityType.watching, name="hentai")
client = commands.Bot(command_prefix = '$', activity=activity, status=discord.Status.online)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0] ['a']
  return(quote)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.command()
async def inspire(ctx):
  quote = get_quote()
  await ctx.send(quote)

@client.command()
async def hello(ctx):
  await ctx.send("Hello, I am sexybot")



@client.command(pass_context = True)
async def join(ctx):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    source = FFmpegPCMAudio('piano.wav')
    player = voice.play(source)
  else:
    await ctx.send("you're not in a voice channel, silly sexy!")

@client.command(pass_context = True)
async def play(ctx, url:str):
  if not (ctx.voice_client):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
  else:
    voice = ctx.guild.voice_client
  if (ctx.author.voice):
    #channel = ctx.message.author.voice.channel
    #voice = await channel.connect()
    
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
    for file in os.listdir("./"):
      if file.endswith(".mp3"):
        os.rename(file, "song.mp3")

    source = FFmpegPCMAudio('song.mp3')
    player = voice.play(source)
    await ctx.send("ayoo this a bop ♫")
    #await ctx.send("yo this shit trash :joy:")
  else:
    await ctx.send("you're not in a voice channel, silly sexy!")



@client.command(pass_context = True)
async def leave(ctx):
  if (ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send("i left the voice channel")
  else:
    await ctx.send("i am not in a voice channel, silly sexy!")

@client.command(pass_context = True)
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("theres no audio playing rn")

@client.command(pass_context = True)
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
  else:
    await ctx.send("there is no paused audio rn")
@client.command(pass_context = True)
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
  voice.stop()


#keep_alive()
client.run(TOKEN)
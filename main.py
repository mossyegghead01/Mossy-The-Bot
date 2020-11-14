import discord
from discord.ext import commands, tasks
import keep_alive
import os
import sys
import json
import flask
import logging
import datetime
import asyncio
import subprocess
import time
from tabulate import tabulate
from re import match

subprocess.Popen(['java', '-jar', 'Lavalink.jar'])
time.sleep(60)

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

intents = discord.Intents.all()
client = commands.Bot(command_prefix = get_prefix, intents=intents, case_insensitive=True, help_command=None)

@client.event
async def on_ready():
    guilds = list(client.guilds)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'!help in {str(len(guilds))} servers'))
    print('Bot Started')
    print(f'Running on python version {sys.version.split()[0]}')
    print(f'Running on discord.py version {discord.__version__}')
    print(f'Flask version {flask.__version__}')
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'loading {filename}')
    c = [["Name", "Description", "Usage", "aliases"]]
    for z in client.cogs:
      m = client.get_cog(z)
      for i in m.get_commands():
        if i.hidden == False and i.name != "help":
          f = [i.name, i.description, f"!{i.name} {i.usage}", i.aliases]
          c.append(f)
    m = tabulate(c, tablefmt='html')
    keep_alive.passcmd(m)
    print(m)

@client.event
async def on_command_error(ctx, error):
    await ctx.send(error)
    logging.error(error)
    raise error

@client.event
async def on_member_join(member):
  if member.guild.id == 748974601786097675:
    channel = client.get_channel(748975860530544733)#<-- requires channel ID to send welcome message
    await channel.send(f'Hi there {member.mention}! Hope you are enjoy your stay here. And remember, be cool!')
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
  if member.guild.id == 748974601786097675:
    channel = client.get_channel(748975860530544733)
    await channel.send(f'Seems like {member.name}#{member.discriminator} does not like this server or lost his spirit. Anyway we hope to see him again.')
    print(f'{member} has left the server.')

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'


    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
        
@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))


    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

logging.basicConfig(filename='log.txt', filemode='a', format='%(asctime)s %(msecs)d- %(process)d -%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S %p', level=logging.INFO)

@client.command(hidden=True)
@commands.is_owner()
async def clearlog(ctx):
  """ Clear the bot log. Owner only. Hidden command"""
  channel = client.get_channel(761904455935328296)
  tn = datetime.datetime.utcnow()
  await channel.send(f'{tn.strftime("%c")} log, timezone: UTC', file=discord.File('log.txt'))
  with open("log.txt","r+") as f:
    f.truncate()
  with open("./logs/spring.log","r+") as r:
    r.truncate()

@tasks.loop(hours=24)
async def clog():
  channel = client.get_channel(761904455935328296)
  tn = datetime.datetime.utcnow()
  await channel.send(f'{tn.strftime("%c")} log, timezone: UTC', file=discord.File('log.txt'))
  with open("log.txt","r+") as f:
    f.truncate()
  with open("./logs/spring.log","r+") as r:
    r.truncate()

@clog.before_loop
async def before_clog():
  hour = 00
  minute = 00
  await client.wait_until_ready()
  now = datetime.datetime.now()
  future = datetime.datetime(now.year, now.month, now.day, hour, minute)
  if now.hour >= hour and now.minute > minute:
    future += datetime.timedelta(days=1)
  await asyncio.sleep((future-now).seconds)

@client.event
async def on_message(msg):
  try:
    if match("<@!738423643314323558>", msg.content) is not None:
      with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
      pre = prefixes[str(msg.guild.id)] 
      await msg.channel.send(f"My prefix for this server is ``{pre}``")
  except:
    pass
  await client.process_commands(msg)

clog.start()
keep_alive.keep_alive()
client.run(os.getenv("BOT_TOKEN"))

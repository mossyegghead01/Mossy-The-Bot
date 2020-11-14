import discord
from discord.ext import commands

client = commands

class owneronly(commands.Cog):
  def __init__(self, client):
    self.client = client

  @client.Cog.listener()
  async def on_ready(self):
    print("onwer only Cog Ready")

  @client.command(hidden=True)
  @commands.is_owner()
  async def resetstatus(self, ctx):
    """ Reset the bot status, owner only, hidden """
    if ctx.author.id == 645405908309901322 or ctx.author.id == 689802280102527124:
      guilds = list(client.guilds)
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'!help in {str(len(guilds))} servers'))
    else:
      await ctx.send("I won't change to that, you not my creator or the choosed.")

  @client.command(hidden=True)
  @commands.is_owner()
  async def status(self, ctx, *, name):
    """ change the bot status, owner only, hidden """
    if ctx.author.id == 645405908309901322 or ctx.author.id == 689802280102527124:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
    else:
      await ctx.send("I won't change to that, you not my creator or the choosed.")

  @commands.command(hidden=True)
  @commands.is_owner()
  async def load(self, ctx, *, module : str):
    """Loads a module."""
    try:
        self.client.load_extension(f'cogs.{module}')
    except Exception as e:
        await ctx.send('\N{PISTOL}')
        await ctx.send('{}: {}'.format(type(e).__name__, e))
    else:
        await ctx.send('\N{OK HAND SIGN}')

  @commands.command(hidden=True)
  @commands.is_owner()
  async def unload(self, ctx, *, module : str):
    """Unloads a module."""
    try:
        self.client.unload_extension(f'cogs.{module}')
    except Exception as e:
        await ctx.send('\N{PISTOL}')
        await ctx.send('{}: {}'.format(type(e).__name__, e))
    else:
        await ctx.send('\N{OK HAND SIGN}')

  @commands.command(hidden=True)
  @commands.is_owner()
  async def reload(self,ctx, *, module : str):
    """Reloads a module."""
    try:
        self.client.unload_extension(f'cogs.{module}')
        self.client.load_extension(f'cogs.{module}')
    except Exception as e:
        await ctx.send('\N{PISTOL}')
        await ctx.send('{}: {}'.format(type(e).__name__, e))
    else:
        await ctx.send('\N{OK HAND SIGN}')

def setup(client):
    client.add_cog(owneronly(client))
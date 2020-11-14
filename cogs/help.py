import discord
from discord.ext import commands
import json

class help(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def help(self, ctx):
    with open("prefixes.json", "r") as f:
      prefixes = json.load(f)
    pre = prefixes[str(ctx.guild.id)]
    em = discord.Embed(title="Bot help", description=f"My prefix for {ctx.guild.name} is ``{pre}``\n[Commands list](https://Mossy-The-Bot-Rewrite.mossyegghead01.repl.co/commands)\n[Support Server](http://discord.gg/McE8rU9)\n[Add me to your server](https://discord.com/api/oauth2/authorize?client_id=738423643314323558&permissions=3402838&scope=bot)", color = discord.Color.red())
    await ctx.author.send(embed=em)
    await ctx.send(f"{ctx.author.mention} Check your DM.")

def setup(client):
  client.add_cog(help(client))
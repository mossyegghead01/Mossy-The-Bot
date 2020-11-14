import discord
from discord.ext import commands
import time
import typing
import json
import requests
import shutil

client = commands

class moderation(commands.Cog):
  def __init__(self, client):
    self.client = client

  @client.Cog.listener()
  async def on_ready(self):
    print("Mod Cog Ready")

  @client.command(description="Ban a user", usage="{user} (resaon)") #<-- ban command
  @commands.guild_only()
  @commands.has_guild_permissions(ban_members=True)
  async def ban(self, ctx, member : discord.Member, *, reason=None):
    """ Ban a user """
    channel = await member.create_dm()
    guild = ctx.guild.name
    await channel.send(f'You are banned from {guild} because: {reason}')
    time.sleep(1)
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

  @client.command(description="Kick a user", usage="{user} (resaon)")
  @commands.guild_only()
  @commands.has_guild_permissions(kick_members=True)
  async def kick(self, ctx, member : discord.Member, *, reason=None):
    """ Kick a user """
    channel = await member.create_dm()
    guild = ctx.guild.name
    await channel.send(f'You are kicked from {guild} because: {reason}')
    time.sleep(1)
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

  @commands.command(description="Unban's a user from the server", usage="{user id|username#user discriminator}")
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *, member):
    try:
      banned_users = await ctx.guild.bans()
      member_name, member_discriminator = member.split('#')

      for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'unbanned {user.name}#{user.discriminator}')
            return
    except:
      member = await self.bot.fetch_user(int(member))
      await ctx.guild.unban(member)
      await ctx.send(f"Unbanned {member.name}")

  @client.command(aliases=['clear'], description="Mass delete messages", usage="{limit/amount}")
  @commands.has_guild_permissions(manage_messages=True)
  async def purge(self, ctx, amount = 1):
    """ Mass delete messages """
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    msg = await ctx.send(f"Purged {amount} message(s)")
    time.sleep(2)
    await msg.delete()

  @client.command(description="Hate the bot? run this command to make the bot leave easly", usage="")
  @commands.guild_only()
  @commands.has_guild_permissions(kick_members=True)
  async def kickbot(self, ctx):
    """ Hate the bot? run this command to make the bot leave easly """
    await ctx.send("leaving...")
    time.sleep(1)
    await ctx.guild.leave()

  @client.command(aliases=['slow'], description="Set the channel message cooldown", usage="(channel) {delay}")
  @commands.guild_only()
  @commands.has_guild_permissions(manage_channels=True)
  async def slowmode(self, ctx, channel: typing.Optional[discord.TextChannel]=None, seconds: int = 0):
    """ Set the channel message cooldown. """
    if channel is None:
      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
    else:
      perm = ctx.author.permissions_in(channel)
      if perm.manage_channels == True:
        await channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode in {channel.mention} to {seconds}")
      else:
        await ctx.send("You cant do this! You don't have manage channel permission in that channel!")

  @client.command(description="Change server bot prefix", usage="{prefix}")
  @commands.guild_only()
  @commands.has_guild_permissions(manage_guild=True)
  async def prefix(self, ctx, prefix):
    """ Change server bot prefix """
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix


    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

def setup(client):
    client.add_cog(moderation(client))
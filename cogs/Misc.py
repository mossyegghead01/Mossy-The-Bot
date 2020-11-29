import discord
from discord.ext import commands
import sys
import typing

class miscellaneous(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description="Make a poll", usage="{poll Question}")
  @commands.has_permissions(manage_messages=True)
  async def poll(self, ctx, *args):
    """ Make a poll """
    mesg = ' '.join(args)
    await ctx.message.delete()
    embed=discord.Embed(title=":ballot_box: Poll", colour=discord.Color.red())
    embed.add_field(name="Question", value=mesg, inline=True)
    message = await ctx.send(embed=embed)
    await message.add_reaction(str('✅'))
    await message.add_reaction(str('❌'))

  @commands.command(description="Repeats after you", usage="{Message}")
  @commands.has_permissions(manage_messages=True)
  async def say(self, ctx, *, msg):
    """ Make the bot say something """
    await ctx.message.delete()
    await ctx.send("{}" .format(msg))

  @commands.command(description="Repeats after you but in an embed", usage="{Message}")
  @commands.has_permissions(manage_messages=True)
  async def embed(self, ctx, *, msg):
    """ Make the bot say something but in embed """
    embed = discord.Embed(description=msg, color=0xff0000)
    await ctx.message.delete()
    await ctx.send(embed=embed)

  @commands.command(pass_context=True, description="Get bot latency", usage="")
  async def ping(self, ctx):
    message = await ctx.send("Pong!")
    await message.edit(content=f"Pong!  ``{round(self.client.latency * 1000)}ms``")

  @commands.command(description="An announcement command, similar to say command but can be used from other channel", usage="(channel) {message}")
  @commands.guild_only()
  @commands.has_permissions(manage_messages=True)
  async def announce(self, ctx, channel:typing.Optional[discord.TextChannel]=None, *, message):
    """ An announcement command, similar to say command but can be used from other channel """
    if channel is None:
      channel = ctx.channel
    perm = ctx.author.permissions_in(channel)
    if perm.send_messages is True:
      embed = discord.Embed(title='Announcement', description=message, color = 0xff0000)
      embed.set_footer(text=f'Announcement by {ctx.author.name}#{ctx.author.discriminator}')
      await channel.send(embed=embed)
    else:
      await ctx.send("You cant send messages there")
    await ctx.message.delete()

  @commands.command(description="Get user profile picture", usage="(user)")
  async def av(self, ctx, user: discord.Member=None):
    """ Get user profile picture """
    user = user or ctx.author
    em = discord.Embed(title=f"{user.name}'s avatar")
    em.set_image(url=user.avatar_url)
    await ctx.send(embed=em)

  @commands.command(description="View bot statistic", usage="")
  async def botinfo(self, ctx):
    """ View bot statistic """
    members = [member for member in self.client.get_all_members() if not member.bot]
    info = await self.client.application_info()
    embed=discord.Embed(title="Bot Information", description="Some Bot Informations", color=0xfd0006)
    embed.set_thumbnail(url=self.client.user.avatar_url)
    embed.add_field(name="Python Version", value=sys.version.split()[0], inline=True)
    embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
    embed.add_field(name="Author", value=info.owner, inline=True)
    embed.add_field(name="Servers", value=len(self.client.guilds), inline=True)
    embed.add_field(name="Users", value=len(members), inline=True)
    await ctx.send(embed=embed)

  @commands.command(description="Get a member info, you can also see your info too", usage="(user)")
  async def userinfo(self, ctx, member:discord.Member=None):
    """ Get a member info, you can also see your info too """
    if member is None:
      member = ctx.author
    if member.status == 'online':
      status = "Online"
    elif member.status == 'dnd' or 'do_not_disturb':
      status = "Do Not Disturb"
    elif member.status == 'idle':
      status = "Idle"
    elif member.status == 'invisible':
      status = "Invisible"
    ca = str(member.created_at)
    ja = str(member.joined_at)
    embed=discord.Embed(title="**User Info**")
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="Discriminator", value= member.discriminator, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=status, inline=True)
    embed.add_field(name="Joined At", value=ja.split()[0], inline=True)
    embed.add_field(name="Created At", value=ca.split()[0], inline=True)
    embed.add_field(name="Name in this server", value=member.display_name, inline=True)
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(miscellaneous(client))
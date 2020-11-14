import discord
from discord.ext import commands
import random
import praw

reddit = praw.Reddit(client_id='c_85u5DZ793OFQ',
                     client_secret='iBBJIhWmv6uB3E6R7UNlgC7t8Go',
                     username = "Electronbot123",
                     password = "Electronbot123",
                     user_agent = "Memes")

client = commands

class fun(commands.Cog):
  def __init__(self, client):
    self.client = client

  @client.command(pass_context = True, aliases=["8ball"], description="8Ball game. It will say ethier yes or no", usage="{question}")
  async def ball(self, ctx, *,question):
    """ 8Ball game. It will say ethier yes or no  """
    idk = random.randint(1, 2)
    if idk == 1:
      answer = "yes"
    if idk == 2:
      answer = "no"
    em = discord.Embed(title=question, description=answer)
    await ctx.send(embed=em)

  @client.command(description="Play Rock Paper Scissors with bot. Invalid choice considered as lose by the bot", usage="{Rock|Paper|Scissors}")
  async def rps(self, ctx, choice):
    """ Play Rock Paper Scissors with bot. """
    bot_choice_list = ["Rock", "Paper", "Scissors"]
    bot_choice = random.choice(bot_choice_list)
    user_choice = choice.capitalize()
    if user_choice == 'Rock' or 'Paper' or 'Scissors':
      aftercheck = rpscheck(user_choice, bot_choice)
      if aftercheck == True:
        result = "You Win!"
      elif aftercheck == False:
        result = "You Lose."
      else:
        result = "It's A Tie!"
      em = discord.Embed(title="Rock, Paper, Scissors!")
      em.add_field(name="Your choice:", value=user_choice, inline=True)
      em.add_field(name="Bot choice:", value=bot_choice, inline=True)
      em.add_field(name="Result:", value=result, inline=False)
      await ctx.send(embed=em)
    else:
      await ctx.send("Your choice isn't valid!")
  
  @client.command(aliases=['meme'], description="Get a reddit meme", usage="")
  async def memes(self, ctx):
        subreddit = reddit.subreddit("memes")
        all_subs = []

        hot = subreddit.hot(limit = 50)

        for submission in hot:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        em = discord.Embed(title = name, colour=0xE1C699)

        em.set_image(url = url)

        await ctx.send(embed= em)

def setup(client):
  client.add_cog(fun(client))

def rpscheck(input1, input2):
  if input1 == input2:
    return None
  elif input1 == 'Rock' and input2 == 'Paper':
    return False
  elif input1 == 'Paper' and input2 == 'Rock':
    return True
  elif input1 == 'Scissors' and input2 == 'Rock':
    return False
  elif input1 == 'Rock' and input2 == 'Scissors':
    return True
  elif input1 == 'Paper' and input2 == 'Scissors':
    return False
  elif input1 == 'Scissors' and input2 == 'Paper':
    return True
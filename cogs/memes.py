import discord
from discord.ext import commands
import praw
import random as rd 

reddit = praw.Reddit(client_id = "m0lp571yFdeo9Q", client_secret = "aNHAXU8gzKCnT21vEhV0KSePVAFuwA", user_agent = "memeSpanish")

class Memes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def wrap(self, srd):
      subreddit = reddit.subreddit(srd)

      storage = []

      number = subreddit.top(limit = 50)

      for subs in number:
        storage.append(subs)

      the_chosen_one = rd.choice(storage)    
      return the_chosen_one

    @commands.Cog.listener()
    async def on_ready(self):
        print("Memes Cog has been loaded\n-----")


    @commands.command(aliases = ["meme"])
    async def memes(self, ctx, sub: str = "ESP"):
             
        sr = {"ESP": ["SpanishMeme", "MemesESP", "orslokx", "iLuTV"], "ENG": ["memes", "AnimeFunny"], "FRN": ["FrenchMemes"], "GER": ["ich_iel"]}
        muda = ""
        if sub.upper() in sr.keys():
          muda = rd.choice(sr[sub.upper()])
        else:
          muda = sub
          
        the_chosen_one = self.wrap(muda)  

        headline = the_chosen_one.title
        pic = the_chosen_one.url

        embeddo = discord.Embed(title = headline, color = discord.Color.from_rgb(233, 30, 98))
        embeddo.set_image(url = pic)
        embeddo.set_footer(text = "Meme obtenido de: " + muda)

        await ctx.send(embed = embeddo)


def setup(bot):
    bot.add_cog(Memes(bot))
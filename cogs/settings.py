import discord
from discord.ext import commands

import json

class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Settings Cog has been loaded\n-----")


    @commands.group()
    async def set(self, ctx):
      if ctx.invoked_subcommand == None:
        with open("data_config/servers.json", "r") as f:
          data = json.load(f)
        embed = discord.Embed(title = "**NOemi settings**", color = discord.Color.red())   



def setup(bot):
    bot.add_cog(Settings(bot))
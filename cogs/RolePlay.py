import discord
from discord.ext import commands
import asyncio
import requests
import os
import json
import dbn
import random as rd

reaction_info = {"hug": {"aliases": ["abrazo"], "description": " está abrazando a ", "search": "Anime hug"},
"kiss": {"aliases": ["beso", "mame"],
"description": " está besando a ", "search": "Anime kiss"},
"sip": {"aliases": ["sorbito"], "description":{"solo" : " está tomando juguito ", "non-solo": " está tomando juguito, mientras mira a "}, "search": "Anime sip"},
"slap": {"aliases": ["cachetada"], "description": " Cachetea a ", "search": "Anime slap"},
"sad": {"aliases": ["triste", "llora", "cry"], "description":{"solo" : " está triste ", "non-solo": " está triste por "}, "search": "Anime sad"},
"happy": {"aliases": ["feliz"], "description":{"solo" : " está feliz ", "non-solo": " está feliz por "}, "search": "Anime happy"},
"pat": {"aliases": ["palmadita"], "description": " Da palmaditas a ", "search": "Anime pat"},
"power":{"aliases": ["ulti", "provocar", "taunt"], "description": " Está siendo provocado por ", "search": "anime power"},
"surprise": {"aliases": ["sorpresa", "nani", "shock"], "description":{"solo" : " está en modo nani ", "non-solo": " se quedó wtf por "}, "search": "Anime surprise"},
"fear": {"aliases": ["susto", "miedo"], "description":{"solo" : " tiene miedo", "non-solo": " Teme a "}, "search": "Anime fear"},
"blush": {"aliases": ["sonrojo"], "description":{"solo" : " se sonrojó", "non-solo": " Hizo sonrojar a "}, "search": "Anime blush"},
"smirk": {"aliases": ["risita"], "description":{"solo" : " ", "non-solo": " Se ríe de "}, "search": "Anime smirk"},
"rage": {"aliases": ["angry", "enojo", "emputa"], "description": {"solo": " está enojado", "non-solo": " está enojado con "}, "search" : "Anime rage"},
"jojopose": {"aliases": ["yoyoz"], "description": {"solo": " Está haciendo una Jojopose ", "non-solo": " Está haciendo una Jojopose, mientras mira a  "}, "search" : "jojopose"},
"greet": {"aliases": ["wave", "saludo"], "description": " está saludando a ", "search": "Anime wave"}
}

class RolePlay(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Almost copy paste from the api webpage
    def gif_fetch(self, search, t = 25):
            # set the apikey and limit
      apikey = os.getenv("TENOR")  # test value
      lmt = t

      # our test search
      search_term = search

      # get the top 8 GIFs for the search term
      r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

      if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        data = json.loads(r.content)
        gif = data["results"][rd.randint(0, lmt-1)]["media"][0]["gif"]["url"]
        return gif
      else:
        data = None
        return data  
      

    @commands.Cog.listener()
    async def on_ready(self):
        print("RolePlay Cog has been loaded\n-----")




    @commands.command(aliases = ["casar"])
    async def marry(self, ctx, member: discord.Member):

      data = dbn.check("data_config/users.json")
      a = data[str(ctx.author.id)]["married"] = data[str(ctx.author.id)].get("married", "0")
      if str(member.id) != "831610548210630708":
        b = data[str(member.id)]["married"] = data[str(member.id)].get("married", "0")
      else:
        await ctx.send("No puedo, estoy chikita.")
        return  
      if (a == "0") and (b == "0"):

        await ctx.send(f"{member.mention}, {ctx.author.mention} te está proponiendo matrimonio, (0:No, 1:Sí), tienes 30 segundos para responder.")
        while True:
          try:
            message = await self.bot.wait_for("message", check=lambda m: m.author == member and m.channel == ctx.channel, timeout=30.0)


          except asyncio.TimeoutError:
            await ctx.channel.send("Parece que necesita más tiempo para pensar.")
            break

          else:
            if message.content == "0":
              await ctx.send(f"{ctx.author.mention} ha sido rechazado.")
              break
            elif message.content == "1":
              data[str(member.id)]["married"] = str(ctx.author.id)
              data[str(ctx.author.id)]["married"] = str(member.id)
              dbn.update("data_config/users.json", data)

              await ctx.send(f"{ctx.author.mention} y {member.mention} están casados.")
              break  
      else:
        await ctx.send("Parece que alguien está casado, qué atrevido.")      

    @commands.command(aliases = ["divorce"])
    async def divorciar(self, ctx, member: discord.Member):
      data = dbn.check("data_config/users.json")
      a = data[str(ctx.author.id)]["married"] = data[str(ctx.author.id)].get("married", "0")

      if a == str(member.id):
        data[str(ctx.author.id)]["married"] = "0"
        data[str(member.id)]["married"] = "0"
        dbn.update("data_config/users.json", data)
        await ctx.send("Divorcio exitoso.")

      else:
        await ctx.send("Algo anda mal.")  


    @commands.command(aliases = ["añio", "Hi", "Hello"])
    async def hola(self,ctx):
        greetings = ["Hola.", "Hi!", "Añio", "\'Sup."]
        await ctx.send(rd.choice(greetings))


    @commands.command(aliases = ["say"])
    async def di(self, ctx, *, message):
        message = message or "No dijiste nada ctm."
        await ctx.message.delete()
        await ctx.send(message)
    
    @commands.command(aliases = ["hug"])
    async def abrazo (self, ctx, member: discord.Member = None, *, reason = None):
      gif = self.gif_fetch(reaction_info["hug"]["search"])

      if reason == None:
        embed = discord.Embed(
        description = "**" + ctx.author.display_name + "**" + reaction_info["hug"]["description"] + "**" + member.display_name + "**" + ".",
        colour = discord.Colour.from_rgb(233, 30, 98))
      else:
        embed = discord.Embed(
        description = member.display_name + reaction_info["hug"]["description"] + ctx.author.display_name + "." + '\n' + '\"' + reason + '\"',
        colour = discord.Colour.from_rgb(233, 30, 98))

      embed.set_image(url = gif)
      await ctx.send(embed = embed)

    @commands.command(aliases = reaction_info["kiss"]["aliases"])
    async def kiss(self, ctx, member: discord.Member = None, *, reason = None):
      gif = self.gif_fetch(reaction_info["kiss"]["search"])

      if reason == None:
        embed = discord.Embed(
        description = "**" + ctx.author.display_name + "**" + reaction_info["kiss"]["description"] + "**" + member.display_name + "**" + ".",
        colour = discord.Colour.from_rgb(233, 30, 98))
      else:
        embed = discord.Embed(
        description = ctx.author.display_name + reaction_info["kiss"]["description"] + member.display_name + "." + '\n' + '\"' + reason + '\"',
        colour = discord.Colour.from_rgb(233, 30, 98))

      embed.set_image(url = gif)
      await ctx.send(embed = embed)

    @commands.command(aliases = reaction_info["sip"]["aliases"])
    async def sip (self, ctx, member: discord.Member = None, *, reason = None):
      gif = self.gif_fetch(reaction_info["sip"]["search"], t = 50)
      if member != None:
        if reason == None:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info["sip"]["description"]["non-solo"] + "**" + member.display_name + "**" + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info["sip"]["description"]["non-solo"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))

      else:
        if reason == None:
          embed = discord.Embed(
          description = "**"+ ctx.author.display_name + "**"+ reaction_info["sip"]["description"]["solo"] + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**"  + reaction_info["sip"]["description"]["solo"] + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))


      embed.set_image(url = gif)
      await ctx.send(embed = embed)

    @commands.command(aliases = reaction_info["slap"]["aliases"])
    async def  slap(self, ctx, member: discord.Member = None, *, reason = None):
      gif = self.gif_fetch(reaction_info["slap"]["search"])

      if reason == None:
        embed = discord.Embed(
        description = "**" + ctx.author.display_name + "**" + reaction_info["slap"]["description"] + "**" + member.display_name + "**" + ".",
        colour = discord.Colour.from_rgb(233, 30, 98))
      else:
        embed = discord.Embed(
        description = "**" + ctx.author.display_name + "**" + reaction_info["slap"]["description"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
        colour = discord.Colour.from_rgb(233, 30, 98))

      embed.set_image(url = gif)
      await ctx.send(embed = embed)

    @commands.command(aliases = reaction_info["sad"]["aliases"])
    async def sad(self, ctx, member: discord.Member = None, *, reason = None):
      gif = self.gif_fetch(reaction_info["sad"]["search"], t = 50)
      if member != None:
        if reason == None:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info["sad"]["description"]["non-solo"] + "**" + member.display_name + "**" + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info["sad"]["description"]["non-solo"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))

      else:
        if reason == None:
          embed = discord.Embed(
          description = "**"+ ctx.author.display_name + "**"+ reaction_info["sad"]["description"]["solo"] + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**"  + reaction_info["sad"]["description"]["solo"] + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))


      embed.set_image(url = gif)
      await ctx.send(embed = embed)

    @commands.command(aliases = reaction_info["happy"]["aliases"])
    async def happy(self, ctx, member: discord.Member = None, *, reason = None):
      gif = self.gif_fetch(reaction_info["happy"]["search"], t = 50)
      if member != None:
        if reason == None:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info["happy"]["description"]["non-solo"] + "**" + member.display_name + "**" + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info["happy"]["description"]["non-solo"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))

      else:
        if reason == None:
          embed = discord.Embed(
          description = "**"+ ctx.author.display_name + "**"+ reaction_info["happy"]["description"]["solo"] + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**"  + reaction_info["happy"]["description"]["solo"] + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))


      embed.set_image(url = gif)
      await ctx.send(embed = embed)

    @commands.command(aliases = reaction_info["surprise"]["aliases"])
    async def surprise(self, ctx, member: discord.Member = None, *, reason = None):
      var = "surprise"
      gif = self.gif_fetch(reaction_info[var]["search"], t = 50)
      if member != None:
        if reason == None:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))

      else:
        if reason == None:
          embed = discord.Embed(
          description = "**"+ ctx.author.display_name + "**"+ reaction_info[var]["description"]["solo"] + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**"  + reaction_info[var]["description"]["solo"] + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))


      embed.set_image(url = gif)
      await ctx.send(embed = embed)  
    
    @commands.command(aliases = reaction_info["pat"]["aliases"])
    async def  pat(self, ctx, member: discord.Member = None, *, reason = None):
      var = "pat"
      gif = self.gif_fetch(reaction_info[var]["search"])

      if reason == None:
        embed = discord.Embed(
        description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"] + "**" + member.display_name + "**" + ".",
        colour = discord.Colour.from_rgb(233, 30, 98))
      else:
        embed = discord.Embed(
        description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
        colour = discord.Colour.from_rgb(233, 30, 98))

      embed.set_image(url = gif)
      await ctx.send(embed = embed)

    @commands.command(aliases = reaction_info["power"]["aliases"])
    async def  power(self, ctx, member: discord.Member = None, *, reason = None):
      var = "power"
      gif = self.gif_fetch(reaction_info[var]["search"])

      if reason == None:
        embed = discord.Embed(
        description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"] + "**" + member.display_name + "**" + ".",
        colour = discord.Colour.from_rgb(233, 30, 98))
      else:
        embed = discord.Embed(
        description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
        colour = discord.Colour.from_rgb(233, 30, 98))

      embed.set_image(url = gif)
      await ctx.send(embed = embed)

    @commands.command(aliases = reaction_info["fear"]["aliases"])
    async def fear(self, ctx, member: discord.Member = None, *, reason = None):
      var = "fear"
      gif = self.gif_fetch(reaction_info[var]["search"], t = 50)
      if member != None:
        if reason == None:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))

      else:
        if reason == None:
          embed = discord.Embed(
          description = "**"+ ctx.author.display_name + "**"+ reaction_info[var]["description"]["solo"] + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**"  + reaction_info[var]["description"]["solo"] + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))


      embed.set_image(url = gif)
      await ctx.send(embed = embed)              

    @commands.command(aliases = reaction_info["blush"]["aliases"])
    async def blush(self, ctx, member: discord.Member = None, *, reason = None):
      var = "blush"
      gif = self.gif_fetch(reaction_info[var]["search"], t = 50)
      if member != None:
        if reason == None:
          embed = discord.Embed(
          description = "**" + member.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + ctx.author.display_name + "**" + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + member.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + ctx.author.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))

      else:
        if reason == None:
          embed = discord.Embed(
          description = "**"+ ctx.author.display_name + "**"+ reaction_info[var]["description"]["solo"] + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**"  + reaction_info[var]["description"]["solo"] + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))


      embed.set_image(url = gif)
      await ctx.send(embed = embed)                 

    @commands.command(aliases = reaction_info["smirk"]["aliases"])
    async def smirk(self, ctx, member: discord.Member = None, *, reason = None):
      var = "smirk"
      gif = self.gif_fetch(reaction_info[var]["search"], t = 50)
      if member != None:
        if reason == None:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))

      else:
        if reason == None:
          embed = discord.Embed(
          description = "**"+ ctx.author.display_name + "**"+ reaction_info[var]["description"]["solo"] + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**"  + reaction_info[var]["description"]["solo"] + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))


      embed.set_image(url = gif)
      await ctx.send(embed = embed) 

    @commands.command(aliases = reaction_info["rage"]["aliases"])
    async def rage(self, ctx, member: discord.Member = None, *, reason = None):
      var = "rage"
      gif = self.gif_fetch(reaction_info[var]["search"], t = 50)
      if member != None:
        if reason == None:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))

      else:
        if reason == None:
          embed = discord.Embed(
          description = "**"+ ctx.author.display_name + "**"+ reaction_info[var]["description"]["solo"] + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**"  + reaction_info[var]["description"]["solo"] + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))


      embed.set_image(url = gif)
      await ctx.send(embed = embed)

    @commands.command(aliases = reaction_info["jojopose"]["aliases"])
    async def jojopose(self, ctx, member: discord.Member = None, *, reason = None):
      var = "jojopose"
      gif = self.gif_fetch(reaction_info[var]["search"], t = 50)
      if member != None:
        if reason == None:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**" + reaction_info[var]["description"]["non-solo"] + "**" + member.display_name + "**" + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))

      else:
        if reason == None:
          embed = discord.Embed(
          description = "**"+ ctx.author.display_name + "**"+ reaction_info[var]["description"]["solo"] + ".",
          colour = discord.Colour.from_rgb(233, 30, 98))
        else:
          embed = discord.Embed(
          description = "**" + ctx.author.display_name + "**"  + reaction_info[var]["description"]["solo"] + "." + '\n' + '\"' + reason + '\"',
          colour = discord.Colour.from_rgb(233, 30, 98))


      embed.set_image(url = gif)
      await ctx.send(embed = embed) 

    @commands.command(aliases = reaction_info["greet"]["aliases"])
    async def greet(self, ctx, member: discord.Member = None, *, reason = None):
      gif = self.gif_fetch(reaction_info["greet"]["search"])

      if reason == None:
        embed = discord.Embed(
        description = "**" + ctx.author.display_name + "**" + reaction_info["greet"]["description"] + "**" + member.display_name + "**" + ".",
        colour = discord.Colour.from_rgb(233, 30, 98))
      else:
        embed = discord.Embed(
        description = ctx.author.display_name + reaction_info["greet"]["description"] + member.display_name + "." + '\n' + '\"' + reason + '\"',
        colour = discord.Colour.from_rgb(233, 30, 98))

      embed.set_image(url = gif)
      await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(RolePlay(bot))

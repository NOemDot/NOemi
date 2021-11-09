import discord
from discord.ext import commands
import random
import json
import dbn
import datetime 

class leveling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("leveling Cog has been loaded\n-----")

    def level_system(self, xp):
      xp_to_add = random.randint(10, 20)
      new_lvl = int(((xp+xp_to_add)//42) ** 0.55)
      return xp_to_add, new_lvl
		  

    async def check_xp(self, message):
      data = dbn.check("data_config/servers.json")

      data[str(message.guild.id)]["exp"]["users"][str(message.author.id)] = data[str(message.guild.id)]["exp"]["users"].get(str(message.author.id), {"xp": 0, "level": 0, "cd": 0})

      ch = data[str(message.guild.id)]["exp"]["exp_channel"]      

      user = data[str(message.guild.id)]["exp"]["users"][str(message.author.id)]

      

      dbn.update("data_config/servers.json", data)

      
      if user["cd"] == 0:
        await self.add_xp(message, int(user["xp"]), int(user["level"]),ch)
      elif datetime.datetime.strptime(user["cd"], '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(seconds = 15) <= datetime.datetime.now():
        await self.add_xp(message, int(user["xp"]), int(user["level"]),ch)

    async def add_xp(self, message, xp, level,ch):

      xp_to_add, new_lvl = self.level_system(xp)

      data = dbn.check("data_config/servers.json")



      if ch != "" and new_lvl > level:
        channel = discord.utils.get(message.guild.channels, id = int(ch))
        await channel.send(f"Omedettou {message.author.mention} - ¡has subido a nivel {new_lvl:,}!")

        data[str(message.guild.id)]["exp"]["users"][str(message.author.id)]["level"] = new_lvl
  

      data[str(message.guild.id)]["exp"]["users"][str(message.author.id)]["xp"] += xp_to_add



      data[str(message.guild.id)]["exp"]["users"][str(message.author.id)]["cd"] = str(datetime.datetime.now())

      dbn.update("data_config/servers.json", data)

      

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def levelsys(self, ctx, cond: str = None):
      data = dbn.check("data_config/servers.json")


      if cond != None:
        data[str(ctx.guild.id)]["exp"]["active"] = cond.lower()
        dbn.update("data_config/servers.json", data)  
      if data[str(ctx.guild.id)]["exp"]["active"] != "off":
        await ctx.channel.send("El sistema de niveles ha sido activado o ya está activo")
      else:
        await ctx.channel.send("El sistema de niveles está desactivado")      

      #close

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def setexpch(self, ctx, channel: discord.TextChannel):
      data = dbn.check("data_config/servers.json")

      data[str(ctx.guild.id)]["exp"]["exp_channel"] = channel.id          

      dbn.update("data_config/servers.json", data)     

      await ctx.send("Ahora las actualizaciones de nivel serán publicadas en {}.".format(channel.mention))

      

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def nofarm(self, ctx, channel: discord.TextChannel):
      data = dbn.check("data_config/servers.json")

      if channel.id not in data[str(ctx.guild.id)]["exp"]["noexp"]:
        data[str(ctx.guild.id)]["exp"]["noexp"].append(channel.id)
        up = '👍'
        await ctx.message.add_reaction(up)

      else:
        await ctx.send("Canal ya bloqueado.")     

      dbn.update("data_config/servers.json", data)

      

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def allowexp(self, ctx, channel: discord.TextChannel):
      data = dbn.check("data_config/servers.json")

      if channel.id in data[str(ctx.guild.id)]["exp"]["noexp"]:
        data[str(ctx.guild.id)]["exp"]["noexp"].remove(channel.id)

        await ctx.send("Ahora se puede ganar experiencia en {}".format(channel.mention))
      else:
        await ctx.send("El canal {} no tiene restricciones de experiencia".format(channel.mention))  

      dbn.update("data_config/servers.json", data)
          
      

    @commands.command()
    async def estado(self, ctx, member: discord.Member = None):
      member = member or ctx.author
      data = dbn.check("data_config/servers.json")

      if str(member.id) in data[str(ctx.guild.id)]["exp"]["users"].keys():
        user = data[str(ctx.guild.id)]["exp"]["users"][str(member.id)]
        await ctx.send("{} está en nivel **{}** con **{}** puntos de experiencia".format(member.display_name, user["level"], user["xp"]))
      else:
        await ctx.send("Usuario no registrado.")
               

    @commands.command()
    async def leaderboard(self, ctx):
      data = dbn.check("data_config/servers.json")

      users = data[str(ctx.guild.id)]["exp"]["users"]
      rank = []
      for k in users:
        rank.append((k, users[k]["xp"], users[k]["level"]))
      
      rank.sort(key = lambda k: k[1], reverse= True)  

      out = ""
      j = 1
      for i in rank:
       
        out += "{}. {} nivel: {} xp: {}".format(str(j),discord.utils.get(ctx.guild.members, id = int(i[0])).name, i[2], i[1]) + "\n"
        j+=1

      await ctx.send(out)
        


    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def  giveaway_lvl(self, ctx, channel: discord.TextChannel = None):
      data = dbn.check("data_config/servers.json")

      loto = list(data[str(ctx.guild.id)]["exp"]["users"].keys())
      winner = discord.utils.get(ctx.guild.members, id = int(random.choice(loto)))

      channel = channel or ctx.channel

      await channel.send("¡Felicidades {} eres el ganador del sorteo! :tada: :tada: :tada: ".format(winner.mention))
      
      

    @commands.Cog.listener()
    async def on_message(self, message):
      data = dbn.check("data_config/servers.json")
      cond = data[str(message.guild.id)]["exp"]["active"]
      cond2 = data[str(message.guild.id)]["exp"]["noexp"]
      if not message.author.bot and cond != "off" and message.channel.id not in cond2:
        await self.check_xp(message)
      




def setup(bot):
    bot.add_cog(leveling(bot))
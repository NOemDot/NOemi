import discord
from discord.ext import commands
from datetime import datetime
import json
import dbn

class Automod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Automod Cog has been loaded\n-----")

    @commands.command(aliases = ["bch"])
    @commands.has_permissions(manage_channels = True)
    async def blockchannel(self, ctx, channel: discord.TextChannel):
      data = dbn.check("data_config/servers.json")

      if channel.id not in data[str(ctx.guild.id)]["BlockedChannels"]:
        data[str(ctx.guild.id)]["BlockedChannels"].append(channel.id)
        await ctx.send("Noemi no tiene permiso de jugar en {}.".format(channel.mention))

      else:
        await ctx.send("Canal ya bloqueado.")     

      dbn.update("data_config/servers.json", data)

      


    '''@commands.command()
    @commands.has_permissions(manage_messages = True)
    async def ignore(self, ctx, *,command):

      with open("data_config/servers.json", "r") as f:
        data = json.load(f)

      command = self.bot.get_command(command)
      print(command, type(command))
      if command == None:
        await ctx.send("Comando no válido.")

      elif command == ctx.command:
        await ctx.send("Memento, homo, quia pulvis es, et in pulverem reverteris.")

      if command.name in data[str(ctx.guild.id)]["IgnoredCommands"]:
        await ctx.send("Comando ya bloqueado.")

      else:
         data[str(ctx.guild.id)]["IgnoredCommands"].append(command.name)

      with open("data_config/servers.json", "w") as f:
          json.dump(data, f)

      f.close()


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def allow(self, ctx, *,command):

      with open("data_config/servers.json", "r") as f:
        data = json.load(f)

      command = self.bot.get_command(command)
      
      if command == None:
        await ctx.send("Comando no válido.")

      elif command == ctx.command:
        await ctx.send("Memento, homo, quia pulvis es, et in pulverem reverteris.")

      if command.name in data[str(ctx.guild.id)]["IgnoredCommands"]:
        data[str(ctx.guild.id)]["IgnoredCommands"].remove(command.name)
        

      else:
        await ctx.send("Comando no bloqueado.")

      with open("data_config/servers.json", "w") as f:
          json.dump(data, f)

      f.close()'''        



    @commands.command(aliases = ["ubch"])
    @commands.has_permissions(manage_channels = True)
    async def unblockchannel(self, ctx, channel: discord.TextChannel):
      data = dbn.check("data_config/servers.json")

      if channel.id in data[str(ctx.guild.id)]["BlockedChannels"]:
        data[str(ctx.guild.id)]["BlockedChannels"].remove(channel.id)

        await ctx.send("Ahora puedo volver a ser usada en {}".format(channel.mention))
      else:
        await ctx.send("El canal {} no está bloqueado, no puedo desbloquearlo. \n -Capitán obvio.".format(channel.mention))  

      dbn.update("data_config/servers.json", data)
          
      

      

def setup(bot):
    bot.add_cog(Automod(bot))
import discord
from discord.ext import commands
from unlimited_caffeine_works import caffeine

from insensitive_prefix import mixedCase
import time


import os

import dbn 

from threading import Thread





bot = commands.Bot(case_insensitive=True, command_prefix=mixedCase("noemi " ), intents =discord.Intents.all())

@bot.event
async def on_ready():
  print("I am ready, master")


@bot.event
async def on_guild_join(guild):

  data = dbn.check("data_config/servers.json")

  data[str(guild.id)] = {"BlockedChannels": [], "BannedUsers": [], "BlackList": [], "Settings": {"logs": "", "chat" : 0}, "IgnoredCommands": [], "exp": {"active": "off", "users": {}, "exp_channel": "", "noexp": []  } }

  dbn.update("data_config/servers.json", data)


         


@bot.event
async def on_message(message):
    data = dbn.check("data_config/servers.json")  
    #bot no cuenta
    if message.author.id == bot.user.id:
        return

    if message.channel.id in data[str(message.guild.id)]["BlockedChannels"]:
        return

    dato = dbn.check("data_config/users.json")
    dato[str(message.author.id)] = dato.get(str(message.author.id), {"married": "0", "xp": 0, "lvl": 0, "coins": 0, "items": []})

    dbn.update("data_config/users.json", dato)

    '''for field in message.content.split(" "):
       
        if field in data[str(message.guild.id)]["IgnoredCommands"]:
          return '''

    
    await bot.process_commands(message)


@bot.command()
async def bio(ctx):
  embed = discord.Embed(title = "この NOemi だ!!!", description = "NOemi es un bot multipropósito en español, de código abierto y actualmente en fase de beta abierta desarrollado por " + str(bot.get_user(740933924259102782)) + " y colaboradores en MIYYE server.", color =  discord.Color.red())
  embed.set_image(url ="https://media.discordapp.net/attachments/800511149442727961/838237920715341864/IMG_20210501_211805.jpg?width=366&height=473")
  await ctx.send(embed = embed)



#Working on this event
'''@bot.event 
async def on_message_delete(message):
  with open("data_config/servers.json", "r") as f:
      data = json.load(f)  
  #ignore ourselves
  if message.author.id == bot.user.id:
      return

  elif message.channel.id in data[str(message.guild.id)]["BlockedChannels"]:
      return
  else:      
    channel = message.channel
    await channel.send("Uy ve, {} escribió algo malo.".format(message.author))

  f.close()'''  


#Working on this event
'''
@bot.event
async def on_command_error(self, ctx, error):
    #Ignore these errors
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.CommandOnCooldown):
        
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f' You must wait {int(s)} seconds to use this command!')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
        else:
            await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')

    elif isinstance(error, commands.CheckFailure):
        
        await ctx.send("Not enough power to use this command.")
    raise error
'''


@bot.event 
async def on_member_join(member):
  data = dbn.check("data_config/servers.json")
  channel = bot.get_channel(data[str(member.guild.id)]["Settings"]["logs"])
  
  await channel.send("{} ha llegao.".format(member.name))


@bot.event 
async def on_member_remove(member):
  data = dbn.check("data_config/servers.json")
  channel = bot.get_channel(data[str(member.guild.id)]["Settings"]["logs"])
   
  channel = bot.get_channel(int(channel))
  await channel.send("{} se nos fue.".format(member.name))
  





initial_extensions = ['cogs.announcements',
                      'cogs.RolePlay',
                      'cogs.memes', 
                      'cogs.MIYYE',
                      'cogs.automod',
                      'cogs.leveling'
                      #'cogs.music'
                      ]



# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)



def run_lavalink():
  os.system("java -jar Lavalink.jar")

Thread(target=run_lavalink).start()
time.sleep(60) #wait until lavalink is ready up

caffeine()

bot.run(os.getenv("TOKEN"))
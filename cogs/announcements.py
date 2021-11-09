import discord
import asyncio
import typing
import dbn
from discord.ext import commands

import json

class Com(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Com Cog has been loaded\n-----")


    @commands.command(aliases = ["ce"])
    @commands.has_permissions(manage_messages = True)
    async def customembed(self,ctx,channel: discord.TextChannel,*,arg):
      
        em = json.loads(arg)
        print(em)
        embeddo = discord.Embed.from_dict(em)
        
        channel = channel.id
        
        channel = discord.utils.get(ctx.guild.text_channels, id = channel)
        
        await channel.send(embed = embeddo)

    @commands.command(aliases = ["etxt"])
    @commands.has_permissions(manage_messages = True)
    async def embedtext(self,ctx,channel: discord.TextChannel,*,arg):
      channel = channel.id
      channel = discord.utils.get(ctx.guild.text_channels, id = channel)
      em = discord.Embed(description = arg)
      await channel.send(embed = em)    

    @commands.command(aliases = ["server"])
    async def info(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        babelson = str(ctx.guild.owner)
        sid = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(
            title=name,
            description=description,
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=babelson, inline=True)
        embed.add_field(name="Server ID", value=sid, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Number of Adepti", value=memberCount, inline=True)

        await ctx.send(embed=embed)


    @commands.command(aliases = ["pp"])
    async def profilepicture(self, ctx):
        NOemi_pic = "https://imgur.com/uzRlPg7"
        await ctx.send(NOemi_pic)      

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
      member = member or ctx.author
      await ctx.send(member.avatar_url)

    @commands.command(aliases = ["rrtxt"])
    @commands.has_permissions(manage_messages = True)
    async def reactionRoletxt(self,ctx, mes = None):
      embed = discord.Embed(
            title="Tutorial de reacciones de rol v1",
            description="Estás por crear un reaction role a partir de un mensaje ya creado. Para empezar usa NOemi rrtxt <id del mensaje a convertir en reaction role>",
            color=discord.Color.from_rgb(233, 30, 98)
        )
      embed.add_field(name = "Añadir roles", value = "Para añadir roles usa **NOemi rrtxtadd <id> <emoji> <rol> <canal>** \n **id**: id de un reaction role \n **emoji**: el emoji a usar \n **rol**:mención del rol relacionado al emoji \n **canal**: mención del canal de donde proviene **<id>**", inline = False)
      embed.add_field(name = "Nota", value = "Si usas rrtxtadd en un mensaje creado por mí, añadiré automáticamente los roles y el emoji en el cotenido del mensaje, de lo contrario debe editarlo el autor del mensaje.", inline = False)
      await ctx.send(embed = embed)
      if mes == None:
        await ctx.send("No me has dado la id de un mensaje.")
      else:
        data = dbn.check("data_config/servers.json")
        data[str(ctx.guild.id)]["reactionRole"] = data[str(ctx.guild.id)].get("reactionRole", {})
        if mes not in data[str(ctx.guild.id)]["reactionRole"]:
          data[str(ctx.guild.id)]["reactionRole"][mes] = {}
          dbn.update("data_config/servers.json", data)
          await ctx.send("Listo, una nuevo reaction role ha sido definido, puedes proceder a personalizarlo.")
              
        else:
          await ctx.send("Estás tratando crear un reaction rol ya creado -_-")


    @commands.command(aliases = ["encuesta"])
    @commands.has_permissions(manage_messages = True)
    async def poll(self,ctx, mes = None):
      if mes == None:
        await ctx.send("No me has dado la id de un mensaje.")
      else:
        data = dbn.check("data_config/servers.json")
        data[str(ctx.guild.id)]["poll"] = data[str(ctx.guild.id)].get("poll", {})
        if mes not in data[str(ctx.guild.id)]["poll"]:
          data[str(ctx.guild.id)]["poll"][mes] = {"status": 1, "opciones":{}, "usuarios":[]}
          dbn.update("data_config/servers.json", data)
          await ctx.send("Encuesta creada")
              
        else:
          await ctx.send("Estás tratando crear un reaction rol ya creado -_-")       
          


    @commands.command(aliases = ["rrtxtadd"])
    @commands.has_permissions(manage_messages = True)
    async def reactionRoletxtadd(self,ctx, mes, emoji: typing.Union[discord.Emoji, str], rol: discord.Role, channel: discord.TextChannel):
      if type(emoji) != str:
        emoji = await emoji.guild.fetch_emoji(emoji.id)
        emojid = emoji.id
      else:
        emoji = str(emoji)
        emojid = emoji

      data = dbn.check("data_config/servers.json")

      if mes in data[str(ctx.guild.id)]["reactionRole"]:
        data[str(ctx.guild.id)]["reactionRole"][mes][emojid] = rol.id
        msg = await channel.fetch_message(mes)
        if msg.author.id == self.bot.user.id:
          await msg.edit(content = msg.content+ "\n" + str(emoji)  + rol.mention)
        await msg.add_reaction(emoji)
        dbn.update("data_config/servers.json", data) 
      else:
        await ctx.send("La id del mensaje no corresponde a un reaction role creado.")
        #close

    @commands.command(aliases = ["padd"])
    @commands.has_permissions(manage_messages = True)
    async def polladd(self,ctx, mes, emoji: typing.Union[discord.Emoji, str],  channel: discord.TextChannel):
      if type(emoji) != str:
        emoji = await emoji.guild.fetch_emoji(emoji.id)
        emojid = emoji.id
      else:
        emoji = str(emoji)
        emojid = emoji

      data = dbn.check("data_config/servers.json")

      if mes in data[str(ctx.guild.id)]["poll"]:
        data[str(ctx.guild.id)]["poll"][mes]["opciones"][emojid] = 0
        msg = await channel.fetch_message(mes)
        
        await msg.add_reaction(emoji)
        dbn.update("data_config/servers.json", data) 
      else:
        await ctx.send("La id del mensaje no corresponde a una encuesta creada.")
        #close

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def pollclose(self, ctx, mes):
      data = dbn.check("data_config/servers.json")
      if mes not in data[str(ctx.guild.id)]["poll"]:
        await ctx.send("Intenta cerrar el vacío.")
      else:
        desc = ""
        for e, n in data[str(ctx.guild.id)]["poll"][mes]["opciones"].values():
          e = discord.utils.get(ctx.guild.roles, id = e)
          desc += f"<>"
        
        embed = discord.Embed(title = "**Resultados de la encuesta**")       


    @commands.command(aliases=["reaccionar"])
    @commands.has_permissions(manage_messages = True)
    async def react(self, ctx,emoji: typing.Union[discord.Emoji, str], mes = None):
      if mes == None:
        mes = ctx.reply
      else:
        mes = await ctx.channel.fetch_message(mes)
      await mes.add_reaction(emoji)
      await ctx.message.delete()  
    
      





    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
      data = dbn.check("data_config/servers.json")

      mid = str(payload.message_id)
      guild = str(payload.guild_id)
      g = self.bot.get_guild(payload.guild_id)
      emojid = payload.emoji.id or payload.emoji.name
      emojid = str(emojid)
      roles = g.roles

      if payload.member.id == self.bot.user.id:
        return

      if mid  in data[guild]["reactionRole"]:

        if emojid in data[guild]["reactionRole"][mid]: 

          rol = discord.utils.get(roles, id = data[guild]["reactionRole"][mid][emojid])
          await payload.member.add_roles(rol)

      #close   

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
      data = dbn.check("data_config/servers.json")
      mid = str(payload.message_id)
      guild = str(payload.guild_id)
      g = self.bot.get_guild(payload.guild_id)
      emojid = payload.emoji.id or payload.emoji.name
      emojid = str(emojid)
      roles = g.roles
      member = discord.utils.get(g.members, id=payload.user_id)

      if member.id == self.bot.user.id:
        return

      if mid  in data[guild]["reactionRole"]:

        if emojid in data[guild]["reactionRole"][mid]: 

          rol = discord.utils.get(roles, id = data[guild]["reactionRole"][mid][emojid])
          await member.remove_roles(rol)

      #close

         








      
      
    

def setup(bot):
    bot.add_cog(Com(bot))

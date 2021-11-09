import discord
from discord.ext import commands
from datetime import datetime
import json
import dbn


roles = [800513621347532822 #Mochi
  ,800515131552825345        #Mini-admin
  ,885706435093213244        #Mod    
  ,810580478829658113        #Sugar booster
  ,754527426188410950        #Bro
  ,735958065353981953        #Super pana
  ,797673403611086869        #Pana 
  ,797930361723158599        #Humanito
  ,735935726922760285        #Homúnculo
  ,834486799224406066        #MIYYE bot
  ,797684927427641344        #No iniciado
  ,775399755425382440]       #Condenado

class MIYYE(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("MIYYE Cog has been loaded\n-----")

    @commands.group(aliases = ["house"])
    async def MIYYE(self, ctx):
      if ctx.invoked_subcommand is None:
        name = str(ctx.guild.name)
        description = "Miyye es tu casa así que se bienvenido, siente de chill, de tranquis y en confi para pasar agradables experiencias junto a la familia Miyye."
        
        homun = discord.utils.get(ctx.guild.roles, id = 735935726922760285)
        owner = "<@651912728528551957>"+ ", " + "<@219633606765707267>" + " & " + "Twenny"

        sid = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(len([m for m in ctx.guild.members if homun in m.roles]))
        icon = str(ctx.guild.icon_url)
        fecha = ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
        embed = discord.Embed(
            title=name,
            description=description,
            color=discord.Color.from_rgb(233, 30, 98)
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name=":crown: Owners", value= owner, inline=True)
        embed.add_field(name=":birthday: Creado", value= fecha, inline=True)
        embed.add_field(name=":bust_in_silhouette: Miembros", value=memberCount, inline=True)
        embed.add_field(name=":dvd: Más datos", value="SERVER ID: " + sid + "\n" + "Región: " + region, inline=True)

        embed.set_footer(text = "Information requested by: {}".format(ctx.author.display_name), icon_url = "https://cdn.discordapp.com/attachments/734857096004370535/743895434686365726/picasion.com_c70480901f649925fa18032f20e5c19f.gif")

        await ctx.send(embed = embed)
 

    @MIYYE.command(aliases = ["crew", "pandilla"])
    async def team(self, ctx):


      ocupados = []

      embed = discord.Embed(
            title="MIYYE team",
            description="",
            color=discord.Color.from_rgb(233, 30, 98)
        )

      embed.set_thumbnail(url=ctx.guild.icon_url)

      for i in roles:
        rol = discord.utils.get(ctx.guild.roles, id = i)

        temp = [] #Stores the members of a role if not superior role owned
        for member in ctx.guild.members:
          if (member.id not in ocupados) and rol in member.roles:
            
            ocupados.append(member.id)
            temp.append("• " + member.name)
        temp.sort()
        if len(temp) >= 2:
          embed.add_field(name=rol.name + " " + "**(" + str(len(temp)) +")**" ,value="\n".join(temp) + "\n", inline=False)
        elif len(temp) == 1:
          embed.add_field(name=rol.name,value=temp[0] + "\n", inline=False)
        else:
          embed.add_field(name=rol.name,value="No hay nadie aquí.", inline=False)


      await ctx.send(embed = embed)        

    @MIYYE.command(aliases = ["rewards"])
    async def rangos(self, ctx):
        desc = ["Poderosos seres dueños de estas tierras. Propietarios del servidor.", "Quien conecta lo divino con la humanidad. El administrador, un pilar.","Los duros de estas tierras, cuidan, supervisan y apoyan a los miembros de MIYYE." ,"Aquel ser con capacidades económicas que ha apoyado de forma monetaria al servidor.", "La puerta más alta a aspirar y poder mirar desde lo alto. Tendrás conexión directa con los " + discord.utils.get(ctx.guild.roles, id = 734858971688599672).mention + " y descubrirás secretos. Puedes sugerir un emoji normal y animado extra. ***[lvl 60]***", "Tu perseverancia, tu confianza y tus conexiones te han convertido en un personaje principal y te ha dado la capacidad de poder convocar nuevos miembros a MIYYE. Invitalos desde <#735966650037305394>. Puedes sugerir un emoji animado y uno normal. ***[lvl.40]***", "Ganas el  acceso a la zona profunda de MIYYE ( <#825181309731078194> ). Puedes sugerir un emoji animado. ***[lvl.25]***", "Obtienes el derecho a tener un alias en el servidor y el derecho a la privacidad con la llave del cuarto privado en los canales de voz. ***[lvl.10]***", "Te has comido la manzana y ganado la oportunidad de ser un iniciado en esta nueva aventura. ***[lvl.0]***", "Entes omnipresentes que sirven a MIYYE.", "Eres un extranjero que no todavía no ha aceptado entrar a esta tierra.", "Tus pecados te han llevado a cargar con el peso de tus actos."]
        embed = discord.Embed(
            title="Rangos de MIYYE",
            description="",
            color=discord.Color.from_rgb(233, 30, 98)
        )
        for i in range(len(roles)):
          rol = discord.utils.get(ctx.guild.roles, id = roles[i])
          embed.add_field(name=rol.name ,value= desc[i] + "\n", inline=False)

        await ctx.send(embed = embed)

    @commands.group()
    async def protecc(self, ctx):
      if ctx.invoked_subcommand is None:
        data = dbn.check("data_config/proteccs.json")
        if str(ctx.author.id) in data.keys():
          await ctx.send("{} ha escogido a {}".format(ctx.author.display_name, data[str(ctx.author.id)]))

        else:
            await ctx.send("No hay un protecc seleccionado para este jugador.")

        dbn.update("data_config/proteccs.json", data)

        

    @protecc.command()
    async def set(self, ctx, char):
      with open("data_config/proteccs.json", "r") as f:
        data = json.load(f)

      if str(ctx.author.id) not in data.keys():
        data[ctx.author.id] = char
        up = '👍'
        await ctx.message.add_reaction(up)
      else:
        await ctx.send(" Fate is called as such, for it cannot be changed, nor can it be reversed. It can only but be accepted.")
      
      with open("data_config/proteccs.json", "w") as f:
         data = json.dump(data, f)    
      
      f.close()


    @protecc.command()
    @commands.has_permissions(manage_channels = True)
    async def clear(self, ctx):
      data = dbn.check("data_config/proteccs.json")

      data = {}

      dbn.update("data_config/proteccs.json", data)   

      up = '👍'
      await ctx.message.add_reaction(up)

      

    @protecc.command()
    @commands.has_permissions(manage_channels = True)
    async def show(self, ctx):
      data = dbn.check("data_config/proteccs.json")
      desc = ""
      for c, v in data.items():
        user = discord.utils.get(ctx.guild.members, id = int(c))
        desc += user.display_name + ": " + v + "\n"  
      embed = discord.Embed(title = "Proteccs", description = desc, color=discord.Color.from_rgb(233, 30, 98))

      await ctx.send(embed = embed)   

       

def setup(bot):
    bot.add_cog(MIYYE(bot))
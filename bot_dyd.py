import asyncio
from datetime import datetime
from random import choice
import discord
from discord.ext import commands
from token_discord import TOKEN
from config import links
import modulos.DowYotMp3 as dw

TIPOS_CALCULO = ["+", "-", "*", "/"]
TOKEN = TOKEN

canciones_borrar = []
lista_espera = []
intents = discord.Intents.default()
intents.typing = False
intents.message_content = True
icon = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.9hBa8STW1UePWdKWCXuMZAHaIj%26pid%3DApi&f=1&ipt=bececd143785f9502fb2d9ca32f45ca587e1bd9689ff029acb25fc20956d69f0&ipo=images"
foter = "D&D Rol Bot by @emmanuelmmontesinos"


bot = commands.Bot(command_prefix='dd ', intents=intents,
                   help_command=None, description="Dungeon Master")


@bot.command(name="help")
async def help(ctx):
    description = """
    
    `dd help`: Muestra los comandos (ventana actual)
    `dd link`: Muestra los links configurados en config.py
    `dd roll`: Tira los dados, EJ: dd tira 2d20 +5V -> 2 dados de 20 caras + 5 con Ventaja
    `dd calcula`: Calculadora rápida, EJ: dd calcula 50+10/2 -> = 30
    `dd sorteo`: Hace un sorteo entre los elementos separados por comas, EJ: dd sorteo 1,2,3,4 -> 3
    `dd play link_youtube`: Reproduce el audio de un link de YouTube(Depende de la conexión del bot)
    `dd next link_youtube`: Pasa a la siguiente canción de la lista
    `dd stop`: Para la canción en curso
    
                """
    embed = discord.Embed(title="Panel de Ayuda",
                          description=description,
                          color=discord.Color.gold())
    marca_de_tiempo = datetime.now()
    embed.set_footer(text=foter, icon_url=icon)
    embed.timestamp = marca_de_tiempo
    await ctx.send(embed=embed)


@bot.command(name="link")
async def link(ctx):
    description = ""
    for url in links.keys():
        description += f"\n[{url}]({links[url]})"
    embed = discord.Embed(title="Links del Server",
                          description=description,
                          color=discord.Color.brand_green())
    marca_de_tiempo = datetime.now()
    embed.set_footer(text=foter, icon_url=icon)
    embed.timestamp = marca_de_tiempo
    await ctx.send(embed=embed)


@bot.command(name="sorteo")
async def sorteo(ctx, *args):
    nombre = ctx.author.name
    mediante = ""
    set_sorteo = []

    for l in args:
        for ll in l:
            if ll != ",":
                mediante += ll
            else:
                set_sorteo.append(mediante)
                mediante = ""
    ganador = choice(set_sorteo)
    descr = f"🥇🥇🥇GANADOR🥇🥇🥇\n👑👑👑 {ganador.upper()} 👑👑👑"
    embed = discord.Embed(
        title=f"Sorteo de {nombre.capitalize()}", description=descr, color=discord.Color.gold())
    marca_de_tiempo = datetime.now()
    embed.set_footer(text=foter, icon_url=icon)
    embed.timestamp = marca_de_tiempo
    await ctx.send(embed=embed)


@bot.command(name="calcula")
async def calc(ctx, *args):
    pedido = ""
    for lot in args:
        for l in lot:
            if l == "x" or l == "X":
                pedido += "*"
            else:
                pedido += l

    total = eval(pedido)
    embed = discord.Embed(
        title="Resultado", description=f"{pedido} = {total}")
    marca_de_tiempo = datetime.now()
    embed.set_footer(text=foter, icon_url=icon)
    embed.timestamp = marca_de_tiempo
    await ctx.send(embed=embed)


@bot.command(name="roll")
async def tira(ctx, num="1d20", *args):
    d_flag = False
    caras = ""
    veces = ""
    for n in num:
        if n.lower() == "d":
            d_flag = True
        elif n.isdigit() and d_flag == True:
            caras += n
        elif n.isdigit() and d_flag == False:
            veces += n
    if "d" not in num.lower() or caras == "":
        for nuu in args:
            for nu in nuu:
                if nu in TIPOS_CALCULO or not nu.isascii():
                    if nu.lower() != "d":
                        break
                elif nu.lower() != "d":
                    caras += nu

    if caras == "":
        embed = discord.Embed(
            title=f"El Master te mira raro", description=f"{num} no es valido, para poner el dado, pon:\nEjempo: dd tira 5d20 +6")
        marca_de_tiempo = datetime.now()
        embed.set_footer(text=foter, icon_url=icon)
        embed.timestamp = marca_de_tiempo

        await ctx.send(embed=embed)
        return
    final = ""
    extra = ""
    check_d = False
    for aa in args:
        for a in aa:
            if a in TIPOS_CALCULO:
                final += a
                check_d = True
            elif a.isnumeric() and check_d is True:
                final += a
            if a.lower() == "v":
                if a == args[0][-1] or a == args[-1]:
                    extra = a.lower()
            elif a.lower() == "d":
                if a == args[0][-1] or a == args[-1]:
                    extra = a.lower()

    try:
        veces = int(veces)
        caras = int(caras)
        extra_min = caras + 1
        extra_max = 0
        if veces > 1:
            tiradas = ""
            total = 0
            n_tirada = 1
            for dado in range(veces):
                tirada = choice(range(1, caras + 1))
                if tirada < extra_min:
                    extra_min = tirada
                if tirada > extra_max:
                    extra_max = tirada
                total += tirada
                print(
                    f"Tirada nº{n_tirada}\nha salido un `{tirada}` en el 🎲 de {caras}\n")
                tiradas += f"`Tirada nº{n_tirada}`\nHa salido un `{tirada}` en el 🎲 de {caras}\n"
                n_tirada += 1

            final_2 = str(total) + final
            desc_total = eval(final_2)

            tiradas += f"\n*TOTAL: {total} + MOD[{final}] =* `{desc_total}`\n"
            if extra:
                if extra == "v":
                    tiradas += "`<------------------------VENTAJA------------------------>`\n"
                    tiradas += f"Tirada con ventaja, mejor resultado `{extra_max}`\nTOTAL VENTAJA + MOD[{final}] = `{eval(str(extra_max)+final)}`"
                elif extra == "d":
                    tiradas += "`<---------------------DESVENTAJA--------------------->`\n"
                    tiradas += f"Tirada con desventaja, peor resultado `{extra_min}`\nTOTAL DESVENTAJA + MOD = `{eval(str(extra_min)+final)}`"
            embed = discord.Embed(
                title=f"Resultado de {num}", description=tiradas)
            marca_de_tiempo = datetime.now()
            embed.set_footer(text=foter, icon_url=icon)
            embed.timestamp = marca_de_tiempo

            await ctx.send(embed=embed)
        else:
            dado = choice(range(1, int(caras)+1))
            final_2 = str(dado) + final
            desc_total = eval(final_2)
            print(f"caras{num} resultado{dado}")
            if dado != 1 and dado != caras:
                embed = discord.Embed(
                    title=f"Tirada de 🎲D{num}", description=f"Ha salido un ***`{dado}`*** en el 🎲 de {caras}\n*Total {final_2} =* `{desc_total}`")
                marca_de_tiempo = datetime.now()
                embed.set_footer(text=foter, icon_url=icon)
                embed.timestamp = marca_de_tiempo
                await ctx.send(embed=embed)
            elif dado == 1:
                embed = discord.Embed(
                    title=f"Tirada de 🎲D{num}", description=f"Ha salido un ***`{dado}`*** en el 🎲 de {caras}\n*`PIFIA` - Total {final_2} =*  `{desc_total}`")
                marca_de_tiempo = datetime.now()
                embed.set_footer(text=foter, icon_url=icon)
                embed.timestamp = marca_de_tiempo
                await ctx.send(embed=embed)
            elif dado == caras:
                embed = discord.Embed(
                    title=f"Tirada de 🎲D{num}", description=f"Ha salido un ***`{dado}`*** en el 🎲 de {caras}\n*`CRITICO` - Total {final_2} =*  `{desc_total}`")
                marca_de_tiempo = datetime.now()
                embed.set_footer(text=foter, icon_url=icon)
                embed.timestamp = marca_de_tiempo
                await ctx.send(embed=embed)
    except:
        embed = discord.Embed(
            title=f"El Master te mira raro...", description=f"Entrada no valida\nEjempo: dd tira 5d20 +6 V")
        marca_de_tiempo = datetime.now()
        embed.set_footer(text=foter, icon_url=icon)
        embed.timestamp = marca_de_tiempo
        await ctx.send(embed=embed)


@bot.command(name="next")
async def pasar_siguiente(ctx):
    global lista_espera, canciones_borrar
    if lista_espera:
        url = lista_espera.pop(0)
        if ctx.voice_client.is_playing():
            await ctx.voice_client.disconnect()
        canal = ctx.author.voice.channel
        con_canal = await canal.connect()
        archivo, nombre_cancion, ruta = dw.audio(url)
        con_canal.play(discord.FFmpegPCMAudio(
            source="play.mp3", executable=".\\recursos\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"))
        descr = f"El bardo os canta ---> {nombre_cancion}"
        embed = discord.Embed(description=descr)
        await ctx.send(embed=embed)


@bot.command(name="play")
async def play(ctx, url):
    global canciones_borrar
    if ctx.voice_client is None:
        canal = ctx.author.voice.channel
        con_canal = await canal.connect()
    else:
        con_canal = ctx.voice_client
    if con_canal.is_playing():
        lista_espera.append(url)
        descr = "Añadida a lista de espera del `Bardo`"
        embed = discord.Embed(description=descr)
        mensaje = await ctx.send(embed=embed)
        await mensaje.add_reaction("⏩")
        return

    nombre = ctx.author.name
    canal = ctx.author.voice.channel

    archivo, nombre_cancion, ruta = dw.audio(url)
    try:
        con_canal.play(discord.FFmpegPCMAudio(
            source="play.mp3", executable=".\\recursos\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"))
        descr = f"El bardo os canta ---> {nombre_cancion}"
        embed = discord.Embed(description=descr)
        await ctx.send(embed=embed)

    except Exception as e:
        print(f"Error durante la reproducción: {e}")


@bot.command(name="alerta")
async def alerta(ctx, num1="", num2="", num3=""):
    datos = [num1, num2, num3]
    try:
        check = 0
        datos = [num1, num2, num3]
        for d in datos:
            if d != "":
                tim_h = float(d[:-1])
            else:
                datos.pop(d)
                check += 1
        if check == 3:
            embed = discord.Embed(title="One Piece Suspira",
                                  description=f"{str(ctx)} no es una opción valida")
            await ctx.send(embed=embed)
    except ValueError:
        return
    finally:
        tiempo = 0
        datos = [num1, num2, num3]
        tim_h = 0
        tim_m = 0
        tim_s = 0
        for n in datos:
            if n != "":
                if n[-1].lower() == "s":
                    tim_s = float(n[:-1])
                    tiempo += tim_s

                if n[-1].lower() == "m":
                    tim_m = float(n[:-1])
                    tiempo += tim_m * 60

                if n[-1].lower() == "h":
                    tim_h = float(n[:-1])
                    tiempo += tim_h * 60 * 60
        await ctx.send(embed=discord.Embed(title=f"Alerta registrada {str(ctx.author.display_name).capitalize()}",
                                           description=f"{int(tim_h)} H {int(tim_m)} min {int(tim_s)} segundos"))
        await asyncio.sleep(tiempo)
        embed = discord.Embed(
            title="ALERTA!!!",
            description=f"{ctx.author.mention} ya ha pasado {int(tim_h)} H {int(tim_m)} min {int(tim_s)} segundos")
        await ctx.send(embed=embed)


@bot.command(name='stop')
async def leave(ctx):
    global canciones_borrar
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    if os.path.exists("play.mp3"):
        with open("play.mp3", "rb") as fichero:
            pass
        os.remove("play.mp3")
    descrip = f"{ctx.author.name} ha parado la cancion"
    await ctx.send(descrip)


@bot.event
async def on_ready():
    print('Estamos logueado como {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="D&D 5E by @EmmanuelMMontesinos"))


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.embeds and user != bot.user:
        if str(reaction.emoji) == '⏩':
            global lista_espera
            if lista_espera:
                url = lista_espera.pop(0)
                canal = user.voice.channel
                if reaction.message.guild.voice_client:
                    con_canal = reaction.message.guild.voice_client
                    await con_canal.disconnect()
                con_canal = await canal.connect()
                archivo, nombre_cancion, ruta = dw.audio(url)
                con_canal.play(discord.FFmpegPCMAudio(
                    source="play.mp3", executable=".\\recursos\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"))
                await reaction.message.channel.send(f"El bardo os canta ---> {nombre_cancion}")
                await reaction.message.add_reaction("⏩")
        embed = reaction.message.embeds[0]


bot.run(TOKEN)

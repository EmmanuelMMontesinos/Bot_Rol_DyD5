import discord
import os
from pytube import YouTube


def audio(link):
    yt = YouTube(str(link))
    audio_2 = "play" + ".mp3"
    if os.path.exists(audio_2):
        with open(audio_2, 'rb') as file:
            pass
        os.remove("play.mp3")
    video = yt.streams.filter(only_audio=True,
                              progressive=False,
                              audio_codec="mp4a.40.2").first()
    destino = ""
    salida = video.download(output_path=destino)
    nombre, extension = os.path.splitext(salida)

    os.rename(salida, audio_2)

    nombre_completo_total = salida.split("\\")
    nombre_completo = nombre_completo_total[-1].split(".")[0] + ".mp3"
    ruta = f"{nombre_completo}"
    audio_salida = discord.File(fp=audio_2, filename=nombre_completo)
    return audio_salida, nombre_completo, ruta

    print(f"{yt.title} ha sido descargado en MP3")

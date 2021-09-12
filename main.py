#!/usr/bin/python3.8

import discord
import os
from spotipyapi import request_valid_song, get_token
import youtube_dl
from dotenv import load_dotenv
from functions import chat,search,knowledge,kerang_ajaib
from keep_alive import keep_alive
import numpy as np
load_dotenv()

def is_me(m):
    return m.author == client.user

intents = discord.Intents().all()
client = discord.Client(intents=intents,activity=discord.Game('"help ko"'))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    channel = client.get_channel(790274325533378682)
    embed = discord.Embed(title="Halo " + member.name,
                          description="Langsung mabar dota lah kita",
                          color=0xcef5ec)
    await channel.send(embed=embed)


@client.event
async def on_message(message):

    ydl_opts = {
        'format':
        'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    if message.author == client.user:
        return

    elif message.content.startswith('ko play lagu random'):
        voiceChannel = discord.utils.get(message.guild.voice_channels)
        await voiceChannel.connect()

        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        try:
            if voice.is_playing():
                await message.channel.send("Tunggu lagunya selese dulu gan")
                return
        except:
            pass

        await message.channel.send("Mohon tunggu gan...")

        lagu = search(request_valid_song(get_token(), genre='anime'))
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(lagu, download=False)
            URL = info['formats'][0]['url']
        voice.play(discord.FFmpegPCMAudio(URL))
        await message.channel.purge(limit=1, check=is_me)
        await message.channel.send("Now playing : " + lagu)
        if not voice.is_playing():
            await message.channel.purge(limit=1, check=is_me)
        return

    elif message.content.startswith('kerang ajaib'):
        await message.channel.send(kerang_ajaib(message.content[13:]))
        return

    elif message.content.startswith('ko play lagu'):
        try:
            voiceChannel = message.author.voice.channel
            await voiceChannel.connect()
        except Exception as er:
            print(er)
            pass
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice and voice.is_playing():
            await message.channel.send("Tunggu lagunya selese dulu gan")
            return

        await message.channel.send("Mohon tunggu gan...")

        lagu = search(message.content[13:])
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(lagu, download=True)
            filename = ydl.prepare_filename(info)
            URL = info['formats'][0]['url']
        voice.play(discord.FFmpegPCMAudio(filename[:-5]+'.mp3'))
        await message.channel.purge(limit=1, check=is_me)
        await message.channel.send("Now playing : " + lagu)
        if not voice.is_playing():
            await message.channel.purge(limit=1, check=is_me)
        return

    elif message.content.startswith('ko join'):
        voiceChannel = message.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if not voice.is_connected():
            await message.channel.send("Dah connect lah aku njeng")
        else:
            await voiceChannel.connect()
        return

    elif message.content.startswith('ko leave'):
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await message.channel.send("Gada connect lah aku njeng")
        return

    elif message.content.startswith('ko pause'):
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await message.channel.send("Gada play apa aku sat")
    
    elif message.content.startswith('ko lanjut'):
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice != None:
            if voice.is_paused():
                voice.resume()
        else:
            await message.channel.send("Gada play apa aku sat")
    
    elif message.content.startswith('ko stop'):
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice.is_playing():
            await message.channel.purge(limit=1, check=is_me)
        voice.stop()

    elif message.content.startswith('login'):
        await message.channel.send('Gas lah tol\ninvit dota id: 207870596')
        return

    elif message.content.startswith('ko '):
        await message.channel.send(chat(message.content[4:]))
        return

    elif message.content.startswith('tau gak ko'):
        await message.channel.send(knowledge(message.content[11:]))
        return

    elif message.content.startswith('rekomen lagu'):
        await message.channel.send(request_valid_song(
            get_token(), 'anime' if message.content ==
            "rekomen lagu" else message.content[13:]))
        print(message.content[13:])
        return

    elif client.user.mentioned_in(message):
        await message.channel.send('Apa njeng?')
        return

    elif message.content.startswith('help ko'):
        embedVar = discord.Embed(
            title="Yuriko Bot",
            description=
            "Bot Ga Guna\nhttps://discord.yurikochristian.repl.co\n\nList command:",
            color=0xcef5ec)
        embedVar.add_field(name="ko play lagu random",
                           value="memutar lagu jepang random\n",
                           inline=False)
        embedVar.add_field(name="ko play lagu [keyword lagu]",
                           value="memutar lagu yang diinginkan\n",
                           inline=False)
        embedVar.add_field(name="ko leave",
                           value="suruh bot leave voice channel\n",
                           inline=False)
        embedVar.add_field(name="ko pause",
                           value="pause lagu yang dimainkan\n",
                           inline=False)
        embedVar.add_field(name="ko stop",
                           value="stop lagu yang dimainkan\n",
                           inline=False)
        embedVar.add_field(name="ko lanjut",
                           value="lanjut lagu yang dipause\n",
                           inline=False)
        embedVar.add_field(name="ko [percakapan]",
                           value="akan dibalas oleh bot yuriko\n",
                           inline=False)
        embedVar.add_field(name="kerang ajaib [pertanyaan]",
                           value="dijawab kerang ajaib\n",
                           inline=False)
        embedVar.add_field(name="rekomen lagu [genre(opsional)]",
                           value="rekomendasi judul lagu dan artisnya\n",
                           inline=False)
        embedVar.add_field(name="login",
                           value="Ajak bot login DoTA\n",
                           inline=False)
        embedVar.add_field(name="tau gak ko [apa aja]",
                           value="pengetahuan tentang apa aja\n\n",
                           inline=False)
        embedVar.add_field(name="Note",
                           value="*kalau dimention botnya ga nyante",
                           inline=False)
        await message.channel.send(embed=embedVar)
        return


keep_alive()
client.run(os.getenv('TOKEN'))
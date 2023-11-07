# -*- coding: utf-8 -*-
import env
import discord
import pytz
import os
import pytube
import math
import asyncio
import shutil
import tinydb
from discord.utils import get
from math import floor
from datetime import datetime
from discord.ext import commands
from PIL import Image
from random import randrange
from discord import FFmpegPCMAudio
from urllib.parse import urlparse

class abot(discord.Client):
    global guild
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.sycned = False
    async def on_ready(self):
        guild = self.get_guild(env.GUILD_ID)
        birth = asyncio.create_task(birthday(guild))
        print("Bot is online")

bot = abot()
tree = discord.app_commands.CommandTree(bot)

#constants
mee6 = 159985870458322944

#tinydb
def reloadDb():
    global db, search
    db = tinydb.TinyDB('db.json')
    search = tinydb.Query()
reloadDb()

#tinydb init tables if not exist
db.table('bannedWords')
db.table('cyrograf')
db.table('variables')

#variables
lastNumber = 0

#music player
queue = []
nowPlaying = ""

#banned words in last deleted message
lastDeleted = []

#bithday
def lastBirthMessageToday():
    global db, search
    if len(db.table('variables').search(search.lastBirthMessage == datetime.now().strftime("%d-%m-%Y"))):
        lastBirthMessageToday = True
    else:
        lastBirthMessageToday = False
    db.table('variables').upsert({'lastBirthMessage': datetime.now().strftime("%d-%m-%Y")}, search.lastBirthMessage == datetime.now().strftime("%d-%m-%Y"))
    return lastBirthMessageToday

def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

async def birthday(guild):
    while (True):
        for i in guild.members:
            if not i.bot:
                if i.joined_at.strftime("%d-%m")==datetime.now().strftime("%d-%m") and i.joined_at.strftime("%Y")!=datetime.now().strftime("%Y"):
                    await i.add_roles(discord.utils.get(guild.roles,id=env.BIRTHDAY_ROLE))
                elif env.BIRTHDAY_ROLE in [role.id for role in i.roles]:
                    await i.remove_roles(discord.utils.get(guild.roles,id=env.BIRTHDAY_ROLE))
        channel = bot.get_channel(env.BIRTHDAY_CHANNEL)
        if (not lastBirthMessageToday()):
            birthdayPeople = []
            for i in guild.members:
                if not i.bot:
                    if i.joined_at.strftime("%d-%m")==datetime.now().strftime("%d-%m"):
                        birthdayPeople.append("<@"+str(i.id)+">")
            if (len(birthdayPeople)):
                await channel.send("Dzisiaj urodziny obchodzą:")
                await channel.send(", ".join(birthdayPeople))
            else:
                await channel.send("Dzisiaj nikt nie ma urodzin :(")
        await asyncio.sleep(600)

async def afterPlayAsync():
    global queue
    global nowPlaying
    if (len(queue)):
        if ((nowPlaying not in queue) and os.path.isfile("yt/"+nowPlaying+".mp3")):
            os.remove("yt/"+nowPlaying)
        playSong(queue.pop(0))
    else:
        nowPlaying = ""
        queue = []
        if (len(bot.voice_clients)):
            await bot.voice_clients[0].disconnect()

def afterPlay(err):
    asyncio.run_coroutine_threadsafe(afterPlayAsync(), bot.loop)

def playSong(vid_id):
    global nowPlaying
    nowPlaying = vid_id
    source = FFmpegPCMAudio("yt/"+vid_id+".mp3")
    bot.voice_clients[0].play(source, after=afterPlay)

@tree.command(name="play", description="Dodaj utwór do kolejki odtwarzania")
async def self(interaction: discord.Interaction, fraza:str):
    global queue
    channel = interaction.user.voice
    if channel is None:
        await interaction.response.send_message("Musisz być na kanale głosowym!")
    else:
        srch = pytube.Search(fraza)
        if len(srch.results) == 0:
            await interaction.response.send_message("Nie znaleziono takiego utworu!")
        else:
            await interaction.response.send_message("Trwa pobieranie wybranego utworu...")
            try:
                if (not os.path.isfile("yt/"+srch.results[0].video_id+".mp3")):
                    yt = pytube.YouTube("https://www.youtube.com/watch?v="+srch.results[0].video_id)
                    video = yt.streams.filter(only_audio=True).first()
                    video.download(filename=srch.results[0].video_id+".mp3",output_path="yt")
                if (len(bot.voice_clients) == 0):
                    await channel.channel.connect()
                    playSong(srch.results[0].video_id)
                elif (bot.voice_clients[0].is_playing()):
                    queue.append(srch.results[0].video_id)
                else:
                    playSong(srch.results[0].video_id)
                await interaction.edit_original_response(content="Wyszukano: **"+fraza+"**.\nDodano do kolejki: **"+srch.results[0].title+"**!")
            except:
                await interaction.edit_original_response(content="Głupi youtube nie pozwala mi pobrać tego utworu.")

@tree.command(name="pause", description="Pauzuje i wznawia odtwarzanie muzyki")
async def self(interaction: discord.Interaction):
    if (len(bot.voice_clients) and (bot.voice_clients[0].is_playing() or bot.voice_clients[0].is_paused)):
        if (bot.voice_clients[0].is_paused()):
            bot.voice_clients[0].resume()
            await interaction.response.send_message("Wznowiono odtwarzanie muzyki.")
        else:
            bot.voice_clients[0].pause()
            await interaction.response.send_message("Spauzowano odtwarzanie muzyki.")
    else:
        await interaction.response.send_message("Bot nic nie gra przystojniaczku. Nie jestem w stanie zarzucić pauzy JOŁ.")

@tree.command(name="queue", description="Sprawdź kolejkę odtwarzania")
async def self(interaction: discord.Interaction, page:int=1):
    global queue
    if (len(queue) == 0):
        await interaction.response.send_message("Aktualnie nic nie czeka na odtworzenie.")
    else:
        prefix = "Kolejka odtwarzania:\n\n"
        if (page < 1):
            prefix = "Podana strona nie istnieje. Wyświetlam pierwszą dostępną stronę.\n\n"
            page = 1
        elif (page > math.ceil(len(queue)/10)):
            prefix = "Podana strona nie istnieje. Wyświetlam ostatnią dostępną stronę.\n\n"
            page = math.ceil(len(queue)/10)
        pg = page-1
        middle = ""
        for i in range(10):
            if (len(queue) == pg*10+i):
                break
            srch = pytube.Search(queue[pg*10+i])
            middle += str(pg*10+i+1)+". **"+srch.results[0].title+"**\n"
        sufix = "\nWyświetlono stronę: "+str(page)+"/"+str(math.ceil(len(queue)/10))
        await interaction.response.send_message(prefix+middle+sufix)

"""
@tree.command(name="skip", description="Pomija aktualnie odtwarzany utwór (lub więcej)")
async def self(interaction: discord.Interaction, count:int=1):
    global queue
    if (count > 0):
        counter = 1
        while (count > 1):
            count -= 1
            counter += 1
            if (not len(queue)):
                break
            queue.pop(0)
        bot.voice_clients[0].stop()
        await afterPlayAsync()
        await interaction.response.send_message("Pominięto "+str(counter)+" utworów.")
    else:
        await interaction.response.send_message("Nie można pominąć mniej niż 1 utworów.")
"""

@tree.command(name="stop", description="Zatrzymuje odtwarzacz")
async def self(interaction: discord.Interaction):
    global queue
    queue = []
    try:
        shutil.rmtree("yt")
    except:
        pass
    os.mkdir("yt")
    if (len(bot.voice_clients)):
        bot.voice_clients[0].stop()
        bot.voice_clients[0].disconnect()
    await interaction.response.send_message("Zatrzymano odtwarzacz.")

@tree.command(name="author", description="Bot poda ci najważniejsze informacje o autorze")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Autorem bocika jest <@386237687008591895>.\n\nGithub: https://github.com/kasztandor\nFacebook: https://www.facebook.com/kasztandor\nReddit: https://www.reddit.com/user/Kasztandor\nInstagram: https://www.instagram.com/kasztandor_art\nInstagram: https://www.instagram.com/kasztandor_photos", suppress_embeds=True)

@tree.command(name="generate", description="Bot wygeneruje wybrany przez ciebie napis")
async def self(interaction: discord.Interaction, argument:str):
    process = argument.lower().replace("ą","a").replace("ć","c").replace("ę","e").replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").replace("ż","z").replace("ź","z")
    images = []
    width = 0
    for i in process:
        if i == " ":
            images.append(Image.open("letters/space.png").convert('RGBA'))
            width += images[-1].width
        elif os.path.exists("letters/"+i+".png"):
            images.append(Image.open("letters/"+i+".png"))
            width += images[-1].width
    newImage = Image.new('RGBA', (width, images[0].height))
    width = 0
    for i in images:
        newImage.paste(i, (width, 0))
        width += i.width
    newImage.save("napis.png")
    await interaction.response.send_message(file=discord.File('napis.png'))
    os.remove("napis.png")

@bot.event
async def on_message(message):
    global db, search, mee6, lastDeleted

    guild = message.guild
    msg = message.content
    msgLowercase = msg.lower()
    msgLowercaseNoPolish = msgLowercase.replace("ą","a").replace("ć","c").replace("ę","e").replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").replace("ż","z").replace("ź","z")
    sender = message.author
    badGuys = [421932366802714625, 771078648140791808, 883308544600973363]
    badGuysDate = ["15-10-2023", "15-10-2023", "26-10-2023"]

    IST = pytz.timezone('Europe/Warsaw')
    time = [datetime.now(IST).hour,datetime.now(IST).minute,datetime.now(IST).second]
    timeString = [str(time[0]),str(time[1]),str(time[2])]

    bannedBaypass = False

    for i in range(len(timeString)):
        if len(timeString[i])==1:
            timeString[i] = "0"+timeString[i]
    timeNow = timeString[0]+":"+timeString[1]+":"+timeString[2]
    bannedWords = []
    for i in db.table("bannedWords").all():
        bannedWords.append(i['word'])
    containsBadWords = False
    remove = False

    if (msg == "!rathelp"):
        await message.channel.send("""
Lista zawiera komendy dla administracji serwera:
    **!rathelp** - wyświetla tą wiadomość
  *Komendy "Kasztandor only":*
    **!sync** - synchronizuje drzewo komend
    **!dbreload** - synchronizuje bazę danych
    **!cyrograf** discord_id - objęcie cyrografem użytkownika
  *Komendy "Ratbot controler only":*
    **!bannedadd** słowo - dodawanie słowa do listy słów banowanych
    **!bannedremove** słowo - usuwanie słowa do listy słów banowanych
    **!displaylast** - wyświetla niepoprawne słowa w ostatniej usuniętej wiadomości
        """)

    if (msg == "!sync" and message.author.id == 386237687008591895):
        await tree.sync()
        await message.channel.send("Zsynchronizowano drzewo!")
        bannedBaypass = True

    if (msg == "!dbreload" and message.author.id == 386237687008591895):
        reloadDb()
        await message.channel.send("Zsynchronizowano bazę danych!")
        bannedBaypass = True

    if (len(msg)>11 and msg[0:10] == "!cyrograf " and message.author.id == 386237687008591895):
        victim = msg[10:len(msg)]
        if (len(db.table("cyrograf").search(search.id == int(victim))) > 0):
            await message.channel.send(f"<@{victim}> już jest objęty cyrografem!")
            return
        db.table("cyrograf").insert({'id': int(victim), 'time': str(datetime.now(IST).strftime("%d-%m-%Y"))})
        bannedBaypass = True
        await tree.sync()
        await message.channel.send(f"Właśnie <@{victim}> został objęty cyrografem!")

    if (len(msg)>12 and msg[0:11] == "!bannedadd " and env.BOT_CONTROLLER in [role.id for role in message.author.roles]):
        word = msg[11:len(msg)]
        if (len(bannedWords) == 0):
            bannedWords.append(word)
        elif (word not in bannedWords):
            bannedWords.append(word)
        db.table("bannedWords").insert({'word': word})
        bannedBaypass = True
        await message.channel.send(f"Dodano słowo {word} do listy słów banowanych!")

    if (len(msg)>15 and msg[0:14] == "!bannedremove " and env.BOT_CONTROLLER in [role.id for role in message.author.roles]):
        word = msg[14:len(msg)]
        if (word in bannedWords):
            bannedWords.remove(word)
            db.table("bannedWords").remove(search.word == word)
            bannedBaypass = True
            await message.channel.send(f"Usunięto słowo {word} z listy słów banowanych!")
        else:
            await message.channel.send(f"Słowo {word} nie znajduje się na liście słów banowanych!")
        bannedBaypass = True
    
    if (msg == "!displaylast" and env.BOT_CONTROLLER in [role.id for role in message.author.roles]):
        await message.channel.send("Ostatnio usunięta wiadomość zawierała słowa: "+", ".join(lastDeleted))
        bannedBaypass = True

    for i in bannedWords:
        if msgLowercaseNoPolish.find(i)!=-1:
            containsBadWords = True

    if (time[0] < 20 and time[0] >= 5 and containsBadWords):
        remove = True

    if (not bannedBaypass and (remove and len(db.table("cyrograf").search(search.id == sender.id)) == 0) or (not containsBadWords and len(db.table("cyrograf").search(search.id == sender.id)) > 0 and len(msg) and not is_url(msg))) and sender.id != bot.user.id:
        if len(db.table("cyrograf").search(search.id == sender.id)) > 0:
            toRemove = await message.channel.send("<@"+str(sender.id)+"> na mocy cyrografu zawartego dnia "+db.table("cyrograf").search(search.id == sender.id)[0]['time']+" każda twa wiadomość nie zawierająca słowa z listy wulgaryzmów serwerowych została usuinięta!")
        else:
            toRemove = await message.channel.send("<@"+str(sender.id)+">!!! Zgodnie z paragrafem §1.8 na kanale <#935612476156936272> o godzinie "+timeNow+" czasu polskiego panuje bezwzględny zakaz używania przekleństw (z wyjątkami opisanymi w tym podpunkcie). W związku z powyższym wiadomość została usunięta. Pilnuj się!")
            lastDeleted = []
            for i in bannedWords:
                if msgLowercaseNoPolish.find(i)!=-1:
                    lastDeleted.append(i)
        await message.delete()
        await toRemove.delete(delay=15)
    elif message.channel.id == env.COUNTING_CHANNEL and message.author.id != bot.user.id:
        try:
            int(msg)
        except:
            toRemove = await message.channel.send("To nie jest kanał do pisania! Tutaj liczymy!")
            await message.delete()
            await toRemove.delete(delay=15)
    elif message.channel.id == env.MEMES_CHANNEL and message.author.id != bot.user.id:
        message.channel.send("test"+str(message.attachments.count))
        if len(message.attachments) or message.content.startswith("j:") or "https://" in msg or "http://" in msg:
            await message.add_reaction("\U0001F44D")
            await message.add_reaction("\U0001F44E")
    elif len(message.mentions) > 0 and message.author.id == mee6:
        userID = msg[(msg.find("<@")+2):msg.find(">")]
        #theUser = get(guild.members, id=userID)
        theUser = message.mentions[0]
        level = int(msg[(msg.find("level")+6):msg.find("!")])
        if level <= 100:
            rankPosition = floor(level/10)
            if rankPosition > 100:
                rankPosition = 10
            roleToGiveID = env.ROLES[rankPosition]
            roleToGive = discord.utils.get(guild.roles,id=roleToGiveID)
            await theUser.add_roles(roleToGive)
            if rankPosition > 0:
                roleToRevokeID = env.ROLES[rankPosition-1]
                roleToRevoke = discord.utils.get(guild.roles,id=roleToRevokeID)
                await theUser.remove_roles(roleToRevoke)
            if level/10 == floor(level/10):
                sendedMessage = await message.channel.send("Loading...")
                await sendedMessage.edit(content="Gratulacje <@"+str(userID)+"> Właśnie osiągnąłeś rangę <@&"+str(roleToGiveID)+">")
    elif len(message.mentions) > 0 and message.mentions[0] == bot.user and (msgLowercaseNoPolish.find("przedstaw sie") != -1):
        await message.channel.send("Siema! Jestem sobie botem napisanym przez Kasztandora i tak sobie tutaj działam i robię co do mnie należy. Pozdrawiam wszystkich i życzę udanego dnia!")

bot.run(env.TOKEN)

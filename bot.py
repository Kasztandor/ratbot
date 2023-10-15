# -*- coding: utf-8 -*-
import env
import discord
import pytz
import os
import pytube
import math
import asyncio
import shutil
from discord.utils import get
from math import floor
from datetime import datetime
from discord.ext import commands
from PIL import Image
from random import randrange
from discord import FFmpegPCMAudio

#constants
mee6 = 159985870458322944
guild = discord.Object(id=env.GUILD_ID)

#variables
lastNumber = 0

#music player
queue = []
nowPlaying = ""

def ball8():
    x=["Mój wywiad donosi: NIE","Wygląda dobrze","Kto wie?","Zapomnij o tym","Tak - w swoim czasie","Prawie jak tak","Nie teraz","YES, YES, YES","To musi poczekać","Mam pewne wątpliwości","Możesz na to liczyć","Zbyt wcześnie aby powiedzieć","Daj spokój","Absolutnie","Chyba żatrujesz?","Na pewno nie","Zrób to","Prawdopodobnie","Dla mnie rewelacja","Na pewno tak"]
    return "Magiczna kula mówi: "+x[randrange(0,len(x))]

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.sycned = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.sycned:
            await tree.sync(guild=guild)
            self.synced = True
        print("Bot is online")

bot = abot()
tree = discord.app_commands.CommandTree(bot)

async def afterPlayAsync():
    global queue
    global nowPlaying
    if (len(queue)):
        print("Następny song")
        if ((nowPlaying not in queue) and os.path.isfile("yt/"+nowPlaying+".mp3")):
            os.remove("yt/"+nowPlaying)
        playSong(queue.pop(0))
    else:
        print("Uciekam")
        nowPlaying = ""
        queue = []
        if (len(bot.voice_clients)):
            await bot.voice_clients[0].disconnect()

def afterPlay(err):
    asyncio.run_coroutine_threadsafe(afterPlayAsync(), bot.loop)

def playSong(vid_id):
    global nowPlaying
    print("playSong()")
    nowPlaying = vid_id
    source = FFmpegPCMAudio("yt/"+vid_id+".mp3")
    bot.voice_clients[0].play(source, after=afterPlay)

@tree.command(name="play", description="Dodaj utwór do kolejki odtwarzania", guild=guild)
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

@tree.command(name="pause", description="Pauzuje i wznawia odtwarzanie muzyki", guild=guild)
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

@tree.command(name="queue", description="Sprawdź kolejkę odtwarzania", guild=guild)
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
@tree.command(name="skip", description="Pomija aktualnie odtwarzany utwór (lub więcej)", guild=guild)
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

@tree.command(name="stop", description="Zatrzymuje odtwarzacz", guild=guild)
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

@tree.command(name="ping", description="Bot odpowie ci pong", guild=guild)
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="author", description="Bot poda ci najważniejsze informacje o autorze", guild=guild)
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Autorem bocika jest <@386237687008591895>.\n\nGithub: https://github.com/kasztandor\nFacebook: https://www.facebook.com/kasztandor\nReddit: https://www.reddit.com/user/Kasztandor\nInstagram: https://www.instagram.com/kasztandor_art\nInstagram: https://www.instagram.com/kasztandor_photos", suppress_embeds=True)

@tree.command(name="macja", description="Bot wylosuje hasło z magicznej kuli nr 8", guild=guild)
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(ball8())

@tree.command(name="generate", description="Bot wygeneruje wybrany przez ciebie napis", guild=guild)
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
    #os.remove("napis.png")

#@tree.command(name="sync", description="[admin] Synchronizacja drzewa", guild=guild)
#async def self(interaction: discord.Interaction):
#    await tree.sync()
#    await interaction.response.send_message("Zsynchronizowano drzewo!")

@bot.event
async def on_message(message):
    guild = message.guild
    msg = message.content
    msgLowercase = msg.lower()
    msgLowercaseNoPolish = msgLowercase.replace("ą","a").replace("ć","c").replace("ę","e").replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").replace("ż","z").replace("ź","z")
    sender = message.author
    badGuys = [421932366802714625, 771078648140791808]

    IST = pytz.timezone('Europe/Warsaw')
    time = [datetime.now(IST).hour,datetime.now(IST).minute,datetime.now(IST).second]
    timeString = [str(time[0]),str(time[1]),str(time[2])]
    for i in range(len(timeString)):
        if len(timeString[i])==1:
            timeString[i] = "0"+timeString[i]
    timeNow = timeString[0]+":"+timeString[1]+":"+timeString[2]
    bannedWords = ['chuj','chuja','chujek','chuju','chujem','chujnia','chujowy','chujowa','chujowe','dojebac','dojebac','dojebie','dojebal','dojebal','dojebala','dojebala','dojebalem','dojebalem','dojebalam','dojebalam','dojebie','dojebie','dopieprzac','dopieprzac','dopierdalac','dopierdalac','dopierdala','dopierdalal','dopierdalal','dopierdalala','dopierdalala','dopierdoli','dopierdolil','dopierdolil','dopierdole','dopierdole','dopierdoli','dopierdalajacy','dopierdalajacy','dopierdolic','dopierdolic','huj','hujek','hujnia','huja','huje','hujem','huju','jebac','jebac','jebal','jebal','jebie','jebia','jebia','jebak','jebaka','jebal','jebal','jebany','jebane','jebanka','jebanko','jebankiem','jebanymi','jebana','jebanym','jebanej','jebana','jebana','jebani','jebanych','jebanymi','jebcie','jebiacy','jebiacy','jebiaca','jebiaca','jebiacego','jebiacego','jebiacej','jebiacej','jebia','jebia','jebie','jebie','jebliwy','jebnac','jebnac','jebnac','jebnac','jebnal','jebnal','jebna','jebna','jebnela','jebnela','jebnie','jebnij','jebut','koorwa','korwa','kurestwo','kurew','kurewski','kurewska','kurewskiej','kurewska','kurewska','kurewsko','kurewstwo','kurwa','kurwaa','kurwami','kurwa','kurwe','kurwe','kurwie','kurwiska','kurwo','kurwy','kurwach','kurwami','kurewski','kurwiarz','kurwiacy','kurwica','kurwic','kurwic','kurwidolek','kurwik','kurwiki','kurwiszcze','kurwiszon','kurwiszona','kurwiszonem','kurwiszony','matkojebca','matkojebcy','matkojebca','matkojebca','matkojebcami','matkojebcach','nabarlozyc','najebac','najebac','najebal','najebal','najebala','najebala','najebane','najebany','najebana','najebana','najebie','najebia','najebia','naopierdalac','naopierdalac','naopierdalal','naopierdalal','naopierdalala','naopierdalala','naopierdalala','napierdalac','napierdalac','napierdalajacy','napierdalajacy','napierdolic','napierdolic','nawpierdalac','nawpierdalac','nawpierdalal','nawpierdalal','nawpierdalala','nawpierdalala','odpieprzac','odpieprzac','odpierdalac','odpierdalac','odpierdol','odpierdolil','odpierdolil','odpierdolila','odpierdolila','odpierdoli','odpierdalajacy','odpierdalajacy','odpierdalajaca','odpierdalajaca','odpierdolic','odpierdolic','odpierdoli','odpierdolil','opieprzajacy','opierdalac','opierdalac','opierdala','opierdalajacy','opierdalajacy','opierdol','opierdolic','opierdolic','opierdoli','opierdola','opierdola','piczka','pieprzniety','pieprzniety','pieprzony','pierdel','pierdlu','pierdolacy','pierdolacy','pierdolaca','pierdolaca','pierdol','pierdole','pierdolenie','pierdoleniem','pierdoleniu','pierdole','pierdolec','pierdola','pierdola','pierdolic','pierdolicie','pierdolic','pierdolil','pierdolil','pierdolila','pierdolila','pierdoli','pierdolniety','pierdolniety','pierdolisz','pierdolnac','pierdolnac','pierdolnal','pierdolnal','pierdolnela','pierdolnela','pierdolnie','pierdolniety','pierdolnij','pierdolnik','pierdolona','pierdolone','pierdolony','pierdolki','podpierdalac','podpierdalac','podpierdala','podpierdalajacy','podpierdalajacy','podpierdolic','podpierdolic','podpierdoli','pojeb','pojeba','pojebami','pojebani','pojebanego','pojebanemu','pojebani','pojebany','pojebanych','pojebanym','pojebanymi','pojebem','pojebac','pojebac','pojebalo','popierdala','popierdalac','popierdalac','popierdolic','popierdolic','popierdoli','popierdolonego','popierdolonemu','popierdolonym','popierdolone','popierdoleni','popierdolony','porozpierdalac','porozpierdala','porozpierdalac','przejebac','przejebane','przejebac','przyjebali','przepierdalac','przepierdalac','przepierdala','przepierdalajacy','przepierdalajacy','przepierdalajaca','przepierdalajaca','przepierdolic','przepierdolic','przyjebac','przyjebac','przyjebie','przyjebala','przyjebala','przyjebal','przyjebal','przypieprzac','przypieprzac','przypieprzajacy','przypieprzajacy','przypieprzajaca','przypieprzajaca','przypierdalac','przypierdalac','przypierdala','przypierdoli','przypierdalajacy','przypierdalajacy','przypierdolic','przypierdolic','qrwa','rozjebac','rozjebac','rozjebie','rozjebala','rozjebia','rozpierdalac','rozpierdalac','rozpierdala','rozpierdolic','rozpierdolic','rozpierdole','rozpierdoli','rozpierducha','skurwic','skurwiel','skurwiela','skurwielem','skurwielu','skurwysyn','skurwysynow','skurwysynow','skurwysyna','skurwysynem','skurwysynu','skurwysyny','skurwysynski','skurwysynski','skurwysynstwo','skurwysynstwo','spierdalac','spierdalac','spierdala','spierdalal','spierdalala','spierdalal','spierdalalcie','spierdalala','spierdalajacy','spierdalajacy','spierdolic','spierdolic','spierdoli','spierdolila','spierdolilo','spierdola','spierdola','srac','srac','srajacy','srajacy','srajac','srajac','sraj','sukinsyn','sukinsyny','sukinsynom','sukinsynowi','sukinsynow','sukinsynow','smierdziel','udupic','ujebac','ujebac','ujebal','ujebal','ujebana','ujebany','ujebie','ujebala','ujebala','upierdalac','upierdalac','upierdala','upierdoli','upierdolic','upierdolic','upierdoli','upierdola','upierdola','upierdoleni','wjebac','wjebac','wjebie','wjebia','wjebia','wjebiemy','wjebiecie','wkurwiac','wkurwiac','wkurwi','wkurwia','wkurwial','wkurwial','wkurwiajacy','wkurwiajacy','wkurwiajaca','wkurwiajaca','wkurwic','wkurwic','wkurwi','wkurwiacie','wkurwiaja','wkurwiali','wkurwia','wkurwia','wkurwimy','wkurwicie','wkurwiacie','wkurwic','wkurwic','wkurwia','wpierdalac','wpierdalac','wpierdalajacy','wpierdalajacy','wpierdol','wpierdolic','wpierdolic','wpizdu','wyjebac','wyjebac','wyjebali','wyjebal','wyjebac','wyjebala','wyjebaly','wyjebie','wyjebia','wyjebia','wyjebiesz','wyjebie','wyjebiecie','wyjebiemy','wypieprzac','wypieprzac','wypieprza','wypieprzal','wypieprzal','wypieprzala','wypieprzala','wypieprzy','wypieprzyla','wypieprzyla','wypieprzyl','wypieprzyl','wypierdal','wypierdalac','wypierdalac','wypierdala','wypierdalaj','wypierdalal','wypierdalal','wypierdalala','wypierdalala','wypierdalac','wypierdolic','wypierdolic','wypierdoli','wypierdolimy','wypierdolicie','wypierdola','wypierdola','wypierdolili','wypierdolil','wypierdolil','wypierdolila','wypierdolila','zajebac','zajebac','zajebie','zajebia','zajebia','zajebial','zajebial','zajebala','zajebiala','zajebali','zajebana','zajebani','zajebane','zajebany','zajebanych','zajebanym','zajebanymi', 'zapieprzyc','zapieprzyc','zapieprzy','zapieprzyl','zapieprzyl','zapieprzyla','zapieprzyla','zapieprza','zapieprza','zapieprzy','zapieprzymy','zapieprzycie','zapieprzysz','zapierdala','zapierdalac','zapierdalac','zapierdalaja','zapierdalal','zapierdalaj','zapierdalajcie','zapierdalala','zapierdalala','zapierdalali','zapierdalajacy','zapierdalajacy','zapierdolic','zapierdolic','zapierdoli','zapierdolil','zapierdolil','zapierdolila','zapierdolila','zapierdola','zapierdola','zapierniczac','zapierniczajacy','zasrac','zasranym','zasrywac','zasrywajacy','zesrywac','zesrywajacy','zjebac','zjebac','zjebal','zjebal','zjebala','zjebala','zjebana','zjebia','zjebali','zjeby']
    
    containsBadWord = False
    remove = False
    
    if (msg == "!sync" and message.author.id == 386237687008591895):
        await tree.sync()
        await message.channel.send("Zsynchronizowano drzewo!")

    for i in bannedWords:
        if msgLowercaseNoPolish.find(i) != -1:
            containsBadWords = True

    if (time[0] < 20 and time[0] >= 5 and containsBadWord):
        remove = True

    if ((remove and message.author.id not in badGuys) or (containsBadWords and message.author.id in badGuys)) and message.author.id != bot.user.id:
        if remove:
            toRemove = await message.channel.send("<@"+str(sender.id)+">!!! Zgodnie z paragrafem §1.8 na kanale <#935612476156936272> o godzinie "+timeNow+" czasu polskiego panuje bezwzględny zakaz używania przekleństw (z wyjątkami opisanymi w tym podpunkcie oraz za wyjątkiem boskiego Pabito). W związku z powyższym wiadomość została usunięta. Pilnuj się!")
        else:
            toRemove = await message.channel.send("<@"+str(sender.id)+"Na mocy cyrografu zawartego dnia 15-10-2023 każda twa wiadomość nie zawierająca słowa z listy wulgaryzmów serwerowych została usuinięta!")
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

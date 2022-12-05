# -*- coding: utf-8 -*-
import env
import discord
from discord.utils import get
from math import floor
from datetime import datetime
import pytz
from discord.ext import commands
from PIL import Image
import os
from random import randrange

roles = [698047161245630545,698047575013457931,703327203068346388,723329755465777193,732345037798506497,736570299537031280,736570295954964542,736570323234848930,36570319921348619,736571825043013672,736571823600435280]
mee6 = 159985870458322944
counting = 935612354832511026
guild = discord.Object(id=697876849036099726)

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

@bot.event
async def on_message(message):
    guild = message.guild
    msg = message.content
    msgLowercase = msg.lower()
    msgLowercaseNoPolish = msgLowercase.replace("ą","a").replace("ć","c").replace("ę","e").replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").replace("ż","z").replace("ź","z")
    sender = message.author

    IST = pytz.timezone('Europe/Warsaw')
    time = [datetime.now(IST).hour,datetime.now(IST).minute,datetime.now(IST).second]
    timeString = [str(time[0]),str(time[1]),str(time[2])]
    for i in range(len(timeString)):
        if len(timeString[i])==1:
            timeString[i] = "0"+timeString[i]
    timeNow = timeString[0]+":"+timeString[1]+":"+timeString[2]
    bannedWords = ['chuj','chuja','chujek','chuju','chujem','chujnia','chujowy','chujowa','chujowe','cipa','cipe','cipe','cipa','cipie','dojebac','dojebac','dojebie','dojebal','dojebal','dojebala','dojebala','dojebalem','dojebalem','dojebalam','dojebalam','dojebie','dojebie','dopieprzac','dopieprzac','dopierdalac','dopierdalac','dopierdala','dopierdalal','dopierdalal','dopierdalala','dopierdalala','dopierdoli','dopierdolil','dopierdolil','dopierdole','dopierdole','dopierdoli','dopierdalajacy','dopierdalajacy','dopierdolic','dopierdolic','huj','hujek','hujnia','huja','huje','hujem','huju','jebac','jebac','jebal','jebal','jebie','jebia','jebia','jebak','jebaka','jebal','jebal','jebany','jebane','jebanka','jebanko','jebankiem','jebanymi','jebana','jebanym','jebanej','jebana','jebana','jebani','jebanych','jebanymi','jebcie','jebiacy','jebiacy','jebiaca','jebiaca','jebiacego','jebiacego','jebiacej','jebiacej','jebia','jebia','jebie','jebie','jebliwy','jebnac','jebnac','jebnac','jebnac','jebnal','jebnal','jebna','jebna','jebnela','jebnela','jebnie','jebnij','jebut','koorwa','korwa','kurestwo','kurew','kurewski','kurewska','kurewskiej','kurewska','kurewska','kurewsko','kurewstwo','kurwa','kurwaa','kurwami','kurwa','kurwe','kurwe','kurwie','kurwiska','kurwo','kurwy','kurwach','kurwami','kurewski','kurwiarz','kurwiacy','kurwica','kurwic','kurwic','kurwidolek','kurwik','kurwiki','kurwiszcze','kurwiszon','kurwiszona','kurwiszonem','kurwiszony','kutas','kutasa','kutasie','kutasem','kutasy','kutasow','kutasow','kutasach','kutasami','matkojebca','matkojebcy','matkojebca','matkojebca','matkojebcami','matkojebcach','nabarlozyc','najebac','najebac','najebal','najebal','najebala','najebala','najebane','najebany','najebana','najebana','najebie','najebia','najebia','naopierdalac','naopierdalac','naopierdalal','naopierdalal','naopierdalala','naopierdalala','naopierdalala','napierdalac','napierdalac','napierdalajacy','napierdalajacy','napierdolic','napierdolic','nawpierdalac','nawpierdalac','nawpierdalal','nawpierdalal','nawpierdalala','nawpierdalala','obsrywac','obsrywac','obsrywajacy','obsrywajacy','odpieprzac','odpieprzac','odpieprzy','odpieprzyl','odpieprzyl','odpieprzyla','odpieprzyla','odpierdalac','odpierdalac','odpierdol','odpierdolil','odpierdolil','odpierdolila','odpierdolila','odpierdoli','odpierdalajacy','odpierdalajacy','odpierdalajaca','odpierdalajaca','odpierdolic','odpierdolic','odpierdoli','odpierdolil','opieprzajacy','opierdalac','opierdalac','opierdala','opierdalajacy','opierdalajacy','opierdol','opierdolic','opierdolic','opierdoli','opierdola','opierdola','piczka','pieprzniety','pieprzniety','pieprzony','pierdel','pierdlu','pierdola','pierdola','pierdolacy','pierdolacy','pierdolaca','pierdolaca','pierdol','pierdole','pierdolenie','pierdoleniem','pierdoleniu','pierdole','pierdolec','pierdola','pierdola','pierdolic','pierdolicie','pierdolic','pierdolil','pierdolil','pierdolila','pierdolila','pierdoli','pierdolniety','pierdolniety','pierdolisz','pierdolnac','pierdolnac','pierdolnal','pierdolnal','pierdolnela','pierdolnela','pierdolnie','pierdolniety','pierdolnij','pierdolnik','pierdolona','pierdolone','pierdolony','pierdolki','pierdzacy','pierdziec','pierdziec','pizda','pizda','pizde','pizde','pizdzie','pizdzie','pizdnac','pizdnac','pizdu','podpierdalac','podpierdalac','podpierdala','podpierdalajacy','podpierdalajacy','podpierdolic','podpierdolic','podpierdoli','pojeb','pojeba','pojebami','pojebani','pojebanego','pojebanemu','pojebani','pojebany','pojebanych','pojebanym','pojebanymi','pojebem','pojebac','pojebac','pojebalo','popierdala','popierdalac','popierdalac','popierdolic','popierdolic','popierdoli','popierdolonego','popierdolonemu','popierdolonym','popierdolone','popierdoleni','popierdolony','porozpierdalac','porozpierdala','porozpierdalac','poruchac','poruchac','przejebac','przejebane','przejebac','przyjebali','przepierdalac','przepierdalac','przepierdala','przepierdalajacy','przepierdalajacy','przepierdalajaca','przepierdalajaca','przepierdolic','przepierdolic','przyjebac','przyjebac','przyjebie','przyjebala','przyjebala','przyjebal','przyjebal','przypieprzac','przypieprzac','przypieprzajacy','przypieprzajacy','przypieprzajaca','przypieprzajaca','przypierdalac','przypierdalac','przypierdala','przypierdoli','przypierdalajacy','przypierdalajacy','przypierdolic','przypierdolic','qrwa','rozjebac','rozjebac','rozjebie','rozjebala','rozjebia','rozpierdalac','rozpierdalac','rozpierdala','rozpierdolic','rozpierdolic','rozpierdole','rozpierdoli','rozpierducha','skurwic','skurwiel','skurwiela','skurwielem','skurwielu','skurwysyn','skurwysynow','skurwysynow','skurwysyna','skurwysynem','skurwysynu','skurwysyny','skurwysynski','skurwysynski','skurwysynstwo','skurwysynstwo','spieprzac','spieprzac','spieprza','spieprzaj','spieprzajcie','spieprzaja','spieprzaja','spieprzajacy','spieprzajacy','spieprzajaca','spieprzajaca','spierdalac','spierdalac','spierdala','spierdalal','spierdalala','spierdalal','spierdalalcie','spierdalala','spierdalajacy','spierdalajacy','spierdolic','spierdolic','spierdoli','spierdolila','spierdolilo','spierdola','spierdola','srac','srac','srajacy','srajacy','srajac','srajac','sraj','sukinsyn','sukinsyny','sukinsynom','sukinsynowi','sukinsynow','sukinsynow','smierdziel','udupic','ujebac','ujebac','ujebal','ujebal','ujebana','ujebany','ujebie','ujebala','ujebala','upierdalac','upierdalac','upierdala','upierdoli','upierdolic','upierdolic','upierdoli','upierdola','upierdola','upierdoleni','wjebac','wjebac','wjebie','wjebia','wjebia','wjebiemy','wjebiecie','wkurwiac','wkurwiac','wkurwi','wkurwia','wkurwial','wkurwial','wkurwiajacy','wkurwiajacy','wkurwiajaca','wkurwiajaca','wkurwic','wkurwic','wkurwi','wkurwiacie','wkurwiaja','wkurwiali','wkurwia','wkurwia','wkurwimy','wkurwicie','wkurwiacie','wkurwic','wkurwic','wkurwia','wpierdalac','wpierdalac','wpierdalajacy','wpierdalajacy','wpierdol','wpierdolic','wpierdolic','wpizdu','wyjebac','wyjebac','wyjebali','wyjebal','wyjebac','wyjebala','wyjebaly','wyjebie','wyjebia','wyjebia','wyjebiesz','wyjebie','wyjebiecie','wyjebiemy','wypieprzac','wypieprzac','wypieprza','wypieprzal','wypieprzal','wypieprzala','wypieprzala','wypieprzy','wypieprzyla','wypieprzyla','wypieprzyl','wypieprzyl','wypierdal','wypierdalac','wypierdalac','wypierdala','wypierdalaj','wypierdalal','wypierdalal','wypierdalala','wypierdalala','wypierdalac','wypierdolic','wypierdolic','wypierdoli','wypierdolimy','wypierdolicie','wypierdola','wypierdola','wypierdolili','wypierdolil','wypierdolil','wypierdolila','wypierdolila','zajebac','zajebac','zajebie','zajebia','zajebia','zajebial','zajebial','zajebala','zajebiala','zajebali','zajebana','zajebani','zajebane','zajebany','zajebanych','zajebanym','zajebanymi', 'zapieprzyc','zapieprzyc','zapieprzy','zapieprzyl','zapieprzyl','zapieprzyla','zapieprzyla','zapieprza','zapieprza','zapieprzy','zapieprzymy','zapieprzycie','zapieprzysz','zapierdala','zapierdalac','zapierdalac','zapierdalaja','zapierdalal','zapierdalaj','zapierdalajcie','zapierdalala','zapierdalala','zapierdalali','zapierdalajacy','zapierdalajacy','zapierdolic','zapierdolic','zapierdoli','zapierdolil','zapierdolil','zapierdolila','zapierdolila','zapierdola','zapierdola','zapierniczac','zapierniczajacy','zasrac','zasranym','zasrywac','zasrywajacy','zesrywac','zesrywajacy','zjebac','zjebac','zjebal','zjebal','zjebala','zjebala','zjebana','zjebia','zjebali','zjeby']
    remove = False
    if time[0] < 20 and time[0] >= 5:
        for i in bannedWords:
            if msgLowercaseNoPolish.find(i) != -1:
                remove = True

    if remove:
        toRemove = await message.channel.send("<@"+str(sender.id)+">!!! Zgodnie z paragrafem §1.8 na kanale <#935612476156936272> o godzinie "+timeNow+" czasu polskiego panuje bezwzględny zakaz używania przekleństw (z wyjątkami opisanymi w tym podpunkcie). W związku z powyższym wiadomość została usunięta. Pilnuj się!")
        await message.delete()
        await toRemove.delete(delay=15)
    elif message.channel.id == counting:
        pass # do zrobienia
    elif len(message.mentions) > 0 and message.author.id == mee6:
        userID = msg[(msg.find("<@")+2):msg.find(">")]
        #theUser = get(guild.members, id=userID)
        theUser = message.mentions[0]
        level = int(msg[(msg.find("level")+6):msg.find("!")])
        if level <= 100:
            rankPosition = floor(level/10)
            if rankPosition > 100:
                rankPosition = 10
            roleToGiveID = roles[rankPosition]
            roleToGive = discord.utils.get(guild.roles,id=roleToGiveID)
            await theUser.add_roles(roleToGive)
            if rankPosition > 0:
                roleToRevokeID = roles[rankPosition-1]
                roleToRevoke = discord.utils.get(guild.roles,id=roleToRevokeID)
                await theUser.remove_roles(roleToRevoke)
            if level/10 == floor(level/10):
                sendedMessage = await message.channel.send("Loading...")
                await sendedMessage.edit(content="Gratulacje <@"+str(userID)+"> Właśnie osiągnąłeś rangę <@&"+str(roleToGiveID)+">")
    elif len(message.mentions) > 0 and message.mentions[0] == bot.user and (msgLowercaseNoPolish.content.find("przedstaw sie") != -1):
        await message.channel.send("Siema! Jestem sobie botem napisanym przez Kasztandora i tak sobie tutaj działam i robię co do mnie należy. Pozdrawiam wszystkich i życzę udanego dnia!")

bot.run(TOKEN)

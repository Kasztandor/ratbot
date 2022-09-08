# to ratcraft
token = "MTAxNjQxNDc0NjQ2MDgyMzU2Mg.GiJyQJ.FKMwOLjSNJGfDKTwdj-zWgotmjRJnmO_FoAhok"
roles = [698047161245630545,698047575013457931,703327203068346388,723329755465777193,732345037798506497,736570299537031280,736570295954964542,736570323234848930,736570319921348619,736571825043013672,736571823600435280]
mee6 = 159985870458322944

# to testbot
#token = "NzIyNzQ0NzI1NzU2NzA2ODU3.GXlyrf.yGGwtT5EvsvbmrSgUhDf0VPcUUv5rYsQRSmzpE"
#roles = [1016433847296086037,1016433864303980545,1016433874043162655,1016433882507255829,1016433889864069211,1016433896654639114,1016433907220107274,1016433916862799893,1016433924211232899,1016433930418798655,1016433939096817836]
#mee6 = 386237687008591895
counting = 1017465965883170917

import discord
from discord.utils import get
from math import floor
from datetime import datetime
import pytz

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

@client.event
async def on_message(message):
    guild = message.guild
    msg = message.content
    sender = message.author

    IST = pytz.timezone('Europe/Warsaw')
    hour = datetime.now(IST).hour
    minute = datetime.now(IST).minute
    second = datetime.now(IST).second
    timeNow = str(hour)+":"+str(minute)+":"+str(second)
    bannedWords = ["kurwa","kurwi","pierdole","pierdolę","jebać","jebac","pierdolić","pierdolic","fuck","shit","chuj","huj"]
    remove = False
    if hour < 20 and hour >= 5:
        for i in bannedWords:
            if msg.find(i) != -1:
                remove = True

    if message.channel.id == counting:
        pass # do zrobienia
    if remove:
        toRemove = await message.channel.send("<@"+str(sender.id)+">!!! Zgodnie z paragrafem §1.8 na kanale <#935612476156936272> o godzinie "+timeNow+" czasu polskiego panuje bezwzględny zakaz używania przekleństw (z wyjątkami opisanymi w tym podpunkcie). W związku z powyższym wiadomość została usunięta. Pilnuj się!")
        await message.delete()
        await toRemove.delete(delay=15)
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
    elif len(message.mentions) > 0 and message.mentions[0] == client.user and (message.content.find("przedstaw się") != -1 or message.content.find("przedstaw sie") != -1):
        await message.channel.send("Siema! Jestem sobie botem napisanym przez Kasztandora i tak sobie tutaj działam i robię co do mnie należy. Pozdrawiam wszystkich i życzę udanego dnia!")

client.run(token)
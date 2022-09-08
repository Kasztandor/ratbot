# to testbot
#roles = [1016433847296086037,1016433864303980545,1016433874043162655,1016433882507255829,1016433889864069211,1016433896654639114,1016433907220107274,1016433916862799893,1016433924211232899,1016433930418798655,1016433939096817836]
# to ratcraft
roles = [698047161245630545,698047575013457931,703327203068346388,723329755465777193,732345037798506497,736570299537031280,736570295954964542,736570323234848930,736570319921348619,736571825043013672,736571823600435280]

import discord
from discord.utils import get
from math import floor

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
    if len(message.mentions) > 0 and message.author.id == 159985870458322944: # Kasztandor: 386237687008591895 MEE6: 159985870458322944
        guild = message.guild
        msg = message.content
        userID = msg[(msg.find("<@")+2):msg.find(">")]
        #theUser = get(guild.members, id=userID)
        theUser = message.mentions[0]
        level = int(msg[(msg.find("level")+6):msg.find("!")])
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
            await message.channel.send("Gratulacje <@"+str(userID)+"> Właśnie osiągnąłeś rangę <@&"+str(roleToGiveID)+">")
    elif len(message.mentions) > 0 and message.mentions[0] == client.user and (message.content.find("przedstaw się") != -1 or message.content.find("przedstaw sie") != -1):
        await message.channel.send("Siema! Jestem sobie botem napisanym przez Kasztandora i tak sobie tutaj działam i robię co do mnie należy. Pozdrawiam wszystkich i życzę udanego dnia!")



client.run('MTAxNjQxNDc0NjQ2MDgyMzU2Mg.GiJyQJ.FKMwOLjSNJGfDKTwdj-zWgotmjRJnmO_FoAhok')

# ratbot: MTAxNjQxNDc0NjQ2MDgyMzU2Mg.GiJyQJ.FKMwOLjSNJGfDKTwdj-zWgotmjRJnmO_FoAhok
# kasztan testbot: NzIyNzQ0NzI1NzU2NzA2ODU3.GXlyrf.yGGwtT5EvsvbmrSgUhDf0VPcUUv5rYsQRSmzpE
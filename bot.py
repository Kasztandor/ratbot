roles = [1016433847296086037,1016433864303980545,1016433874043162655,1016433882507255829,1016433889864069211,1016433896654639114,1016433907220107274,1016433916862799893,1016433924211232899,1016433930418798655,1016433939096817836]
#[698047161245630545,698047575013457931,703327203068346388,723329755465777193,732345037798506497,736570299537031280,736570295954964542,736570323234848930,736570319921348619,736571825043013672,736571823600435280]

import discord
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
    if message.author == client.user:
        return

    if message.author.id == 386237687008591895:
        msg = message.content
        userID = msg[(msg.find("<@")+2):msg.find(">")]
        level = int(msg[(msg.find("level")+6):msg.find("!")])
        if level > 100:
            fixedLevel = 100
        else:
            fixedLevel = level
        roleToGive = roles[floor(fixedLevel/10)]
        if fixedLevel < 10:
            roleToRevoke = None
        else:
            roleToRevoke = roles[floor(fixedLevel/10)-1]
        await message.channel.send(userID+" "+str(fixedLevel)+": +<@&"+str(roleToGive)+"> -<@&"+str(roleToRevoke)+">")
        print(message.content)

    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run('NzIyNzQ0NzI1NzU2NzA2ODU3.GXlyrf.yGGwtT5EvsvbmrSgUhDf0VPcUUv5rYsQRSmzpE')
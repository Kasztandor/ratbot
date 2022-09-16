# To testbot
TOKEN = "NzIyNzQ0NzI1NzU2NzA2ODU3.GXlyrf.yGGwtT5EvsvbmrSgUhDf0VPcUUv5rYsQRSmzpE"
roles = [1016433847296086037,1016433864303980545,1016433874043162655,1016433882507255829,1016433889864069211,1016433896654639114,1016433907220107274,1016433916862799893,1016433924211232899,1016433930418798655,1016433939096817836]
mee6 = 386237687008591895
"""
import interactions

bot = interactions.Client(token=TOKEN)

@bot.command(
    name="pingus",
    description="Bot odpowie ci pong!",
)
async def pingus(ctx: interactions.CommandContext):
    await ctx.send("Pong!")

@bot.event
async def on_message(message):
    print("dziala")

bot.start()
"""

import discord
from discord.ext import commands

#guilds = [discord.Object(id=690599090928484403),discord.Object(id=690599090928484403)]

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.sycned = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=690599090928484403))
            self.synced = True
        print("Bot is online")

bot = abot()
tree = discord.app_commands.CommandTree(bot)

@tree.command(guild=guild)
async def post(interaction: discord.Interaction):
    await interaction.response.send_message("office")

@tree.command(name="ping",description="uwu",guild=discord.Object(id=690599090928484403))
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Pong")

@tree.command(name="refresh",description="uhu",guild=discord.Object(id=690599090928484403))
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(interaction.guild_id)
    await tree.sync(guild=discord.Object(id=interaction.guild_id))
    await tree.sync()

@tree.command(name="test",description="uhu",guild=discord.Object(id=690599090928484403))
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("test")

@tree.command(name="test2",description="uhu")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("test2")

bot.run(TOKEN)


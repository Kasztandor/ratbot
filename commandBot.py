# To testbot
TOKEN = "NzIyNzQ0NzI1NzU2NzA2ODU3.GXlyrf.yGGwtT5EvsvbmrSgUhDf0VPcUUv5rYsQRSmzpE"
roles = [1016433847296086037,1016433864303980545,1016433874043162655,1016433882507255829,1016433889864069211,1016433896654639114,1016433907220107274,1016433916862799893,1016433924211232899,1016433930418798655,1016433939096817836]
mee6 = 386237687008591895

import interactions

bot = interactions.Client(token=TOKEN)

@bot.command(
    name="ping",
    description="Bot odpowie ci pong!",
)
async def ping(ctx: interactions.CommandContext):
    await ctx.send("Pong!")

@bot.event
async def on_message(message):
    print("dziala")

bot.start()
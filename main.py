from alias import aliaschecker
import discord
from discord.ext import commands
import os
os.system("color")

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

aliasbot = aliaschecker("INPUT WEBHOOK HERE", "ENTER VAT AMOUNT HERE - e.g. 19% = 1.19")


@client.event
async def on_ready():
    print("Logged In {}".format(client.user.name))


@client.command()
async def a(ctx, *args):
    aliasbot.check(args)



client.run("DISCORD BOT TOKEN")

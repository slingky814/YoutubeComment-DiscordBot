import os
import discord
import random
from time import sleep
from dotenv import load_dotenv
from discord.ext import commands
from videoURL import videoURL
from comments import get_comment


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')
COMMENT = "Truly disgusting that some \"people\" would do this horrible thing."
bot = commands.Bot(command_prefix='!')
links = []

@bot.event
async def on_ready():
    print("Bot is online.\n")

@bot.command(pass_context = True, help = "Gets a random YouTube comment")
async def comment(ctx):
    if ctx.author.bot:
        return;

    try:

        url = videoURL()
        print(url+"\n")

        links.append(url)
        condenseLinks()

        comment = get_comment(url)
        print("Comment: " + comment)

        await ctx.send(comment)
        
    except:
        await ctx.send("URL fail, try again")


@bot.command(pass_context=True, help = "Removes messages from channel; specify how many messages to be removed")
async def clear(ctx, number):
    number =  int(number)
    await ctx.channel.purge(limit = 100)

@bot.command(pass_context=True, help = "Gets the youtube link of the last comment")
async def link(ctx):
    await ctx.send(links[len(links)-1])

def condenseLinks():
    if len(links) == 2:
        links.pop(0)

bot.run(TOKEN)

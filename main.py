import discord
from discord.ext import commands
from discord.ext import tasks
import os
import data_grabber
import tqdm
from pytube import *
from art import *

intents = discord.Intents().default()
intents.message_content = True
bot = commands.Bot(command_prefix = "holo> ", intents = intents)
bot_status = 1069251825045344326
developer = 535335309769179136
hologra_update = []
daily_hologra = []

@bot.command(name = "hello", help = "Say hello.")
async def hello(ctx):
    await ctx.reply("Yo dazo!")

@bot.command(name = "get_latest_hologra", help = "Get the newest Hologra episode.")
async def getvid(ctx):
    episode = data_grabber.get_latest_Hologra()
    await ctx.send(f"[{episode.url}]")

@bot.command(name = "get_random_hologra", help = "Get a random Hologra episode.")
async def getrandomvid(ctx):
    episode = data_grabber.get_random_Hologra()
    await ctx.send(f"[{episode.url}]")

@bot.command(name = "set_update_channel", help = "Add this channel as one of the update channel.")
@commands.has_permissions(administrator = True)
async def update_channel_add(ctx):
    try:
        if ctx.channel.id not in hologra_update:
            hologra_update.append(ctx.channel.id)
            await ctx.reply(f"This channel is added to the list of channel to recieve update about new Hologra!")
        else:
            await ctx.reply(f"This channel is already one of the update channel.")
    except:
        await ctx.reply(f"Something went wrong.")

@bot.command(name = "delete_update_channel", help = "Remove this channel from the list of update channel.")
@commands.has_permissions(administrator = True)
async def update_channel_remove(ctx):
    try:
        if ctx.channel.id in hologra_update:
            hologra_update.remove(ctx.channel.id)
            await ctx.reply(f"This channel is no longer one of the update channel.")
        else:
            await ctx.reply(f"This channel is not one of the update channel.")
    except:
        await ctx.reply(f"Something went wrong.")

@bot.command(name = "set_daily_channel", help = "Add this channel as one of the daily Hologra channel.")
@commands.has_permissions(administrator = True)
async def daily_channel_add(ctx):
    try:
        if ctx.channel.id not in daily_hologra:
            daily_hologra.append(ctx.channel.id)
            await ctx.reply(f"This channel is added to the list of channel to recieve an Hologra everyday!")
        else:
            await ctx.reply(f"This channel is already one of the daily channel.")
    except:
        await ctx.reply(f"Something went wrong.")

@bot.command(name = "delete_daily_channel", help = "Remove this channel from the list of daily channel.")
@commands.has_permissions(administrator = True)
async def daily_channel_remove(ctx):
    try:
        if ctx.channel.id in daily_hologra:
            daily_hologra.remove(ctx.channel.id)
            await ctx.reply(f"This channel is no longer one of the daily channel.")
        else:
            await ctx.reply(f"This channel is not one of the daily channel.")
    except:
        await ctx.reply(f"Something went wrong.")

@bot.command(name = "strike_three_oni_out", help = "(Only usable by the Developer)")
async def complete_program(ctx):
    if ctx.author.id == developer:
        await ctx.reply(f"aaaaa~")
        finish_program()

@tasks.loop(minutes = 5)
async def check_for_new_Hologra():
    new_hologra = data_grabber.update()
    if new_hologra != None:
        for channel in hologra_update:
            try:
                send_location = bot.get_channel(channel)
                send_location.send("@everyone")
                for episode in new_hologra:
                    send_location.send(f"[{episode.url}]")
            except:
                pass

@tasks.loop(hours = 24)
async def send_daily_hologra():
    for channel in hologra_update:
        try:
            send_location = bot.get_channel(channel)
            episode = data_grabber.get_random_Hologra()
            await send_location.send(f"@everyone \nToday's random Hologra is: {episode.url}")
        except:
            pass

@bot.event
async def on_ready():
    print(f"Nakirium v1.0 had been installed as {bot.user}")
    channel = bot.get_channel(bot_status)
    await channel.send("Nakiri-online!")
    check_for_new_Hologra.start()
    send_daily_hologra.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"{message.author} : {message.content}")
    await bot.process_commands(message)

def initiation():
    global daily_hologra, hologra_update
    data_grabber.init()
    update_file = open("data/hologra_update.txt", "r+")
    daily_file = open("data/daily_hologra.txt", "r+")
    daily_hologra = daily_file.read().splitlines()
    daily_hologra = [int(channel) for channel in daily_hologra]
    hologra_update = update_file.read().splitlines()
    hologra_update = [int(channel) for channel in hologra_update]
    update_file.close()
    daily_file.close()

def finish_program():
    global daily_hologra, hologra_update
    update_file = open("data/hologra_update.txt", "w+")
    daily_file = open("data/daily_hologra.txt", "w+")
    print("Close program:")
    for channel in tqdm.tqdm(daily_hologra):
        daily_file.write(f"{channel}\n")
    for channel in tqdm.tqdm(hologra_update):
        update_file.write(f"{channel}\n")
    exit()

#-------------------------------------
initiation()
bot.run(os.environ['TOKEN'])

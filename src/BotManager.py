import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import configs.DefaultConfig as defaultConfig
import utils.DiscordUtils as discordUtils

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("Bot is online...")

@bot.event
async def on_member_join(member):
    print("New member has joined..")
    guild = member.guild
    guildname = guild.name

    dmchannel = await member.create_dm()

    await dmchannel.send(f"Welcome to {guildname}! Feel free to ask me questions here.")

@bot.command(aliases = ["about"])
async def help(ctx):
    MyEmbed = discord.Embed(title = "Commands",
                            description="Welcome Master! I am Alfred Pennyworth - butler to Bruce Wayne, the CEO of Wayne Enterprises. Mr. Wayne is getting ready, but here are the Commands that you can use for me. If you require a private message with me, you can interact with it normally without issuing commands",
                            color = discord.Color.dark_purple())
    
    MyEmbed.add_field(name = "!query", value = "Use this command to allow you to communicate with me on the Server. Please wrap your questions with quotation marks.", inline = False)
    MyEmbed.add_field(name = "!pm", value = "Use this command allows you to send me a private message.", inline = False)
    await ctx.send(embed = MyEmbed)

bot.run(defaultConfig.discord_sdk)

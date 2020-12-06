# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from cog import Chess 


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix = '[]')


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.event
async def on_message(msg):
    await bot.process_commands(msg)
        


bot.add_cog(Chess(bot))
bot.run(TOKEN)
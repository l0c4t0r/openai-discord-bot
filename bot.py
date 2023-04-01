"""OpenAI Relayer Bot"""
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    print(f"Responding to message in {message.channel.name}")
    if hasattr(message.channel, "parent"):
        history = message.channel.history()
        async for m in history:
            print(f"{m.author}: {m.content}")
        await message.channel.send("Responding in thread")
    else:
        await message.channel.send("Responding in main")
        await message.create_thread(name=message.content[:20], auto_archive_duration=1440)

client.run(TOKEN)
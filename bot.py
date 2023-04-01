"""OpenAI Relayer Bot"""
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from openai_discord_bot.chat import get_chat_completion, parse_history

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

COMMAND_PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord")


@bot.listen("on_message")
async def on_message(message: discord.Message):
    # Don't process if it's a bot message, or if it is a command
    if (message.author == bot.user) or message.content.startswith(COMMAND_PREFIX):
        return

    if hasattr(message.channel, "parent"):
        messages = await parse_history(
            history=message.channel.history(), bot_user=bot.user
        )
        chat_response = get_chat_completion(messages)
        await message.channel.send(chat_response)


@bot.command(name="new")
async def new_thread(ctx: commands.Context, thread_name: str):
    if hasattr(ctx.channel, "parent"):
        return
    await ctx.message.create_thread(name=thread_name)
    await ctx.message.delete()


@bot.command(name="system")
async def system_message(ctx: commands.Context, message: str):
    await ctx.message.delete()
    if not hasattr(ctx.channel, "parent"):
        return
    await ctx.send(f"[SYSTEM] {message}")
    messages = await parse_history(history=ctx.history(), bot_user=bot.user)

    print(messages)
    chat_response = get_chat_completion(messages)
    await ctx.send(chat_response)


bot.run(TOKEN)

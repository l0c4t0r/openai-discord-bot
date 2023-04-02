"""OpenAI Relayer Bot"""
import discord
from discord.ext import commands

from openai_discord_bot.chat import create_message, get_chat_completion, parse_history
from openai_discord_bot.config import DISCORD_TOKEN
from openai_discord_bot.enums import Roles

COMMAND_PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    """When bot connects to discord"""
    print(f"{bot.user.name} has connected to Discord")


@bot.listen("on_message")
async def on_message(message: discord.Message):
    """Listen to messages and relay to chatGPT"""
    # Don't process if it's a bot message, or if it is a command
    if (message.author == bot.user) or message.content.startswith(COMMAND_PREFIX):
        return

    # Only process latest message in random channel
    if message.channel.name == "random":
        chat_response = await get_chat_completion(
            [create_message(Roles.USER, message.content)]
        )
        await message.channel.send(chat_response)

    if hasattr(message.channel, "parent"):
        messages = await parse_history(
            history=message.channel.history(), bot_user=bot.user
        )
        chat_response = await get_chat_completion(messages)
        await message.channel.send(chat_response)


@bot.command(name="new")
async def new_thread(ctx: commands.Context, thread_name: str):
    """Create new thread with provided name"""
    # Don't allow creating subthreads
    if hasattr(ctx.channel, "parent") or ctx.channel.name == "random":
        return
    await ctx.message.create_thread(name=thread_name)


@bot.command(name="system")
async def system_message(ctx: commands.Context, message: str):
    """Send system messages"""
    await ctx.message.delete()
    if not hasattr(ctx.channel, "parent"):
        return
    await ctx.send(f"[SYSTEM] {message}")
    messages = await parse_history(history=ctx.history(), bot_user=bot.user)

    print(messages)
    chat_response = await get_chat_completion(messages)
    await ctx.send(chat_response)


bot.run(DISCORD_TOKEN)

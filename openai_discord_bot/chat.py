import discord
import openai

from openai_discord_bot.config import OPENAI_API_KEY
from openai_discord_bot.enums import Roles

openai.api_key = OPENAI_API_KEY


async def get_chat_completion(messages, model_id: str = "gpt-3.5-turbo"):
    """Get chat completion from openai api"""
    response = await openai.ChatCompletion.acreate(messages=messages, model=model_id)
    return response["choices"][0]["message"]["content"]


def create_message(role: Roles, content: str):
    """Create message from roles and message content"""
    return {"role": role.value, "content": content}


async def parse_history(history, bot_user: discord.User) -> list[dict[str, str]]:
    """Parse thread history into openAI message"""
    all_messages = []
    async for message in history:
        if not message.content:
            continue
        if message.author == bot_user:
            if message.content.startswith("[SYSTEM]"):
                entry = create_message(Roles.SYSTEM, message.content[9:])
            else:
                entry = create_message(Roles.ASSISTANT, message.content)
        else:
            entry = create_message(Roles.USER, message.content)

        all_messages.insert(0, entry)

    return all_messages

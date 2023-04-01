import os
import openai

from openai_discord_bot.enums import Roles
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_chat_completion(messages, model_id: str = "gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(messages=messages, model=model_id)
    return response["choices"][0]["message"]["content"]


def create_message(role: Roles, content: str):
    return {"role": role.value, "content": content}


async def parse_history(history, bot_user) -> list[dict[str, str]]:
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

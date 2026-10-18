import os

import discord
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

llm = AsyncOpenAI(base_url=os.environ["OPENAI_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
MODEL = os.environ.get("MODEL", "llama-3.3-70b-instruct")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author.bot or not client.user.mentioned_in(message):
        return
    prompt = message.clean_content.replace(f"@{client.user.name}", "").strip()
    async with message.channel.typing():
        resp = await llm.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
        )
    await message.reply(resp.choices[0].message.content[:2000])


client.run(os.environ["DISCORD_TOKEN"])

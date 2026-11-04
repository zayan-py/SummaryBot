import discord
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot()

# Grabs prompt from file
with open('AI-Prompt.txt') as file:
    prompt = file.read()

# Initiates Discord bot
@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')

# Main command
@bot.slash_command(guild_ids=[1551242720079519814]) 
async def summarise(ctx, amount: int = discord.Option(int, description="How many messages to read?")):
    
    amount += 1
    
    await ctx.defer()

    messages = []
    user_avatars = {}

    # Grabs messages from the chat history
    async for message in ctx.channel.history(limit=amount):
        if message.content:
            messages.insert(0, f"{message.author.name}: {message.content}")
            if message.author.name not in user_avatars:
                user_avatars[message.author.name] = message.author.display_avatar.url

    if not messages:
        await ctx.respond("No text messages found to summarize.")
        return
    
    avatar_list_text = "\n".join(
        f"{user}: {url}" for user, url in user_avatars.items()
    )

    # Groups grabbed messages for AI prompting
    formatted_chat = "\n".join(messages)

    # Sends request using AI API
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"User Avatars:\n{avatar_list_text}\n\n" f"Conversation:\n{formatted_chat} "},
        ],
    }

    async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                data = await resp.json()
                summary_text = data["choices"][0]["message"]["content"]

    # Builds Discord emebed with AI response embedded
    embed = discord.Embed(
        title="Conversation Summary",
        description=summary_text,
        color=discord.Color.blurple(),
    )
    
    embed.set_footer(text=f"Summarised {len(messages)} messages with gpt-4o-mini")
   
    embed.set_author(name="SummaryBot", icon_url="https://media.discordapp.net/attachments/1467981906208489523/1565871793414344864/911699f8-6f0c-428b-ad2d-9b5820739c7c.jpg?ex=6ae67b40&is=6ae529c0&hm=8f212df84c277233027dde5cbdc82a5793bf2dc5cc7fdfa73c381ca3f457eb92&=&format=webp&width=1240&height=1240")
    # print(messages) Was used for debugging

    await ctx.respond(embed=embed)

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

bot.run(BOT_TOKEN)
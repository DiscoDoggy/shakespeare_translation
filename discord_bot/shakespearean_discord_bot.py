#what we want is to grab text from the user and send that text to inference.py
# where it then sends translated text back
#https://realpython.com/how-to-make-a-discord-bot-python/ 

import os
import discord
from dotenv.main import load_dotenv

load_dotenv('discord_bot\secrets.env')
TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

print(TOKEN)

@client.event
async def on_ready():
    print(f"{client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("Shi ass bot"):
        await message.channel.send("You a shi ass human")

client.run(TOKEN)
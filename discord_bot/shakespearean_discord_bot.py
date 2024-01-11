#what we want is to grab text from the user and send that text to inference.py
# where it then sends translated text back
#https://realpython.com/how-to-make-a-discord-bot-python/ 

import os
import discord
from database import get_database
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
    #function catches the message the user sent, 
    #deletes the message from the discord server,
    #then cleans and preprocesses the message converting it to a tensor
    #feeds it into the ml model to translate
    #Converts back to text MongoDB stored vocabulary
    #sends the translated message back to the chat. 

    if message.author == client.user:
        return
    
    print(f"Message: {message.content}")
    message_content = message.content
    message_content_len = len(message_content)

    await message.channel.send(type(message_content))
    await message.channel.send(f"message length {message_content_len}")
    # await message.delete()
    await message.channel.send(message.content)

client.run(TOKEN)
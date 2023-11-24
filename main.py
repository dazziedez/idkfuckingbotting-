import discord
from discord.ext import commands
import asyncio
import json


intents = discord.Intents.all()

client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command("help")

with open("config.json", "r") as config: 
	data = json.load(config)
	token = data["token"]


async def load():
	await client.load_extension('cogs.core')
	print('🟪 core extension loaded')

asyncio.run(load())
client.run(token)

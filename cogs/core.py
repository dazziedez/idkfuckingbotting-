import discord
import os
from discord.ext import commands

class Core(commands.Cog, name="Core"):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.content == "<@879083602082684968>":
			await message.reply("uwu")
		
	@commands.Cog.listener()
	async def on_ready(self):

		await self.client.change_presence(status=discord.Status.idle, activity=discord.Activity(
			type=discord.ActivityType.watching, name='loading...'))

		for filename in os.listdir('./cogs'):
			if filename.endswith('.py') and not filename.startswith('core'):
				try:
					await self.client.load_extension(f'cogs.{filename[:-3]}')
					print(f'🟨 {filename} was loaded')

				except Exception as e:
					print(f'🟥 {filename} was not loaded - {e}')
		
		print('🟪 all extensions loaded!!')

		try:
			synced = await self.client.tree.sync()
			print(f"🔁 synced {len(synced)} slash commands")
		except Exception as e:
			print(e)
		
		await self.client.change_presence(activity=discord.Activity(
			type=discord.ActivityType.watching, name="you - .gg/bottle"))
		print(f"🟩 Logged in as {self.client.user} with a {round(self.client.latency * 1000)}ms delay")

async def setup(client):
	await client.add_cog(Core(client))
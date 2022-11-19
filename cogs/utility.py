import discord
import time
import asyncio
import os
from datetime import datetime
from discord import app_commands
from discord import ui
from discord.ext import commands


start_time = time.time()

snipe_message_content = ''
snipe_message_author = None
snipe_message_id = None
sn_author_name = None
delete_time = None
creation_date = None
attachment = None


class Menu(discord.ui.View):

	def __init__(self):
		super().__init__()
		self.value = None

class Utility(commands.Cog):
	def __init__(self, client):
		self.client = client

	@app_commands.command(name='status', description='View info about the running instance of the bot. I '
															  'don\'t know what i\'m saying')
	async def status(self, interaction):

		timeUp = time.time() - start_time
		hours = timeUp / 3600
		minutes = (timeUp / 60) % 60
		seconds = timeUp % 60

		users = 0
		channel = 0
		for guild in self.client.guilds:
			users += len(guild.members)
			channel += len(guild.channels)

		cmdcount = 0
		for _ in self.client.commands:
			cmdcount += 1

		embed = discord.Embed(title=self.client.user.name + '#' + self.client.user.discriminator)
		embed.set_thumbnail(url=self.client.user.avatar.url)
		embed.add_field(name='Owner', value='`bottle#6843`', inline=True)
		embed.add_field(name='Uptime',
						value='`{0:.0f} hours, {1:.0f} minutes and {2:.0f} seconds`'.format(hours, minutes, seconds),
						inline=True)
		embed.add_field(name='Total users', value=f'`{users}`', inline=True)
		embed.add_field(name='Total channels', value=f'`{channel}`', inline=True)
		embed.add_field(name='Bot version', value='`0.6.0`', inline=True)
		embed.add_field(name='Discord.py Version', value=f'`{discord.__version__}`', inline=True)
		embed.add_field(name='Commands count', value=f'`{cmdcount}`', inline=True)
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name='ping', description='View bot\'s latency')
	async def ping(self, interaction):
		before = time.monotonic()
		await interaction.response.send_message("Pinging...")
		ping = (time.monotonic() - before) * 1000
		await interaction.edit_original_response(content=f"Pong! `{int(ping)} ms`")

	@commands.Cog.listener()
	async def on_message_delete(self, message):

		if message.author.bot:
			return

		global snipe_message
		global snipe_message_author
		global sn_author_name
		global snipe_message_id
		global creation_date
		global attachment

		snipe_message = str(message.content)
		snipe_message_author = message.author.id
		snipe_message_id = message.id
		if message.attachments != []:
			attachment = message.attachments[0]
		sn_author_name = message.author
		creation_date = str(message.created_at)

		await asyncio.sleep(60)

		if message.id == snipe_message_id:
			snipe_message_author = None
			snipe_message = None
			snipe_message_id = None
			sn_author_name = None
			creation_date = None
			attachment = None


	@app_commands.command(name='snipe', description='Get last deleted message')
	async def snipe(self, interaction: discord.Interaction):
		if snipe_message_id is None:
			await interaction.response.send_message('There is nothing to snipe!', ephemeral=True)

		else:
			embed = discord.Embed(title=None, description=f'{snipe_message}')
			embed.set_author(
				name=f"{sn_author_name} · at {creation_date[11:-16]}", icon_url=sn_author_name.avatar.url)

			if attachment != None:
				embed.set_image(url=attachment.url)

			await interaction.response.send_message(embed=embed)
			return
	
	@app_commands.command(name="membercount")
	async def members(self, interaction):
		member_count = len(interaction.guild.members)
		user_count = len([m for m in interaction.guild.members if not m.bot])
		await interaction.response.send_message(f"all: `{member_count}`\nusers: `{user_count}`", ephemeral=True)

	@app_commands.command()
	async def extensions(self, interaction):
		message = ''
		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				message = f'{message}\n{filename}'
		await interaction.response.send_message(message, ephemeral=True)
	
	@app_commands.command(name='purge')
	@app_commands.checks.has_permissions(manage_messages=True)
	async def clean(self, interaction, limit: int):
		await interaction.response.send_message(f"Deleting {limit} messages...", ephemeral=True)
		try:
			await interaction.channel.purge(limit=limit + 1)
		except:
			pass
		await interaction.edit_original_response(content=f'Purged {limit} messages')

	

	@app_commands.command(name='slowmode')
	@app_commands.checks.has_permissions(manage_channels=True)
	async def setdelay(self, interaction, seconds: int = None):
		if seconds == None or seconds == 0:
			seconds = 0
			await interaction.channel.edit(slowmode_delay=seconds)
			await interaction.response.send_message(f"Removed the slowmode!", ephemeral=True)
			return
			
		await interaction.channel.edit(slowmode_delay=seconds)
		await interaction.response.send_message(f"The slowmode is now {seconds}", ephemeral=True)

async def setup(client):
	await client.add_cog(Utility(client))
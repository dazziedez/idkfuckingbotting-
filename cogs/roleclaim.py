import discord
import re
import json
import io
import aiohttp, aiofiles

from discord import app_commands
from discord.ext import commands, tasks

guild_id = 874440438604496976
booster_id = 881222980858966017

async def http_get(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as resp:
			if resp.status == 200:
				return await resp.read()


class BoostPerks(commands.Cog):
	def __init__(self, ce):
		self.ce = ce

	@app_commands.command()
	@app_commands.describe(name="Name of your role, dare to type a slur and i ban you for LIFE",
						   color="Hex color for your role, example #2596be",
						   icon="A picture if you want a role icon, only PNG/JPEG allowed")
	async def claim(self, inter, name:str, color:str, icon:discord.Attachment=None):
		await inter.response.defer(thinking=True, ephemeral=True)
		guild = self.ce.get_guild(guild_id)
		boost_role = guild.get_role(booster_id)

		member = guild.get_member(inter.user.id)
		if boost_role not in member.roles:
			return await inter.followup.send("You are not elegible to claim your booster role. Check <#1130928599046819900>")
		
		if icon:
			icon = await http_get(icon.url)

		if color and not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
			color=None
		else:
			color=discord.Color.from_str(color)

		with open('config.json', 'r') as file:
			data = json.load(file)

			boosters = data.get('boosters', {})

			if str(inter.user.id) in boosters:
				role_id = boosters[str(inter.user.id)]
				print(f"User {inter.user.id} found in boosters. Editing role {role_id}.")
				role = guild.get_role(role_id)
				color = color or role.color
				await role.edit(name=name, color=color, display_icon=icon, reason=f"{str(inter.user)} updated their booster role")

			else:
				print(f"User {inter.user.id} not found in boosters. Creating new role and adding user.")
				
				role = await guild.create_role(name=name, color=color, display_icon=icon, reason=f"{str(inter.user)} claimed their booster role")
				await guild.edit_role_positions(positions={role:boost_role.position})
				boosters[str(inter.user.id)] = role.id
			
			await member.add_roles(role)

			with open('config.json', 'w') as file:
				json.dump(data, file, indent=4)
			
			await inter.followup.send(f"Thank you! Here is your role: {role.mention}")

async def setup(ce):
	await ce.add_cog(BoostPerks(ce))

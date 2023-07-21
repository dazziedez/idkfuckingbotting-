import discord
import os
import json

from discord.ext import commands, tasks

guild_id = 874440438604496976
booster_id = 881222980858966017

class Core(commands.Cog, name="Core"):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_message(self, message):
		if "<@879083602082684968>" in message.content:
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

		if not self.check_boosters.is_running():
			self.check_boosters.start()

	@tasks.loop(minutes=1)
	async def check_boosters(self):
		with open('config.json', 'r') as file:
			data = json.load(file)
			boosters = data.get('boosters', {})
			guild = self.client.get_guild(guild_id)
			users_to_remove = []  # List to store user IDs to remove
			for user_id, role_id in boosters.items():
				member = guild.get_member(int(user_id))
				if member is None:
					print(f"User {user_id} is no longer in the guild. Removing from boosters and deleting role.")
					role = guild.get_role(int(role_id))
					await role.delete()
					users_to_remove.append(user_id)  # Add user ID to the list for removal
				elif booster_id not in [r.id for r in member.roles if r.id != guild.id]:
					print(f"User {user_id} has stopped boosting. Removing from boosters and deleting role.")
					role = guild.get_role(int(role_id))
					if role is not None:
						await role.delete()
					users_to_remove.append(user_id)  # Add user ID to the list for removal
	
			# Remove users from the boosters dictionary
			for user_id in users_to_remove:
				del boosters[user_id]
	
		with open('config.json', 'w') as file:
			json.dump(data, file, indent=4)


async def setup(client):
	await client.add_cog(Core(client))
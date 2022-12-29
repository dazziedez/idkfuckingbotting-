import discord
import time
from discord.ext import commands

class Events(commands.Cog, name="Events"):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.content == "<@838817491169705994>":
			await message.reply("uwu")

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send(f'Please pass in all requirements - `{error}`')
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"You don't have permission to do that - `{error}`")

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		guild = self.client.get_guild(874440438604496976)
		log = guild.get_channel(876104888122212413)
		logembed = discord.Embed(title='Member left', description=f'{member}')
		logembed.set_thumbnail(url=member.avatar.url)
		logembed.add_field(name="Joined At", value=f'<t:{int(member.joined_at.timestamp())}:R>')

		await log.send(embed=logembed)

	@commands.Cog.listener()
	async def on_bulk_message_delete(self, messages):
		guild = self.client.get_guild(874440438604496976)
		log = guild.get_channel(876104888122212413)
		embed = discord.Embed(title='🗑 Bulk message delete', description=f'{len(messages)} messages were bulk deleted')
		await log.send(embed=embed)

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		guild = self.client.get_guild(874440438604496976)
		log = guild.get_channel(876104888122212413)

		embed = discord.Embed(title='✏ Message edited')
		embed.add_field(name='Before', value=before.content)
		embed.add_field(name='After', value=after.content)
		embed.set_author(name=str(before.author), icon_url=before.author.avatar.url)
		embed.set_footer(text='in #' + before.channel.name)
		await log.send(embed=embed)


async def setup(client):
	await client.add_cog(Events(client))

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
	async def on_member_join(self, member):
		guild = self.client.get_guild(874440438604496976)
		log = guild.get_channel(876104888122212413)
		verify = guild.get_channel(876102248185339925)
		general = guild.get_channel(876085929117352016)
		channel = guild.get_channel(876101520297443388)
	
		if time.time() - member.created_at.timestamp() < 2592000:
			embed = discord.Embed(description=f'You were kicked from `{guild.name}` because your account is too young \n<t:{int(member.created_at.timestamp())}:R> < `30 days ago`')
			logembed = discord.Embed(description=f'{member.name} was kicked because their account is too young \n<t:{int(member.created_at.timestamp())}:R> < `30 days ago`')
			await member.send(embed=embed)
			await member.kick()
			await log.send(embed=logembed)
		else:
			logembed = discord.Embed(title='📥 Member joined', description=f'{member}')
			logembed.add_field(name="Account Created",
						value=f'<t:{int(member.created_at.timestamp())}:R>')
			logembed.set_thumbnail(url=member.avatar.url)
			await channel.send(
			f'{member.mention} joined this server :O\nRemember, you can\'t leave')
			await member.send(f'Welcome to **{guild.name}**, {member.name}!\njust to make things clear, you\'ll die if you leave\nhttps://discord.gg/T5BZayunBB')
			await general.send(f'{member.mention} just joined, say hi!',
						   delete_after=60)
			await verify.send(f'welcome {member.mention}!\nPlease react with ✅ above to gain access to the server',
			delete_after=10)
			await log.send(embed=logembed)

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		guild = self.client.get_guild(874440438604496976)
		log = guild.get_channel(876104888122212413)
		channel = guild.get_channel(876101520297443388)
		logembed = discord.Embed(title='Member left', description=f'{member}')
		logembed.set_thumbnail(url=member.avatar.url)
		logembed.add_field(name="Joined At", value=f'<t:{int(member.joined_at.timestamp())}:R>')
		await channel.send(
			f'Someone just left...\nMay {member.name}#{member.discriminator} rest in peace.'
		)
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
import discord
import random
import time
from discord.ext import commands
from discord import app_commands

reactions = ['https://tenor.com/view/aou-cat-sniffing-camera-live-reaction-gif-22414746', 'https://tenor.com/bLKz1.gif', 'https://tenor.com/bR3O6.gif', 'https://tenor.com/bEHp8.gif', 'https://tenor.com/bCWrH.gif', 'https://tenor.com/bBByi.gif',
			 'https://tenor.com/bREJk.gif', "https://tenor.com/bSf4N.gif", 'https://tenor.com/bLHDh.gif', 'https://tenor.com/bFvZt.gif', 'https://tenor.com/bI1vf.gif', 'https://tenor.com/bRv90.gif', 'https://tenor.com/bHOYo.gif']


class Fun(commands.Cog):
	def __init__(self, client):
		self.client = client

	@app_commands.command(name='reaction', description='Live slug reaction')
	async def reaction(self, interaction):
		await interaction.response.send_message(random.choice(reactions))

	@app_commands.command(name='avatar')
	async def avatar(self, interaction, member: discord.User = None):
		if member == None:
			member = interaction.user

		avatar = member.avatar.url

		embed = discord.Embed(title=f'{member.name}\'s avatar',
							  description=f'[Download]({member.avatar.url})')
		embed.set_footer(
			text=f"Asked by {str(interaction.user)}")
		embed.set_image(url=avatar)
		await interaction.response.send_message(embed=embed)
	
	@app_commands.command(name='whois', description="Gets info about the user")
	async def userinfo(self, interaction, member: discord.Member = None):
		if member == None:
			member = interaction.guild.get_member(interaction.user.id)
	
		embed = discord.Embed(title=f'{member}')
		embed.set_thumbnail(url=member.avatar.url)
		embed.add_field(name="Name", value=f'`{member.name}`')
		embed.add_field(name="Nickname", value=f'`{member.nick}`')
		embed.add_field(name="ID", value=f'`{member.id}`')
		embed.add_field(name="Account Created",
					value=f'<t:{int(member.created_at.timestamp())}:R>')
		embed.add_field(name="Joined",
					value=f'<t:{int(member.joined_at.timestamp())}:R>')
		members = sorted(interaction.guild.members, key=lambda m: m.joined_at)
		embed.add_field(name="Join Position",
					value=f'`{str(members.index(member)+1)}`')
		await interaction.response.send_message(embed=embed)
	
async def setup(client):
	await client.add_cog(Fun(client))
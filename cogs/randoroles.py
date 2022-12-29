import discord
import random
import asyncio
from discord.ext import commands


class Randroles(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def membersync(self, ctx):

		await ctx.message.add_reaction("🦕")
		count = 0
		msg = await ctx.send(f"⏳ synced {count} users...")
		member_roles = ["1058073878494191646", "1058073795165966456",
						"1058073526185238609", "876106482695938068"]
		for i in ctx.guild.members:
			
			if not i.bot:
				
				roles = tuple(discord.utils.get(ctx.guild.roles, id=int(i)) for i in member_roles)
				await i.remove_roles(*roles)
				count += 1
				zingus = ctx.guild.get_role(int(random.choice(member_roles)))
				await i.add_roles(zingus)
				await msg.edit(content=f"⏳ synced {count} users...")
				print(f"{str(i)}, {zingus}")
		await ctx.send(content=f"⛳ completed ({count} users synced) {ctx.author.mention}")
		await asyncio.sleep(5)
		await msg.delete()


async def setup(client):
	await client.add_cog(Randroles(client))

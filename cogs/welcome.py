import discord
import time
import random
from discord.ext import commands
from random import choice


class Welcome(commands.Cog, name="Welcome"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.client.get_guild(874440438604496976)
        log = guild.get_channel(876104888122212413)
        verify = guild.get_channel(876102248185339925)
        general = guild.get_channel(876085929117352016)

        member_roles = [1058073878494191646, 1058073795165966456,
                        1058073526185238609, 876106482695938068]

        if time.time() - member.created_at.timestamp() < 2592000:
            embed = discord.Embed(
                description=f'You were kicked from `{guild.name}` because your account is too young \n<t:{int(member.created_at.timestamp())}:R> < `30 days ago`')
            logembed = discord.Embed(
                description=f'{member.name} was kicked because their account is too young \n<t:{int(member.created_at.timestamp())}:R> < `30 days ago`')
            await member.send(embed=embed)
            await member.kick()
            await log.send(embed=logembed)
            return

        for _ in member_roles:
            roles = []
            role_obj = discord.utils.get(
                guild.roles, id=random.choice(member_roles))
            roles.append(role_obj)

        if not member.bot:
            zingus = random.choice(roles)
            await member.add_roles(zingus)


        logembed = discord.Embed(
            title='📥 Member joined', description=f'{member}')
        logembed.add_field(name="Account Created",
                                value=f'<t:{int(member.created_at.timestamp())}:R>')
        logembed.set_thumbnail(url=member.avatar.url)

        await member.send(f'Welcome to **{guild.name}**, {member.name}!\njust to make things clear, you\'ll die if you leave\nhttps://discord.gg/T5BZayunBB')
        await general.send(f'{member.mention} just joined, say hi!',
                           delete_after=60)
        await verify.send(f'welcome {member.mention}!\nPlease react with ✅ above to gain access to the server',
                          delete_after=10)
        await log.send(embed=logembed)


async def setup(client):
    await client.add_cog(Welcome(client))

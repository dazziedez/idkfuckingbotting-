import discord
import time
import random
from discord.ext import commands
from random import choice

thing = [
    "Welcome aboard, {user}!",
    "Glad to have you here, {user}!",
    "Welcome to the party, {user}!",
    "It's great to have you here, {user}!",
    "Welcome to the family, {user}!",
    "Glad you could join us, {user}!",
    "Welcome with open arms, {user}!",
    "We've been expecting you, {user}!",
    "Glad you made it, {user}!",
    "Welcome to the club, {user}!",
    "You made it, {user}!"]


class WelcomeButton(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.vaule = None
        self.msg = None
        self.reacted = []

    async def disable_all(self):
        for i in self.children:
            i.disabled = True
        await self.msg.edit(view=self)

    async def on_timeout(self):
        self.reacted = None
        self.msg = None
        return await self.disable_all()

    @discord.ui.button(label="Say hi!", emoji="<a:waving:1070739085506924635>")
    async def wave(self, interaction, button):
        await interaction.response.defer()
        if self.msg is None:
            self.msg = await interaction.followup.send(f"{interaction.user.mention} says hi!")
        else:
            self.msg = await interaction.channel.fetch_message(self.msg.id)
            if interaction.user.id not in self.reacted:
                msg = f"{interaction.user.mention}, {self.msg.content}"
                await self.msg.edit(content=msg)
            else:
                await interaction.followup.send("You've already greeted this individual!! :)", ephemeral=True)
        if interaction.user.id not in self.reacted:
            self.reacted.append(interaction.user.id)


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

        roles = tuple(discord.utils.get(guild.roles, id=int(i))
                      for i in member_roles)

        if not member.bot:
            zingus = random.choice(roles)
            await member.add_roles(zingus)

        welcome_msg = random.choice(thing).replace("{user}", member.mention)
        view = WelcomeButton()
        logembed = discord.Embed(
            title=':inbox_tray: Member joined', description=f'{member}')
        logembed.add_field(name="Account Created",
                           value=f'<t:{int(member.created_at.timestamp())}:R>')
        logembed.set_thumbnail(url=member.avatar.url)

        await member.send(f'Welcome to **{guild.name}**, {member.name}!\njust to make things clear, you\'ll die if you leave\nhttps://discord.gg/etyCBVj8Bx')
        await general.send(welcome_msg,
                           delete_after=240,
                           view=view)
        await log.send(embed=logembed)


async def setup(client):
    await client.add_cog(Welcome(client))

import json

from discord.ext import commands


class Autopublish(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def autopub(self, ctx, value):
        try:
            if not ctx.channel.is_news():
                await ctx.reply(f"You IDOT!! {ctx.channel.mention} is __NOT__ an announcement channel!!! Loser!! :PP")
                return

            if value == "true":
                with open('config.json', 'r') as f:
                    data = json.load(f)

                data["autopub"].append(ctx.channel.id)

                with open('config.json', 'w') as f:
                    json.dump(data, f)

                await ctx.reply(f"Autopublishing for {ctx.channel.mention}")

            else:
                with open('config.json', 'r') as f:
                    data = json.load(f)

                data["autopub"].remove(ctx.channel.id)

                with open('config.json', 'w') as f:
                    json.dump(data, f)

                await ctx.reply(f"No autopublishing for {ctx.channel.mention}!!")
        except Exception as e:
            ctx.reply(e)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('config.json', 'r') as f:
            data = json.load(f)
            if message.channel.id in data["autopub"]:
                try:
                    await message.publish()
                except:
                    pass


async def setup(client):
    await client.add_cog(Autopublish(client))

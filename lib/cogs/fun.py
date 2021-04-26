from aiohttp import request
from discord.ext.commands import command, cooldown
from discord.ext.commands import Cog, BucketType


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="fact")
    @cooldown(1, 60, BucketType.guild)
    async def fact_command(self, ctx, topic: str):
        if topic.lower() in ("dog", "cat", "panda", "fox", "bird", "koala"):
            url = f"https://some-random-api.ml/facts/{topic.lower()}"

            async with request("GET", url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    await ctx.send(data["fact"])

                else:
                    await ctx.send(f"The Facts API returned a {response.status} status code.")

        else:
            await ctx.send("No facts available for that animal.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
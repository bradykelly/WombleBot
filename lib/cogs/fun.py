from aiohttp import request
from discord.embeds import Embed
from discord.ext.commands import command, cooldown
from discord.ext.commands import Cog, BucketType


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="zen", aliases=["quote"],brief="Display a random Zen Quote")
    @cooldown(5, 30, BucketType.default)
    async def zen_command(self, ctx):
        url = f"https://zenquotes.io/api/random"

        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json(content_type="text/plain")

                embed=Embed(title=f"{data[0]['q']} - {data[0]['a']}", colour=ctx.author.colour)
                embed.set_thumbnail(url=ctx.guild.me.avatar_url)
                embed.set_author(name="Zen Quotes")
                embed.set_footer(text="Inspirational quotes provided by ZenQuotes API (https://zenquotes.io/)")
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"The Zen Quotes API returned a {response.status} status code.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
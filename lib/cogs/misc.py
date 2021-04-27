from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions
from lib.db.database import Database


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix", brief="Set the command prefix")
    @has_permissions(manage_guild=True)
    async def prefix_command(self, ctx, new: str):
        """Sets the command prefix for this bot"""

        if len(new) > 5: 
            await ctx.send("The prefix may not be more than 5 characters in length.")

        else:
            await self.bot.db.execute("INSERT INTO config (guild_id, command_prefixes) VALUES($1, $2) "
                + "ON CONFLICT (guild_id) DO UPDATE SET command_prefixes = EXCLUDED.command_prefixes",
                ctx.guild.id, new.strip())
            # self.bot.db.execute("UPDATE config SET command_prefixes = $1 WHERE guild_id = $2", new, ctx.guild.id)
            await ctx.send(f"The prefix is set to {new}")     

    @prefix_command.error
    async def prefix_command_error(self, ctx, exc)   :
        if isinstance(exc, CheckFailure):
            await ctx.send("You need the Manage Server permission to do that.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")


def setup(bot):
    bot.add_cog(Misc(bot))
from typing import Optional
from datetime import datetime
from discord import Embed, Member, NotFound, Object
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions
from discord.ext.commands.converter import MemberConverter


DEFAULT_LOG = 839178154215473202

class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot 

    @command(name="kick", brief="Kick members")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided"):
        """Kick one or more members from this server"""
        if not len(targets):
            await ctx.send("One or more required arguments are missing.")

        else:
            for target in targets:
                await target.kick(reason=reason)

                embed = Embed(title="Member kicked",
							  colour=0xDD2222,
							  timestamp=datetime.utcnow())
                embed.set_thumbnail(url=target.avatar_url)

                fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
						  ("Actioned by", ctx.author.display_name, False),
						  ("Reason", reason, False)]
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                log_channel = await self.bot.db.field("SELECT log_chan_id FROM config WHERE guild_id = $1", ctx.guild.id)
                log_channel = log_channel or DEFAULT_LOG      

                await self.bot.get_channel(log_channel).send(embed=embed)          

    @kick_command.error
    async def kick_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            ctx.send("Insufficient permissions to perform this action.")

    @command(name="ban", brief="Ban members")
    async def ban_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided"):
        """Ban one or more members from this server"""
        pass

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")


def setup(bot):
    bot.add_cog(Mod(bot))
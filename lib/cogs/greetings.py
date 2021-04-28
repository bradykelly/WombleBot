from discord.ext.commands import Cog


class Greetings(Cog):
    def __init__(self,bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("greetings")

    @Cog.listener()
    async def on_member_join(self, member):
        await self.bot.db.execute("INSERT INTO experience (guild_id, user_id) VALUES ($1, $2) " +
            "ON CONFLICT(guild_id, user_id) DO NOTHING", member.guild.id, member.id)

        welcome = await self.bot.db.field("SELECT welcome_id FROM config WHERE guild_id = $1", member.guild.id)
        await self.bot.get_channel(welcome).send(f"Welcome to **{member.guild.name}** {member.mention}! "
            + "Head over to <#734386829587120272> to say hello.")

    @Cog.listener()
    async def on_member_leave(self, member):
        pass


def setup(bot):
    bot.add_cog(Greetings(bot))            

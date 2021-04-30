from discord.errors import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands.core import guild_only


DEFAULT_GREETING = 836528471328161812
DEFAULT_GENERAL = 836987836498575370
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

        record = await self.bot.db.record("SELECT greetings_chan_id, general_chan_id FROM config WHERE guild_id = $1", member.guild.id)
        greeting = record["greetings_chan_id"] or DEFAULT_GREETING
        general = record["general_chan_id"] or DEFAULT_GENERAL
        await self.bot.get_channel(greeting).send(f"Welcome to **{member.guild.name}** {member.mention}! "
            + f"Head over to <#{general}> to say hello.")
        await self.bot.get_channel(general).send(f"{member.mention} has arrived!")

        try:
            await member.send(f"Welcome to **{member.guild.name}**! Enjoy your stay!")
            
        except Forbidden:
            pass

        start_role_list = await self.bot.db.field("SELECT start_role_list FROM config WHERE guild_id = $1", member.guild.id)
        if start_role_list is not None:
            roles_list = start_role_list.split(";")
            try:
                an_int = int(roles_list[0])   

            except ValueError:
                pass     

            else:
                to_add = [member.guild.get_role(int(role)) for role in roles_list]
                await member.add_roles(*to_add)
                
    @Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.db.execute("DELETE FROM experience WHERE guild_id = $1 AND user_id = $2", member.guild.id, member.id)
        greeting = await self.bot.db.field("SELECT greetings_chan_id FROM config WHERE guild_id = $1", member.guild.id)
        greeting = greeting or DEFAULT_GREETING
        await self.bot.get_channel(greeting).send(f"{member.display_name} has left {member.guild.name}")

def setup(bot):
    bot.add_cog(Greetings(bot))            

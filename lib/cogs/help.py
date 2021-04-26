from discord.ext.commands import Cog
from discord.ext.commands import command


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

        
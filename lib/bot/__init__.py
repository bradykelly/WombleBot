from asyncio.tasks import sleep
from glob import glob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.errors import Forbidden
from discord.ext.commands import Bot as BotBase
from discord import Intents
from discord.ext.commands import when_mentioned_or
from discord.ext.commands.context import Context
from discord.ext.commands.errors import BadArgument, CommandNotFound, CommandOnCooldown, MissingRequiredArgument
#from lib.db.database import Database

DEFAULT_PREFIX = "`"
OWNDER_IDS = [695627499891065033]
STD_OUT = 835859792924114954
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound,)

def get_prefix(bot, message):
    return when_mentioned_or(DEFAULT_PREFIX)(bot, message)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"  {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler

        # with open("./lib/bot/dsn", "r", encoding="utf-8") as df:
        #     dsn = df.read()
        #     self.db = Database(self, dsn)

        super().__init__(
            command_prefix=DEFAULT_PREFIX, 
            ownder_ids=OWNDER_IDS,
            intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"  {cog} loaded")

        print("Setup complete")
        
    def run(self, version):
        self.version = version

        print("Running setup")
        self.setup()

        with open("./lib/bot/token", "r", encoding="utf-8") as tf:
            self.token = tf.read()

        print("Running bot...")
        super().run(self.token, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:            
                await self.invoke(ctx)

            else:
                await ctx.send("I'm not ready to take commands. Please wait a few seconds.")

    async def on_connect(self):
        print("Bot connected")    

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send("An error occurred: " + err)        
        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        if isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} seconds.")

        elif hasattr(exc, "original"):
            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permission to do that")
                
            else:
                raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.stdout = self.get_channel(STD_OUT)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            guild_list = "WombleBot is online in guilds: \n"
            for guild in self.guilds:
                guild_list += "\t  " + guild.name + "\n"
            await self.stdout.send(guild_list)

            self.ready = True
            print("Bot ready")            

        else:
            print("Bot reconnected")

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)


bot = Bot()
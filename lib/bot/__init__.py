from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

DEFAULT_PREFIX = "`"
OWNDER_IDS = ["695627499891065033"]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = DEFAULT_PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler

        super().__init__(command_prefix=DEFAULT_PREFIX, ownder_ids=OWNDER_IDS)
        
    def run(self, version):
        self.version = version

        with open("./lib/bot/token", "r", encoding="utf-8") as tf:
            self.token = tf.read()

        print("Running bot...")
        super().run(self.token, reconnect=True)

    async def on_connect(self):
        print("Bot connected")    

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print("Bot ready")

        else:
            print("Bot reconnected")

    async def on_message(self, msg):
        pass


bot = Bot()
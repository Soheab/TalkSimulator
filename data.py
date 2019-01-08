from concurrent.futures import ThreadPoolExecutor
from discord.ext.commands import AutoShardedBot as _Bot


class Bot(_Bot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix
        self.executor = ThreadPoolExecutor(max_workers=16)

    async def on_message(self, msg):
        if not self.is_ready():
            return

        # Might be useful for later
        await self.process_commands(msg)

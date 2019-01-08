import os
import asyncio

from utils import default, stats
from data import Bot

config = default.get("config.json")
loop = asyncio.get_event_loop()
tasks = []

print("Logging in...\n------------------------------")
stats.reset_stats()


def prefixer(bot, message):
    return [f"<@!{bot.user.id}> ", f"<@{bot.user.id}> "]


for g in config.tokens:
    bot = Bot(command_prefix=prefixer, prefix=prefixer, pm_help=True, help_attrs=dict(hidden=True))

    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            bot.load_extension(f"cogs.{name}")

    tasks.append(loop.create_task(bot.start(g)))

try:
    loop.run_until_complete(asyncio.gather(*tasks))
except KeyboardInterrupt:
    print("CTRL + C was pressed, closing asyncio...")
    loop.close()
except asyncio.CancelledError:
    print("Process killed, closing asyncio...")
    loop.close()

import asyncio

from utils import default, cleverbot, stats

config = default.get("config.json")
botstats = default.get("stats.json")
client = cleverbot.Caller(user=config.API.user, key=config.API.key, nick=config.API.nick)


class Events:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)}')
        stats.append_value("bots", self.bot.user.id)

        if not default.get("stats.json").started:
            stats.change_value(started=True)
            print(f"{self.bot.user} was first to boot, waiting for the other bot to boot")

            waiter = asyncio.ensure_future(default.wait_for(len(botstats.bots), 2))
            waiter.cancel()

            await self.bot.get_channel(config.channel).send(config.startMessage)
            print("Detected other bot, starting conversation...")

    async def on_message(self, msg):
        if msg.author.id == self.bot.user.id:
            return

        if msg.channel.id == config.channel and msg.author.bot:
            async with msg.channel.typing():
                if default.get("stats.json").reset:
                    print(f"{self.bot.user} detected a reset and has completed it.")
                    stats.change_value(reset=False)
                    await asyncio.sleep(5)  # Let's keep the typing a bit more realistic huh?
                    return await msg.channel.send(default.get("stats.json").startMessage)

                response = await client.ask(msg.content)
                await msg.channel.send(response)

                if not default.get("stats.json").reset:
                    stats.change_value(startMessage=response)


def setup(bot):
    bot.add_cog(Events(bot))

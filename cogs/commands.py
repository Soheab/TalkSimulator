import time

from discord.ext import commands
from utils import stats, default


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("Pong   |   <a:Loading:393742933360246794>")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong   |   {int(ping)}ms")

    @commands.command()
    async def source(self, ctx):
        """ Check out my source code <3 """
        await ctx.send(f"**{ctx.bot.user}** is powered by this source code:\nhttps://github.com/AlexFlipnote/TalkSimulator")

    @commands.command()
    @commands.check(default.is_mod)
    async def reset(self, ctx, *, sentence: str):
        """ Reset the bots from an endless loop """
        stats.change_value(startMessage=sentence, reset=True)
        await ctx.send(f"Next message sent in <#{self.config.channel}> will be:\n```fix\n{sentence}```")

    @commands.command()
    @commands.check(default.is_mod)
    async def forcereset(self, ctx, *, sentence: str):
        """ Reset the bots when no one even replies """
        stats.change_value(startMessage=sentence, reset=True)
        await ctx.send(f"Sending message to <#{self.config.channel}> right now:\n```fix\n{sentence}```")
        await self.bot.get_channel(self.config.channel).send(sentence)


def setup(bot):
    bot.add_cog(Commands(bot))

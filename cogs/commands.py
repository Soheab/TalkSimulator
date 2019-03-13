import datetime
import time
import discord
import psutil

from discord.ext import commands
from utils import stats, default

def f_time(time):
    h, r = divmod(int(time.total_seconds()), 3600)
    m, s = divmod(r, 60)
    d, h = divmod(h, 24)

    return "%02d:%02d:%02d:%02d" % (d, h, m, s)

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self.config = default.get("config.json")

    @commands.command()
    async def stats(self, ctx):
        """ Shows some basic stats """
        stats=default.get("stats.json")
        ram = self.process.memory_full_info().rss / 1024**2
        uptime = f_time(datetime.datetime.now() - self.bot.startup)
        embed = discord.Embed(color=0xbe2f2f,
                              description='Some basic stats')       
        embed.add_field(name=u'📤 Messagses send in total', value=stats.talked, inline=False)
        embed.add_field(name=u'✏ Last message', value=stats.startMessage, inline=False)
        embed.add_field(name=u'💾 RAM Usage', value=f'{ram:.2f} MB', inline=False)
        embed.add_field(name=u'🕓 Uptime', value=uptime, inline=False)
        embed.add_field(name='⏱ Latency', value=f'{round(self.bot.latency * 1000)} ms', inline=False)
        await ctx.send(embed=embed)

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
    
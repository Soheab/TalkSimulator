import asyncio
import traceback

from utils import default, cleverbot, stats
from discord.ext import commands
from discord.ext.commands import errors

config = default.get("config.json")
botstats = default.get("stats.json")
client = cleverbot.Caller(user=config.API.user, key=config.API.key, nick=config.API.nick)


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        await ctx.send(page)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            await send_cmd_help(ctx)

        elif isinstance(err, errors.CommandInvokeError):
            err = err.original

            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = ''.join(_traceback)
            error = ('```py\n{2}{0}: {3}\n```').format(type(err).__name__, ctx.message.content, _traceback, err)

            await ctx.send(f"There was an error processing the command ;-;\n{error}")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.0f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            pass

    @commands.Cog.listener()
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

    @commands.Cog.listener()
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
                    stats.change_value(
                        startMessage=response,
                        talked=default.get("stats.json").talked + 1
                    )


def setup(bot):
    bot.add_cog(Events(bot))

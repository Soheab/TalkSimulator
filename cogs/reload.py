from discord.ext import commands
from utils import default


class Loader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(default.is_admin)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```diff\n- {e}```")
        await ctx.send(f"Reloaded extension **{name}.py**")

    @commands.command()
    @commands.check(default.is_admin)
    async def load(self, ctx, name: str):
        """ Loads an extension. """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```diff\n- {e}```")
        await ctx.send(f"Loaded extension **{name}.py**")

    @commands.command()
    @commands.check(default.is_admin)
    async def unload(self, ctx, name: str):
        """ Unloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```diff\n- {e}```")
        await ctx.send(f"Unloaded extension **{name}.py**")


def setup(bot):
    bot.add_cog(Loader(bot))

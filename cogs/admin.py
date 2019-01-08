import json
import discord

from discord.ext import commands
from utils import default


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.configfile = "config.json"

    @commands.group(aliases=["mod"])
    @commands.check(default.is_admin)
    async def mods(self, ctx):
        """ Checks all current mods """
        if ctx.invoked_subcommand is None:
            getconfig = default.get("config.json")
            modNames = "\n".join([f"**{self.bot.get_user(g)}**" for g in getconfig.mods])
            await ctx.send(f"Moderators of <#{getconfig.channel}>:\n{modNames}")

    @mods.command(name="add")
    async def mods_add(self, ctx, user: discord.Member):
        """ Add a mod """
        with open(self.configfile, "r") as jsonFile:
            data = json.load(jsonFile)

        if user.id in data["mods"]:
            return await ctx.send("This user is already a moderator")

        data["mods"].append(user.id)
        with open(self.configfile, "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)

        await ctx.send(f"Added **{user.name}** to the moderator list")

    @mods.command(name="remove")
    async def mods_remove(self, ctx, user: discord.Member):
        """ Remove a mod """
        with open(self.configfile, "r") as jsonFile:
            data = json.load(jsonFile)

        if user.id not in data["mods"]:
            return await ctx.send("This user isn't a moderator")

        data["mods"] = [g for g in data["mods"] if g != user.id]

        with open(self.configfile, "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)

        return await ctx.send(f"Removed **{user.name}** to the moderator list")


def setup(bot):
    bot.add_cog(Admin(bot))

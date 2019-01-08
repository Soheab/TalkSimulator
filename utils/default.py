import json
import asyncio

from collections import namedtuple


async def wait_for(target, value):
    print("While loop started now")
    while target is not value:
        # Waiting for target to be as value
        await asyncio.sleep(2)
    print("While loop escaped")


def get(file, name="Data"):
    try:
        with open(file) as data:
            return json.load(data, object_hook=lambda d: namedtuple(name, d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")


def is_admin(ctx):
    admins = get("config.json").admins
    return ctx.author.id in admins


def is_mod(ctx):
    mods = get("config.json").mods
    return ctx.author.id in mods or is_admin(ctx)

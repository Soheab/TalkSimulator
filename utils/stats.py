import os
import json
import time

filename = "stats.json"
default = {
    "bots": [],
    "started": False,
    "reset": False,
    "startMessage": "",
    "talked": 0,
    "lastTalked": int(round(time.time()))
}


def change_value(**values):
    """ Change value to a JSON file """
    with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)

    for g in values:
        data[g] = values[g]

    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)


def append_value(key, addition):
    """ Append value to a JSON file """
    with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)

    data[key].append(addition)
    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)


def reset_stats():
    """ Reset the stats """
    try:
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
    except FileNotFoundError:
        target = os.path.join(f"./{filename}")
        render = open(target, "w")
        render.write("{}")
        render.close()
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)

    data = default
    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)

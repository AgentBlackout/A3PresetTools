#!/usr/bin/env python3

import modset_common as common
import argparse
import math

parser = argparse.ArgumentParser(
    prog="total_modset_size.py",
    usage="%(prog)s [modset]",
    description="Computes the combined size of all mods in a preset or workshop collection.",
)
parser.add_argument("modset")
args = parser.parse_args()


def format_bytes(num):
    num = int(num)
    order = math.log(num, 10)
    if order > 9:
        return str(round(num / 10 ** 9, 2)) + " gb"
    if order > 6:
        return str(round(num / 10 ** 6, 2)) + " mb"
    if order > 3:
        return str(round(num / 10 ** 3, 2)) + " kb"
    else:
        return str(num) + " bytes"


modset = common.ModSet.from_collection_preset(args.modset)


total_size = 0
unknown_size = False
modset.mods = sorted(
    modset.mods, key=lambda mod: -1 if mod.size is None else mod.size, reverse=True
)
for mod in modset.mods:
    if not mod.size is None:
        total_size += mod.size
        print(format_bytes(mod.size) + " — " + str(mod))
    else:
        print(str(mod) + " size is unknown")
        unknown_size = True

if unknown_size:
    print(
        "Preset contains at least "
        + format_bytes(total_size)
        + " of mods (some mods were unlisted or private)."
    )
else:
    print("Preset contains " + format_bytes(total_size) + " of mods.")

#!/usr/bin/env python3

import modset_common as common
import argparse
import math

parser = argparse.ArgumentParser(
    prog="total_modset_size.py",
    usage="%(prog)s [modset] [options]",
    description="Computes the combined size of all mods in a preset or workshop collection.",
)
parser.add_argument("modset")
parser.add_argument(
    "-s",
    "--sort",
    choices=["S", "s", "N", "n"],
    help="sorts the modset in the specified order: S- size descending, s- size ascending, N- name descending, n- name ascending, No value- no sort",
    default="S",
    nargs="?"
)
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


def sort(mod):
    if args.sort.lower() == "s":
        return -1 if mod.size is None else mod.size
    elif args.sort.lower() == "n":
        return -1 if mod.name is None else mod.name.lower()


modset = common.ModSet.from_collection_preset(args.modset)

total_size = 0
unknown_size = False
# Sort into ascending then reverse if descending is requested.
if not args.sort is None:
    modset.mods = sorted(modset.mods, key=sort, reverse=args.sort.isupper())

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

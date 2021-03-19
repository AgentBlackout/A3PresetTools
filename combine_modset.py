import os
import modset_common as common
import argparse

parser = argparse.ArgumentParser(
    prog="combine_modset.py",
    usage="%(prog)s [output] [options]",
    description="Adds and subtracts modsets to produce a single preset.",
)
parser.add_argument("output")
parser.add_argument(
    "-a",
    "--add",
    help="a modset to add",
    nargs="+",
)
parser.add_argument(
    "-s",
    "--subtract",
    help="a modset to subtract (any mods in these sets will not be included even if they are added more than once)",
    nargs="+",
)
args = parser.parse_args()

mods = []
for addition in args.add:
    modset = common.ModSet.from_collection_preset(addition)
    for mod in modset.mods:
        if not mod in mods:
            mods.append(mod)

for subtraction in args.subtract:
    modset = common.ModSet.from_collection_preset(subtraction)
    for mod in modset.mods:
        try:
            mods.remove(mod)
        except ValueError:
            pass

name = os.path.splitext(os.path.basename(args.output))[0]
modset = common.ModSet(name, mods)
modset.export_preset(args.output)
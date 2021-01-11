import modset_common as common
import argparse
import math

parser = argparse.ArgumentParser(
    prog="total_preset_size.py",
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
        return str(round(num / 10 ** 3, 2)) + " mb"
    else:
        return str(num) + " bytes"


modset = common.ModSet.from_collection_preset(args.modset)


total_size = 0
modset.mods = sorted(modset.mods, key=lambda mod: mod.size)
for mod in modset.mods:
    mod_size = mod.size
    total_size += mod_size
    print("'" + mod.name + "' is " + format_bytes(mod_size))

print("Preset contains " + format_bytes(total_size) + " of mods.")
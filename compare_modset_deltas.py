import modset_common as common
import sys
import os
import argparse

parser = argparse.ArgumentParser(
    prog="compare_preset_deltas.py",
    usage="%(prog)s [modset1] [modset2]",
    description="Compared two arma preset files or workshop collections.",
)
parser.add_argument("modset1")
parser.add_argument("modset2")
args = parser.parse_args()

modset1 = common.ModSet.from_collection_preset(args.modset1)
modset2 = common.ModSet.from_collection_preset(args.modset2)

commonMods = []
for mod in modset1.mods:
    if mod in modset2.mods:
        commonMods.append(mod)

modset1Only = []
for mod in modset1.mods:
    if not mod in commonMods:
        modset1Only.append(mod)

modset2Only = []
for mod in modset2.mods:
    if not mod in commonMods:
        modset2Only.append(mod)

print("Common Mods:")
for mod in commonMods:
    print(" - " + str(mod))

print(modset1.name + " Mods:")
for mod in modset1Only:
    print(" - " + str(mod))

print(modset2.name + " Mods:")
for mod in modset2Only:
    print(" - " + str(mod))

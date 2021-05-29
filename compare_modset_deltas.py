#!/usr/bin/env python3

import modset_common as common
import sys
import os
import argparse

parser = argparse.ArgumentParser(
    prog="compare_modset_deltas.py",
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

if modset1.is_collection():
    print(modset1.name + " Mods (" + modset1.get_url() + "):")
else:
    print(modset1.name + " Mods:")
if len(modset1.mods) == 0:
    print("None")
for mod in modset1Only:
    print(" - " + str(mod))

if modset2.is_collection():
    print(modset2.name + " Mods (" + modset2.get_url() + "):")
else:
    print(modset2.name + " Mods:")
if len(modset2.mods) == 0:
    print("None")
for mod in modset2Only:
    print(" - " + str(mod))

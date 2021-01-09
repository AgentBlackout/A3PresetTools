import preset_common as common
import sys
import os
import argparse

parser = argparse.ArgumentParser(prog="compare_preset_deltas.py", usage="%(prog)s [preset1] [preset2]",
    description="Compared two arma preset files.")
parser.add_argument("preset1")
parser.add_argument("preset2")
args = parser.parse_args()


if not os.path.isfile(args.preset1) or not os.path.isfile(args.preset2):
    raise Error("Both presets must exist.")

preset1 = common.getPreset(args.preset1)
preset2 = common.getPreset(args.preset2)

commonMods = []
for mod in preset1.mods:
    if mod in preset2.mods:
        commonMods.append(mod)

preset1Only = []
for mod in preset1.mods:
    if not mod in commonMods:
        preset1Only.append(mod)

preset2Only = []
for mod in preset2.mods:
    if not mod in commonMods:
        preset2Only.append(mod)

print("Common Mods:")
for mod in commonMods:
    print(" - " + str(mod))

_, tail = os.path.split(args.preset1)
print(tail + " Mods:")
for mod in preset1Only:
    print(" - " + str(mod))

_, tail = os.path.split(args.preset2)
print(tail + " Mods:")
for mod in preset2Only:
    print(" - " + str(mod))

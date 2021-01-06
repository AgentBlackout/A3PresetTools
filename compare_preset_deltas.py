import preset_common as common
import sys
import os

if len(sys.argv) < 3:
    print("Not enough arguments!")
    quit()

preset1Path = sys.argv[1]
preset2Path = sys.argv[2]

preset1 = common.getPreset(preset1Path)
preset2 = common.getPreset(preset2Path)

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

_, tail = os.path.split(preset1Path)
print(tail + " Mods:")
for mod in preset1Only:
    print(" - " + str(mod))

_, tail = os.path.split(preset2Path)
print(tail + " Mods:")
for mod in preset2Only:
    print(" - " + str(mod))

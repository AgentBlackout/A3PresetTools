import preset_common as common

preset = common.getPreset()

modIds = ""
for mod in preset.mods:
    modIds += str(mod.id) + "\n"

with open("mods.txt", "w") as f:
    f.write(modIds)
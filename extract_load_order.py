import preset_common as common

preset = common.getPreset()

loadString = ""
for mod in preset.mods:
    loadString += "@" + mod.name + ";"

print(loadString)
input()
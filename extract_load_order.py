import preset_common as common
import argparse

parser = argparse.ArgumentParser(prog="extract_load_order.py", usage="%(prog)s [preset]",
    description="Reads a presets mods out in the assigned load order formatted for use in the arma '-mods=' argument.")
parser.add_argument("preset")
args = parser.parse_args()

preset = common.getPreset(args.preset)

loadString = ""
for mod in preset.mods:
    loadString += "@" + mod.name + ";"

print(loadString)
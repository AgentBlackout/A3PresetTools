import preset_common as common
import argparse

parser = argparse.ArgumentParser(
    prog="extract_load_order.py",
    usage="%(prog)s [preset] [options]",
    description="Reads a presets mods out in the assigned load order formatted for use in the arma '-mods=' argument.",
)
parser.add_argument("preset")
parser.add_argument(
    "-e",
    "--escape",
    help="escapes spaces so that the load order can be used for linux servers",
    action="store_true",
)
args = parser.parse_args()

preset = common.getPreset(args.preset)

loadString = ""
for mod in preset.mods:
    if args.escape:
        loadString += "@" + mod.name.replace(" ", "\\ ")
    else:
        loadString += "@" + mod.name + ";"

print(loadString)
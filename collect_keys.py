import preset_common as common
import argparse
import shutil
import glob

parser = argparse.ArgumentParser(
    prog="compare_preset_deltas.py",
    usage="%(prog)s {-l [load_order] OR -p [preset]} [options]",
    description="Collect the .bikey files from the mods contained a preset or load order string.",
)
parser.add_argument("-p", "--preset", help="preset to select mods from", default=None)
parser.add_argument(
    "-l", "--load-order", help="load order to select mods from", default=None
)
parser.add_argument(
    "-i", "--input", help="directory to search for mods in", default="./"
)
parser.add_argument(
    "-o", "--output", help="directory to output the collected keys to", default="./keys"
)
args = parser.parse_args()

possible_mod_paths = []
if not args.preset is None:
    preset = common.getPreset(args.preset)
    possible_mod_paths = [[mod.id, "@" + mod.name] for mod in preset.mods]
elif not args.load_order is None:
    mod_folders = args.load_order.split(";")
    possible_mod_paths = [[(mod_folder) for mod_folder in mod_folders]]
else:
    raise Exception("You must specify either a -l/--load-order or -p/--preset.")

all_keys = []
for possible_path in possible_mod_paths:
    keys = []
    for mod in possible_path:
        keys.extend(glob.glob(args.input + "/" + mod + "/*.bikey", recursive=True))
        keys.extend(glob.glob(args.input + "/" + mod + "/keys/*.bikey", recursive=True))

    if len(keys) == 0:
        raise Exception("Key was not found for '" + mod + "'")
    all_keys.extend(keys)


for key in all_keys:
    print("Copying '" + key + "' to '" + args.output + "'")
    shutil.copy(key, args.output)
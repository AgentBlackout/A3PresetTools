import modset_common as common
import argparse
import shutil
import glob

parser = argparse.ArgumentParser(
    prog="compare_preset_deltas.py",
    usage="%(prog)s {-l [load_order] OR -p [modset]} [options]",
    description="Collect the .bikey files from the downloaded mods contained a preset or workshop collection or load order string.",
)
parser.add_argument(
    "-m",
    "--modset",
    help="preset or workshop collection (id or url) to select mods from",
    default=None,
)
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
if not args.modset is None:
    modset = common.ModSet.from_collection_preset(args.modset)
    possible_mod_paths = [["@" + mod.name, mod.id] for mod in modset.mods]
elif not args.load_order is None:
    mod_folders = args.load_order.split(";")
    possible_mod_paths = [[(mod_folder) for mod_folder in mod_folders]]
else:
    raise Exception("You must specify either a -l/--load-order or -m/--modset.")

all_keys = []
for possible_path in possible_mod_paths:
    keys = []
    for mod in possible_path:
        keys.extend(
            glob.glob(args.input + "/" + glob.escape(mod) + "/*.bikey", recursive=True)
        )
        keys.extend(
            glob.glob(
                args.input + "/" + glob.escape(mod) + "/[kK]eys/*.bikey", recursive=True
            )
        )
        keys.extend(
            glob.glob(
                args.input + "/" + glob.escape(mod) + "/[kK]ey/*.bikey", recursive=True
            )
        )

    if len(keys) == 0:
        print("Key was not found for '" + possible_path[0] + "'.")
    all_keys.extend(keys)


for key in all_keys:
    print("Copying '" + key + "' to '" + args.output + "'")
    shutil.copy(key, args.output)
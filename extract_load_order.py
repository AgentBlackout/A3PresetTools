#!/usr/bin/env python3

import modset_common as common
import argparse

parser = argparse.ArgumentParser(
    prog="extract_load_order.py",
    usage="%(prog)s [preset] [options]",
    description="Reads a presets mods out in the assigned load order formatted for use in the arma '-mods=' argument.",
)
parser.add_argument(
    "--readable-names",
    help="use escaped mod names for folder directories (by default mod ids are used), see download_mods.py",
    action="store_true"
)
parser.add_argument("preset")
args = parser.parse_args()

preset = common.ModSet.from_preset(args.preset)

loadString = ""
common.get_load_order(loadString, args.readable_names)
print(loadString)
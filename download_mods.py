import preset_common as common
import subprocess
import argparse
import shutil
import glob
import sys
import os

APPID = "107410"
# Steam mod download directory relative to root steam directory.
WORKSHOP_CONTENT_DIR = "steamapps/workshop/content/" + APPID

parser = argparse.ArgumentParser(
    prog="compare_preset_deltas.py",
    usage="%(prog)s [preset] [options]",
    description="Download the mods in a preset using steamcmd.",
)
parser.add_argument("preset")
parser.add_argument(
    "-s",
    "--steamcmd-path",
    help="command used to run steamcmd (defaults to 'steamcmd')",
    default="steamcmd",
)
parser.add_argument(
    "-u",
    "--username",
    help="username to login to steam with (account must own arma 3)",
    required=True,
)
parser.add_argument(
    "-p", "--password", help="password to login to steam with", required=True
)
parser.add_argument(
    "-o",
    "--output-path",
    help="directory to move downloaded mods to. if this is set mods will be renamed to @\{mod_name\}. \
    mods will not be moved by default.",
    default=None,
)
parser.add_argument(
    "-d",
    "--download-path",
    help="temporary directory to download mods to (defaults to ./steam)",
    default="./steam",
)
parser.add_argument(
    "--update",
    help="if enabled preset mods in [output-path] are moved to [download-path] and updated with steamcmd rather than\
    re-downloaded",
    action="store_true",
)
args = parser.parse_args()

preset = common.getPreset(args.preset)

if args.update:
    if not args.output_path is None:
        print("Moving existing mods to [download-path]... ", end="")
        for mod in preset.mods:
            if os.path.isdir(args.output_path + "/@" + mod.name):
                # Move mods in the preset from [output-path] to steamcmds actual download path.
                shutil.move(
                    args.output_path + "/@" + mod.name,
                    args.download_path + "/" + WORKSHOP_CONTENT_DIR + "/" + mod.id,
                )
        print("Done")
    else:
        raise Exception("You must set -o/--output-path to enable --update mode.")

steamcmd_cmd = [
    args.steamcmd_path,
    "+login",
    args.username,
    args.password,
    "+force_install_dir",
    os.path.abspath(args.download_path),
]
for mod in preset.mods:
    steamcmd_cmd.extend(["+workshop_download_item", APPID, mod.id])
steamcmd_cmd.append("+quit")

print("Running steamcmd...")
steamcmd = subprocess.run(steamcmd_cmd)
print("steamcmd done.")

# Apparently 'not var is None' is fine but 'not var is 0' is worthy of a syntax warning.
if steamcmd.returncode != 0:
    raise Exception(
        "steamcmd failed for some reason. Please review its output and try again."
    )

if not args.output_path is None:
    print("Moving mods to [output-path]... ", end="")
    for mod in preset.mods:
        shutil.move(
            args.download_path + "/" + WORKSHOP_CONTENT_DIR + "/" + mod.id,
            args.output_path + "/@" + mod.name,
        )
    print("Done")

if sys.platform == "linux" or sys.platform == "linux2":
    print("Renaming mod files to lower case (for linux compatibility)... ", end="")
    for mod in preset.mods:
        for mod_file in glob.glob(
            args.output_path + "/@" + mod.name + "/**/", recursive=True
        ):
            mod_file_split = mod_file.split(mod.name)
            shutil.move(
                mod_file, mod_file_split[0] + mod.name + mod_file_split[1].lower()
            )
        for mod_file in glob.glob(
            args.output_path + "/@" + mod.name + "/**", recursive=True
        ):
            mod_file_split = mod_file.split(mod.name)
            shutil.move(
                mod_file, mod_file_split[0] + mod.name + mod_file_split[1].lower()
            )
    print("Done")
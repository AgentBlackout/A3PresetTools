#!/usr/bin/env python3

import modset_common as common
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
    prog="download_mods.py",
    usage="%(prog)s [modset] [options]",
    description="Download the mods in a preset or workshop collection using steamcmd.",
)
parser.add_argument("modset")
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
    help=r"directory to move downloaded mods to. if this is set mods will be renamed to @{mod_name}. \
    mods will not be moved by default",
    default=None,
)
parser.add_argument(
    "-d",
    "--download-path",
    help="directory to place steamapps folder in for downloading mods (defaults to .)",
    default=".",
)
parser.add_argument(
    "-l",
    "--symlink",
    help="instead of copying mods from [download-path] to [output-path] mods will be symlinked (caution arma doesnt seem to follow symlinks)",
    action="store_true",
)
parser.add_argument(
    "--update",
    help="if enabled preset mods in [output-path] are moved to [download-path] and updated with steamcmd rather than\
    re-downloaded",
    action="store_true",
)
parser.add_argument(
    "--clean",
    help="any folders prefixed with @ in [output-path] not in the current modset will be deleted",
    action="store_true",
)
args = parser.parse_args()

modset = common.ModSet.from_collection_preset(args.modset)

if args.symlink and args.output_path is None:
    raise Exception("You must specify -o/--output-path to enable --symlink mode.")

if args.update and not args.symlink:
    # No need to copy mods if they are symlinked.
    if args.output_path is None:
        raise Exception("You must set -o/--output-path to enable --update mode.")

    print("Moving existing mods to [download-path]... ", end="")
    for mod in modset.mods:
        if os.path.isdir(args.output_path + "/@" + mod.name):
            # Move mods in the modset from [output-path] to steamcmds actual download path.
            shutil.move(
                args.output_path + "/@" + mod.name,
                args.download_path + "/" + WORKSHOP_CONTENT_DIR + "/" + mod.id,
            )
    print("Done")


if args.clean:
    if args.output_path is None:
        raise Exception("You must set -o/--output-path to enable --clean mode.")

    for mod_folder in glob.glob(args.output_path + "/@*"):
        mod_name = mod_folder.split("/@")[1]
        if not mod_name in [m.name for m in modset.mods]:
            print(
                "Deleting @"
                + mod_name
                + " because clean mode is enabled an this mod it not the in specified modset."
            )
            shutil.rmtree(mod_folder)


steamcmd_cmd = [
    args.steamcmd_path,
    "+login",
    args.username,
    args.password,
    "+force_install_dir",
    os.path.abspath(args.download_path),
]
for mod in modset.mods:
    steamcmd_cmd.extend(["+workshop_download_item", APPID, mod.id, "validate"])
steamcmd_cmd.append("+quit")

print("Running steamcmd...")
steamcmd = subprocess.run(steamcmd_cmd)
print("steamcmd done.")

if steamcmd.returncode != 0:
    raise Exception(
        "steamcmd failed for some reason. Please review its output and try again."
    )

if not args.output_path is None:
    if args.symlink:
        print("Symlinking mods to [output-path]...", end="")

        for mod in modset.mods:
            os.symlink(
                args.download_path + "/" + WORKSHOP_CONTENT_DIR + "/" + mod.id,
                args.output_path + "/@" + mod.name,
                True,
            )
    else:
        print("Moving mods to [output-path]... ", end="")

        for mod in modset.mods:
            shutil.move(
                args.download_path + "/" + WORKSHOP_CONTENT_DIR + "/" + mod.id,
                args.output_path + "/@" + mod.name,
            )

    print("Done")


def rename_files_lower(directory):
    for mod_file in glob.glob(glob.escape(directory) + "/*"):
        mod_file_name = os.path.split(mod_file)[1]
        shutil.move(mod_file, directory + "/" + mod_file_name.lower())

        if os.path.isdir(mod_file):
            rename_files_lower(directory + "/" + mod_file_name.lower())


if sys.platform == "linux" or sys.platform == "linux2":
    # PBOs are loaded with lower case names which breaks in case sensitive filesystems.
    print("Renaming mod files to lower case (for linux compatibility)... ", end="")
    for mod in modset.mods:
        rename_files_lower(args.output_path + "/@" + mod.name)
    print("Done")

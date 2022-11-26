#!/usr/bin/env python3

from modset_constants import *
import modset_common as common
import subprocess
import argparse
import shutil
import glob
import sys
import os

parser = argparse.ArgumentParser(
    prog="download_mods.py",
    usage="%(prog)s [modset] [options]",
    description="Download the mods in a preset or workshop collection using steamcmd.",
)
parser.add_argument("modset")
parser.add_argument(
    "-s",
    "--steamcmd",
    help="command used to run steamcmd (defaults to 'steamcmd')",
    default="steamcmd",
)
parser.add_argument(
    "-u",
    "--username",
    help="username to login to steam with (the account must own Arma3)",
    required=True,
)
parser.add_argument(
    "-p",
    "--password",
    help="password to login to steam with (by default steamcmd will prompt for a password)",
    default=None,
)
parser.add_argument(
    "-o",
    "--output-path",
    help="directory for downloaded mods to be placed in (defaults to working directory)",
    default=".",
)
parser.add_argument(
    "-d",
    "--download-path",
    help="directory to temporarily place steamapps folder in for downloading mods (defaults to .)",
    default=".",
)
parser.add_argument(
    "--readable-names",
    help="use escaped mod names for folder directories (by default mod ids are used)",
    action="store_true"
)
parser.add_argument(
    "--clean",
    help="delete any folders prefixed with @ in [output-path] not matching the current preset",
    action="store_true",
)
args = parser.parse_args()

modset = common.ModSet.from_collection_preset(args.modset)

# Path within the steamcmd folder structure
def get_mod_source_path(mod: common.Mod = None):
    dir = os.path.abspath(args.download_path) + "/steamapps/workshop/content/" + ARMA3_APPID
    if mod is None:
        return dir
    
    return dir + "/" + mod.id

# Path within the output folder structure
def get_mod_target_path(mod: common.Mod = None):
    dir = os.path.abspath(args.output_path)
    if mod is None:
        return dir
    
    if args.readable_names:
        return dir + "/@" + mod.name
    else:
        return dir + "/@" + mod.id
    

if args.clean:
    print("Cleaning unused mods...", flush=True)
    expected_mod_folders = [get_mod_target_path(mod) for mod in modset.mods]

    for mod_folder in glob.glob(args.output_path + "/@*"):
        if not os.path.abspath(mod_folder) in expected_mod_folders:
            print(
                "Deleting '"
                + mod_folder
            )
            shutil.rmtree(mod_folder)
    print("Done\n")

print("Preparing mod folders... ", flush=True, end="") 
for mod in modset.mods:
    source = get_mod_source_path(mod)
    target = get_mod_target_path(mod)

    if os.path.islink(source):
        print("[Warning] Overwriting the symlink at '" + source + "'")
        os.unlink(source)

    # Make sure we don't overwrite any existing downloads by accident.
    if os.path.exists(source):
        raise Exception("Please move or delete '" + source + "'")

    # Make an empty steamcmd target folder
    os.makedirs(get_mod_source_path(), exist_ok=True)

    # Make an empty target directory to download into (or link to the existing one)
    os.makedirs(target, exist_ok=True)
    os.symlink(target, source, True)
        
print("Done")

steamcmd_command = [
    args.steamcmd,
    "+force_install_dir",
    os.path.abspath(args.download_path),
    "+login",
    args.username,
]
if not args.password is None:
    steamcmd_command.append(args.password)
for mod in modset.mods:
    steamcmd_command.extend(["+workshop_download_item", ARMA3_APPID, mod.id, "validate"])
steamcmd_command.append("+quit")

print("Running steamcmd...")
steamcmd = subprocess.run(steamcmd_command)
if steamcmd.returncode != 0:
    raise Exception(
        "steamcmd failed for some reason. Please review its output."
    )
else:
    print("steamcmd done.\n")

def rename_files_lower(directory):
    for mod_file in glob.glob(glob.escape(directory) + "/*"):
        mod_file_name = os.path.split(mod_file)[1]
        shutil.move(mod_file, directory + "/" + mod_file_name.lower())

        if os.path.isdir(mod_file):
            rename_files_lower(directory + "/" + mod_file_name.lower())

if sys.platform == "linux" or sys.platform == "linux2":
    # PBOs are loaded with lower case names which breaks in case sensitive filesystems.
    print("Renaming mod files to lower case for linux compatibility... ", flush=True, end="")
    for mod in modset.mods:
        rename_files_lower(args.output_path + "/@" + mod.name)
    print("Done")

print("Cleaning up download path... ", flush=True, end="")
for mod in modset.mods:
    source = get_mod_source_path(mod)
    if not os.path.islink(source):
        # Source isn't the same symlink we created earlier for some reason.
        print("[Warning] Couldn't clean up '" + source + "'")
        continue
    else:
        os.unlink(source)
print("Done")
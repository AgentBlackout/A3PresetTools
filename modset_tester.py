#!/usr/bin/env python3

import os
import argparse
import subprocess
import threading
from time import sleep
import modset_common as common

parser = argparse.ArgumentParser(
    prog="modset_tester.py",
    usage="%(prog)s [modset] [server-args] [options]",
    description="""Enables mods in a modset one-by-one until a server fails to launch.
    Note: Persistent must be enabled and a valid map must be set in the server.cfg.""",
)
parser.add_argument("modset")
parser.add_argument(
    "--server-cmd",
    help="command used to start the testing server (-mod and -noLogs will be ignored)",
    default="./arma3server_x64",
)
parser.add_argument(
    "--mods-path",
    help="directory containing all mods in the preset - you should run download_mods.py before this script",
    default=".",
)
parser.add_argument(
    "--debug",
    help="if set server output will be displayed via stdout",
    action="store_true",
)
args, unknown = parser.parse_known_args()

if len(unknown) > 0:
    print(
        "The following args were unrecognised and will be passed to the Arma 3 server:"
    )
    for arg in unknown:
        print(arg, end=" ")
    print("")

# Ensure the mods_path has a trailing /
if args.mods_path[-1] != "/":
    args.mods_path = args.mods_path + "/"
modset = common.ModSet.from_collection_preset(args.modset)
# Check that all the mods we need are already downloaded.
for mod in modset.mods:
    if not os.path.exists(args.mods_path + "@" + mod.name):
        raise Exception(
            "'@{}' was not found. Please download it or update the --mods-path argument.".format(
                mod.name
            )
        )


def get_mod_arg(mods):
    if len(mods) == 0:
        return None

    mod_string = ""

    for mod in mods:
        mod_string += "@" + mod.name + ";"

    return '-mod="' + mod_string + '"'


# Pass any unknown argparse arguments to the server.
server_cmd = [args.server_cmd, "-autoInit"]
server_cmd.extend(unknown)

# Ignore -mod and -noLogs arguments since they conflict
for arg in unknown:
    if "-mod=" in arg:
        unknown.remove(arg)
    if "-noLogs" in arg:
        unknown.remove(arg)


def test_mods(mods):
    cmd = server_cmd.copy()
    load_order = get_mod_arg(mods)
    if not load_order is None:
        cmd.append(load_order)

    # Print the command as a single string.
    for arg in cmd:
        print(arg, end=" ")
    print("")

    server = subprocess.Popen(
        cmd, shell=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    read_mission = False
    for line in server.stdout:
        if args.debug:
            print(line, end="")

        # Server should only read the mission once.
        if "Reading mission" in line:
            if read_mission:
                return False
            read_mission = True

        # -autoInit isn't working properly.
        if "Autoinit is supported only for persistent missions" in line:
            raise Exception(
                "Please enable persistent the server cfg and ensure the server is loading the config."
            )

        # Server seems to have started properly.
        if "Game started" in line:
            return True
    return False


print("Testing server without mods.")
if not test_mods([]):
    raise Exception("Sever failed to launch correctly without any mods.")

active_mods = []
failed_mods = []
last_mod = None
for mod in modset.mods:
    print("Testing '" + str(mod) + "'.")
    active_mods.append(mod)

    if not test_mods(active_mods):
        print(str(mod) + " caused the server to fail. Disabling and continuing.")
        active_mods.remove(mod)
        failed_mods.append(mod)

print("The following mods failed testing:")
for mod in failed_mods:
    print(mod, end=" ")
print("")

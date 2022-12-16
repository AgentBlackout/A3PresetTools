#!/usr/bin/env python3

import os
import argparse
import subprocess
import threading
import signal
import time
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
parser.add_argument(
    "--timeout",
    help="maximum time in seconds to allow for a mod to start",
    default=60,
    type=int,
)
parser.add_argument(
    "--readable-names",
    help="use escaped mod names for folder directories (by default mod ids are used)",
    action="store_true"
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

# Pass any unknown argparse arguments to the server.
server_cmd = [args.server_cmd, "-autoInit"]
server_cmd.extend(unknown)

# Ignore -mod and -noLogs arguments since they conflict
for arg in unknown:
    if "-mod=" in arg:
        unknown.remove(arg)
    if "-noLogs" in arg:
        unknown.remove(arg)


def test_mods(mods, max_duration):
    cmd = server_cmd.copy()
    mod_arg = "-mod=" + common.get_load_order(mods, args.readable_names)
    if not mod_arg is None:
        cmd.append(mod_arg)

    # Print the command as a single string.
    if args.debug:
        print("")
        for arg in cmd:
            print(arg, end=" ")
        print("")

    start_time = time.time()
    server = subprocess.Popen(
        cmd, shell=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    mutex = threading.Lock()
    def timeout():
        while (not mutex.locked()):
            time.sleep(0.5)

            if (start_time + max_duration <= time.time() and mutex.acquire(False)):
                os.kill(server.pid, signal.SIGTERM)
                print("server start timed out.")
                break
        
    timer = threading.Thread(target=timeout)
    timer.start()

    read_mission = False
    for line in server.stdout:
        if args.debug:
            print(line, end="")

        # Server should only read the mission once.
        if "Reading mission" in line:
            if read_mission and mutex.acquire(False):
                return False
            read_mission = True

        # -autoInit isn't working properly.
        if "Autoinit is supported only for persistent missions" in line:
            raise Exception(
                "please enable persistent the server cfg and ensure the server is loading the config."
            )

        # Server seems to have started properly.
        if "Game started" in line and mutex.acquire(False):
            return time.time() - start_time

    return False


print("Testing server without mods... ", end="")
runtime = test_mods([], 60)
if not runtime:
    raise Exception("Sever failed to launch correctly without any mods.")
else:
    print("Done.")

active_mods = []
failed_mods = []
last_mod = None
for mod in modset.mods:
    print("Testing '" + str(mod) + "'... ", end="")
    active_mods.append(mod)

    last_runtime = runtime
    runtime = test_mods(active_mods, last_runtime + args.timeout)
    if not runtime:
        print(str(mod) + " caused the server to fail. Disabling and continuing.")
        active_mods.remove(mod)
        failed_mods.append(mod)
    else:
        load_time = max(runtime - last_runtime, 0)
        print("added ~" + str(round(load_time, 2)) + "s to load time.")
    

if len(failed_mods) == 0:
    print("No mods failed testing")
else:
    print("The following mods failed testing:")
    for mod in failed_mods:
        print(mod, end=" ")
    print("")

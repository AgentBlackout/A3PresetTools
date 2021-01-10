import preset_common as common
import argparse
import math

parser = argparse.ArgumentParser(
    prog="total_preset_size.py",
    usage="%(prog)s [preset]",
    description="Computes the combined size of all mods in a preset.",
)
parser.add_argument("preset")
args = parser.parse_args()


def format_bytes(num):
    num = int(num)
    order = math.log(num, 10)
    if order > 9:
        return str(round(num / 10 ** 9, 2)) + " gb"
    if order > 6:
        return str(round(num / 10 ** 6, 2)) + " mb"
    if order > 3:
        return str(round(num / 10 ** 3, 2)) + " mb"
    else:
        return str(num) + " bytes"


preset = common.getPreset()
preset.query_details()

sizes = []
for mod in preset.mods:
    sizes.append(mod.get_size())

sorted(sizes)

for size in sizes:
    total_size += size
    print("'" + mod.name + "' is " + format_bytes(size))

print("Preset contains " + format_bytes(total_size) + " of mods.")
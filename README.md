# Preset ingest scripts

Just a few small scripts to ease intaking new presets.

## `extract_load_order.py`

This script is used to extract a presets load order which can then be coppied to the clipboard.

```
py ./extract_load_order.py <path-to-preset>
```

## `extract_mod_ids.py`

This script is used to create a file with a list of all mod ids for the steam mod update notifier.

```
py ./extract_mod_ids.py <path-to-preset>
```

Creates `mods.txt` file in the current folder.

## `compare_preset_deltas.py`

Compare the differences between two presets. Lists the common mods, and mods unique to either preset.

```
py ./compare_preset_deltas.py <path-to-preset> <path-to-preset>
```

# Preset ingest scripts

Just a few small scripts to ease dealing with presets.

## `extract_load_order.py`

Reads a presets load order for use in the '-mods=' argument which can then be copied to the clipboard.

```
py ./extract_load_order.py <path-to-preset>
```

## `extract_mod_ids.py`

Creates a file with a list of all mod ids.

```
py ./extract_mod_ids.py <path-to-preset>
```

Creates `mods.txt` file in the current folder.

## `compare_preset_deltas.py`

Compare the differences between two presets. Lists the common mods, and mods unique to either preset.

```
py ./compare_preset_deltas.py <path-to-preset> <path-to-preset>
```

## `download_mods.py`

Downloads the mods contained in a preset. Note that the steam user must have Arma 3 in their library.

```
py ./download_mods.py <path-to-preset> -u <steam-username> -p <steam-password>
```
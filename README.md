# Preset ingest scripts

Just a few small scripts to ease dealing with arma presets and workshop collections.

## `extract_load_order.py`

Reads a presets load order for use in the '-mods=' argument which can then be copied to the clipboard.

```
py ./extract_load_order.py <path-to-preset>
```

## `extract_mod_ids.py`

Creates a file with a list of all mod ids in a preset.

```
py ./extract_mod_ids.py <path-to-preset>
```

Creates `mods.txt` file in the current folder.

## `compare_modset_deltas.py`

Lists the mods common and unique to a pair of presets/ workshop collections.

```
py ./compare_preset_deltas.py <path-to-preset-or-collection-id> <path-to-preset-or-collection-id>
```

## `download_mods.py`

Downloads the mods contained in a preset or workshop collection. Note that the steam user must have Arma 3 in their library.

```
py ./download_mods.py <path-to-preset-or-collection-id> -u <steam-username> -p <steam-password>
```

## `total_modset_size.py`

Determines the individual size and total size of all mods in a preset or steam collection.

```
py ./total_modset_size.py <path-to-preset-or-collection-id>
```

## `collect_keys.py`

Moves the .bikey files in the downloaded mods contained in a preset or workshop collection to a single folder (for use with server/keys).

```
py ./collect_keys.py <path-to-preset-or-collection-id>
```

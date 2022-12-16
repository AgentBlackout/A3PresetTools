#!/usr/bin/env python3

ARMA3_APPID = "107410"

STEAM_URL_FORMAT = "http://steamcommunity.com/sharedfiles/filedetails/?id="

PUBLISHED_FILE_DETAILS_ENDPOINT = (
    "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
)

COLLECTION_DETAILS_ENDPOINT = (
    "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
)

STEAM_MOD_FORMAT = """
            <tr data-type="ModContainer">
                <td data-type="DisplayName">{mod_name}</td>
                <td>
                    <span class="from-steam">Steam</span>
                </td>
                <td>
                    <a href="{mod_url}" data-type="Link">{mod_url}</a>
                </td>
            </tr>"""

PRESET_FORMAT = """
<?xml version="1.0" encoding="utf-8"?>
<html>
    <head>
        <meta name="arma:Type" content="preset" />
        <meta name="arma:PresetName" content="{preset_name}" />
        <meta name="generator" content="A3PresetTools - https://github.com/AgentBlackout/A3PresetTools" />
        <title>Arma 3</title>
        <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" type="text/css" />
        <style>
body {{
    margin: 0;
	padding: 0;
	color: #fff;
	background: #000;
}}

body, th, td {{
	font: 95%/1.3 Roboto, Segoe UI, Tahoma, Arial, Helvetica, sans-serif;
}}

td {{
    padding: 3px 30px 3px 0;
}}

h1 {{
    padding: 20px 20px 0 20px;
    color: white;
    font-weight: 200;
    font-family: segoe ui;
    font-size: 3em;
    margin: 0;
}}

em {{
    font-variant: italic;
    color:silver;
}}

.before-list {{
    padding: 5px 20px 10px 20px;
}}

.mod-list {{
    background: #222222;
    padding: 20px;
}}

.dlc-list {{
    background: #222222;
    padding: 20px;
}}

.footer {{
    padding: 20px;
    color:gray;
}}

.whups {{
    color:gray;
}}

a {{
    color: #D18F21;
    text-decoration: underline;
}}

a:hover {{
    color:#F1AF41;
    text-decoration: none;
}}

.from-steam {{
    color: #449EBD;
}}
.from-local {{
    color: gray;
}}

    </style>
</head>
<body>
    <h1>Arma 3  - Preset <strong>{preset_name}</strong></h1>
    <p class="before-list">
      <em>Drag this file or link to it to Arma 3 Launcher or open it Mods / Preset / Import.</em>
    </p>
    <div class="mod-list">
        <table>
{mod_list}
        </table>
    </div>
    <div class="footer">
      <span>Created by Arma 3 Launcher by Bohemia Interactive.</span>
    </div>
</body>
</html>"""

if __name__ == "__main__":
    print("Don't run this, this is a common library!")

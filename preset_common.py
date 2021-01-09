import os
import sys
import requests
from bs4 import BeautifulSoup

STEAM_URL_FORMAT = "http://steamcommunity.com/sharedfiles/filedetails/?id="

PUBLISHED_FILE_DETAILS_ENDPOINT = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1"


class Mod:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self._details = None

    def __eq__(self, other):
        if not isinstance(other, Mod):
            return False
        if not self.id == other.id:
            return False
        return True

    def __repr__(self):
        return self.name + " (" + STEAM_URL_FORMAT + self.id + ")"

    def get_details(self, force_refresh=False):
        if self._details is None or force_refresh:
            data = [("itemcount", "1"), ("publishedfileids[0]", self.id)]
            response = requests.post(PUBLISHED_FILE_DETAILS_ENDPOINT, data=data)
            if response.status_code != 200:
                raise Exception("Steam API query failed for '" + self.name + "'")
            self._details = response.json()["response"]["publishedfiledetails"][0]
        return self._details

    def get_size(self):
        return self.get_details()["file_size"]


class Preset:
    def __init__(self, name, mods):
        self.name = name
        self.mods = mods


def __getPath():
    args = sys.argv
    if len(args) > 1:  # A file has been dragged onto the script
        return args[1]
    print("Where is the preset located?")
    path = input(">")
    if os.path.exists(path):
        return path
    raise Exception("Please enter a valid path.")


def __getSoup(path):
    if not os.path.exists(path):
        print("Invalid path!")
        raise Exception("Invalid preset path")
    fileContent = ""
    with open(path, "r") as f:
        fileContent = "\n".join(f.readlines())
    return BeautifulSoup(fileContent, "html.parser")


def __metaGetTitle(soup):
    metas = soup.find_all("meta")
    for meta in metas:
        if meta["name"] == "arma:PresetName":
            return meta["content"]
    return "Invalid Preset"


def __getMod(tr):
    name = tr.td.text
    url = tr.a.text
    id = url[len(STEAM_URL_FORMAT) :]
    return Mod(name, id)


def __getMods(soup):
    modHtmls = soup.find_all("tr")
    mods = []
    for modHtml in modHtmls:
        mods.append(__getMod(modHtml))
    return mods


def getPreset(path=None):
    if path == None:
        path = __getPath()
    soup = __getSoup(path)
    title = __metaGetTitle(soup)
    mods = __getMods(soup)
    return Preset(title, mods)


if __name__ == "__main__":
    print("Don't run this, this is a common library!")

import os
import sys
import requests
from bs4 import BeautifulSoup

STEAM_URL_FORMAT = "http://steamcommunity.com/sharedfiles/filedetails/?id="
PUBLISHED_FILE_DETAILS_ENDPOINT = (
    "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
)
COLLECTION_DETAILS_ENDPOINT = (
    "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
)


class Mod:
    @staticmethod
    def from_api_details(details):
        return Mod(details["title"], details["publishedfileid"], details["file_size"])

    def __init__(self, name, id, size):
        if sys.platform == "linux" or sys.platform == "linux2":
            self.name = name.replace(" ", "_")
        else:
            self.name = name
        self.id = id
        self.size = size

    def __eq__(self, other):
        if not isinstance(other, Mod):
            return False
        if not self.id == other.id:
            return False
        return True

    def __repr__(self):
        return self.name + " (" + STEAM_URL_FORMAT + self.id + ")"


class ModSet:
    @staticmethod
    def from_collection(id):
        ids = ModSet.__get_collection_ids(id)
        ids.append(id)
        details = ModSet.__get_published_file_details(ids)
        title = details[-1]["title"]
        mods = ModSet.__get_mods(details[:-1])
        return ModSet(title, mods)

    @staticmethod
    def from_preset(path):
        if not os.path.isfile(path):
            raise Exception("Preset does not exist at '" + path + "'.")

        soup = ModSet.__get_preset_soup(path)
        title = ModSet.__get_preset_title(soup)
        ids = ModSet.__get_preset_mod_ids(soup)
        details = ModSet.__get_published_file_details(ids)
        mods = []
        for modDetails in details:
            if not "title" in modDetails:
                # Mod title is unavailable (eg mod is unlisted) so fallback to the name in the preset.
                details.remove(modDetails)
                name = ModSet.__find_preset_mod_name(
                    modDetails["publishedfileid"], soup
                )
                mods.append(Mod(name, modDetails["publishedfileid"], float("nan")))

        mods.extend(ModSet.__get_mods(details))
        return ModSet(title, mods)

    @staticmethod
    def from_collection_preset(input):
        if input.isnumeric():
            return ModSet.from_collection(input)
        elif "steamcommunity.com/sharedfiles/filedetails/?id=" in input:
            return ModSet.from_collection(input.split("id=")[1])
        else:
            return ModSet.from_preset(input)

    def __init__(self, name, mods):
        self.name = name
        self.mods = mods

    @staticmethod
    def __get_published_file_details(ids):
        data = {"itemcount": str(len(ids))}
        for i in range(len(ids)):
            data.update({"publishedfileids[" + str(i) + "]": ids[i]})
        response = requests.post(PUBLISHED_FILE_DETAILS_ENDPOINT, data=data)
        if response.status_code != 200:
            raise Exception("Steam GetPublishedFileDetails API failed")
        return response.json()["response"]["publishedfiledetails"]

    @staticmethod
    def __get_mods(details):
        mods = []
        for item in details:
            mods.append(Mod.from_api_details(item))
        return mods

    @staticmethod
    def __get_collection_ids(id):
        data = {"collectioncount": "1", "publishedfileids[0]": id}
        response = requests.post(COLLECTION_DETAILS_ENDPOINT, data=data)
        if response.status_code != 200:
            raise Exception("Steam GetCollectionDetails API failed")
        children = response.json()["response"]["collectiondetails"][0]["children"]
        ids = []
        for child in children:
            ids.append(child["publishedfileid"])
        return ids

    @staticmethod
    def __get_preset_soup(path):
        if not os.path.exists(path):
            print("Invalid path!")
            raise Exception("Invalid preset path")
        fileContent = ""
        with open(path, "r") as f:
            fileContent = "\n".join(f.readlines())
        return BeautifulSoup(fileContent, "html.parser")

    @staticmethod
    def __get_preset_title(soup):
        metas = soup.find_all("meta")
        for meta in metas:
            if meta["name"] == "arma:PresetName":
                return meta["content"]
        return "Invalid Preset"

    @staticmethod
    def __get_preset_mod_name(tr):
        return tr.td.text

    @staticmethod
    def __find_preset_mod_name(id, soup):
        modHtmls = soup.find_all("tr")
        for modHtml in modHtmls:
            if ModSet.__get_preset_mod_id(modHtml) == id:
                return ModSet.__get_preset_mod_name(modHtml)

        raise Exception("Could not find mod with id '" + id + "' in the preset.")

    @staticmethod
    def __get_preset_mod_id(tr):
        url = tr.a.text
        id = url[len(STEAM_URL_FORMAT) :]
        return id

    @staticmethod
    def __get_preset_mod_ids(soup):
        modHtmls = soup.find_all("tr")
        mods = []
        for modHtml in modHtmls:
            mods.append(ModSet.__get_preset_mod_id(modHtml))
        return mods


if __name__ == "__main__":
    print("Don't run this, this is a common library!")

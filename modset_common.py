#!/usr/bin/env python3

import os
import re
import requests
from modset_constants import *
from bs4 import BeautifulSoup


class Mod:
    @staticmethod
    def from_api_details(details):
        return Mod(
            details["title"] if "title" in details else None,
            details["publishedfileid"],
            details["file_size"] if "file_size" in details else None,
        )

    def __init__(self, name, id, size):
        if name is None:
            self.name = id
        else:
            name = name.replace(" ", "_")
            self.name = re.sub(r"[\\\/:*?\"<>|]", "", name)

        self.id = id
        self.size = size

    def __eq__(self, other):
        if not isinstance(other, Mod):
            return False
        if not self.id == other.id:
            return False
        return True

    def __repr__(self):
        return self.name + " (" + self.get_url() + ")"

    def get_url(self):
        return STEAM_URL_FORMAT + self.id


class ModSet:
    @staticmethod
    def from_collection(id):
        ids = ModSet.__get_collection_ids(id)
        ids.append(id)
        details = ModSet.__get_published_file_details(ids)
        title = details[-1]["title"]
        mods = ModSet.__get_mods(details[:-1])
        return ModSet(title, mods, id)

    @staticmethod
    def from_preset(path):
        if not os.path.isfile(path):
            raise Exception("Preset does not exist at '" + path + "'.")

        soup = ModSet.__get_preset_soup(path)
        title = ModSet.__get_preset_title(soup)
        ids = ModSet.__get_preset_mod_ids(soup)
        details = ModSet.__get_published_file_details(ids)
        mods = ModSet.__get_mods(details)

        for mod in mods:
            # Mod title is unavailable (eg mod is unlisted) so fallback to the name in the preset.
            if mod.name is None:
                mod.name = ModSet.__find_preset_mod_name(mod.id, soup)
                
        return ModSet(title, mods)

    @staticmethod
    def from_collection_preset(input):
        if input.isnumeric():
            return ModSet.from_collection(input)
        elif "id=" in input:
            return ModSet.from_collection(input.split("id=")[1])
        else:
            return ModSet.from_preset(input)

    def __init__(self, name, mods, id=None):
        self.name = name
        self.mods = mods
        self.id = id

    def is_preset(self):
        return self.id is None

    def is_collection(self):
        return not self.id is None

    def get_url(self):
        return (STEAM_URL_FORMAT + self.id) if self.is_collection() else None

    def export_preset(self, outfile):
        mod_list = ""
        for mod in self.mods:
            mod_list += STEAM_MOD_FORMAT.format(
                mod_name=mod.name, mod_url=mod.get_url()
            )
        preset = PRESET_FORMAT.format(preset_name=self.name, mod_list=mod_list)
        out = open(outfile, "wt")
        out.write(preset)
        out.close()
        
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
        id = url.split("id=")[1]
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

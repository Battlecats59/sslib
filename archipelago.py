import base64
import yaml
import random
import os
from pathlib import Path

from logic.logic_input import Areas
from logic.placement_file import PlacementFile
from options import Options, OPTIONS
from version import VERSION


class Archipelago:
    def __init__(self, apssr: str):
        if os.path.isfile(apssr) and Path(apssr).suffix == ".apssr":
            pass
        else:
            raise Exception("Invalid APSSR file.")

        apdata = self.load_apssr_yaml(apssr)
        self.apversion: list = apdata["AP Version"]
        self.worldversion: list = apdata["World Version"]
        self.hash: str = apdata["Hash"]
        self.apseed: int = int(apdata["AP Seed"])
        self.randoseed: int = apdata["Rando Seed"]
        self.player: int = apdata["Slot"]
        self.name: str = apdata["Name"]
        self.all_players: list[str] = apdata["All Players"]
        self.options: dict[str, any] = apdata["Options"]
        self.starting_items: list = apdata["Starting Items"]
        self.dungeons: list[str] = apdata["Required Dungeons"]
        self.locations: dict[str, dict] = apdata["Locations"]
        self.hints: dict[str, list] = apdata["Hints"]
        self.impa_hint: tuple[str, str] | None = apdata["SoT Location"]
        self.dungeon_connections: dict[str, str] = apdata["Dungeon Entrances"]
        self.trial_connections: dict[str, str] = apdata["Trial Entrances"]

    def fill_placement_file(
        self, options: Options, areas: Areas, rng: random.Random
    ) -> PlacementFile:
        self.placement_file = PlacementFile()
        self.placement_file.version = VERSION
        self.placement_file.options = options
        for optkey, opt in OPTIONS.items():  # Set placement file options
            if "cosmetic" in opt:
                pass
            elif optkey in UNTOUCHED_OPTIONS:
                pass
            elif optkey in FORCED_OPTIONS:
                self.placement_file.options.set_option(optkey, FORCED_OPTIONS[optkey])
                options.set_option(optkey, FORCED_OPTIONS[optkey])
            elif optkey in self.options:
                if opt["type"] == "boolean":
                    self.placement_file.options.set_option(
                        optkey, bool(self.options[optkey])
                    )
                    options.set_option(optkey, bool(self.options[optkey]))
                elif opt["type"] == "singlechoice":
                    self.placement_file.options.set_option(
                        optkey, opt["choices"][self.options[optkey]]
                    )
                    options.set_option(optkey, opt["choices"][self.options[optkey]])
                elif opt["type"] == "int":
                    self.placement_file.options.set_option(optkey, self.options[optkey])
                    options.set_option(optkey, self.options[optkey])
                elif optkey == "starting-items":
                    self.placement_file.options.set_option(optkey, [])
                    options.set_option(optkey, [])
                else:
                    print("unknown type yet found in apssr: " + optkey)
            else:
                print("Could not find a value to set option: " + optkey)
        self.placement_file.hash_str = self.hash
        self.placement_file.starting_items.extend(self.starting_items)
        self.placement_file.required_dungeons.extend(self.dungeons)
        for loc, itm in self.locations.items():
            if itm["player"] != self.player:
                if itm["game"] == "Skyward Sword":
                    if itm["name"] in SS_ARCHIPELAGO_SPECIAL_ITEMS:
                        item_to_place = SS_ARCHIPELAGO_SPECIAL_ITEMS[itm["name"]][0]
                    else:
                        item_to_place = "Archipelago Item"
                else:
                    item_to_place = (
                        "Archipelago Item"  # Represents a general Archipelago item
                    )
            else:
                item_to_place = itm["name"]
            self.placement_file.item_locations[areas.short_to_full(loc)] = item_to_place
            self.placement_file.chest_dowsing[areas.short_to_full(loc)] = self.get_dowsing_slot(itm, options)
        for hint, data in self.hints.items():
            if "Gossip Stone" in hint:
                self.placement_file.hints[areas.short_to_full(hint)] = data
            else:
                self.placement_file.hints[hint] = data
        self.placement_file.dungeon_connections = self.dungeon_connections
        self.placement_file.trial_connections = self.trial_connections
        self.placement_file.trial_object_seed = rng.randint(1, 1_000_000)
        self.placement_file.music_rando_seed = rng.randint(1, 1_000_000)
        self.placement_file.bk_angle_seed = rng.randint(1, 2**32 - 1)

        return self.placement_file

    def load_apssr_yaml(self, fp) -> dict:
        with open(fp, "r") as apssr:
            apssr_encoded = apssr.read()
        apssr_decoded = base64.b64decode(apssr_encoded)
        return yaml.safe_load(apssr_decoded)

    def get_dowsing_slot(self, item, options) -> int:
        # Get info for which dowsing slot (if any) a chest should respond to.
        # Dowsing slots:
        # 0: Main quest
        # 1: Rupee
        # 2: Key Piece / Scrapper Quest
        # 3: Crystal
        # 4: Heart
        # 5: Goddess Cube
        # 6: Look around (not usable afaik)
        # 7: Treasure
        # 8: None
        dowsing_setting = options.get("chest-dowsing")
        if dowsing_setting == "Vanilla":
            return 8
        elif dowsing_setting == "All Chests":
            return 0
        else:
            assert dowsing_setting == "Progress Items"
            if item["classification"] in ["progression", "progression_skip_balancing", "trap"]:
                return 0
            return 8

SS_ARCHIPELAGO_SPECIAL_ITEMS = {
    # These items have their normal models if you find another player's
    "Progressive Sword": ["Archipelago Sword", 217],
    "Goddess's Harp": ["Archipelago Harp", 218],
    "Progressive Bow": ["Archipelago Bow", 219],
    "Clawshots": ["Archipelago Clawshots", 220],
    "Spiral Charge": ["Archipelago Spiral Charge", 221],
    "Gust Bellows": ["Archipelago Gust Bellows", 222],
    "Progressive Slingshot": ["Archipelago Slingshot", 223],
    "Progressive Beetle": ["Archipelago Beetle", 224],
    "Progressive Mitts": ["Archipelago Mitts", 225],
    "Water Dragon's Scale": ["Archipelago Scale", 226],
    "Progressive Bug Net": ["Archipelago Bug Net", 227],
    "Bomb Bag": ["Archipelago Bomb Bag", 228],
    "Triforce of Courage": ["Archipelago Triforce", 229],
    "Triforce of Power": ["Archipelago Triforce", 229],
    "Triforce of Wisdom": ["Archipelago Triforce", 229],
    "Whip": ["Archipelago Whip", 230],
    "Fireshield Earrings": ["Archipelago Earrings", 231],
    "Tumbleweed": ["Archipelago Tumbleweed", 232],
    "Emerald Tablet": ["Archipelago Emerald Tablet", 233],
    "Ruby Tablet": ["Archipelago Ruby Tablet", 234],
    "Amber Tablet": ["Archipelago Amber Tablet", 235],
    "Stone of Trials": ["Archipelago Stone of Trials", 236],
    "Scrapper": ["Archipelago Scrapper", 237],
}

UNTOUCHED_OPTIONS = [
    # If cosmetic, assume untouched
    "dry-run",
    "output-folder",
    "json",
    "noui",
    "apssr",
    "gui-theme",
    "gui-theme-preset",
    "use-custom-theme",
    "font-family",
    "font-size",
    "use-sharp-corners",
    "seed",
    "no-spoiler-log",
    "out-placement-file",
]

FORCED_OPTIONS = {
    "logic-mode": "BiTless",
    "enabled-tricks-bitless": [],
    "enabled-tricks-glitched": [],
    "excluded-locations": [],
    "hint-distribution": "Balanced",
}

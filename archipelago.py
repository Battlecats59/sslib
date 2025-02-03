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
        self.options: dict[str, any] = apdata["Options"]
        self.starting_items: list = apdata["Starting Items"]
        self.dungeons: list[str] = apdata["Required Dungeons"]
        self.locations: dict[str, dict] = apdata["Locations"]
        self.hints: dict[str, list] = apdata["Hints"]
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
                item_to_place = "Archipelago"  # Represents an Archipelago item, for now
            else:
                item_to_place = itm["name"]
            self.placement_file.item_locations[areas.short_to_full(loc)] = item_to_place
            self.placement_file.chest_dowsing[areas.short_to_full(loc)] = itm[
                "chest_dowsing"
            ]
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
    "impa-sot-hint": False,
    "logic-mode": "BiTless",
    "enabled-tricks-bitless": [],
    "enabled-tricks-glitched": [],
    "excluded-locations": [],
    "hint-distribution": "Balanced",
}

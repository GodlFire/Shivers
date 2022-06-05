"""
Defines progression, junk and event items for The Witness
"""
import copy
from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, MultiWorld
from . import StaticWitnessLogic, WitnessPlayerLocations, WitnessPlayerLogic
from .Options import get_option_value, is_option_enabled
from fractions import Fraction


class ItemData(NamedTuple):
    """
    ItemData for an item in The Witness
    """
    code: Optional[int]
    progression: bool
    event: bool = False
    trap: bool = False


class WitnessItem(Item):
    """
    Item from the game The Witness
    """
    game: str = "The Witness"


class StaticWitnessItems:
    """
    Class that handles Witness items independent of world settings
    """

    ALL_ITEM_TABLE: Dict[str, ItemData] = {}

    # These should always add up to 1!!!
    BONUS_WEIGHTS = {
        "Speed Boost": Fraction(1, 1),
    }

    # These should always add up to 1!!!
    TRAP_WEIGHTS = {   
        "Slowness": Fraction(8, 10),
        "Power Surge": Fraction(2, 10),
    }

    ALL_JUNK_ITEMS = set(BONUS_WEIGHTS.keys()) | set(TRAP_WEIGHTS.keys())

    def __init__(self):
        item_tab = dict()

        for item in StaticWitnessLogic.ALL_ITEMS:
            if item[0] == "11 Lasers" or item == "7 Lasers":
                continue

            item_tab[item[0]] = ItemData(158000 + item[1], True, False)

        for item in StaticWitnessLogic.ALL_TRAPS:
            item_tab[item[0]] = ItemData(
                158000 + item[1], False, False, True
            )

        for item in StaticWitnessLogic.ALL_BOOSTS:
            item_tab[item[0]] = ItemData(158000 + item[1], False, False)

        item_tab = dict(sorted(
            item_tab.items(),
            key=lambda single_item: single_item[1].code
            if isinstance(single_item[1].code, int) else 0)
        )

        for key, item in item_tab.items():
            self.ALL_ITEM_TABLE[key] = item


class WitnessPlayerItems:
    """
    Class that defines Items for a single world
    """

    def __init__(self, locat: WitnessPlayerLocations, world: MultiWorld, player: int, player_logic: WitnessPlayerLogic):
        """Adds event items after logic changes due to options"""
        self.EVENT_ITEM_TABLE = dict()
        self.ITEM_TABLE = copy.copy(StaticWitnessItems.ALL_ITEM_TABLE)

        self.GOOD_ITEMS = [
            "Dots", "Black/White Squares", "Stars",
            "Shapers", "Symmetry"
        ]

        if is_option_enabled(world, player, "shuffle_discarded_panels"):
            self.GOOD_ITEMS.append("Triangles")
        if not is_option_enabled(world, player, "disable_non_randomized_puzzles"):
            self.GOOD_ITEMS.append("Colored Squares")

        for event_location in locat.EVENT_LOCATION_TABLE:
            location = player_logic.EVENT_ITEM_PAIRS[event_location]
            self.EVENT_ITEM_TABLE[location] = ItemData(None, True, True)
            self.ITEM_TABLE[location] = ItemData(None, True, True)

        trap_percentage = get_option_value(world, player, "trap_percentage")

        self.JUNK_WEIGHTS = dict()

        if trap_percentage != 0:
            # I'm sure there must be some super "pythonic" way of doing this :D

            for trap_name, trap_weight in StaticWitnessItems.TRAP_WEIGHTS.items():
                self.JUNK_WEIGHTS[trap_name] = (trap_weight * trap_percentage) / 100

        if trap_percentage != 100:
            for bonus_name, bonus_weight in StaticWitnessItems.BONUS_WEIGHTS.items():
                self.JUNK_WEIGHTS[bonus_name] = (bonus_weight * (100 - trap_percentage)) / 100

        self.JUNK_WEIGHTS = {
            key: value for (key, value)
            in self.JUNK_WEIGHTS.items()
            if key in self.ITEM_TABLE.keys()
        }

        # JUNK_WEIGHTS will add up to 1 if the boosts weights and the trap weights each add up to 1 respectively.

        for junk_item in StaticWitnessItems.ALL_JUNK_ITEMS:
            if junk_item not in self.JUNK_WEIGHTS.keys():
                del self.ITEM_TABLE[junk_item]
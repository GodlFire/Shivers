from Options import Choice, DefaultOnToggle, Toggle, PerGameCommonOptions, Range
from dataclasses import dataclass


class IxupiCapturesNeeded(Range):
    """
    Number of Ixupi Captures needed for goal condition.
    """
    display_name = "Number of Ixupi Captures Needed"
    range_start = 1
    range_end = 10
    default = 10

class LobbyAccess(Choice):
    """Chooses how keys needed to reach the lobby are placed.
    - Normal: Keys are placed anywhere
    - Early: Keys are placed early 
    - Local: Keys are placed locally
    """
    display_name = "Lobby Access"
    option_normal = 0
    option_early = 1
    option_local = 2
    default = 1

class PuzzleHintsRequired(DefaultOnToggle):
    """
    If turned on puzzle hints will be available before the corresponding puzzle is required. For example: The Shaman
    Drums puzzle will be placed after access to the security cameras which give you the solution. Turning this off
    allows for greater randomization.
    """
    display_name = "Puzzle Hints Required"

class InformationPlaques(Toggle):
    """
    Adds Information Plaques as checks.
    (40 Locations)
    """
    display_name = "Include Information Plaques"

class FrontDoorUsable(Toggle):
    """
    Adds a key to unlock the front door of the museum.
    """
    display_name = "Front Door Usable"

class ElevatorsStaySolved(DefaultOnToggle):
    """
    Adds elevators as checks and will remain open upon solving them.
    (3 Locations)
    """
    display_name = "Elevators Stay Solved"

class EarlyBeth(DefaultOnToggle):
    """
    Beth's body is open at the start of the game. This allows any pot piece to be placed in the slide and early checks on the second half of the final riddle.
    """
    display_name = "Early Beth"

class EarlyLightning(Toggle):
    """
    Allows lightning to be captured at any point in the game. You will still need to capture all ten Ixupi for victory.
    (1 Location)
    """
    display_name = "Early Lightning"

class LocationPotPieces(Choice):
    """
    Chooses where pot pieces will be located within the multiworld.
    - Own World: Pot pieces will be located within your own world
    - Different World: Pot pieces will be located in another world
    - Any World: Pot pieces will be located in any world
    """
    display_name = "Location of Pot Pieces"
    option_own_world = 0
    option_different_world = 1
    option_any_world = 2

class FullPots(Choice):
    """
    Chooses if pots will be in pieces or already completed
    - Pieces: Only pot pieces will be added to the item pool
    - Complete: Only completed pots will be added to the item pool
    - Mixed: Each pot will be randomly chosen to be pieces or already completed.
    """
    display_name = "Full Pots"
    option_pieces = 0
    option_complete = 1
    option_mixed = 2

class IxupiCapturesPriority(DefaultOnToggle):
    """
    Ixupi captures are set to priority locations. This forces a progression item into these locations if possible.
    """
    display_name = "Ixupi Captures are Priority"


@dataclass
class ShiversOptions(PerGameCommonOptions):
    ixupi_captures_needed: IxupiCapturesNeeded
    lobby_access: LobbyAccess
    puzzle_hints_required: PuzzleHintsRequired
    include_information_plaques: InformationPlaques
    front_door_usable: FrontDoorUsable
    elevators_stay_solved: ElevatorsStaySolved
    early_beth: EarlyBeth
    early_lightning: EarlyLightning
    location_pot_pieces: LocationPotPieces
    ixupi_captures_priority: IxupiCapturesPriority
    full_pots: FullPots

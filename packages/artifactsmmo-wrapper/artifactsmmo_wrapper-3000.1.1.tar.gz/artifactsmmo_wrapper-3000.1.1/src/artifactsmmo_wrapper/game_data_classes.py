from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any
from .log import logger

# --- Dataclasses ---
# --- Utility ---
@dataclass
class Position:
    """Represents a position on a 2D grid."""
    x: int
    y: int

    def __repr__(self) -> str:
        """String representation of the position in (x, y) format."""
        return f"({self.x}, {self.y})"

    def dist(self, other: 'Position') -> int:
        """
        Calculate the Manhattan distance to another position.
        
        Args:
            other (Position): The other position to calculate distance to.
        
        Returns:
            int: Manhattan distance to the other position.
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __iter__(self):
        yield self.x
        yield self.y

@dataclass
class Drop:
    code: str
    rate: int
    min_quantity: int
    max_quantity: int

@dataclass
class ContentMap:
    name: str
    code: str
    level: int
    skill: str
    pos: Position
    drops: List[Drop]

    def __iter__(self):
        yield self.pos.x
        yield self.pos.y

    def __repr__(self) -> str:
        return f"{self.name} ({self.code}) at {self.pos}\n  Requires {self.skill} level {self.level}"
    
@dataclass
class Content:
    type: str
    code: str

@dataclass
class TaskReward:
    items: List[Dict[str, Any]]
    gold: int

@dataclass
class Effect:
    code: str
    name: str
    description: str
    attributes: Dict[str, Any]

@dataclass
class CraftingRecipe:
    skill: Optional[str]
    level: Optional[int]
    items: Optional[List[dict]]  # Example: [{'code': 'iron', 'quantity': 6}]
    quantity: Optional[int]

@dataclass
class AchievementReward:
    gold: int

# --- subclass related ---
@dataclass
class Item:
    name: str
    code: str
    type: str
    subtype: Optional[str]
    description: Optional[str]
    effects: Optional[List[Effect]]
    craft: Optional[Dict[str, Any]]
    tradeable: bool = False
    level: Optional[int] = None

@dataclass
class Map:
    x: int
    y: int
    content_code: Optional[str]
    content_type: Optional[str]

@dataclass
class Monster:
    code: str
    name: str
    level: int
    hp: int
    attack_fire: int
    attack_earth: int
    attack_water: int
    attack_air: int
    res_fire: int
    res_earth: int
    res_water: int
    res_air: int
    min_gold: int
    max_gold: int
    drops: List[Drop]

@dataclass
class Resource:
    code: str
    name: str
    skill: Optional[str]
    level: int
    drops: List[Drop]

@dataclass
class Task:
    code: str
    level: int
    type: Optional[str]
    min_quantity: int
    max_quantity: int
    skill: Optional[str]
    rewards: Optional[TaskReward]

@dataclass
class Reward:
    code: str
    rate: int
    min_quantity: int
    max_quantity: int

@dataclass
class Achievement:
    code: str
    name: str
    description: str
    points: int
    type: str
    target: int
    total: int
    rewards_gold: int

# --- Other ---

class ContentMaps:
    def __init__(self, api):
        logger.debug("Initializing ContentMaps", src="Root")
        self.api = api
        self.maps: Dict[str, ContentMap] = {}  # Initialize the maps attribute as an empty dictionary
        self._cache_content_maps()
        self._initialize_attributes()


    def _cache_content_maps(self, force=False):
        """
        Fetch all content maps using `api.maps.get` and populate them based on content type.
        """
        try:
            logger.debug("Fetching all maps using api.maps.get()", src=self.api.char.name)
            all_maps = self.api.maps.get()  # Use the updated `get` method
            logger.debug(f"Retrieved {len(all_maps)} maps from the API", src=self.api.char.name)

            # Process each map and populate the maps dictionary
            for map_data in all_maps:
                x, y = map_data.x, map_data.y
                content_type = map_data.content_type
                content_code = map_data.content_code

                # Fetch content-specific data
                if content_type == "monster":
                    monster = self.api.monsters.get(content_code)
                    name = monster.name
                    level = monster.level
                    skill = "combat"
                    drops = monster.drops
                elif content_type == "resource":
                    resource = self.api.resources.get(content_code)
                    name = resource.name
                    level = resource.level
                    skill = resource.skill
                    drops = resource.drops
                elif content_type == "workshop":
                    name = f"{content_code.capitalize()} Workshop"
                    level = None
                    skill = None
                    drops = []
                elif content_type == "":
                    continue
                else:
                    name = f"{content_code.capitalize()}"
                    level = None
                    skill = None
                    drops = []

                position = Position(x, y)
                content_map = ContentMap(
                    name=name,
                    code=content_code,
                    level=level,
                    skill=skill,
                    pos=position,
                    drops=drops
                )

                # Handle duplicates based on Manhattan distance from (0, 0)
                if content_code in self.maps:
                    existing_map = self.maps[content_code]
                    new_distance = position.dist(Position(0, 0))
                    existing_distance = existing_map.pos.dist(Position(0, 0))
                    if new_distance < existing_distance:
                        self.maps[content_code] = content_map
                else:
                    self.maps[content_code] = content_map

            logger.debug(f"Finished caching {len(self.maps)} content maps", src=self.api.char.name)

        except Exception as e:
            logger.error(f"Error while caching content maps: {e}", src="Root")

    def _initialize_attributes(self):
        """
        Dynamically create attributes for each content map.
        """
        for map_code, content_map in self.maps.items():
            attribute_name = self._sanitize_attribute_name(map_code)
            setattr(self, attribute_name, content_map)

    @staticmethod
    def _sanitize_attribute_name(name: str) -> str:
        """
        Sanitize map codes to create valid Python attribute names.

        Args:
            name (str): The original map code.

        Returns:
            str: A sanitized attribute name.
        """
        return name.lower().replace(" ", "_").replace("-", "_")

    def get_map(self, code: str) -> Optional[ContentMap]:
        """
        Retrieve a specific content map by its code.

        Args:
            code (str): The unique code for the content map.

        Returns:
            ContentMap or None: The content map if found, otherwise None.
        """
        return self.maps.get(code)

    def get_all_maps(self) -> List[ContentMap]:
        """
        Retrieve all cached content maps.

        Returns:
            List[ContentMap]: List of all cached content maps.
        """
        return list(self.maps.values())

@dataclass
class InventoryItem:
    """Represents an item in the player's inventory."""
    slot: int
    code: str
    quantity: int

    def __repr__(self) -> str:
        """String representation of the inventory item."""
        return f"({self.slot}) {self.quantity}x {self.code}"


@dataclass
class PlayerData:
    """
    Represents all data and stats related to a player.
    
    Attributes include levels, experience, stats, elemental attributes, 
    position, inventory, equipment slots, and task information.
    """
    name: str
    account: str
    skin: str
    level: int
    xp: int
    max_xp: int
    gold: int
    speed: int
    
    # Skill levels and XP
    mining_level: int
    mining_xp: int
    mining_max_xp: int
    woodcutting_level: int
    woodcutting_xp: int
    woodcutting_max_xp: int
    fishing_level: int
    fishing_xp: int
    fishing_max_xp: int
    weaponcrafting_level: int
    weaponcrafting_xp: int
    weaponcrafting_max_xp: int
    gearcrafting_level: int
    gearcrafting_xp: int
    gearcrafting_max_xp: int
    jewelrycrafting_level: int
    jewelrycrafting_xp: int
    jewelrycrafting_max_xp: int
    cooking_level: int
    cooking_xp: int
    cooking_max_xp: int
    alchemy_level: int
    alchemy_xp: int
    alchemy_max_xp: int

    # Stats
    hp: int
    max_hp: int
    haste: int
    critical_strike: int
    
    # Elemental attributes
    attack_fire: int
    attack_earth: int
    attack_water: int
    attack_air: int
    dmg: int
    dmg_fire: int
    dmg_earth: int
    dmg_water: int
    dmg_air: int
    res_fire: int
    res_earth: int
    res_water: int
    res_air: int
    
    # Position and state
    pos: Position
    cooldown: int
    cooldown_expiration: str
    
    # Equipment slots
    weapon_slot: str
    shield_slot: str
    helmet_slot: str
    body_armor_slot: str
    leg_armor_slot: str
    boots_slot: str
    ring1_slot: str
    ring2_slot: str
    amulet_slot: str
    artifact1_slot: str
    artifact2_slot: str
    artifact3_slot: str
    utility1_slot: str
    utility1_slot_quantity: int
    utility2_slot: str
    utility2_slot_quantity: int
    rune_slot: str
    bag_slot: str
    
    # Modifiers
    wisdom: int
    prospecting: int
    
    # Task information
    task: str
    task_type: str
    task_progress: int
    task_total: int
    
    # Inventory
    inventory_max_items: int
    inventory: List[InventoryItem]

    def get_skill_progress(self, skill: str) -> Tuple[int, float]:
        """
        Get level and progress percentage for a given skill.
        
        Args:
            skill (str): The skill name (e.g., 'mining', 'fishing').
        
        Returns:
            tuple: A tuple containing the level (int) and progress (float) in percentage.
        """
        level = getattr(self, f"{skill}_level")
        xp = getattr(self, f"{skill}_xp")
        max_xp = getattr(self, f"{skill}_max_xp")
        progress = (xp / max_xp) * 100 if max_xp > 0 else 0
        return level, progress

    def get_equipment_slots(self) -> Dict[str, str]:
        """
        Get all equipped items in each slot as a dictionary.
        
        Returns:
            dict: A dictionary mapping each slot name to the equipped item.
        """
        return {
            "weapon": self.weapon_slot,
            "shield": self.shield_slot,
            "helmet": self.helmet_slot,
            "body": self.body_armor_slot,
            "legs": self.leg_armor_slot,
            "boots": self.boots_slot,
            "ring1": self.ring1_slot,
            "ring2": self.ring2_slot,
            "amulet": self.amulet_slot,
            "artifact1": self.artifact1_slot,
            "artifact2": self.artifact2_slot,
            "artifact3": self.artifact3_slot,
            "utility1": self.utility1_slot,
            "utility2": self.utility2_slot
        }

    def get_inventory_space(self) -> int:
        """
        Calculate remaining inventory space.
        
        Returns:
            int: Number of available inventory slots.
        """
        items = 0
        for item in self.inventory:
            items += item.quantity
        return self.inventory_max_items - items

    def has_item(self, item_code: str) -> Tuple[bool, int]:
        """
        Check if the player has a specific item and its quantity.
        
        Args:
            item_code (str): The code of the item to check.
        
        Returns:
            tuple: A tuple with a boolean indicating presence and the quantity.
        """
        for item in self.inventory:
            if item.code == item_code:
                return True, item.quantity
        return False, 0

    def get_task_progress_percentage(self) -> float:
        """
        Get the current task progress as a percentage.
        
        Returns:
            float: The task completion percentage.
        """
        return (self.task_progress / self.task_total) * 100 if self.task_total > 0 else 0
    
    def __repr__(self) -> str:
        """String representation of player's core stats and skills."""
        ret = \
        f"""{self.name}
  Combat Level {self.level} ({self.xp}/{self.max_xp} XP)
  Mining Level {self.mining_level} ({self.mining_xp}/{self.mining_max_xp} XP)
  Woodcutting Level {self.woodcutting_level} ({self.woodcutting_xp}/{self.woodcutting_max_xp} XP)
  Fishing Level {self.fishing_level} ({self.fishing_xp}/{self.fishing_max_xp} XP)
  Weaponcrafting Level {self.weaponcrafting_level} ({self.weaponcrafting_xp}/{self.weaponcrafting_max_xp} XP)
  Gearcrafting Level {self.gearcrafting_level} ({self.gearcrafting_xp}/{self.gearcrafting_max_xp} XP)
  Jewelrycrafting Level {self.jewelrycrafting_level} ({self.jewelrycrafting_xp}/{self.jewelrycrafting_max_xp} XP)
  Cooking Level {self.cooking_level} ({self.cooking_xp}/{self.cooking_max_xp} XP)
        """
        return ret
# --- End Dataclasses ---


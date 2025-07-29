import requests
import logging
import time
from threading import Thread
from datetime import timedelta, datetime
from typing import List, Dict, Optional

from .game_data_classes import PlayerData, ContentMaps, InventoryItem, Position
from .exceptions import APIException
from .helpers import CooldownManager, with_cooldown
from .subclasses import (
    Account, Character, Actions, Maps, Items, 
    Monsters, Resources, Tasks, Rewards, Achievements, Events, GE, Leaderboard, Accounts
)
from .log import logger
from .database import cache_db, cache_db_cursor
from .config import config


# --- Globals ---
_task_loops = []

# --- Wrapper ---
class ArtifactsAPI:
    """Main API wrapper class with improved initialization and error handling."""
    
    def __init__(self, api_key: str, character_name: str):
        self.logger = logging.LoggerAdapter(logger, {"char": character_name})
        self.logger.debug(f"Initializing wrapper for {character_name}")

        self.token: str = api_key
        self.base_url: str = config.api_base_url
        self.headers: Dict[str, str] = {
            "content-type": "application/json",
            "Accept": "application/json",
            "Authorization": f'Bearer {self.token}'
        }
        
        # Initialize managers
        self._cooldown_manager = CooldownManager()
        self._cooldown_manager.logger = self.logger
        
        self.character_name = character_name
        self.char: Optional[PlayerData] = None
        self._initialize_character(character_name)
        self.account = Account(self)
        self.character = Character(self)
        self.actions = Actions(self)
        self.maps = Maps(self)
        self.items = Items(self)
        self.monsters = Monsters(self)
        self.resources = Resources(self)
        self.events = Events(self)
        self.ge = GE(self)
        self.tasks = Tasks(self)
        self.task_rewards = Rewards(self)
        self.achievements = Achievements(self)
        self.leaderboard = Leaderboard(self)
        self.accounts = Accounts(self)
        #self.content_maps = ContentMaps(self)

    def _initialize_character(self, character_name: str) -> None:
        """Separate character initialization for better error handling."""
        try:
            self.char = self.get_character(character_name=character_name)
        except Exception as e:
            self.logger.error(f"Failed to initialize character: {e}")
            raise
            
    @with_cooldown
    def _make_request(self, method: str, endpoint: str, json: Optional[dict] = None, 
                    source: Optional[str] = None, retries: int = 3, 
                    include_headers: bool = False) -> dict:
        """Enhanced request handling with better error management."""
        try:
            url = f"{self.base_url}/{endpoint.strip('/')}"
            
            if source != "get_character":
                self.logger.debug(f"API request: {url} - JSON: {json}")

            response = requests.request(
                method, 
                url, 
                headers=self.headers, 
                json=json, 
                timeout=10
            )

            if response.status_code != 200:
                self._handle_error_response(response, endpoint, json, source)

            if source != "get_character":
                self.get_character()
            
            return {
                "json": response.json(),
                "headers": dict(response.headers)
            } if include_headers else response.json()

        except requests.Timeout:
            self.logger.error("Request timed out")
            if retries > 0:
                return self._make_request(method, endpoint, json, source, retries - 1, include_headers)
            raise
        except Exception as e:
            if "Character already at destination" not in str(e) and retries > 0:
                return self._make_request(method, endpoint, json, source, retries - 1, include_headers)
            raise

    def _handle_error_response(self, response: requests.Response, endpoint: str, 
                             json: Optional[dict], source: Optional[str]) -> None:
        """Separate error handling logic for cleaner code."""
        error_data = response.json().get('error', {})
        message = f"Error {response.status_code}: {error_data.get('message', '')}"
        message += f"\nEndpoint: {endpoint}"
        if json:
            message += f"\nBody: {json}"
        if source:
            message += f"\nSource: {source}"
        
        self._raise(response.status_code, message)

    def _get_version(self):
        version = self._make_request(endpoint="", method="GET").get("data").get("version")
        return version
    
    def _cache(self, force=False):
        cache_db_cursor.execute("SELECT v FROM cache_table WHERE k = 'Cache Expiration'")
        cache_expiration = cache_db_cursor.fetchone() or None
        now = datetime.now()
            
        if cache_expiration is None or datetime.strptime(cache_expiration[0], '%Y-%m-%d %H:%M:%S.%f') < now or force:
            cache_db_cursor.execute(
                "INSERT or REPLACE INTO cache_table (k, v) VALUES (?, ?)", 
                ("Cache Expiration", datetime.now() + timedelta(days=2))
            )
            cache_db.commit()
            print("Recaching...")
            self.maps._cache_maps(force=force)
            self.items._cache_items(force=force)
            self.monsters._cache_monsters(force=force)
            self.resources._cache_resources(force=force)
            self.tasks._cache_tasks()
            self.task_rewards._cache_rewards(force=force)
            self.achievements._cache_achievements(force=force)
            #self.content_maps._cache_content_maps(force=force)

    def _raise(self, code: int, m: str) -> None:
        """
        Raises an API exception based on the response code and error message.

        Args:
            code (int): HTTP status code.
            m (str): Error message.

        Raises:
            Exception: Corresponding exception based on the code provided.
        """
        match code:
            case 404:
                raise APIException.NotFound(m)
            case 478:
                raise APIException.InsufficientQuantity(m)
            case 486:
                raise APIException.ActionAlreadyInProgress(m)
            case 493:
                raise APIException.TooLowLevel(m)
            case 496:
                raise APIException.TooLowLevel(m)
            case 497:
                raise APIException.InventoryFull(m)
            case 498:
                raise APIException.CharacterNotFound(m)
            case 499:
                raise APIException.CharacterInCooldown(m)
            case 497:
                raise APIException.GETooMany(m)
            case 480:
                raise APIException.GENoStock(m)
            case 482:
                raise APIException.GENoItem(m)
            case 483:
                raise APIException.TransactionInProgress(m)
            case 486:
                raise APIException.InsufficientGold(m)
            case 461:
                raise APIException.TransactionInProgress(m)
            case 462:
                raise APIException.BankFull(m)
            case 489:
                raise APIException.TaskMasterAlreadyHasTask(m)
            case 487:
                raise APIException.TaskMasterNoTask(m)
            case 488:
                raise APIException.TaskMasterTaskNotComplete(m)
            case 474:
                raise APIException.TaskMasterTaskMissing(m)
            case 475:
                raise APIException.TaskMasterTaskAlreadyCompleted(m)
            case 473:
                raise APIException.RecyclingItemNotRecyclable(m)
            case 484:
                raise APIException.EquipmentTooMany(m)
            case 485:
                raise APIException.EquipmentAlreadyEquipped(m)
            case 491:
                raise APIException.EquipmentSlot(m)
            case 490:
                logger.warning(m, src=self.char.name)
            case 452:
                raise APIException.TokenMissingorEmpty(m)
            case _:
                raise Exception(m)


    # --- Helper Functions ---
    def get_character(self, data: Optional[dict] = None, character_name: Optional[str] = None) -> PlayerData:
        """
        Retrieve or update the character's data and initialize the character attribute.

        Args:
            data (Optional[dict]): Pre-loaded character data; if None, data will be fetched.
            character_name (Optional[str]): Name of the character; only used if data is None.

        Returns:
            PlayerData: The PlayerData object with the character's information.
        """
        if data is None:
            if character_name:
                endpoint = f"characters/{character_name}"
            else:
                endpoint = f"characters/{self.char.name}"
            data = self._make_request("GET", endpoint, source="get_character").get('data')

        inventory_data = data.get("inventory", [])
        player_inventory: List[InventoryItem] = [
            InventoryItem(slot=item["slot"], code=item["code"], quantity=item["quantity"]) 
            for item in inventory_data if item["code"]
        ]

        self.char = PlayerData(
            name=data["name"],
            account=data["account"],
            skin=data["skin"],
            level=data["level"],
            xp=data["xp"],
            max_xp=data["max_xp"],
            gold=data["gold"],
            speed=data["speed"],
            mining_level=data["mining_level"],
            mining_xp=data["mining_xp"],
            mining_max_xp=data["mining_max_xp"],
            woodcutting_level=data["woodcutting_level"],
            woodcutting_xp=data["woodcutting_xp"],
            woodcutting_max_xp=data["woodcutting_max_xp"],
            fishing_level=data["fishing_level"],
            fishing_xp=data["fishing_xp"],
            fishing_max_xp=data["fishing_max_xp"],
            weaponcrafting_level=data["weaponcrafting_level"],
            weaponcrafting_xp=data["weaponcrafting_xp"],
            weaponcrafting_max_xp=data["weaponcrafting_max_xp"],
            gearcrafting_level=data["gearcrafting_level"],
            gearcrafting_xp=data["gearcrafting_xp"],
            gearcrafting_max_xp=data["gearcrafting_max_xp"],
            jewelrycrafting_level=data["jewelrycrafting_level"],
            jewelrycrafting_xp=data["jewelrycrafting_xp"],
            jewelrycrafting_max_xp=data["jewelrycrafting_max_xp"],
            cooking_level=data["cooking_level"],
            cooking_xp=data["cooking_xp"],
            cooking_max_xp=data["cooking_max_xp"],
            alchemy_level=data["alchemy_level"],
            alchemy_xp=data["alchemy_xp"],
            alchemy_max_xp=data["alchemy_max_xp"],
            hp=data["hp"],
            max_hp=data["max_hp"],
            haste=data["haste"],
            critical_strike=data["critical_strike"],
            attack_fire=data["attack_fire"],
            attack_earth=data["attack_earth"],
            attack_water=data["attack_water"],
            attack_air=data["attack_air"],
            dmg_fire=data["dmg_fire"],
            dmg_earth=data["dmg_earth"],
            dmg_water=data["dmg_water"],
            dmg_air=data["dmg_air"],
            res_fire=data["res_fire"],
            res_earth=data["res_earth"],
            res_water=data["res_water"],
            res_air=data["res_air"],
            pos=Position(data["x"], data["y"]),
            cooldown=data["cooldown"],
            cooldown_expiration=data["cooldown_expiration"],
            weapon_slot=data["weapon_slot"],
            shield_slot=data["shield_slot"],
            helmet_slot=data["helmet_slot"],
            body_armor_slot=data["body_armor_slot"],
            leg_armor_slot=data["leg_armor_slot"],
            boots_slot=data["boots_slot"],
            ring1_slot=data["ring1_slot"],
            ring2_slot=data["ring2_slot"],
            amulet_slot=data["amulet_slot"],
            artifact1_slot=data["artifact1_slot"],
            artifact2_slot=data["artifact2_slot"],
            artifact3_slot=data["artifact3_slot"],
            utility1_slot=data["utility1_slot"],
            utility2_slot=data["utility2_slot"],
            utility1_slot_quantity=data["utility1_slot_quantity"],
            utility2_slot_quantity=data["utility2_slot_quantity"],
            task=data["task"],
            task_type=data["task_type"],
            task_progress=data["task_progress"],
            task_total=data["task_total"],
            inventory_max_items=data["inventory_max_items"],
            inventory=player_inventory,
            wisdom=data["wisdom"],
            prospecting=data["prospecting"],
            dmg=data["dmg"],
            rune_slot=data["rune_slot"],
            bag_slot=data["bag_slot"]
            
        )
        return self.char

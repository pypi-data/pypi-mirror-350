from .database import cache_db, cache_db_cursor
from .helpers import _re_cache
import math
import json
from typing import Optional, List, Dict, Any, Union
from .game_data_classes import Item, Drop, Reward, Resource, Map, Monster, Task, Achievement, Effect
from .log import logger
import sqlite3

class Account:
    
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        logger.debug("Initializing Account class", src="Root")
        self.api = api

    # --- Account Functions ---
    def get_bank_details(self) -> dict:
        """Retrieve the details of the player's bank account."""
        endpoint = "my/bank"
        return self.api._make_request("GET", endpoint, source="get_bank_details")

    def get_bank_items(self, item_code=None, page=1) -> dict:
        """Retrieve the list of items stored in the player's bank."""
        query = "size=100"
        query += f"&item_code={item_code}" if item_code else ""
        query += f"&page={page}"
        endpoint = f"my/bank/items?{query}"
        return self.api._make_request("GET", endpoint, source="get_bank_items")

    def get_ge_sell_orders(self, item_code=None, page=1) -> dict:
        """Retrieve the player's current sell orders on the Grand Exchange."""
        query = "size=100"
        query += f"&item_code={item_code}" if item_code else ""
        query += f"&page={page}"
        endpoint = f"my/grandexchange/orders?{query}"
        return self.api._make_request("GET", endpoint, source="get_ge_sell_orders")

    def get_ge_sell_history(self, item_code=None, item_id=None, page=1) -> dict:
        """Retrieve the player's Grand Exchange sell history."""
        query = "size=100"
        query += f"&item_code={item_code}" if item_code else ""
        query += f"&id={item_id}" if item_id else ""
        query += f"&page={page}"
        endpoint = f"my/grandexchange/history?{query}"
        return self.api._make_request("GET", endpoint, source="get_ge_sell_history")

    def get_account_details(self) -> dict:
        """Retrieve details of the player's account."""
        endpoint = "my/details"
        return self.api._make_request("GET", endpoint, source="get_account_details")

class Character:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        logger.debug("Initializing Character class", src="Root")
        self.api = api

    # --- Character Functions ---
    def create_character(self, name: str, skin: str = "men1") -> dict:
        """
        Create a new character with the given name and skin.

        Args:
            name (str): The name of the new character.
            skin (str): The skin choice for the character (default is "men1").

        Returns:
            dict: Response data with character creation details.
        """
        endpoint = "characters/create"
        json = {"name": name, "skin": skin}
        return self.api._make_request("POST", endpoint, json=json, source="create_character")

    def delete_character(self, name: str) -> dict:
        """
        Delete a character by name.

        Args:
            name (str): The name of the character to delete.

        Returns:
            dict: Response data confirming character deletion.
        """
        endpoint = "characters/delete"
        json = {"name": name}
        return self.api._make_request("POST", endpoint, json=json, source="delete_character")

    def get_logs(self, page: int = 1, name: str = None) -> dict:
        """_summary_

        Args:
            page (int): Page number for results. Defaults to 1.

        Returns:
            dict: Response data with character logs
        """
        query = f"?size=100&page={page}"
        if name:
            query = f"/{name}?size=100&page={page}"
        endpoint = f"my/logs{query}"
        self.api._make_request("GET", endpoint, source="get_logs")

class Actions:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        logger.debug("Initializing Actions class", src="Root")
        self.api = api

    # --- Character Actions ---
    def move(self, x: int, y: int) -> dict:
        """
        Move the character to a new position.

        Args:
            x (int): X-coordinate to move to.
            y (int): Y-coordinate to move to.

        Returns:
            dict: Response data with updated character position.
        """
        endpoint = f"my/{self.api.char.name}/action/move"
        json = {"x": x, "y": y}
        res = self.api._make_request("POST", endpoint, json=json, source="move")
        return res

    def rest(self) -> dict:
        """
        Perform a rest action to regain energy.

        Returns:
            dict: Response data confirming rest action.
        """
        endpoint = f"my/{self.api.char.name}/action/rest"
        res = self.api._make_request("POST", endpoint, source="rest")
        return res

    # --- Item Action Functions ---
    def equip_item(self, item_code: str, slot: str, quantity: int = 1) -> dict:
        """
        Equip an item to a specified slot.

        Args:
            item_code (str): The code of the item to equip.
            slot (str): The equipment slot.
            quantity (int): The number of items to equip (default is 1).

        Returns:
            dict: Response data with updated equipment.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/equip"
        json = {"code": item_code, "slot": slot, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="equip_item")
        return res

    def unequip_item(self, slot: str, quantity: int = 1) -> dict:
        """
        Unequip an item from a specified slot.

        Args:
            slot (str): The equipment slot.
            quantity (int): The number of items to unequip (default is 1).

        Returns:
            dict: Response data with updated equipment.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/unequip"
        json = {"slot": slot, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="unequip_item")
        return res

    def use_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Use an item from the player's inventory.

        Args:
            item_code (str): Code of the item to use.
            quantity (int): Quantity of the item to use (default is 1).

        Returns:
            dict: Response data confirming the item use.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/use"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="use_item")
        return res

    def delete_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Delete an item from the player's inventory.

        Args:
            item_code (str): Code of the item to delete.
            quantity (int): Quantity of the item to delete (default is 1).

        Returns:
            dict: Response data confirming the item deletion.
        """
        endpoint = f"my/{self.api.char.name}/action/delete-item"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="delete_item")
        return res

    # --- Resource Action Functions ---
    def fight(self) -> dict:
        """
        Initiate a fight with a monster.

        Returns:
            dict: Response data with fight details.
        """
        endpoint = f"my/{self.api.char.name}/action/fight"
        res = self.api._make_request("POST", endpoint, source="fight")
        return res

    def gather(self) -> dict:
        """
        Gather resources, such as mining, woodcutting, or fishing.

        Returns:
            dict: Response data with gathered resources.
        """
        endpoint = f"my/{self.api.char.name}/action/gathering"
        res = self.api._make_request("POST", endpoint, source="gather")
        return res

    def craft_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Craft an item.

        Args:
            item_code (str): Code of the item to craft.
            quantity (int): Quantity of the item to craft (default is 1).

        Returns:
            dict: Response data with crafted item details.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/crafting"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="craft_item")
        return res

    def recycle_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Recycle an item.

        Args:
            item_code (str): Code of the item to recycle.
            quantity (int): Quantity of the item to recycle (default is 1).

        Returns:
            dict: Response data confirming the recycling action.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/recycle"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="recycle_item")
        return res

    # --- Bank Action Functions ---
    def bank_deposit_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Deposit an item into the bank.

        Args:
            item_code (str): Code of the item to deposit.
            quantity (int): Quantity of the item to deposit (default is 1).

        Returns:
            dict: Response data confirming the deposit.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/bank/deposit"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="bank_deposit_item")
        return res

    def bank_deposit_gold(self, quantity: int) -> dict:
        """
        Deposit gold into the bank.

        Args:
            quantity (int): Amount of gold to deposit.

        Returns:
            dict: Response data confirming the deposit.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/bank/deposit/gold"
        json = {"quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="bank_deposit_gold")
        return res

    def bank_withdraw_item(self, item_code: str, quantity: int = 1) -> dict:
        """
        Withdraw an item from the bank.

        Args:
            item_code (str): Code of the item to withdraw.
            quantity (int): Quantity of the item to withdraw (default is 1).

        Returns:
            dict: Response data confirming the withdrawal.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/bank/withdraw"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="bank_withdraw_item")
        return res

    def bank_withdraw_gold(self, quantity: int) -> dict:
        """
        Withdraw gold from the bank.

        Args:
            quantity (int): Amount of gold to withdraw.

        Returns:
            dict: Response data confirming the withdrawal.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/bank/withdraw/gold"
        json = {"quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="bank_withdraw_gold")
        return res

    def bank_buy_expansion(self) -> dict:
        """
        Purchase an expansion for the bank.

        Returns:
            dict: Response data confirming the expansion purchase.
        """
        endpoint = f"my/{self.api.char.name}/action/bank/buy_expansion"
        res = self.api._make_request("POST", endpoint, source="bank_buy_expansion")
        return res


    # --- Taskmaster Action Functions ---
    def taskmaster_accept_task(self) -> dict:
        """
        Accept a new task from the taskmaster.

        Returns:
            dict: Response data confirming task acceptance.
        """
        endpoint = f"my/{self.api.char.name}/action/tasks/new"
        res = self.api._make_request("POST", endpoint, source="accept_task")
        return res

    def taskmaster_complete_task(self) -> dict:
        """
        Complete the current task with the taskmaster.

        Returns:
            dict: Response data confirming task completion.
        """
        endpoint = f"my/{self.api.char.name}/action/tasks/complete"
        res = self.api._make_request("POST", endpoint, source="complete_task")
        return res

    def taskmaster_exchange_task(self) -> dict:
        """
        Exchange the current task with the taskmaster.

        Returns:
            dict: Response data confirming task exchange.
        """
        endpoint = f"my/{self.api.char.name}/action/tasks/exchange"
        res = self.api._make_request("POST", endpoint, source="exchange_task")
        return res

    def taskmaster_trade_task(self, item_code: str, quantity: int = 1) -> dict:
        """
        Trade a task item with another character.

        Args:
            item_code (str): Code of the item to trade.
            quantity (int): Quantity of the item to trade (default is 1).

        Returns:
            dict: Response data confirming task trade.
        """
        quantity = quantity if quantity < 0 else 1
        endpoint = f"my/{self.api.char.name}/action/tasks/trade"
        json = {"code": item_code, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="trade_task")
        return res

    def taskmaster_cancel_task(self) -> dict:
        """
        Cancel the current task with the taskmaster.

        Returns:
            dict: Response data confirming task cancellation.
        """
        endpoint = f"my/{self.api.char.name}/action/tasks/cancel"
        res = self.api._make_request("POST", endpoint, source="cancel_task")
        return res
 
class BaseCache:
    """Base class for all cache-enabled classes."""
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert a database row to a dictionary."""
        return dict(row)

class Items(BaseCache):
    """Manages item-related operations and caching."""
    
    def __init__(self, api) -> None:
        """
        Initialize Items manager.
        
        Args:
            api: ArtifactsAPI instance for making requests
        """
        logger.debug("Initializing Items class", src="Root")
        self.api = api
        self.cache = {}
        self.all_items = []
        self._cache_items()
    
    def _cache_items(self, force=False):
        if _re_cache(self.api, "item_cache") or force:
            # Create table
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_cache (
            name TEXT PRIMARY KEY,
            code TEXT,
            type TEXT,
            subtype TEXT,
            description TEXT,
            effects TEXT,
            craft TEXT,
            tradeable BOOL
            )
            """)
            cache_db.commit()
                
            endpoint = "items?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_items")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of items", src=self.api.char.name)

            for i in range(pages):
                endpoint = f"items?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_items", include_headers=True)
                item_list = res["json"]["data"]

                for item in item_list:
                    name = item["name"]
                    code = item["code"]
                    type_ = item["type"]
                    subtype = item.get("subtype", "")
                    description = item.get("description", "")
                    effects = json.dumps(item.get("effects", []))
                    craft = json.dumps(item["craft"]) if item.get("craft") else None
                    tradeable = item.get("tradeable", False)

                    # Insert the item into the database
                    cache_db_cursor.execute("""
                        INSERT OR REPLACE INTO item_cache (
                            name, code, type, subtype, description, effects, craft, tradeable
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (name, code, type_, subtype, description, effects, craft, tradeable))
                    
                    self.all_items.append(item)

            cache_db.commit()
            self.cache = {item["code"]: item for item in self.all_items}

            logger.debug(f"Finished caching {len(self.all_items)} items", src=self.api.char.name)

    def _filter_items(self, craft_material=None, craft_skill=None, max_level=None, min_level=None, 
                      name=None, item_type=None):
        query = "SELECT * FROM item_cache WHERE 1=1"
        params = []

        if craft_material:
            query += " AND EXISTS (SELECT 1 FROM json_each(json_extract(item_cache.craft, '$.items')) WHERE json_each.value LIKE ?)"
            params.append(f"%{craft_material}%")
        
        if craft_skill:
            query += " AND json_extract(item_cache.craft, '$.skill') = ?"
            params.append(craft_skill)

        if max_level is not None:
            query += " AND item_cache.level <= ?"
            params.append(max_level)

        if min_level is not None:
            query += " AND item_cache.level >= ?"
            params.append(min_level)

        if name:
            query += " AND item_cache.name LIKE ?"
            params.append(f"%{name}%")

        if item_type:
            query += " AND item_cache.type = ?"
            params.append(item_type)

        cache_db_cursor.execute(query, params)
        return cache_db_cursor.fetchall()

    def get(self, 
            code: Optional[str] = None,
            **filters: Any) -> Union[Item, List[Item]]:
        """
        Get items based on code or filters.

        Args:
            code: Specific item code to retrieve
            **filters: Additional filters to apply

        Returns:
            Single Item if code is provided, otherwise list of Items
        """
        if not self.all_items:
            self._cache_items()
        
        if code:
            query = "SELECT * FROM item_cache WHERE code = ?"
            cache_db_cursor.execute(query, (code,))
            row = cache_db_cursor.fetchone()
            if row is None:
                return None
            
            row_dict = dict(row)
            # Convert JSON strings
            if row_dict['effects']:
                effects_data = json.loads(row_dict['effects'])
                row_dict['effects'] = []
                for effect in effects_data:
                    # Each effect is a dict with 'code' and 'value'
                    row_dict['effects'].append(Effect(
                        code=effect['code'],
                        name=effect['code'],  # Use code as name since that's what we have
                        description=effect['code'],  # Use code as description since that's what we have
                        attributes={'value': effect['value']} if 'value' in effect else {}
                    ))
            if row_dict['craft']:
                row_dict['craft'] = json.loads(row_dict['craft'])
            
            return Item(**row_dict)
        
        return [Item(**dict(row)) for row in self._filter_items(**filters)]
    
class Maps(BaseCache):
    def __init__(self, api):
        logger.debug("Initializing Maps class", src="Root")
        self.api = api
        self.cache = {}
        self.all_maps = []

    def _cache_maps(self, force=False):
        if _re_cache(self.api, "map_cache") or force:
            # Create table
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS map_cache (
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                content_code TEXT,
                content_type TEXT,
                PRIMARY KEY (x, y)
            )
            """)
            cache_db.commit()

            endpoint = "maps?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_maps")
            pages = math.ceil(int(res["pages"]) / 100)
            
            logger.debug(f"Caching {pages} pages of maps", src=self.api.char.name)
            
            all_maps = []
            for i in range(pages):
                endpoint = f"maps?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_maps")
                map_list = res["data"]
                
                for map_item in map_list:
                    x = map_item['x']
                    y = map_item['y']
                    content_code = map_item["content"]["code"] if map_item["content"] else ''
                    content_type = map_item["content"]["type"] if map_item["content"] else ''
                    
                    # Insert or replace the map into the database
                    cache_db_cursor.execute("""
                    INSERT OR REPLACE INTO map_cache (x, y, content_code, content_type)
                    VALUES (?, ?, ?, ?)
                    """, (x, y, content_code, content_type))
                    
                    all_maps.append(map_item)

            cache_db.commit()
            self.cache = {f"{item['x']}/{item['y']}": item for item in all_maps}
            self.all_maps = all_maps

            logger.debug(f"Finished caching {len(all_maps)} maps", src=self.api.char.name)

    def _filter_maps(self, content_code=None, content_type=None):
        query = "SELECT * FROM map_cache WHERE 1=1"
        params = []

        if content_code:
            query += " AND content_code LIKE ?"
            params.append(f"%{content_code}%")

        if content_type:
            query += " AND content_type = ?"
            params.append(content_type)

        cache_db_cursor.execute(query, params)
        return cache_db_cursor.fetchall()

    def get(self, x=None, y=None, **filters):
        """
        Retrieves maps based on coordinates or filters.
        
        Args:
            x (int, optional): X coordinate
            y (int, optional): Y coordinate
            **filters: Optional filter parameters

        Returns:
            Map or list[Map]: Single map if coordinates provided, else list of filtered maps
        """
        if not self.all_maps:
            self._cache_maps()
        
        if x is not None and y is not None:
            query = "SELECT * FROM map_cache WHERE x = ? AND y = ?"
            cache_db_cursor.execute(query, (x, y))
            row = cache_db_cursor.fetchone()
            if row is None:
                return None
            return self._row_to_map(row)
        
        return [self._row_to_map(row) for row in self._filter_maps(**filters)]

    def _row_to_map(self, row):
        return Map(
            x=row['x'],
            y=row['y'],
            content_code=row['content_code'],
            content_type=row['content_type']
        )

class Monsters(BaseCache):
    def __init__(self, api):
        logger.debug("Initializing Monsters class", src="Root")
        self.api = api
        self.cache = {}
        self.all_monsters = []

    def _cache_monsters(self, force=False):
        if _re_cache(self.api, "monster_cache") or force:
            # Create table
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS monster_cache (
                code TEXT PRIMARY KEY,
                name TEXT,
                level INTEGER,
                hp INTEGER,
                attack_fire INTEGER,
                attack_earth INTEGER,
                attack_water INTEGER,
                attack_air INTEGER,
                res_fire INTEGER,
                res_earth INTEGER,
                res_water INTEGER,
                res_air INTEGER,
                min_gold INTEGER,
                max_gold INTEGER,
                drops TEXT
            )
            """)
            cache_db.commit()

            endpoint = "monsters?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_monsters")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of monsters", src=self.api.char.name)

            all_monsters = []
            for i in range(pages):
                endpoint = f"monsters?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_monsters")
                monster_list = res["data"]

                for monster in monster_list:
                    code = monster["code"]
                    name = monster["name"]
                    level = monster["level"]
                    hp = monster["hp"]
                    attack_fire = monster["attack_fire"]
                    attack_earth = monster["attack_earth"]
                    attack_water = monster["attack_water"]
                    attack_air = monster["attack_air"]
                    res_fire = monster["res_fire"]
                    res_earth = monster["res_earth"]
                    res_water = monster["res_water"]
                    res_air = monster["res_air"]
                    min_gold = monster["min_gold"]
                    max_gold = monster["max_gold"]
                    drops = json.dumps([Drop(**drop).__dict__ for drop in monster["drops"]])  # Serialize drops as JSON

                    # Insert or replace the monster into the database
                    cache_db_cursor.execute("""
                    INSERT OR REPLACE INTO monster_cache (
                        code, name, level, hp, attack_fire, attack_earth, attack_water, attack_air,
                        res_fire, res_earth, res_water, res_air, min_gold, max_gold, drops
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (code, name, level, hp, attack_fire, attack_earth, attack_water, attack_air,
                        res_fire, res_earth, res_water, res_air, min_gold, max_gold, drops))

                    all_monsters.append(monster)

            cache_db.commit()
            self.cache = {monster["code"]: monster for monster in all_monsters}
            self.all_monsters = all_monsters

            logger.debug(f"Finished caching {len(all_monsters)} monsters", src=self.api.char.name)

    def _filter_monsters(self, drop=None, max_level=None, min_level=None):
        query = "SELECT * FROM monster_cache WHERE 1=1"
        params = []

        if drop:
            query += " AND EXISTS (SELECT 1 FROM json_each(drops) WHERE json_each.value LIKE ?)"
            params.append(f"%{drop}%")

        if max_level is not None:
            query += " AND level <= ?"
            params.append(max_level)

        if min_level is not None:
            query += " AND level >= ?"
            params.append(min_level)

        cache_db_cursor.execute(query, params)
        return cache_db_cursor.fetchall()

    def _row_to_dict(self, row):
        """Convert a SQLite row tuple to a dictionary with proper field names."""
        # Since we're using sqlite3.Row as row_factory, we can directly convert to dict
        row_dict = dict(row)
        
        # Convert JSON strings back to Python objects
        if 'drops' in row_dict and row_dict['drops']:
            row_dict['drops'] = [Drop(**drop) for drop in json.loads(row_dict['drops'])]
        
        return row_dict

    def get(self, code=None, **filters):
        """
        Retrieves monsters based on code or filters.
        
        Args:
            code (str, optional): Monster code for direct lookup
            **filters: Optional filter parameters

        Returns:
            Monster or list[Monster]: Single monster if code provided, else list of filtered monsters
        """
        if not self.all_monsters:
            self._cache_monsters()
        
        if code:
            query = "SELECT * FROM monster_cache WHERE code = ?"
            cache_db_cursor.execute(query, (code,))
            row = cache_db_cursor.fetchone()
            if row is None:
                return None
            return Monster(**self._row_to_dict(row))
        
        return [Monster(**self._row_to_dict(row)) for row in self._filter_monsters(**filters)]

class Resources(BaseCache):
    def __init__(self, api):
        logger.debug("Initializing Resources class", src="Root")
        self.api = api
        self.cache = {}
        self.all_resources = []

    def _cache_resources(self, force=False):
        if _re_cache(self.api, "resource_cache") or force:
            # Create table
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS resource_cache (
                code TEXT PRIMARY KEY,
                name TEXT,
                skill TEXT,
                level INTEGER,
                drops TEXT
            )
            """)
            cache_db.commit()

            endpoint = "resources?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_resources")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of resources", src=self.api.char.name)

            all_resources = []
            for i in range(pages):
                endpoint = f"resources?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_resources")
                resource_list = res["data"]

                for resource in resource_list:
                    code = resource["code"]
                    name = resource["name"]
                    skill = resource.get("skill")
                    level = resource["level"]
                    drops = json.dumps([Drop(**drop).__dict__ for drop in resource.get("drops", [])])  # Serialize drops as JSON

                    # Insert or replace the resource into the database
                    cache_db_cursor.execute("""
                    INSERT OR REPLACE INTO resource_cache (
                        code, name, skill, level, drops
                    ) VALUES (?, ?, ?, ?, ?)
                    """, (code, name, skill, level, drops))

                    all_resources.append(resource)

            cache_db.commit()
            self.cache = {resource["code"]: resource for resource in all_resources}
            self.all_resources = all_resources

            logger.debug(f"Finished caching {len(all_resources)} resources", src=self.api.char.name)

    def _filter_resources(self, drop=None, max_level=None, min_level=None, skill=None):
        # Base SQL query to select all resources
        query = "SELECT * FROM resource_cache WHERE 1=1"
        params = []

        # Apply filters to the query
        if drop:
            query += " AND EXISTS (SELECT 1 FROM json_each(json_extract(resource_cache.drops, '$')) WHERE json_each.value LIKE ?)"
            params.append(f"%{drop}%")

        if max_level is not None:
            query += " AND resource_cache.level <= ?"
            params.append(max_level)

        if min_level is not None:
            query += " AND resource_cache.level >= ?"
            params.append(min_level)

        if skill:
            query += " AND resource_cache.skill = ?"
            params.append(skill)

        cache_db_cursor.execute(query, params)
        return cache_db_cursor.fetchall()

    def get(self, code=None, **filters):
        """
        Retrieves resources based on code or filters.
        
        Args:
            code (str, optional): Resource code for direct lookup
            **filters: Optional filter parameters

        Returns:
            Resource or list[Resource]: Single resource if code provided, else list of filtered resources
        """
        if not self.all_resources:
            self._cache_resources()
        
        if code:
            query = "SELECT * FROM resource_cache WHERE code = ?"
            cache_db_cursor.execute(query, (code,))
            row = cache_db_cursor.fetchone()
            if row is None:
                return None
            return Resource(**self._row_to_dict(row))
        
        return [Resource(**self._row_to_dict(row)) for row in self._filter_resources(**filters)]

class Tasks(BaseCache):
    def __init__(self, api):
        logger.debug("Initializing Tasks class", src="Root")
        self.api = api
        self.cache = {}
        self.all_tasks = []

    def _cache_tasks(self, force=False):
        if _re_cache(self.api, "task_cache") or force:
            # Create table
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_cache (
                code TEXT PRIMARY KEY,
                level INTEGER,
                type TEXT,
                min_quantity INTEGER,
                max_quantity INTEGER,
                skill TEXT,
                rewards TEXT
            )
            """)
            cache_db.commit()

            endpoint = "tasks/list?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_tasks")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of tasks", src=self.api.char.name)

            all_tasks = []
            for i in range(pages):
                endpoint = f"tasks/list?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_tasks")
                task_list = res["data"]

                for task in task_list:
                    code = task["code"]
                    level = task["level"]
                    task_type = task.get("type")
                    min_quantity = task["min_quantity"]
                    max_quantity = task["max_quantity"]
                    skill = task.get("skill")
                    rewards = json.dumps({
                        "items": [{"code": item["code"], "quantity": item["quantity"]} for item in task["rewards"].get("items", [])],
                        "gold": task["rewards"].get("gold", 0)
                    }) if task.get("rewards") else None

                    # Insert or replace the task into the database
                    cache_db_cursor.execute("""
                    INSERT OR REPLACE INTO task_cache (
                        code, level, type, min_quantity, max_quantity, skill, rewards
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (code, level, task_type, min_quantity, max_quantity, skill, rewards))

                    all_tasks.append(task)

            cache_db.commit()
            self.cache = {task["code"]: task for task in all_tasks}
            self.all_tasks = all_tasks

            logger.debug(f"Finished caching {len(all_tasks)} tasks", src=self.api.char.name)

    def _filter_tasks(self, skill=None, task_type=None, max_level=None, min_level=None, name=None):
        # Base SQL query to select all tasks
        query = "SELECT * FROM task_cache WHERE 1=1"
        params = []

        # Apply filters to the query
        if skill:
            query += " AND task_cache.skill = ?"
            params.append(skill)

        if task_type:
            query += " AND task_cache.type = ?"
            params.append(task_type)

        if max_level is not None:
            query += " AND task_cache.level <= ?"
            params.append(max_level)

        if min_level is not None:
            query += " AND task_cache.level >= ?"
            params.append(min_level)

        if name:
            query += " AND task_cache.code LIKE ?"
            params.append(f"%{name}%")

        cache_db_cursor.execute(query, params)
        return cache_db_cursor.fetchall()

    def get(self, code=None, **filters):
        """
        Retrieves tasks based on code or filters.
        
        Args:
            code (str, optional): Task code for direct lookup
            **filters: Optional filter parameters

        Returns:
            Task or list[Task]: Single task if code provided, else list of filtered tasks
        """
        if not self.all_tasks:
            self._cache_tasks()
        
        if code:
            query = "SELECT * FROM task_cache WHERE code = ?"
            cache_db_cursor.execute(query, (code,))
            row = cache_db_cursor.fetchone()
            if row is None:
                return None
            return Task(**self._row_to_dict(row))
        
        return [Task(**self._row_to_dict(row)) for row in self._filter_tasks(**filters)]

class Rewards(BaseCache):
    def __init__(self, api):
        logger.debug("Initializing Rewards class", src="Root")
        self.api = api
        self.cache = {}
        self.all_rewards = []

    def _cache_rewards(self, force=False):
        if _re_cache(self.api, "reward_cache") or force:
            # Create table
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS reward_cache (
                code TEXT PRIMARY KEY,
                rate INTEGER,
                min_quantity INTEGER,
                max_quantity INTEGER
            )
            """)
            cache_db.commit()

            endpoint = "tasks/rewards?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_task_rewards")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of task rewards", src=self.api.char.name)

            all_rewards = []
            for i in range(pages):
                endpoint = f"tasks/rewards?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_task_rewards")
                reward_list = res["data"]

                for reward in reward_list:
                    code = reward["code"]
                    rate = reward["rate"]
                    min_quantity = reward["min_quantity"]
                    max_quantity = reward["max_quantity"]

                    # Insert or replace the reward into the database
                    cache_db_cursor.execute("""
                    INSERT OR REPLACE INTO reward_cache (
                        code, rate, min_quantity, max_quantity
                    ) VALUES (?, ?, ?, ?)
                    """, (code, rate, min_quantity, max_quantity))

                    all_rewards.append(reward)

            cache_db.commit()
            self.rewards_cache = {reward["code"]: reward for reward in all_rewards}
            self.all_rewards = all_rewards

            logger.debug(f"Finished caching {len(all_rewards)} task rewards", src=self.api.char.name)

    def _filter_rewards(self, name=None):
        # Base SQL query to select all rewards
        query = "SELECT * FROM reward_cache WHERE 1=1"
        params = []

        if name:
            query += " AND reward_cache.code LIKE ?"
            params.append(f"%{name}%")

        cache_db_cursor.execute(query, params)
        return cache_db_cursor.fetchall()

    def get(self, code=None, **filters):
        """
        Retrieves rewards based on code or filters.
        
        Args:
            code (str, optional): Reward code for direct lookup
            **filters: Optional filter parameters

        Returns:
            Reward or list[Reward]: Single reward if code provided, else list of filtered rewards
        """
        if not self.all_rewards:
            self._cache_rewards()

        if code:
            query = "SELECT * FROM reward_cache WHERE code = ?"
            cache_db_cursor.execute(query, (code,))
            row = cache_db_cursor.fetchone()
            if row is None:
                return None
            return Reward(**self._row_to_dict(row))
        
        return [Reward(**self._row_to_dict(row)) for row in self._filter_rewards(**filters)]

class Achievements(BaseCache):
    def __init__(self, api):
        logger.debug("Initializing Achievements class", src="Root")
        self.api = api
        self.cache = {}
        self.all_achievements = []

    def _cache_achievements(self, force=False):
        if _re_cache(self.api, "achievement_cache") or force:
            # Create table
            cache_db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievement_cache (
                code TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                points INTEGER,
                type TEXT,
                target INTEGER,
                total INTEGER,
                rewards_gold INTEGER
            )
            """)
            cache_db.commit()

            endpoint = "achievements?size=1"
            res = self.api._make_request("GET", endpoint, source="get_all_achievements")
            pages = math.ceil(int(res["pages"]) / 100)

            logger.debug(f"Caching {pages} pages of achievements", src=self.api.char.name)

            all_achievements = []
            for i in range(pages):
                endpoint = f"achievements?size=100&page={i+1}"
                res = self.api._make_request("GET", endpoint, source="get_all_achievements")
                achievement_list = res["data"]

                for achievement in achievement_list:
                    code = achievement["code"]
                    name = achievement["name"]
                    description = achievement["description"]
                    points = achievement["points"]
                    achievement_type = achievement["type"]
                    target = achievement["target"]
                    total = achievement["total"]
                    rewards_gold = achievement["rewards"].get("gold", 0)

                    # Insert or replace the achievement into the database
                    cache_db_cursor.execute("""
                    INSERT OR REPLACE INTO achievement_cache (
                        code, name, description, points, type, target, total, rewards_gold
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (code, name, description, points, achievement_type, target, total, rewards_gold))

                    all_achievements.append(achievement)

            cache_db.commit()
            self.cache = {achievement["code"]: achievement for achievement in all_achievements}
            self.all_achievements = all_achievements

            logger.debug(f"Finished caching {len(all_achievements)} achievements", src=self.api.char.name)

    def _filter_achievements(self, name=None, achievement_type=None, max_points=None, min_points=None):
        # Base SQL query to select all achievements
        query = "SELECT * FROM achievement_cache WHERE 1=1"
        params = []

        # Apply filters to the query
        if name:
            query += " AND achievement_cache.name LIKE ?"
            params.append(f"%{name}%")

        if achievement_type:
            query += " AND achievement_cache.type = ?"
            params.append(achievement_type)

        if max_points is not None:
            query += " AND achievement_cache.points <= ?"
            params.append(max_points)

        if min_points is not None:
            query += " AND achievement_cache.points >= ?"
            params.append(min_points)

        cache_db_cursor.execute(query, params)
        return cache_db_cursor.fetchall()

    def get(self, code=None, **filters):
        """
        Retrieves achievements based on code or filters.
        
        Args:
            code (str, optional): Achievement code for direct lookup
            **filters: Optional filter parameters

        Returns:
            Achievement or list[Achievement]: Single achievement if code provided, else list of filtered achievements
        """
        if not self.all_achievements:
            self._cache_achievements()
        
        if code:
            query = "SELECT * FROM achievement_cache WHERE code = ?"
            cache_db_cursor.execute(query, (code,))
            row = cache_db_cursor.fetchone()
            if row is None:
                return None
            return Achievement(**self._row_to_dict(row))
        
        return [Achievement(**self._row_to_dict(row)) for row in self._filter_achievements(**filters)]
    
class Events:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        logger.debug("Initializing Events class", src="Root")
        self.api = api
    # --- Event Functions ---
    def get_active(self, page: int = 1) -> dict:
        """
        Retrieve a list of active events.

        Args:
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with a list of active events.
        """
        query = f"size=100&page={page}"
        endpoint = f"events/active?{query}"
        return self.api._make_request("GET", endpoint, source="get_active_events").get("data")

    def get_all(self, page: int = 1) -> dict:
        """
        Retrieve a list of all events.

        Args:
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with a list of events.
        """
        query = f"size=100&page={page}"
        endpoint = f"events?{query}"
        return self.api._make_request("GET", endpoint, source="get_all_events").get("data")

class GE:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        logger.debug("Initializing GE class", src="Root")
        self.api = api
    # --- Grand Exchange Functions ---
    def get_history(self, item_code: str, buyer: Optional[str] = None, seller: Optional[str] = None, page: int = 1, size: int = 100) -> dict:
        """
        Retrieve the transaction history for a specific item on the Grand Exchange.

        Args:
            item_code (str): Code of the item.
            buyer (Optional[str]): Filter history by buyer name.
            seller (Optional[str]): Filter history by seller name.
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the item transaction history.
        """
        query = f"size={size}&page={page}"
        if buyer:
            query += f"&buyer={buyer}"
        if seller:
            query += f"&seller={seller}"
        endpoint = f"grandexchange/history/{item_code}?{query}"
        return self.api._make_request("GET", endpoint, source="get_ge_history").get("data")

    def get_sell_orders(self, item_code: Optional[str] = None, seller: Optional[str] = None, page: int = 1, size: int = 100) -> dict:
        """
        Retrieve a list of sell orders on the Grand Exchange with optional filters.

        Args:
            item_code (Optional[str]): Filter by item code.
            seller (Optional[str]): Filter by seller name.
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the list of sell orders.
        """
        query = f"size={size}&page={page}"
        if item_code:
            query += f"&item_code={item_code}"
        if seller:
            query += f"&seller={seller}"
        endpoint = f"grandexchange/orders?{query}"
        return self.api._make_request("GET", endpoint, source="get_ge_sell_orders").get("data")

    def get_sell_order(self, order_id: str) -> dict:
        """
        Retrieve details for a specific sell order on the Grand Exchange.

        Args:
            order_id (str): ID of the order.

        Returns:
            dict: Response data for the specified sell order.
        """
        endpoint = f"grandexchange/orders/{order_id}"
        return self.api._make_request("GET", endpoint, source="get_ge_sell_order").get("data")
    
    # --- Grand Exchange Actions Functions ---
    def buy(self, order_id: str, quantity: int = 1) -> dict:
        """
        Buy an item from the Grand Exchange.

        Args:
            order_id (str): ID of the order to buy from.
            quantity (int): Quantity of the item to buy (default is 1).

        Returns:
            dict: Response data with transaction details.
        """
        endpoint = f"my/{self.api.char.name}/action/grandexchange/buy"
        json = {"id": order_id, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="ge_buy")
        return res

    def sell(self, item_code: str, price: int, quantity: int = 1) -> dict:
        """
        Create a sell order on the Grand Exchange.

        Args:
            item_code (str): Code of the item to sell.
            price (int): Selling price per unit.
            quantity (int): Quantity of the item to sell (default is 1).

        Returns:
            dict: Response data confirming the sell order.
        """
        endpoint = f"my/{self.api.char.name}/action/grandexchange/sell"
        json = {"code": item_code, "item_code": price, "quantity": quantity}
        res = self.api._make_request("POST", endpoint, json=json, source="ge_sell")
        return res

    def cancel(self, order_id: str) -> dict:
        """
        Cancel an active sell order on the Grand Exchange.

        Args:
            order_id (str): ID of the order to cancel.

        Returns:
            dict: Response data confirming the order cancellation.
        """
        endpoint = f"my/{self.api.char.name}/action/grandexchange/cancel"
        json = {"id": order_id}
        res = self.api._make_request("POST", endpoint, json=json, source="ge_cancel_sell")
        return res
    
class Leaderboard:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        logger.debug("Initializing Leaderboard class", src="Root")
        self.api = api
    # --- Leaderboard Functions ---
    def get_characters_leaderboard(self, sort: Optional[str] = None, page: int = 1) -> dict:
        """
        Retrieve the characters leaderboard with optional sorting.

        Args:
            sort (Optional[str]): Sorting criteria (e.g., 'level', 'xp').
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the characters leaderboard.
        """
        query = "size=100"
        if sort:
            query += f"&sort={sort}"
        query += f"&page={page}"
        endpoint = f"leaderboard/characters?{query}"
        return self.api._make_request("GET", endpoint, source="get_characters_leaderboard")

    def get_accounts_leaderboard(self, sort: Optional[str] = None, page: int = 1) -> dict:
        """
        Retrieve the accounts leaderboard with optional sorting.

        Args:
            sort (Optional[str]): Sorting criteria (e.g., 'points').
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the accounts leaderboard.
        """
        query = "size=100"
        if sort:
            query += f"&sort={sort}"
        query += f"&page={page}"
        endpoint = f"leaderboard/accounts?{query}"
        return self.api._make_request("GET", endpoint, source="get_accounts_leaderboard")

class Accounts:
    def __init__(self, api):
        """
        Initialize with a reference to the main API to access shared methods.

        Args:
            api (ArtifactsAPI): Instance of the main API class.
        """
        logger.debug("Initializing Accounts class", src="Root")
        self.api = api
    # --- Accounts Functions ---
    def get_account_achievements(self, account: str, completed: Optional[bool] = None, achievement_type: Optional[str] = None, page: int = 1) -> dict:
        """
        Retrieve a list of achievements for a specific account with optional filters.

        Args:
            account (str): Account name.
            completed (Optional[bool]): Filter by completion status (True for completed, False for not).
            achievement_type (Optional[str]): Filter achievements by type.
            page (int): Pagination page number (default is 1).

        Returns:
            dict: Response data with the list of achievements for the account.
        """
        query = "size=100"
        if completed is not None:
            query += f"&completed={str(completed).lower()}"
        if achievement_type:
            query += f"&achievement_type={achievement_type}"
        query += f"&page={page}"
        endpoint = f"/accounts/{account}/achievements?{query}"
        return self.api._make_request("GET", endpoint, source="get_account_achievements") 


    def get_account(self, account: str):
        endpoint = f"/acounts/{account}"
        return self.api._make_request("GET", endpoint, source="get_account")

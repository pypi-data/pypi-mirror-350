# This example helps you level your mining, woodcutting, and player level, and it changes which resource is farmed depending on the player level
# This example relies on the package to be installed. Please install it using pip install --upgrade artifactsmmo-wrapper
TOKEN = "YOUR_TOKEN_HERE" # TODO: Make sure to paste your token here
doods = ["YOUR_CHARACTERS_HERE"] # TODO: Make sure to fill in your characters into this array. If you have 1, or if you have 5, make sure to put them here

import threading
import artifactsmmo_wrapper as wrapper
from itertools import cycle
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Define the logging format you want to apply
formatter = logging.Formatter(
    fmt="[%(levelname)s] %(asctime)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create a handler (e.g., StreamHandler for console output) and set its format
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

def deposit(api):
    # Deposit items and gold in the bank
    items = ""
    golds = 0
    api.actions.move(*api.content_maps.bank)
    for item in api.char.inventory:
        items += f"{item.quantity}x {item.code}, "
        api.actions.bank_deposit_item(item.code, item.quantity)
    
    if api.char.gold > 0:
        golds = api.char.gold
        api.actions.bank_deposit_gold(api.char.gold)
    
    items = items.strip().strip(",")
    d = "Deposited "
    if items:
        d += items
    
    if golds:
        d += f", {str(golds)} gold"
        
    if d == "Deposited ":
        d += "nothing"
    logger.info(d)

def mining(api, stop):
    # Mining routine based on character's level
    content_map = api.content_maps.copper_rocks
    if api.char.mining_level >= api.content_maps.mithril_rocks.level:
        content_map = api.content_maps.mithril_rocks
    elif api.char.mining_level >= api.content_maps.gold_rocks.level:
        content_map = api.content_maps.gold_rocks
    elif api.char.mining_level >= api.content_maps.coal_rocks.level:
        content_map = api.content_maps.coal_rocks
    elif api.char.mining_level >= api.content_maps.iron_rocks.level:
        content_map = api.content_maps.iron_rocks
    else:
        content_map = api.content_maps.copper_rocks

    logger.info(f"Mining {content_map.name}")
    api.actions.move(*content_map)
    while not stop.is_set():
        try:
            if api.char.get_inventory_space() < 5:
                return True
            api.actions.gather()
        except Exception as e:
            logger.error(f"Mining error: {e}")
            stop.set()
            return True
    return False

def woodcutting(api, stop):
    # Woodcutting routine based on character's level
    content_map = api.content_maps.ash_tree
    if api.char.woodcutting_level >= api.content_maps.maple_tree.level:
        content_map = api.content_maps.maple_tree
    elif api.char.woodcutting_level >= api.content_maps.birch_tree.level:
        content_map = api.content_maps.birch_tree
    elif api.char.woodcutting_level >= api.content_maps.spruce_tree.level:
        content_map = api.content_maps.spruce_tree
    else:
        content_map = api.content_maps.ash_tree

    logger.debug(f"Cutting {content_map.name}")
    api.actions.move(*content_map)
    while not stop.is_set():
        try:
            if api.char.get_inventory_space() < 5:
                return True
            api.actions.gather()
        except Exception as e:
            logger.error(f"Woodcutting error: {e}")
            stop.set()
            return True
    return False

def combat(api, stop):
    # Combat routine with a time limit
    end_time = time.time() + 5400
    if api.char.hp < api.char.max_hp:
        api.actions.rest()
    content_map = api.content_maps.chicken

    logger.info(f"Fighting {content_map.name}")
    api.actions.move(*content_map)
    while not stop.is_set() and time.time() < end_time:
        try:
            if api.char.get_inventory_space() < (api.char.inventory_max_items / 2):
                return True
            api.actions.fight()
            api.actions.rest()
        except Exception as e:
            logger.error(f"Combat error: {e}")
            stop.set()
            return False
    return False

def task_rotation(api, stop):
    # Rotate between tasks
    tasks = cycle([woodcutting, mining, combat])
    current_task = next(tasks)
    
    deposit(api)
    
    while not stop.is_set():
        needs_deposit = current_task(api, stop)
        if needs_deposit:
            deposit(api)
            current_task = next(tasks)

def run_tasks():
    chars = [wrapper.ArtifactsAPI(TOKEN, dood) for dood in doods]

    stop = threading.Event()
    threads = []

    # Start threads and listen for KeyboardInterrupt
    try:
        for api in chars:
            thread = threading.Thread(target=task_rotation, args=(api, stop))
            threads.append(thread)
            thread.start()
        
        # Wait for threads to finish
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Stopping threads...")
        stop.set()  # Signal all threads to stop

        for thread in threads:
            thread.join()  # Ensure all threads complete

        print("All threads stopped.")

if __name__ == "__main__":
    run_tasks()

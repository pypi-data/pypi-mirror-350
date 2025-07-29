# This example helps you level your mining, woodcutting, and player level, and it changes which resource is farmed depending on the player level
# This example relies on the package to be installed. Please install it using pip install --upgrade artifactsmmo-wrapper
TOKEN = "YOUR_TOKEN_HERE" # TODO: Make sure to paste your token here
CHARACTER_NAME = "YOUR_CHARACTER_NAME_HERE" # TODO: Make sure to paste your character's name here

from artifactsmmo_wrapper import ArtifactsAPI
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


api = ArtifactsAPI(TOKEN, CHARACTER_NAME)
previous_pos = api.char.pos
if api.char.pos != api.content_maps.ash_wood.pos:
    api.actions.move(*api.content_maps.ash_wood)

api.actions.gather()

api.actions.move(*api.content_maps.bank)
api.actions.bank_deposit_item("ash_wood", 1)
api.actions.move(*previous_pos)
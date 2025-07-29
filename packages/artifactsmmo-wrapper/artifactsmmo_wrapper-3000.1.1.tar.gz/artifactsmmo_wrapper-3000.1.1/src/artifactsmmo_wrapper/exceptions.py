from typing import Optional
from .log import logger
import traceback

# --- Exceptions ---
class APIException(Exception):
    """Enhanced base exception class for API errors with better tracking."""
    
    def __init__(self, message: str, char_name: Optional[str] = "ROOT"):
        super().__init__(message)
        self.char_name = char_name
        self.traceback = traceback.format_exc()
        self._log_error(message)
    
    def _log_error(self, message: str) -> None:
        """Log error with traceback information."""
        logger.error(
            f"{self.__class__.__name__}: {message}\nTraceback:\n{self.traceback}",
            extra={"char": self.char_name}
        )

    class CharacterInCooldown(Exception):
        def __init__(self, message="Character is in cooldown"):
            super().__init__(message)
            logger.warning(f"CharacterInCooldown: {message}", extra={"char": "ROOT"})

    class NotFound(Exception):
        def __init__(self, message="Resource not found"):
            super().__init__(message)
            logger.error(f"NotFound: {message}", extra={"char": "ROOT"})

    class ActionAlreadyInProgress(Exception):
        def __init__(self, message="Action is already in progress"):
            super().__init__(message)
            logger.warning(f"ActionAlreadyInProgress: {message}", extra={"char": "ROOT"})

    class CharacterNotFound(Exception):
        def __init__(self, message="Character not found"):
            super().__init__(message)
            logger.error(f"CharacterNotFound: {message}", extra={"char": "ROOT"})

    class TooLowLevel(Exception):
        def __init__(self, message="Level is too low"):
            super().__init__(message)
            logger.error(f"TooLowLevel: {message}", extra={"char": "ROOT"})

    class InventoryFull(Exception):
        def __init__(self, message="Inventory is full"):
            super().__init__(message)
            logger.warning(f"InventoryFull: {message}", extra={"char": "ROOT"})

    class MapItemNotFound(Exception):
        def __init__(self, message="Map item not found"):
            super().__init__(message)
            logger.error(f"MapItemNotFound: {message}", extra={"char": "ROOT"})

    class InsufficientQuantity(Exception):
        def __init__(self, message="Insufficient quantity"):
            super().__init__(message)
            logger.warning(f"InsufficientQuantity: {message}", extra={"char": "ROOT"})

    class GETooMany(Exception):
        def __init__(self, message="Too many GE items"):
            super().__init__(message)
            logger.error(f"GETooMany: {message}", extra={"char": "ROOT"})

    class GENoStock(Exception):
        def __init__(self, message="No stock available"):
            super().__init__(message)
            logger.error(f"GENoStock: {message}", extra={"char": "ROOT"})

    class GENoItem(Exception):
        def __init__(self, message="Item not found in GE"):
            super().__init__(message)
            logger.error(f"GENoItem: {message}", extra={"char": "ROOT"})

    class TransactionInProgress(Exception):
        def __init__(self, message="Transaction already in progress"):
            super().__init__(message)
            logger.warning(f"TransactionInProgress: {message}", extra={"char": "ROOT"})

    class InsufficientGold(Exception):
        def __init__(self, message="Not enough gold"):
            super().__init__(message)
            logger.warning(f"InsufficientGold: {message}", extra={"char": "ROOT"})

    class TaskMasterNoTask(Exception):
        def __init__(self, message="No task assigned to TaskMaster"):
            super().__init__(message)
            logger.error(f"TaskMasterNoTask: {message}", extra={"char": "ROOT"})

    class TaskMasterAlreadyHasTask(Exception):
        def __init__(self, message="TaskMaster already has a task"):
            super().__init__(message)
            logger.warning(f"TaskMasterAlreadyHasTask: {message}", extra={"char": "ROOT"})

    class TaskMasterTaskNotComplete(Exception):
        def __init__(self, message="TaskMaster task is not complete"):
            super().__init__(message)
            logger.error(f"TaskMasterTaskNotComplete: {message}", extra={"char": "ROOT"})

    class TaskMasterTaskMissing(Exception):
        def __init__(self, message="TaskMaster task is missing"):
            super().__init__(message)
            logger.error(f"TaskMasterTaskMissing: {message}", extra={"char": "ROOT"})

    class TaskMasterTaskAlreadyCompleted(Exception):
        def __init__(self, message="TaskMaster task already completed"):
            super().__init__(message)
            logger.warning(f"TaskMasterTaskAlreadyCompleted: {message}", extra={"char": "ROOT"})

    class RecyclingItemNotRecyclable(Exception):
        def __init__(self, message="Item is not recyclable"):
            super().__init__(message)
            logger.error(f"RecyclingItemNotRecyclable: {message}", extra={"char": "ROOT"})

    class EquipmentTooMany(Exception):
        def __init__(self, message="Too many equipment items"):
            super().__init__(message)
            logger.warning(f"EquipmentTooMany: {message}", extra={"char": "ROOT"})

    class EquipmentAlreadyEquipped(Exception):
        def __init__(self, message="Equipment already equipped"):
            super().__init__(message)
            logger.warning(f"EquipmentAlreadyEquipped: {message}", extra={"char": "ROOT"})

    class EquipmentSlot(Exception):
        def __init__(self, message="Invalid equipment slot"):
            super().__init__(message)
            logger.error(f"EquipmentSlot: {message}", extra={"char": "ROOT"})

    class AlreadyAtDestination(Exception):
        def __init__(self, message="Already at destination"):
            super().__init__(message)
            logger.info(f"AlreadyAtDestination: {message}", extra={"char": "ROOT"})

    class BankFull(Exception):
        def __init__(self, message="Bank is full"):
            super().__init__(message)
            logger.warning(f"BankFull: {message}", extra={"char": "ROOT"})

    class TokenMissingorEmpty(Exception):
        def __init__(self, message="Token is missing or empty"):
            super().__init__(message)
            logger.critical(f"TokenMissingorEmpty: {message}", extra={"char": "ROOT"})
            exit(1)
                
    class NameAlreadyUsed(Exception):
        def __init__(self, message="Name already used"):
            super().__init__(message)
            logger.error(f"NameAlreadyUsed: {message}", extra={"char": "ROOT"})
    
    class MaxCharactersReached(Exception):
        def __init__(self, message="Max characters reached"):
            super().__init__(message)
            logger.warning(f"MaxCharactersReached: {message}", extra={"char": "ROOT"})


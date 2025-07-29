from .database import cache_db, cache_db_cursor
import time
from datetime import timezone, datetime, timedelta
from threading import Lock
from functools import wraps
from typing import Optional, Any, Callable
import logging

# --- Helpers ---
def _re_cache(api: Any, table: str) -> bool:
    """Enhanced caching check with better error handling."""
    try:
        app_version = api._get_version()
        cache_manager = CacheManager()
        return cache_manager.needs_refresh(table, app_version)
    except Exception as e:
        logging.error(f"Cache refresh error for {table}: {e}")
        return False

class CacheManager:
    """Manages caching operations and version control."""
    
    def __init__(self):
        self._cache_lock = Lock()

    def needs_refresh(self, table: str, api_version: str) -> bool:
        """Check if a table needs to be refreshed based on version."""
        with self._cache_lock:
            cache_db_cursor.execute("SELECT v FROM cache_table WHERE k = ?", (table,))
            version = cache_db_cursor.fetchone()
            
            if not version or version[0] != api_version:
                cache_db_cursor.execute(
                    "INSERT OR REPLACE INTO cache_table (k, v) VALUES (?, ?)", 
                    (table, api_version)
                )
                cache_db.commit()
                return True
            return False

class CooldownManager:
    """Enhanced cooldown management with better type hints and error handling."""
    
    def __init__(self):
        self._lock = Lock()
        self._cooldown_expiration_time: Optional[datetime] = None
        self.logger: Optional[logging.Logger] = None

    def is_on_cooldown(self) -> bool:
        with self._lock:
            if not self._cooldown_expiration_time:
                return False
            return datetime.now(timezone.utc) < self._cooldown_expiration_time

    def set_cooldown_from_expiration(self, expiration_time_str: str) -> None:
        """Set cooldown from ISO 8601 timestamp."""
        try:
            with self._lock:
                self._cooldown_expiration_time = datetime.fromisoformat(
                    expiration_time_str.replace("Z", "+00:00")
                )
        except ValueError as e:
            if self.logger:
                self.logger.error(f"Invalid expiration time format: {e}")

    def wait_for_cooldown(self, logger: Optional[logging.Logger] = None, char: Optional[Any] = None) -> None:
        if not self.is_on_cooldown():
            return

        remaining = (self._cooldown_expiration_time - datetime.now(timezone.utc)).total_seconds()
        if logger:
            char_name = getattr(char, 'name', 'Unknown')
            logger.debug(f"Waiting for cooldown... ({remaining:.1f} seconds)", extra={"char": char_name})

        while self.is_on_cooldown():
            remaining = (self._cooldown_expiration_time - datetime.now(timezone.utc)).total_seconds()
            time.sleep(min(remaining, 0.1))

def with_cooldown(func: Callable) -> Callable:
    """Enhanced decorator with better type hints and error handling."""
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not hasattr(self, '_cooldown_manager'):
            self._cooldown_manager = CooldownManager()
        
        source = kwargs.get('source')
        method = kwargs.get('method')
        
        if source != "get_character":
            if hasattr(self, 'char') and hasattr(self.char, 'cooldown_expiration'):
                self._cooldown_manager.set_cooldown_from_expiration(self.char.cooldown_expiration)
            self._cooldown_manager.wait_for_cooldown(logger=getattr(self, 'logger', None), char=getattr(self, 'char', None))

        result = func(self, *args, **kwargs)

        if method not in ["GET", None, "None"] and hasattr(self, 'char') and hasattr(self.char, 'cooldown_expiration'):
                self._cooldown_manager.set_cooldown_from_expiration(self.char.cooldown_expiration)
        
        return result
    return wrapper


from .artifacts import ArtifactsAPI
from .config import config
from .log import logger
from typing import Optional

class ArtifactsWrapper:
    """Main wrapper class for easy token management."""
    
    def __init__(self):
        self._api: Optional[ArtifactsAPI] = None
    
    @property
    def token(self) -> Optional[str]:
        return config.token
    
    @token.setter
    def token(self, value: str) -> None:
        """Set the API token and initialize the API if needed."""
        config.token = value
        self._api = None  # Reset API instance
    
    def character(self, name: str) -> ArtifactsAPI:
        """Get an API instance for a specific character."""
        if not config.token:
            raise ValueError("Token not set. Please set token first: wrapper.token = 'YOUR_TOKEN'")
        
        if not self._api or self._api.character_name != name:
            self._api = ArtifactsAPI(config.token, name)
        return self._api
    
    

# Create global wrapper instance
wrapper = ArtifactsWrapper()

__all__ = ['wrapper', 'logger']
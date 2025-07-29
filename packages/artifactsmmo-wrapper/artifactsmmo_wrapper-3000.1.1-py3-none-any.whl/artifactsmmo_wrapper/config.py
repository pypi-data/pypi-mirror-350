from dataclasses import dataclass
from typing import Optional
import os
import json

@dataclass
class Config:
    """Configuration settings for the wrapper."""
    
    api_base_url: str = "https://api.artifactsmmo.com"
    cache_duration: int = 172800  # 2 days in seconds
    request_timeout: int = 10
    max_retries: int = 3
    debug_mode: bool = False
    _token: Optional[str] = None
    
    @property
    def token(self) -> Optional[str]:
        return self._token
    
    @token.setter
    def token(self, value: str) -> None:
        if not value:
            raise ValueError("Token cannot be empty")
        self._token = value
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> 'Config':
        """Load configuration from file."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                return cls(**config_data)
        return cls()

# Global config instance
config = Config.load() 
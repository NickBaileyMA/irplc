"""
Configuration management for iRacing OAuth Client
"""

import os
from typing import Optional, Literal
from dotenv import load_dotenv


class Config:
    """Configuration class that loads settings from environment variables."""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            env_file: Path to .env file (optional)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()  # Load from default .env file
    
    @property
    def client_id(self) -> str:
        """Get client ID from environment."""
        value = os.getenv('CLIENT_ID')
        if not value:
            raise ValueError("CLIENT_ID environment variable is required")
        return value
    
    @property
    def client_secret(self) -> str:
        """Get client secret from environment."""
        value = os.getenv('CLIENT_SECRET')
        if not value:
            raise ValueError("CLIENT_SECRET environment variable is required")
        return value
    
    @property
    def username(self) -> str:
        """Get username from environment."""
        value = os.getenv('USERNAME')
        if not value:
            raise ValueError("USERNAME environment variable is required")
        return value
    
    @property
    def password(self) -> str:
        """Get password from environment."""
        value = os.getenv('PASSWORD')
        if not value:
            raise ValueError("PASSWORD environment variable is required")
        return value
    
    @property
    def scope(self) -> str:
        """Get OAuth scope from environment."""
        return os.getenv('SCOPE', 'iracing.auth')
    
    @property
    def request_timeout(self) -> int:
        """Get request timeout from environment."""
        return int(os.getenv('REQUEST_TIMEOUT', '30'))
    
    @property
    def token_refresh_buffer_seconds(self) -> int:
        """Get token refresh buffer from environment."""
        return int(os.getenv('TOKEN_REFRESH_BUFFER_SECONDS', '60'))
    
    @property
    def log_level(self) -> str:
        """Get logging level from environment."""
        return os.getenv('LOG_LEVEL', 'INFO').upper()
    
    @property
    def log_format(self) -> Literal["human", "json"]:
        """Get logging format from environment."""
        format_value = os.getenv('LOG_FORMAT', 'human').lower()
        if format_value == 'json':
            return 'json'
        else:
            return 'human'

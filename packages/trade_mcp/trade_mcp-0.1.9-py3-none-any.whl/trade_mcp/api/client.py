from typing import Optional
from trade_mcp.api.http_utils import APIClient

class APIClientManager:
    _instance: Optional[APIClient] = None
    
    @classmethod
    def initialize(cls, axgrad_key: str, api_key: str, api_secret: str, venue: str) -> None:
        """Initialize the API client with credentials for any supported exchange.
        
        Args:
            axgrad_key: Axgrad API key
            api_key: Exchange API key
            api_secret: Exchange API secret
            venue: Venue string (e.g., 'test', 'live')
        """
        cls._instance = APIClient(
            axgrad_key=axgrad_key,
            api_key=api_key,
            api_secret=api_secret,
            venue=venue
        )
        
    @classmethod
    def get_client(cls) -> APIClient:
        """Get the initialized API client instance."""
        if cls._instance is None:
            raise RuntimeError("API client not initialized. Call initialize() first.")
        return cls._instance 
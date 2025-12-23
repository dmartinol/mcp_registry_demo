"""Utility functions for interacting with the MCP Registry API.

This module provides a client class and helper functions for querying
MCP registries and servers deployed in OpenShift/Kubernetes clusters.
"""

import requests
from typing import Optional, Dict, List


# Default configuration constants
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8888
REGISTRY_PATH = "registry"
EXTENSIONS_PATH = "extension"


class RegistryClient:
    """Client for interacting with MCP Registry API.
    
    This class provides methods to query MCP registries and servers
    through the registry API endpoint.
    
    Example:
        >>> client = RegistryClient(host="localhost", port=8888)
        >>> servers = client.get_mcp_servers("default")
        >>> registries = client.get_mcp_registries()
    """
    
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        registry_path: str = REGISTRY_PATH,
        extensions_path: str = EXTENSIONS_PATH
    ):
        """Initialize the registry client.
        
        Args:
            host: Registry API hostname (default: "localhost")
            port: Registry API port (default: 8888)
            registry_path: Path prefix for registry API (default: "registry")
            extensions_path: Path prefix for extensions API (default: "extension")
        """
        self.host = host
        self.port = port
        self.registry_path = registry_path
        self.extensions_path = extensions_path
    
    def _registry_api_url(self, registry: Optional[str], path: str) -> str:
        """Build registry API URL.
        
        Args:
            registry: Registry name (None or empty for aggregated registry)
            path: API path endpoint
            
        Returns:
            Complete URL for the registry API endpoint
        """
        if registry is None or registry == "":
            return f"http://{self.host}:{self.port}/{self.registry_path}/v0.1/{path}"
        return f"http://{self.host}:{self.port}/{self.registry_path}/{registry}/v0.1/{path}"
    
    def _extension_api_url(self, registry: Optional[str], path: str) -> str:
        """Build extension API URL.
        
        Args:
            registry: Registry name (None or empty for aggregated registry)
            path: API path endpoint
            
        Returns:
            Complete URL for the extension API endpoint
        """
        if registry is None or registry == "":
            return f"http://{self.host}:{self.port}/{self.extensions_path}/v0/{path}"
        return f"http://{self.host}:{self.port}/{self.extensions_path}/{registry}/v0/{path}"
    
    def get_mcp_servers(self, registry: Optional[str] = None) -> Dict:
        """Get the list of MCP servers from the registry API.
        
        Args:
            registry: Registry name to query (None for aggregated registry)
            
        Returns:
            Dictionary containing server list and metadata
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = self._registry_api_url(registry, "servers")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching servers: {e}")
            raise
    
    def get_mcp_registries(self) -> Dict:
        """Get the list of MCP registries from the extension API.
        
        Returns:
            Dictionary containing registry list and metadata
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = self._extension_api_url(None, "registries")
        print(url)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching registries: {e}")
            raise


def print_server_details(server_item: Dict) -> None:
    """Print detailed server information in a formatted way.
    
    Args:
        server_item: Dictionary containing server information from the API
    """
    server = server_item["server"]
    print(f"Name:       {server.get('name', 'N/A')}")
    print(f"Description: {server.get('description', 'N/A')}")
    print(f"Version:    {server.get('version', 'N/A')}")
    
    # Check for remotes
    remotes = server.get('remotes', [])
    if remotes:
        print(f"Remotes:    {len(remotes)} remote endpoint(s)")
        for remote in remotes:
            print(f"  - {remote.get('type', 'N/A')}: {remote.get('url', 'N/A')}")
    
    # Package info
    packages = server.get('packages', [])
    if packages:
        package = packages[0]
        print(f"Transport:  {package.get('transport', {}).get('type', 'N/A')}")
        print(f"Identifier: {package.get('identifier', 'N/A')}")
    print()


def print_server_cards(servers_list: List[Dict]) -> None:
    """Print servers in a card layout format.
    
    Args:
        servers_list: List of server dictionaries from the API
    """
    for idx, server_item in enumerate(servers_list, 1):
        server = server_item["server"]
        name = server.get("name", "N/A")
        
        # Extract package information (assuming first package)
        package = server.get("packages", [{}])[0] if server.get("packages") else {}
        registry_type = package.get("registryType", "N/A")
        identifier = package.get("identifier", "N/A")
        transport = package.get("transport", {}).get("type", "N/A")
        
        # Print card
        print(f"{'=' * 80}")
        print(f"Server #{idx}")
        print(f"{'-' * 80}")
        print(f"Name:       {name}")
        print(f"Transport:  {transport}")
        print(f"Registry:   {registry_type}")
        print(f"Identifier: {identifier}")


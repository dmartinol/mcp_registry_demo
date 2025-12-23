"""MCP Registry Demo utility library.

This package provides utilities for interacting with MCP registries
and servers in OpenShift/Kubernetes environments.
"""

from .registry_client import (
    RegistryClient,
    print_server_details,
    print_server_cards,
    DEFAULT_HOST,
    DEFAULT_PORT,
    REGISTRY_PATH,
    EXTENSIONS_PATH,
)

__all__ = [
    "RegistryClient",
    "print_server_details",
    "print_server_cards",
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    "REGISTRY_PATH",
    "EXTENSIONS_PATH",
]


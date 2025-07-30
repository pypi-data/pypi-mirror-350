"""
APIWeaver - Convert any web API into an MCP server.

This package provides a framework for dynamically creating MCP (Model Context Protocol)
servers from web API configurations, making it easy to integrate REST APIs, GraphQL
endpoints, and other web services with AI assistants.
"""

__version__ = "0.2.0"
__author__ = "APIWeaver Contributors"

from .server import APIWeaver
from .models import APIConfig, APIEndpoint, AuthConfig, RequestParam

__all__ = [
    "APIWeaver",
    "APIConfig", 
    "APIEndpoint",
    "AuthConfig",
    "RequestParam"
]

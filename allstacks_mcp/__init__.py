"""Allstacks MCP Server - Modular implementation"""

__all__ = ["AllstacksAPIClient"]


def __getattr__(name: str):
    if name == "AllstacksAPIClient":
        from .client import AllstacksAPIClient

        return AllstacksAPIClient
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

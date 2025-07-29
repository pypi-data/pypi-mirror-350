"""
Trade MCP package for unified trading interface.
"""

from trade_mcp.server import setup_mcp_tools
from trade_mcp.api import APIClientManager, SpotTrading, MarketData

__all__ = ['setup_mcp_tools', 'APIClientManager', 'SpotTrading', 'MarketData']

import argparse
from trade_mcp.server.mcp_tools import setup_mcp_tools
from trade_mcp.api.client import APIClientManager

def main():
    """Main entry point for the trading MCP server.
    
    Run with:
        python -m trade_mcp.server.main --api-key YOUR_KEY --api-secret YOUR_SECRET --provider aster
    """
    parser = argparse.ArgumentParser(description='Run Trading MCP server')
    parser.add_argument('--axgrad-key', required=False, help='API key for the trading platform')
    parser.add_argument('--api-key', required=False, help='API key for the trading platform')
    parser.add_argument('--api-secret', required=False, help='API secret for the trading platform')
    parser.add_argument('--venue', required=True, help='Venue for the trading platform', choices=['test', 'axgrad_game_1', 'live'])
    args = parser.parse_args()

    # Require axgrad-key for certain venues
    if args.venue in ['axgrad_game_1', 'test'] and not args.axgrad_key:
        parser.error("--axgrad-key is required when --venue is 'axgrad_game_1' or 'test'.")

    # Require api-key and api-secret for certain venues
    if args.venue in ['test', 'live']:
        if not args.api_key or not args.api_secret:
            parser.error("--api-key and --api-secret are required when --venue is 'test' or 'live'.")

    # Initialize API client
    APIClientManager.initialize(
        axgrad_key=args.axgrad_key,
        api_key=args.api_key,
        api_secret=args.api_secret,
        venue=args.venue
    )

    # Set up and run MCP server
    mcp = setup_mcp_tools()
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main() 
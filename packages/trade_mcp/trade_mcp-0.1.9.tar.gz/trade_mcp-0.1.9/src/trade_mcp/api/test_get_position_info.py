import asyncio
from trade_mcp.api.client import APIClientManager
from trade_mcp.api import trading

# Replace these with your actual credentials and venue
AXGRAD_KEY = "17f597b026564aad93578e5f8f00d522"
API_KEY = "b8d09dfc73bd0c1c2826d9f663f80f4298bc730c9a2fd74d20c039b50bd3858a"
API_SECRET = "698591b0542be334c21729904a5944dc7174a6e1d48bc118631f3a426d0c5121"
VENUE = "test"  # or 'live'


def main():
    # Initialize the API client
    APIClientManager.initialize(
        axgrad_key=AXGRAD_KEY,
        api_key=API_KEY,
        api_secret=API_SECRET,
        venue=VENUE
    )

    async def run_tests():
        print("--- Testing get_position_info for BTCUSDT ---")
        result_btc = await trading.SpotTrading.get_position_info("BTCUSDT")
        print(result_btc)
        print("\n--- Testing get_position_info for all positions ---")
        result_all = await trading.SpotTrading.get_position_info("")
        print(result_all)

    asyncio.run(run_tests())

if __name__ == "__main__":
    main() 
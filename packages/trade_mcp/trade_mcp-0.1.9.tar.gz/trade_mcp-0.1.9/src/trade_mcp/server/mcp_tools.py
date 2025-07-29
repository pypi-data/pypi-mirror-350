from mcp.server.fastmcp import FastMCP
from trade_mcp.api.trading import SpotTrading
from trade_mcp.api.market_data import MarketData

def setup_mcp_tools() -> FastMCP:
    """Set up MCP tools for futures trading."""
    mcp = FastMCP("binance_mcp_server")
    
    # Register trading tools
    mcp.tool(name="get_position_mode", description="""
        Get user's position mode (Hedge Mode or One-way Mode).
    """)(SpotTrading.get_position_mode)
    
    mcp.tool(name="change_position_mode", description="""
        Change position mode between Hedge Mode and One-way Mode.

        Args:
            dual_side: "true" for Hedge Mode, "false" for One-way Mode
    """)(SpotTrading.change_position_mode)
    
    mcp.tool(name="place_multiple_orders", description="""
        Place multiple orders at once.

        Args:
            symbol: Trading pair symbol
            orders: List of order parameters. Each order must be a dictionary with:
                - type: Order type ("MARKET", "LIMIT", "STOP", "STOP_MARKET", "TRAILING_STOP_MARKET")
                - params: Dictionary containing the parameters for the specific order type
                
                The params dictionary should match the parameters of the corresponding single-order function:
                - For MARKET orders: side, quantity, position_side (optional)
                - For LIMIT orders: side, quantity, price, time_in_force, position_side (optional)
                - For STOP orders: side, quantity, price, stop_price, time_in_force, position_side (optional)
                - For STOP_MARKET orders: side, stop_price, position_side, quantity (if not close_position), close_position (optional)
                - For TRAILING_STOP_MARKET orders: side, callback_rate, quantity, position_side, activation_price
    """)(SpotTrading.place_multiple_orders)
    
    mcp.tool(name="place_order", description="""
        Place a futures order of any type (MARKET, LIMIT, STOP, STOP_MARKET, TRAILING_STOP_MARKET, etc).
        Args:
            symbol: Trading pair symbol (e.g. 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            type: Order type ('MARKET', 'LIMIT', 'STOP', 'STOP_MARKET', 'TRAILING_STOP_MARKET', etc)
            ...and more. See API for full details.
    """)(SpotTrading.place_order)
    
    mcp.tool(name="query_order", description="""
        Query a specific order's status.

        Args:
            symbol: Trading pair symbol
            order_id: Order ID to query
    """)(SpotTrading.query_order)
    
    mcp.tool(name="cancel_order", description="""
        Cancel an active order.

        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel
    """)(SpotTrading.cancel_order)
    
    mcp.tool(name="cancel_all_orders", description="""
        Cancel all open orders for a symbol.

        Args:
            symbol: Trading pair symbol
    """)(SpotTrading.cancel_all_orders)
    
    mcp.tool(name="cancel_multiple_orders", description="""
        Cancel multiple orders.

        Args:
            symbol: Trading pair symbol
            order_id_list: List of order IDs to cancel
    """)(SpotTrading.cancel_multiple_orders)
    
    mcp.tool(name="auto_cancel_all_orders", description="""
        Set up auto-cancellation of all orders after countdown.

        Args:
            symbol: Trading pair symbol
            countdown_time: Countdown time in milliseconds
    """)(SpotTrading.auto_cancel_all_orders)
    
    mcp.tool(name="get_open_order", description="""
        Query current open order by order id.

        Args:
            symbol: Trading pair symbol
            order_id: Order ID to query
    """)(SpotTrading.get_open_order)
    
    mcp.tool(name="get_open_orders", description="""
        Get all open futures orders for a specific symbol.

        Args:
            symbol: Trading pair symbol
    """)(SpotTrading.get_open_orders)
    
    mcp.tool(name="get_all_orders", description="""
        Get all account orders.

        Args:
            symbol: Trading pair symbol
            order_id: Optional order ID to start from
            start_time: Optional start time in ms
            end_time: Optional end time in ms
            limit: Maximum number of orders to return (default 500)
    """)(SpotTrading.get_all_orders)
    
    mcp.tool(name="get_balance", description="""
        Get futures account balance V2.
    """)(SpotTrading.get_balance)
    
    mcp.tool(name="get_account_info", description="""
        Get futures account information V2.
    """)(SpotTrading.get_account_info)
    
    mcp.tool(name="change_leverage", description="""
        Change initial leverage for a symbol.

        Args:
            symbol: Trading pair symbol
            leverage: Target initial leverage (1-125)
    """)(SpotTrading.change_leverage)
    
    mcp.tool(name="change_margin_type", description="""
        Change margin type between isolated and cross.

        Args:
            symbol: Trading pair symbol
            margin_type: 'ISOLATED' or 'CROSSED'
    """)(SpotTrading.change_margin_type)
    
    mcp.tool(name="modify_position_margin", description="""
        Modify isolated position margin.

        Args:
            symbol: Trading pair symbol
            amount: Amount to modify
            position_side: Position side ('BOTH', 'LONG', or 'SHORT')
            margin_type: 1 for add position margin, 2 for reduce position margin
    """)(SpotTrading.modify_position_margin)
    
    mcp.tool(name="get_position_margin_history", description="""
        Get position margin modification history.

        Args:
            symbol: Trading pair symbol
            margin_type: 1 for add position margin, 2 for reduce position margin
            limit: Number of entries to return
    """)(SpotTrading.get_position_margin_history)
    
    mcp.tool(name="get_position_info", description="""
        Get current position information V2.

        Args:
            symbol: Trading pair symbol
    """)(SpotTrading.get_position_info)
    
    mcp.tool(name="get_account_trades", description="""
        Get account trade list.

        Args:
            symbol: Trading pair symbol
            start_time: Optional start time in ms
            end_time: Optional end time in ms
            from_id: Optional trade ID to fetch from
            limit: Maximum number of trades to return (default 500)
    """)(SpotTrading.get_account_trades)
    
    mcp.tool(name="get_income_history", description="""
        Get income history.

        Args:
            symbol: Trading pair symbol
            income_type: Optional income type filter
            start_time: Optional start time in ms
            end_time: Optional end time in ms
            limit: Maximum number of records to return (default 100)
    """)(SpotTrading.get_income_history)
    
    mcp.tool(name="get_leverage_brackets", description="""
        Get notional and leverage brackets.

        Args:
            symbol: Trading pair symbol
    """)(SpotTrading.get_leverage_brackets)
    
    mcp.tool(name="get_adl_quantile", description="""
        Get position ADL quantile estimation.

        Args:
            symbol: Trading pair symbol
    """)(SpotTrading.get_adl_quantile)
    
    mcp.tool(name="get_force_orders", description="""
        Get user's force orders.

        Args:
            symbol: Trading pair symbol
            auto_close_type: Optional filter by auto-close type
            start_time: Optional start time in ms
            end_time: Optional end time in ms
            limit: Maximum number of orders to return (default 50)
    """)(SpotTrading.get_force_orders)
    
    mcp.tool(name="get_commission_rate", description="""
        Get user's commission rate for a symbol.

        Args:
            symbol: Trading pair symbol
    """)(SpotTrading.get_commission_rate)
    
    # Register market data tools based on the endpoint documentation
    mcp.tool(name="get_order_book", description="""
        Get order book for a symbol.
        Weight: 2-20 based on limit parameter.
        Required parameters:
        - symbol: Trading pair symbol
        - limit: Number of bids/asks (5,10,20,50,100,500,1000)
    """)(MarketData.get_order_book)
    
    mcp.tool(name="get_aggregate_trades", description="""
        Get compressed, aggregate market trades.
        Weight: 20
        Required parameters:
        - symbol: Trading pair symbol
        - from_id: ID to get trades from
        - start_time: Start timestamp in ms
        - end_time: End timestamp in ms
        - limit: Number of trades (max 1000)
    """)(MarketData.get_aggregate_trades)
    
    mcp.tool(name="get_klines", description="""
        Get kline/candlestick data for a symbol.
        Weight: 1-10 based on limit parameter.
        Required parameters:
        - symbol: Trading pair symbol
        - interval: Kline interval
        - start_time: Start timestamp in ms
        - end_time: End timestamp in ms
        - limit: Number of klines (max 1500)
    """)(MarketData.get_klines)
    
    mcp.tool(name="get_mark_price", description="""
        Get mark price and funding rate for a symbol.
        Weight: 1
        Required parameters:
        - symbol: Trading pair symbol
    """)(MarketData.get_mark_price)
    
    mcp.tool(name="get_funding_rate_history", description="""
        Get funding rate history for a symbol.
        Weight: 1
        Required parameters:
        - symbol: Trading pair symbol
        - start_time: Start timestamp in ms
        - end_time: End timestamp in ms
        - limit: Number of entries (max 1000)
    """)(MarketData.get_funding_rate_history)
    
    mcp.tool(name="get_price_ticker", description="""
        Get latest price for a symbol.
        Weight: 1
        Required parameters:
        - symbol: Trading pair symbol
    """)(MarketData.get_price_ticker)
    
    mcp.tool(name="get_book_ticker", description="""
        Get best price/qty on the order book for a symbol.
        Weight: 1
        Required parameters:
        - symbol: Trading pair symbol
    """)(MarketData.get_book_ticker)
    
    return mcp 
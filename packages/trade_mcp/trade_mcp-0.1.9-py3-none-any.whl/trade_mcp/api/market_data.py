from typing import Optional
from trade_mcp.api.client import APIClientManager

# Helper to enforce symbol/pair restriction

def _enforce_symbol_restriction(symbol_or_pair, client):
    if symbol_or_pair in [None, "", "null", "None", "none", "null", "Null", "NULL"]:
        symbol_or_pair = None
    if client.venue != "live":
        if symbol_or_pair is None:
            symbol_or_pair = "BTCUSDT"
        if symbol_or_pair != "BTCUSDT":
            raise Exception("Only BTCUSDT is allowed in non-live venues.")
    return symbol_or_pair

class MarketData:
    @staticmethod
    async def get_order_book(symbol: str, limit: int) -> str:
        """Get detailed order book data for a trading pair from the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        try:
            book = await client.get(f"/fapi/v1/depth", params={"symbol": symbol, "limit": limit}, security_type="NONE")
            if isinstance(book, dict) and 'code' in book and book['code'] < 0:
                return f"API Error: {book.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Order Book for {symbol}:\n\nBids (Price | Quantity):\n"
        for bid in book['bids']:
            result += f"{bid[0]} | {bid[1]}\n"
        result += "\nAsks (Price | Quantity):\n"
        for ask in book['asks']:
            result += f"{ask[0]} | {ask[1]}\n"
        return result

    @staticmethod
    async def get_aggregate_trades(
        symbol: str,
        from_id: int = None,
        start_time: int = None,
        end_time: int = None,
        limit: int = None
    ) -> str:
        """Get compressed, aggregate trades data for analysis from the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol}
        if from_id is not None:
            params["fromId"] = from_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        try:
            trades = await client.get("/fapi/v1/aggTrades", params=params, security_type="NONE")
            if isinstance(trades, dict) and 'code' in trades and trades['code'] < 0:
                return f"API Error: {trades.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Aggregate Trades for {symbol}:\n"
        for trade in trades:
            result += f"""- Aggregate ID: {trade['a']}
  Price: {trade['p']}
  Quantity: {trade['q']}
  First Trade ID: {trade['f']}
  Last Trade ID: {trade['l']}
  Time: {trade['T']}
  Buyer is Maker: {trade['m']}\n"""
        return result

    @staticmethod
    async def get_klines(
        symbol: str,
        interval: str,
        start_time: int = None,
        end_time: int = None,
        limit: int = None
    ) -> str:
        """Get candlestick/kline data for technical analysis from the exchange API.
        Optional parameters: start_time, end_time, limit. If not provided, they will be omitted from the request.
        """
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {
            "symbol": symbol,
            "interval": interval
        }
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        try:
            klines = await client.get("/fapi/v1/klines", params=params, security_type="NONE")
            if isinstance(klines, dict) and 'code' in klines and klines['code'] < 0:
                return f"API Error: {klines.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Kline Data for {symbol} ({interval}):\n"
        for k in klines:
            result += f"""- Open Time: {k[0]}
  Open: {k[1]}
  High: {k[2]}
  Low: {k[3]}
  Close: {k[4]}
  Volume: {k[5]}
  Close Time: {k[6]}
  Quote Volume: {k[7]}
  Number of Trades: {k[8]}\n"""
        return result

    @staticmethod
    async def get_index_price_klines(
        pair: str,
        interval: str,
        start_time: int = None,
        end_time: int = None,
        limit: int = None
    ) -> str:
        """Get kline/candlestick bars for the index price of a pair from the exchange API."""
        client = APIClientManager.get_client()
        pair = _enforce_symbol_restriction(pair, client)
        params = {
            "pair": pair,
            "interval": interval
        }
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        try:
            klines = await client.get("/fapi/v1/indexPriceKlines", params=params, security_type="NONE")
            if isinstance(klines, dict) and 'code' in klines and klines['code'] < 0:
                return f"API Error: {klines.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Index Price Kline Data for {pair} ({interval}):\n"
        for k in klines:
            result += f"""- Open Time: {k[0]}
  Open: {k[1]}
  High: {k[2]}
  Low: {k[3]}
  Close: {k[4]}
  Ignore: {k[5]}
  Close Time: {k[6]}
  Ignore: {k[7]}
  Number of Basic Data: {k[8]}\n"""
        return result

    @staticmethod
    async def get_mark_price_klines(
        symbol: str,
        interval: str,
        start_time: int = None,
        end_time: int = None,
        limit: int = None
    ) -> str:
        """Get kline/candlestick bars for the mark price of a symbol from the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {
            "symbol": symbol,
            "interval": interval
        }
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        try:
            klines = await client.get("/fapi/v1/markPriceKlines", params=params, security_type="NONE")
            if isinstance(klines, dict) and 'code' in klines and klines['code'] < 0:
                return f"API Error: {klines.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Mark Price Kline Data for {symbol} ({interval}):\n"
        for k in klines:
            result += f"""- Open Time: {k[0]}
  Open: {k[1]}
  High: {k[2]}
  Low: {k[3]}
  Close: {k[4]}
  Ignore: {k[5]}
  Close Time: {k[6]}
  Ignore: {k[7]}
  Number of Basic Data: {k[8]}\n"""
        return result

    @staticmethod
    async def get_mark_price(symbol: str = None) -> str:
        """Get current mark price and funding rate information from the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol} if symbol else {}
        try:
            mark = await client.get("/fapi/v1/premiumIndex", params=params, security_type="NONE")
            if isinstance(mark, dict) and 'code' in mark and mark['code'] < 0:
                return f"API Error: {mark.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        if symbol:
            return f"""Mark Price Info for {symbol}:
- Mark Price: {mark['markPrice']}
- Index Price: {mark['indexPrice']}
- Estimated Settle Price: {mark['estimatedSettlePrice']}
- Last Funding Rate: {mark['lastFundingRate']}
- Next Funding Time: {mark['nextFundingTime']}
- Interest Rate: {mark['interestRate']}
- Time: {mark['time']}"""
        else:
            # mark is a list of dicts
            result = "All Mark Prices:\n"
            for m in mark:
                result += f"- Symbol: {m['symbol']}, Mark Price: {m['markPrice']}, Index Price: {m['indexPrice']}, Last Funding Rate: {m['lastFundingRate']}, Time: {m.get('time', 'N/A')}\n"
            return result

    @staticmethod
    async def get_funding_rate_history(
        symbol: str = None,
        start_time: int = None,
        end_time: int = None,
        limit: int = None
    ) -> str:
        """Get historical funding rates for analysis from the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        try:
            history = await client.get("/fapi/v1/fundingRate", params=params, security_type="NONE")
            if isinstance(history, dict) and 'code' in history and history['code'] < 0:
                return f"API Error: {history.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Funding Rate History for {symbol if symbol else 'All Symbols'}:\n"
        for rate in history:
            result += f"""- Funding Rate: {rate['fundingRate']}
  Funding Time: {rate['fundingTime']}\n"""
        return result

    @staticmethod
    async def get_price_ticker(symbol: str = None) -> str:
        """Get latest price information for a symbol or all symbols from the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol} if symbol else {}
        try:
            ticker = await client.get("/fapi/v1/ticker/price", params=params, security_type="NONE")
            if isinstance(ticker, dict) and 'code' in ticker and ticker['code'] < 0:
                return f"API Error: {ticker.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        if symbol:
            return f"""Price Ticker for {symbol}:
- Price: {ticker['price']}
- Time: {ticker['time']}"""
        else:
            # ticker is a list of dicts
            result = "All Price Tickers:\n"
            for t in ticker:
                result += f"- Symbol: {t['symbol']}, Price: {t['price']}, Time: {t.get('time', 'N/A')}\n"
            return result

    @staticmethod
    async def get_book_ticker(symbol: str = None) -> str:
        """Get best bid/ask prices and quantities from the order book from the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol} if symbol else {}
        try:
            ticker = await client.get("/fapi/v1/ticker/bookTicker", params=params, security_type="NONE")
            if isinstance(ticker, dict) and 'code' in ticker and ticker['code'] < 0:
                return f"API Error: {ticker.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        if symbol:
            return f"""Order Book Ticker for {symbol}:
- Best Bid Price: {ticker['bidPrice']}
- Best Bid Quantity: {ticker['bidQty']}
- Best Ask Price: {ticker['askPrice']}
- Best Ask Quantity: {ticker['askQty']}
- Time: {ticker['time']}"""
        else:
            # ticker is a list of dicts
            result = "All Book Tickers:\n"
            for t in ticker:
                result += f"- Symbol: {t['symbol']}, Bid: {t['bidPrice']} ({t['bidQty']}), Ask: {t['askPrice']} ({t['askQty']}), Time: {t.get('time', 'N/A')}\n"
            return result 
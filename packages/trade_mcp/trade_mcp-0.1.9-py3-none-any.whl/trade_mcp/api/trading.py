from typing import List, Dict, Optional
from trade_mcp.api.client import APIClientManager
import time
import json

# Helper to enforce symbol/pair restriction

def _enforce_symbol_restriction(symbol_or_pair, client):
    if symbol_or_pair in [None, "ALL", "all", "All"]:
        symbol_or_pair = None
    if client.venue != "live":
        if symbol_or_pair is None:
            symbol_or_pair = "BTCUSDT"
        if symbol_or_pair != "BTCUSDT":
            raise Exception("Only BTCUSDT is allowed in non-live venues.")
    return symbol_or_pair

class SpotTrading:
    @staticmethod
    async def get_position_mode() -> str:
        """Get the current position mode setting for spot trading from the exchange API."""
        client = APIClientManager.get_client()
        try:
            mode = await client.get("/fapi/v1/positionSide/dual", security_type="USER_DATA")
            if isinstance(mode, dict) and 'code' in mode and mode['code'] < 0:
                return f"API Error: {mode.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"Position Mode: {'Hedge Mode' if mode['dualSidePosition'] else 'One-way Mode'}"

    @staticmethod
    async def change_position_mode(dual_side: bool) -> str:
        """Change the position mode between Hedge Mode and One-way Mode via the exchange API."""
        client = APIClientManager.get_client()
        params = {"dualSidePosition": str(dual_side).lower()}
        try:
            result = await client.post("/fapi/v1/positionSide/dual", params=params, security_type="TRADE")
            if isinstance(result, dict) and 'code' in result and result['code'] < 0:
                return f"API Error: {result.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"Position mode changed successfully: {'Hedge Mode' if dual_side else 'One-way Mode'}"

    @staticmethod
    def _transform_order_format(order: Dict) -> Dict:
        """Transform order format to match the expected format.
        
        Handles both flat format and nested params format:
        Flat format:
            {
                "type": "LIMIT",
                "symbol": "BTCUSDT",
                "side": "BUY",
                "quantity": 0.001,
                "price": 50000.0,
                "time_in_force": "GTC"
            }
            
        Nested format:
            {
                "type": "LIMIT",
                "params": {
                    "symbol": "BTCUSDT",
                    "side": "BUY",
                    "quantity": 0.001,
                    "price": 50000.0,
                    "time_in_force": "GTC"
                }
            }
        """
        transformed = {}
        
        # Handle nested params format
        if "params" in order:
            transformed = order["params"].copy()
            transformed["type"] = order.get("type", "LIMIT")
        else:
            transformed = order.copy()
        
        # Handle common key variations
        key_mappings = {
            "orderType": "type",
            "timeInForce": "time_in_force",
            "stopPrice": "stop_price",
            "callbackRate": "callback_rate",
            "activationPrice": "activation_price",
            "closePosition": "close_position",
            "positionSide": "position_side"
        }
        
        for old_key, new_key in key_mappings.items():
            if old_key in transformed:
                transformed[new_key] = transformed.pop(old_key)
        
        # Convert order type to uppercase if present
        if "type" in transformed:
            transformed["type"] = transformed["type"].upper()
        
        # Convert side to uppercase if present
        if "side" in transformed:
            transformed["side"] = transformed["side"].upper()
        
        # Convert position_side to uppercase if present
        if "position_side" in transformed:
            transformed["position_side"] = transformed["position_side"].upper()
        
        # Convert time_in_force to uppercase if present
        if "time_in_force" in transformed:
            transformed["time_in_force"] = transformed["time_in_force"].upper()
        
        # Handle numeric values
        numeric_fields = ["quantity", "price", "stop_price", "callback_rate", "activation_price"]
        for field in numeric_fields:
            if field in transformed and transformed[field] is not None:
                try:
                    transformed[field] = float(transformed[field])
                except (ValueError, TypeError):
                    pass  # Keep original value if conversion fails
        
        # Handle boolean values
        if "close_position" in transformed:
            if isinstance(transformed["close_position"], str):
                transformed["close_position"] = transformed["close_position"].lower() == "true"
        
        return transformed

    @staticmethod
    async def place_multiple_orders(orders: List[Dict], symbol: str = None) -> str:
        """Place multiple orders at once using the batch endpoint, using APIClient for signing and sending. At most 5 orders can be placed in a single batch request. Price and quantity precision are at most 2 decimal places and will be rounded accordingly. If more than 5 orders are provided, they will be split into batches and placed sequentially."""
        import json
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)

        # Helper to normalize and validate a single order
        def normalize_and_validate_order(order, idx):
            # Inject symbol if provided and missing in the order
            if symbol:
                if "params" in order:
                    if "symbol" not in order["params"] or not order["params"]["symbol"]:
                        order["params"]["symbol"] = symbol
                else:
                    if "symbol" not in order or not order["symbol"]:
                        order["symbol"] = symbol
            # Normalize order format
            order = SpotTrading._transform_order_format(order)
            # --- Type Handling Section (from place_order) ---
            # Enums/strings to uppercase
            if "side" in order and order["side"] is not None:
                order["side"] = str(order["side"]).upper()
            if "type" in order and order["type"] is not None:
                order["type"] = str(order["type"]).upper()
            if "position_side" in order and order["position_side"] is not None:
                order["position_side"] = str(order["position_side"]).upper()
            if "time_in_force" in order and order["time_in_force"] is not None:
                order["time_in_force"] = str(order["time_in_force"]).upper()
            if "working_type" in order and order["working_type"] is not None:
                order["working_type"] = str(order["working_type"]).upper()
            if "new_order_resp_type" in order and order["new_order_resp_type"] is not None:
                order["new_order_resp_type"] = str(order["new_order_resp_type"]).upper()
            # Numeric conversions
            def to_float(val):
                try:
                    return float(val)
                except (TypeError, ValueError):
                    return val
            def to_int(val):
                try:
                    return int(val)
                except (TypeError, ValueError):
                    return val
            for num_field in ["quantity", "price", "stop_price", "activation_price", "callback_rate"]:
                if num_field in order and order[num_field] is not None:
                    order[num_field] = to_float(order[num_field])
            # --- Precision Handling ---
            for field in ["quantity", "price"]:
                if field in order and order[field] is not None:
                    try:
                        order[field] = round(float(order[field]), 2)
                    except Exception:
                        pass
            for int_field in ["recv_window", "timestamp"]:
                if int_field in order and order[int_field] is not None:
                    order[int_field] = to_int(order[int_field])
            # Boolean-like string conversions (API expects 'true'/'false' as string)
            def to_api_bool(val):
                if isinstance(val, bool):
                    return 'true' if val else 'false'
                if isinstance(val, str):
                    if val.lower() in ['true', '1', 'yes']:
                        return 'true'
                    elif val.lower() in ['false', '0', 'no']:
                        return 'false'
                return val
            for bool_field in ["close_position", "reduce_only", "price_protect"]:
                if bool_field in order and order[bool_field] is not None:
                    order[bool_field] = to_api_bool(order[bool_field])
            # --- End Type Handling Section ---
            # Ensure quantity and price are strings for API compliance
            for str_field in ["quantity", "price"]:
                if str_field in order and order[str_field] is not None:
                    order[str_field] = str(order[str_field])
            # Prepare for validation and camelCase conversion
            api_order = {}
            order_for_validation = order.copy()
            t = order_for_validation.get("type", "").upper()
            try:
                # Required fields
                if "symbol" not in order_for_validation or not order_for_validation["symbol"]:
                    raise ValueError("Missing required field: symbol")
                if "side" not in order_for_validation or not order_for_validation["side"]:
                    raise ValueError("Missing required field: side")
                if "type" not in order_for_validation or not order_for_validation["type"]:
                    raise ValueError("Missing required field: type")
                # Required/forbidden params by type (from place_order)
                if t == "LIMIT":
                    if "time_in_force" not in order_for_validation or order_for_validation["time_in_force"] is None:
                        order_for_validation["time_in_force"] = "GTC"
                    if "quantity" not in order_for_validation or order_for_validation["quantity"] is None or "price" not in order_for_validation or order_for_validation["price"] is None:
                        raise ValueError("LIMIT order requires quantity and price.")
                elif t == "MARKET":
                    if "quantity" not in order_for_validation or order_for_validation["quantity"] is None:
                        raise ValueError("MARKET order requires quantity.")
                elif t in ["STOP", "TAKE_PROFIT"]:
                    if ("quantity" not in order_for_validation or order_for_validation["quantity"] is None or
                        "price" not in order_for_validation or order_for_validation["price"] is None or
                        "stop_price" not in order_for_validation or order_for_validation["stop_price"] is None):
                        raise ValueError(f"{t} order requires quantity, price, and stop_price.")
                    if "time_in_force" not in order_for_validation or order_for_validation["time_in_force"] is None:
                        order_for_validation["time_in_force"] = "GTC"
                elif t in ["STOP_MARKET", "TAKE_PROFIT_MARKET"]:
                    if order_for_validation.get("close_position", "false") == "true":
                        order_for_validation.pop("quantity", None)
                        order_for_validation.pop("reduce_only", None)
                    else:
                        if "quantity" not in order_for_validation or order_for_validation["quantity"] is None:
                            raise ValueError(f"{t} order requires quantity if not close_position=true.")
                    if "stop_price" not in order_for_validation or order_for_validation["stop_price"] is None:
                        raise ValueError(f"{t} order requires stop_price.")
                elif t == "TRAILING_STOP_MARKET":
                    if "callback_rate" not in order_for_validation or order_for_validation["callback_rate"] is None:
                        raise ValueError("TRAILING_STOP_MARKET order requires callback_rate.")
                # Only include valid fields for the API
                field_map = {
                    "symbol": "symbol",
                    "side": "side",
                    "type": "type",
                    "position_side": "positionSide",
                    "quantity": "quantity",
                    "price": "price",
                    "time_in_force": "timeInForce",
                    "reduce_only": "reduceOnly",
                    "new_client_order_id": "newClientOrderId",
                    "stop_price": "stopPrice",
                    "close_position": "closePosition",
                    "activation_price": "activationPrice",
                    "callback_rate": "callbackRate",
                    "working_type": "workingType",
                    "price_protect": "priceProtect",
                    "new_order_resp_type": "newOrderRespType",
                    "recv_window": "recvWindow",
                }
                for k, v in order_for_validation.items():
                    if k in field_map and v is not None:
                        api_order[field_map[k]] = v
                return api_order, None
            except Exception as e:
                return None, f"Order {idx+1}: Error - {str(e)}"

        # Split orders into batches of at most 5
        batch_size = 5
        batches = [orders[i:i+batch_size] for i in range(0, len(orders), batch_size)]
        all_summaries = []
        all_errors = []
        order_counter = 0
        for batch in batches:
            batch_orders = []
            errors = []
            for idx, order in enumerate(batch):
                api_order, error = normalize_and_validate_order(order, order_counter + idx)
                if api_order:
                    batch_orders.append(api_order)
                if error:
                    errors.append(error)
            order_counter += len(batch)
            if not batch_orders:
                all_errors.extend(errors)
                continue
            params = {"batchOrders": json.dumps(batch_orders, separators=(',', ':'))}
            try:
                result = await client.post("/fapi/v1/batchOrders", params=params, security_type="TRADE")
            except Exception as e:
                all_summaries.append(f"Batch order request failed: {str(e)}")
                continue
            # Format response summary
            if isinstance(result, list):
                for idx, order in enumerate(result):
                    if isinstance(order, dict) and "orderId" in order:
                        all_summaries.append(
                            f"Order {idx+1}: Placed successfully - Symbol: {order.get('symbol')}, Order ID: {order.get('orderId')}, Side: {order.get('side')}, Type: {order.get('type')}, Qty: {order.get('origQty')}, Price: {order.get('price', '')}, Status: {order.get('status')}"
                        )
                    elif isinstance(order, dict) and "code" in order:
                        all_summaries.append(f"Order {idx+1}: Error - {order.get('msg', order.get('code'))}")
                    else:
                        all_summaries.append(f"Order {idx+1}: Unknown response: {order}")
            else:
                all_summaries.append(f"Batch order response: {result}")
            if errors:
                all_errors.extend(errors)
        if all_errors:
            all_summaries.append("\nValidation errors:\n" + "\n".join(all_errors))
        return "\n".join(all_summaries)

    @staticmethod
    async def query_order(
        symbol: str,
        order_id: int
    ) -> str:
        """Query a specific order's status via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        try:
            order = await client.get("/fapi/v1/order", params={"symbol": symbol, "orderId": order_id}, security_type="TRADE")
            if isinstance(order, dict) and 'code' in order and order['code'] < 0:
                return f"API Error: {order.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"""Order Status:
- Symbol: {order['symbol']}
- Order ID: {order['orderId']}
- Status: {order['status']}
- Type: {order['type']}
- Side: {order['side']}
- Price: {order['price']}
- Quantity: {order['origQty']}
- Executed: {order['executedQty']}"""

    @staticmethod
    async def cancel_order(symbol: str, order_id: int) -> str:
        """Cancel an active order via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol, "orderId": order_id}
        try:
            result = await client.delete("/fapi/v1/order", params=params, security_type="TRADE")
            if isinstance(result, dict) and 'code' in result and result['code'] < 0:
                return f"API Error: {result.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"Order {order_id} for {symbol} cancelled successfully"

    @staticmethod
    async def cancel_all_orders(symbol: str) -> str:
        """Cancel all open orders for a symbol via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol}
        try:
            result = await client.delete("/fapi/v1/allOpenOrders", params=params, security_type="TRADE")
            if isinstance(result, dict) and 'code' in result and result['code'] < 0:
                return f"API Error: {result.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"All open orders for {symbol} cancelled successfully"

    @staticmethod
    async def cancel_multiple_orders(symbol: str, order_id_list: list) -> str:
        """Cancel multiple orders via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        # orderIdList must be a JSON array string
        import json
        params = {"symbol": symbol, "orderIdList": json.dumps(order_id_list)}
        try:
            result = await client.delete("/fapi/v1/batchOrders", params=params, security_type="TRADE")
            if isinstance(result, dict) and 'code' in result and result['code'] < 0:
                return f"API Error: {result.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"Multiple orders cancelled for {symbol}: {order_id_list}"

    @staticmethod
    async def auto_cancel_all_orders(symbol: str, countdown_time: int) -> str:
        """Set up auto-cancellation of all orders after countdown via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol, "countdownTime": countdown_time}
        try:
            result = await client.post("/fapi/v1/countdownCancelAll", params=params, security_type="TRADE")
            if isinstance(result, dict) and 'code' in result and result['code'] < 0:
                return f"API Error: {result.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"Auto-cancel set for {symbol} in {countdown_time}ms"

    @staticmethod
    async def get_open_order(symbol: str, order_id: int) -> str:
        """Query current open order by order id via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol, "orderId": order_id}
        try:
            order = await client.get("/fapi/v1/openOrder", params=params, security_type="TRADE")
            if isinstance(order, dict) and 'code' in order and order['code'] < 0:
                return f"API Error: {order.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"""Open Order:
- Symbol: {order['symbol']}
- Order ID: {order['orderId']}
- Type: {order['type']}
- Side: {order['side']}
- Price: {order['price']}
- Quantity: {order['origQty']}
- Status: {order['status']}"""

    @staticmethod
    async def get_open_orders(symbol: str) -> str:
        """Get all open futures orders for a specific symbol via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        try:
            orders = await client.get("/fapi/v1/openOrders", params={"symbol": symbol}, security_type="TRADE")
            if isinstance(orders, dict) and 'code' in orders and orders['code'] < 0:
                return f"API Error: {orders.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        
        if not orders:
            return f"No open orders found for {symbol}"
        
        result = f"Open Orders for {symbol}:\n"
        for order in orders:
            result += f"""- Order ID: {order['orderId']}
  Side: {order['side']}
  Type: {order['type']}
  Quantity: {order['origQty']}
  Price: {order.get('price', 'MARKET')}
  Status: {order['status']}
  Position Side: {order['positionSide']}
  Time: {order['time']}"""
        return result

    @staticmethod
    async def get_all_orders(symbol: str, order_id: int = None, start_time: int = None, end_time: int = None, limit: int = None) -> str:
        """Get all account orders via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol}
        if order_id is not None:
            params["orderId"] = order_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        try:
            orders = await client.get("/fapi/v1/allOrders", params=params, security_type="TRADE")
            if isinstance(orders, dict) and 'code' in orders and orders['code'] < 0:
                return f"API Error: {orders.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"All Orders for {symbol}:\n"
        for order in orders:
            result += f"""- Order ID: {order['orderId']}
  Type: {order['type']}
  Side: {order['side']}
  Price: {order['price']}
  Quantity: {order['origQty']}
  Status: {order['status']}
  Time: {order['time']}\n"""
        return result

    @staticmethod
    async def get_balance() -> str:
        """Get futures account balance information via the exchange API."""
        client = APIClientManager.get_client()
        try:
            balances = await client.get("/fapi/v2/balance", security_type="USER_DATA")
            if isinstance(balances, dict) and 'code' in balances and balances['code'] < 0:
                return f"API Error: {balances.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = "Account Balances:\n"
        for balance in balances:
            result += f"""- Asset: {balance['asset']}
  Wallet Balance: {balance['balance']}
  Cross Wallet Balance: {balance['crossWalletBalance']}
  Unrealized PnL: {balance['crossUnPnl']}
  Available Balance: {balance['availableBalance']}\n"""
        return result

    @staticmethod
    async def get_account_info() -> str:
        """Get account information from the exchange API."""
        client = APIClientManager.get_client()
        try:
            account = await client.get("/fapi/v2/account", security_type="USER_DATA")
            if isinstance(account, dict) and 'code' in account and account['code'] < 0:
                return f"API Error: {account.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        
        # Format assets
        assets_info = "Assets:\n"
        for asset in account['assets']:
            if float(asset['walletBalance']) > 0:
                assets_info += f"- {asset['asset']}: Balance={asset['walletBalance']}, Available={asset['availableBalance']}\n"
        
        # Format positions
        positions_info = "\nOpen Positions:\n"
        active_positions = [p for p in account['positions'] if float(p['positionAmt']) != 0]
        if active_positions:
            for pos in active_positions:
                positions_info += f"- {pos['symbol']}: Amount={pos['positionAmt']}, Entry Price={pos['entryPrice']}, PnL={pos['unrealizedProfit']}\n"
        else:
            positions_info += "No open positions\n"
        
        return assets_info + positions_info

    @staticmethod
    async def change_leverage(symbol: str, leverage: int) -> str:
        """Change the initial leverage setting for a trading pair via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol, "leverage": leverage}
        try:
            result = await client.post("/fapi/v1/leverage", params=params, security_type="TRADE")
            if isinstance(result, dict) and 'code' in result and result['code'] < 0:
                return f"API Error: {result.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"Leverage changed successfully for {symbol} to {leverage}x"

    @staticmethod
    async def change_margin_type(symbol: str, margin_type: str) -> str:
        """Change the margin type between isolated and cross margin via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol, "marginType": margin_type}
        try:
            result = await client.post("/fapi/v1/marginType", params=params, security_type="TRADE")
            if isinstance(result, dict) and 'code' in result and result['code'] < 0:
                return f"API Error: {result.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"Margin type changed successfully for {symbol} to {margin_type}"

    @staticmethod
    async def modify_position_margin(symbol: str, amount: float, position_side: str, margin_type: int) -> str:
        """Modify isolated position margin via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol, "amount": amount, "positionSide": position_side, "type": margin_type}
        try:
            result = await client.post("/fapi/v1/positionMargin", params=params, security_type="TRADE")
            if isinstance(result, dict) and 'code' in result and result['code'] < 0:
                return f"API Error: {result.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"Position margin modified successfully for {symbol}"

    @staticmethod
    async def get_position_margin_history(symbol: str, margin_type: int, limit: int) -> str:
        """Get position margin modification history via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol, "type": margin_type, "limit": limit}
        try:
            history = await client.get("/fapi/v1/positionMargin/history", params=params, security_type="USER_DATA")
            if isinstance(history, dict) and 'code' in history and history['code'] < 0:
                return f"API Error: {history.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        if not history:
            return "No margin modification history found"
        result = "Position Margin History:\n"
        for entry in history:
            result += f"""- Symbol: {entry['symbol']}
  Amount: {entry['amount']}
  Type: {entry['type']}
  Time: {entry['time']}"""
        return result

    @staticmethod
    async def get_position_info(symbol: Optional[str] = None) -> str:
        """Get detailed information about current positions via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        try:
            positions = await client.get("/fapi/v2/positionRisk", params=params, security_type="USER_DATA")
            if isinstance(positions, dict) and 'code' in positions and positions['code'] < 0:
                return f"API Error: {positions.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        if not positions:
            return f"No position information found for {symbol if symbol else 'All Symbols'}"
        result = f"Position Information for {symbol if symbol else 'All Symbols'}:\n"
        for pos in positions:
            result += f"""- Side: {pos['positionSide']}
  Amount: {pos['positionAmt']}
  Entry Price: {pos['entryPrice']}
  Unrealized PnL: {pos['unRealizedProfit']}
  Leverage: {pos['leverage']}
  Margin Type: {pos['marginType']}"""
        return result

    @staticmethod
    async def get_account_trades(
        symbol: str,
        start_time: int = None,
        end_time: int = None,
        from_id: int = None,
        limit: int = None
    ) -> str:
        """Get account trade list from the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if from_id is not None:
            params["fromId"] = from_id
        try:
            trades = await client.get("/fapi/v1/userTrades", params=params, security_type="USER_DATA")
            if isinstance(trades, dict) and 'code' in trades and trades['code'] < 0:
                return f"API Error: {trades.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Trade History for {symbol}:\n"
        for trade in trades:
            result += f"""- Trade ID: {trade['id']}
  Order ID: {trade['orderId']}
  Price: {trade['price']}
  Quantity: {trade['qty']}
  Commission: {trade['commission']}
  Realized PnL: {trade['realizedPnl']}
  Time: {trade['time']}\n"""
        return result

    @staticmethod
    async def get_income_history(symbol: str = None, income_type: str = None, start_time: int = None, end_time: int = None, limit: int = None) -> str:
        """Get income history via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        if income_type is not None:
            params["incomeType"] = income_type
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        try:
            history = await client.get("/fapi/v1/income", params=params, security_type="USER_DATA")
            if isinstance(history, dict) and 'code' in history and history['code'] < 0:
                return f"API Error: {history.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Income History for {symbol if symbol else 'All Symbols'}:\n"
        for income in history:
            result += f"""- Type: {income['incomeType']}
  Income: {income['income']}
  Asset: {income['asset']}
  Time: {income['time']}
  Transaction ID: {income['tranId']}\n"""
        return result

    @staticmethod
    async def get_leverage_brackets(symbol: str = None) -> str:
        """Get notional and leverage brackets via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        try:
            brackets = await client.get("/fapi/v1/leverageBracket", params=params, security_type="USER_DATA")
            if isinstance(brackets, dict) and 'code' in brackets and brackets['code'] < 0:
                return f"API Error: {brackets.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Leverage Brackets for {symbol if symbol else 'All Symbols'}:\n"
        for bracket in brackets:
            result += f"""- Bracket: {bracket['bracket']}
  Initial Leverage: {bracket['initialLeverage']}
  Notional Cap: {bracket['notionalCap']}
  Notional Floor: {bracket['notionalFloor']}
  Maintenance Margin Ratio: {bracket['maintMarginRatio']}\n"""
        return result

    @staticmethod
    async def get_adl_quantile(symbol: str = None) -> str:
        """Get position ADL quantile estimation via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        try:
            quantile = await client.get("/fapi/v1/adlQuantile", params=params, security_type="USER_DATA")
            if isinstance(quantile, dict) and 'code' in quantile and quantile['code'] < 0:
                return f"API Error: {quantile.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"ADL Quantile for {symbol if symbol else 'All Symbols'}:\n"
        for pos in quantile:
            result += f"""- Position Side: {pos['positionSide']}
  ADL Quantile: {pos['adlQuantile']}\n"""
        return result

    @staticmethod
    async def get_force_orders(symbol: str = None, auto_close_type: str = None, start_time: int = None, end_time: int = None, limit: int = None) -> str:
        """Get user's force orders via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        if auto_close_type is not None:
            params["autoCloseType"] = auto_close_type
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        try:
            orders = await client.get("/fapi/v1/forceOrders", params=params, security_type="USER_DATA")
            if isinstance(orders, dict) and 'code' in orders and orders['code'] < 0:
                return f"API Error: {orders.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        result = f"Force Orders for {symbol if symbol else 'All Symbols'}:\n"
        for order in orders:
            result += f"""- Order ID: {order['orderId']}
  Status: {order['status']}
  Type: {order['type']}
  Side: {order['side']}
  Price: {order['price']}
  Average Price: {order['avgPrice']}
  Time: {order['time']}\n"""
        return result

    @staticmethod
    async def get_commission_rate(symbol: str) -> str:
        """Get user's commission rate for a symbol via the exchange API."""
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {"symbol": symbol}
        try:
            rate = await client.get("/fapi/v1/commissionRate", params=params, security_type="USER_DATA")
            if isinstance(rate, dict) and 'code' in rate and rate['code'] < 0:
                return f"API Error: {rate.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        return f"""Commission Rates for {symbol}:
- Maker Commission Rate: {rate['makerCommissionRate']}
- Taker Commission Rate: {rate['takerCommissionRate']}"""

    @staticmethod
    async def place_order(
        symbol: str,
        side: str,
        order_type: str,
        quantity: float = None,
        position_side: str = None,
        price: float = None,
        time_in_force: str = None,
        reduce_only: str = None,
        new_client_order_id: str = None,
        stop_price: float = None,
        close_position: str = None,
        activation_price: float = None,
        callback_rate: float = None,
        working_type: str = None,
        price_protect: str = None,
        new_order_resp_type: str = None,
        recv_window: int = None,
        timestamp: int = None
    ) -> str:
        """General order placement function for all order types, handling required/optional params as per endpoint docs."""
        # --- Type Handling Section ---
        # Enums/strings to uppercase
        if side is not None:
            side = str(side).upper()
        if order_type is not None:
            order_type = str(order_type).upper()
        if position_side is not None:
            position_side = str(position_side).upper()
        if time_in_force is not None:
            time_in_force = str(time_in_force).upper()
        if working_type is not None:
            working_type = str(working_type).upper()
        if new_order_resp_type is not None:
            new_order_resp_type = str(new_order_resp_type).upper()
        # Numeric conversions
        def to_float(val):
            try:
                return float(val)
            except (TypeError, ValueError):
                return val
        def to_int(val):
            try:
                return int(val)
            except (TypeError, ValueError):
                return val
        if quantity is not None:
            quantity = to_float(quantity)
        if price is not None:
            price = to_float(price)
        if stop_price is not None:
            stop_price = to_float(stop_price)
        if activation_price is not None:
            activation_price = to_float(activation_price)
        if callback_rate is not None:
            callback_rate = to_float(callback_rate)
        if recv_window is not None:
            recv_window = to_int(recv_window)
        if timestamp is not None:
            timestamp = to_int(timestamp)
        # Boolean-like string conversions (API expects 'true'/'false' as string)
        def to_api_bool(val):
            if isinstance(val, bool):
                return 'true' if val else 'false'
            if isinstance(val, str):
                if val.lower() in ['true', '1', 'yes']:
                    return 'true'
                elif val.lower() in ['false', '0', 'no']:
                    return 'false'
            return val
        if close_position is not None:
            close_position = to_api_bool(close_position)
        if reduce_only is not None:
            reduce_only = to_api_bool(reduce_only)
        if price_protect is not None:
            price_protect = to_api_bool(price_protect)
        # --- End Type Handling Section ---
        client = APIClientManager.get_client()
        symbol = _enforce_symbol_restriction(symbol, client)
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
        }
        # Only add if not None
        if position_side is not None:
            params["positionSide"] = position_side
        if quantity is not None and not (order_type in ["STOP_MARKET", "TAKE_PROFIT_MARKET"] and close_position == "true"):
            params["quantity"] = quantity
        if price is not None:
            params["price"] = price
        if time_in_force is not None:
            params["timeInForce"] = time_in_force
        if reduce_only is not None:
            params["reduceOnly"] = reduce_only
        if new_client_order_id is not None:
            params["newClientOrderId"] = new_client_order_id
        if stop_price is not None:
            params["stopPrice"] = stop_price
        if close_position is not None:
            params["closePosition"] = close_position
        if activation_price is not None:
            params["activationPrice"] = activation_price
        if callback_rate is not None:
            params["callbackRate"] = callback_rate
        if working_type is not None:
            params["workingType"] = working_type
        if price_protect is not None:
            params["priceProtect"] = price_protect
        if new_order_resp_type is not None:
            params["newOrderRespType"] = new_order_resp_type
        if recv_window is not None:
            params["recvWindow"] = recv_window
        # Always set timestamp if not provided
        if timestamp is not None:
            params["timestamp"] = timestamp
        else:
            params["timestamp"] = int(time.time() * 1000)

        # Logic for required/forbidden params by type
        t = order_type
        if t == "LIMIT":
            if time_in_force is None:
                params["timeInForce"] = "GTC"
            if quantity is None or price is None:
                raise ValueError("LIMIT order requires quantity and price.")
        elif t == "MARKET":
            if quantity is None:
                raise ValueError("MARKET order requires quantity.")
        elif t in ["STOP", "TAKE_PROFIT"]:
            if quantity is None or price is None or stop_price is None:
                raise ValueError(f"{t} order requires quantity, price, and stop_price.")
            if time_in_force is None:
                params["timeInForce"] = "GTC"
        elif t in ["STOP_MARKET", "TAKE_PROFIT_MARKET"]:
            if close_position == "true":
                params.pop("quantity", None)  # Must not send quantity
                params.pop("reduceOnly", None)
            else:
                if quantity is None:
                    raise ValueError(f"{t} order requires quantity if not close_position=true.")
            if stop_price is None:
                raise ValueError(f"{t} order requires stop_price.")
        elif t == "TRAILING_STOP_MARKET":
            if callback_rate is None:
                raise ValueError("TRAILING_STOP_MARKET order requires callback_rate.")
        # Send order
        try:
            order = await client.post("/fapi/v1/order", params=params, security_type="TRADE")
            if isinstance(order, dict) and 'code' in order and order['code'] < 0:
                return f"API Error: {order.get('msg', 'Unknown error')}"
        except Exception as e:
            return f"Request failed: {str(e)}"
        print(order)
        a = f"""Order placed successfully:\n- Symbol: {order['symbol']}\n- Order ID: {order['orderId']}\n- Side: {order['side']}\n- Position Side: {order.get('positionSide', '')}\n- Type: {order['type']}\n- Quantity: {order.get('origQty', '')}\n- Price: {order.get('price', '')}\n- Stop Price: {order.get('stopPrice', '')}\n- Status: {order['status']}""" 
        print(a)
        return a
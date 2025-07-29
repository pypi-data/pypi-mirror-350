import aiohttp
import hmac
import hashlib
import time
from typing import Dict, Any, Optional
from urllib.parse import urlencode

class APIClient:
    BINANCE_TESTNET_BASE_URL = "https://mcp-gateway-759711950494.asia-southeast1.run.app/binance_testnet"
    # BINANCE_TESTNET_BASE_URL = "http://localhost:8080/binance_testnet"
    ASTER_BASE_URL = "https://fapi.asterdex.com"
    
    def __init__(self, axgrad_key: str, api_key: str, api_secret: str, venue: str):
        self.axgrad_key = axgrad_key
        self.api_key = api_key
        self.api_secret = api_secret
        self.venue = venue
        self.base_url = None
        if venue == "live":
            self.base_url = self.ASTER_BASE_URL
        else:
            self.base_url = self.BINANCE_TESTNET_BASE_URL

    def _get_signature(self, params: Dict[str, Any]) -> str:
        """(Deprecated) Signature generation is no longer used."""
        return ""

    async def _request_testnet(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        security_type: str = "NONE"
    ) -> Dict[str, Any]:
        """Make an HTTP request to the exchange API, sending all parameters directly including security_type and axgrad_key."""
        if params is None:
            params = {}
        # Always include security_type in the parameters
        params['security_type'] = security_type
        # Always include axgrad_key in the parameters
        params['axgrad_key'] = self.axgrad_key
        if self.venue == "test":
            params['api_key'] = self.api_key
            params['api_secret'] = self.api_secret
        headers = {}
        url = f"{self.base_url}{endpoint}"
        request_params = None
        json_body = None

        if method == 'GET':
            request_params = params
            json_body = None
        else:
            request_params = None
            json_body = params

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, params=request_params, json=json_body) as response:
                return await response.json()

    async def _request_live(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        security_type: str = "NONE"
    ) -> Dict[str, Any]:
        """Make an HTTP request to the exchange API with security type handling."""
        if params is None:
            params = {}

        headers = {}
        url = f"{self.base_url}{endpoint}"
        request_params = None
        json_body = None

        if security_type in ("TRADE", "USER_DATA"):  # SIGNED endpoints
            params['timestamp'] = int(time.time() * 1000)
            params_for_sig = params.copy()
            query_string = urlencode(params_for_sig)
            signature = hmac.new(
                self.api_secret.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            params['signature'] = signature
            headers['X-MBX-APIKEY'] = self.api_key
            if method == 'POST':
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                # For signed POST, send as urlencoded body
                request_params = f"{urlencode(params)}"
                json_body = None
            else:
                request_params = f"{urlencode(params)}"
                json_body = None
        elif security_type in ("USER_STREAM", "MARKET_DATA"):
            headers['X-MBX-APIKEY'] = self.api_key
            request_params = params if method == 'GET' else None
            json_body = params if method != 'GET' else None
        else:
            request_params = params if method == 'GET' else None
            json_body = params if method != 'GET' else None

        async with aiohttp.ClientSession() as session:
            if method == 'POST' and security_type in ("TRADE", "USER_DATA"):
                async with session.request(method, url, headers=headers, data=request_params) as response:
                    return await response.json()
            else:
                async with session.request(method, url, headers=headers, params=request_params, json=json_body) as response:
                    return await response.json()

    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        security_type: str = "NONE"
    ) -> Dict[str, Any]:
        if self.venue == "live":
            return await self._request_live(method, endpoint, params, security_type)
        else:
            return await self._request_testnet(method, endpoint, params, security_type)

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, security_type: str = "NONE") -> Dict[str, Any]:
        """Make a GET request to the exchange API with security type."""
        return await self._request('GET', endpoint, params, security_type)
    
    async def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None, security_type: str = "TRADE") -> Dict[str, Any]:
        """Make a POST request to the exchange API with security type."""
        return await self._request('POST', endpoint, params, security_type)
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None, security_type: str = "TRADE") -> Dict[str, Any]:
        """Make a DELETE request to the exchange API with security type."""
        return await self._request('DELETE', endpoint, params, security_type) 
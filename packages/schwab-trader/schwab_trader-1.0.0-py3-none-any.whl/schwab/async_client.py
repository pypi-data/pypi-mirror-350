from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import aiohttp
from urllib.parse import urljoin

from .models.base import AccountNumbers  # Keep for now - custom aggregation model
from .models.generated.market_data_models import ErrorResponse, QuoteResponse
from .models.generated.trading_models import (
    AccountNumberHash as AccountNumber, Account, Order
)
from .api.quotes import QuotesMixin

class AsyncSchwabClient(QuotesMixin):
    """Async client for interacting with the Schwab Trading API."""
    
    TRADING_BASE_URL = "https://api.schwabapi.com/trader/v1"
    MARKET_DATA_BASE_URL = "https://api.schwabapi.com/marketdata/v1"
    
    def __init__(self, api_key: str):
        """Initialize the client with API credentials.
        
        Args:
            api_key: The API key (Bearer token) for authentication
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        self._session = None
    
    async def __aenter__(self):
        """Create session on context manager enter."""
        self._session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session on context manager exit."""
        if self._session:
            await self._session.close()
            self._session = None
    
    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make an async request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Optional query parameters
            json: Optional JSON body
            
        Returns:
            API response as dictionary
            
        Raises:
            aiohttp.ClientError: If the request fails
        """
        if not self._session:
            raise RuntimeError("Client must be used as a context manager")
            
        # Choose base URL based on endpoint
        if endpoint.startswith("/marketdata/"):
            base_url = "https://api.schwabapi.com"
        elif endpoint.startswith("/trader/"):
            base_url = "https://api.schwabapi.com"
        else:
            # Default to trading base URL for backward compatibility
            base_url = "https://api.schwabapi.com"
            endpoint = f"/trader/v1{endpoint}"
            
        url = urljoin(base_url, endpoint)
        async with self._session.request(method, url, params=params, json=json) as response:
            response.raise_for_status()
            return await response.json()
            
    async def _async_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make an async GET request to the API.
        
        Args:
            endpoint: API endpoint
            params: Optional query parameters
            
        Returns:
            API response as dictionary
        """
        return await self._make_request("GET", endpoint, params=params)
    
    async def get_account_numbers(self) -> AccountNumbers:
        """Get list of account numbers and their encrypted values."""
        data = await self._make_request("GET", "/accounts/accountNumbers")
        return AccountNumbers(accounts=[AccountNumber(**account) for account in data])
    
    async def get_accounts(self, include_positions: bool = False) -> List[Account]:
        """Get all linked accounts with balances and optionally positions.
        
        Args:
            include_positions: Whether to include position information
            
        Returns:
            List of account information
        """
        params = {"fields": "positions"} if include_positions else None
        data = await self._make_request("GET", "/accounts", params=params)
        return [Account(**account) for account in data]
    
    async def get_account(self, account_number: str, include_positions: bool = False) -> Account:
        """Get specific account information.
        
        Args:
            account_number: The encrypted account number
            include_positions: Whether to include position information
            
        Returns:
            Account information
        """
        params = {"fields": "positions"} if include_positions else None
        data = await self._make_request("GET", f"/accounts/{account_number}", params=params)
        return Account(**data)
    
    async def get_orders(
        self,
        account_number: str,
        from_entered_time: datetime,
        to_entered_time: datetime,
        max_results: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Order]:
        """Get orders for a specific account.
        
        Args:
            account_number: The encrypted account number
            from_entered_time: Start time for order history
            to_entered_time: End time for order history
            max_results: Maximum number of orders to return
            status: Filter orders by status
            
        Returns:
            List of orders
        """
        params = {
            "fromEnteredTime": from_entered_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "toEnteredTime": to_entered_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        }
        if max_results is not None:
            params["maxResults"] = max_results
        if status is not None:
            params["status"] = status
            
        data = await self._make_request("GET", f"/accounts/{account_number}/orders", params=params)
        return [Order(**order) for order in data]
        
    async def place_order(self, account_number: str, order: Order) -> None:
        """Place an order for a specific account.
        
        Args:
            account_number: The encrypted account number
            order: The order to place
            
        Returns:
            None if successful
            
        Raises:
            aiohttp.ClientError: If the request fails
        """
        await self._make_request("POST", f"/accounts/{account_number}/orders", json=order.model_dump(by_alias=True))
        
    async def replace_order(self, account_number: str, order_id: int, new_order: Order) -> None:
        """Replace an existing order with a new order.
        
        The existing order will be canceled and a new order will be created.
        
        Args:
            account_number: The encrypted account number
            order_id: The ID of the order to replace
            new_order: The new order to place
            
        Returns:
            None if successful
            
        Raises:
            aiohttp.ClientError: If the request fails
        """
        await self._make_request(
            "PUT",
            f"/accounts/{account_number}/orders/{order_id}",
            json=new_order.model_dump(by_alias=True)
        )
        
    async def cancel_order(self, account_number: str, order_id: int) -> None:
        """Cancel a specific order.
        
        Args:
            account_number: The encrypted account number
            order_id: The ID of the order to cancel
            
        Returns:
            None if successful
            
        Raises:
            aiohttp.ClientError: If the request fails
        """
        await self._make_request("DELETE", f"/accounts/{account_number}/orders/{order_id}")
        
    async def get_order(self, account_number: str, order_id: int) -> Order:
        """Get a specific order by its ID.
        
        Args:
            account_number: The encrypted account number
            order_id: The ID of the order to retrieve
            
        Returns:
            The order details
            
        Raises:
            aiohttp.ClientError: If the request fails
        """
        data = await self._make_request("GET", f"/accounts/{account_number}/orders/{order_id}")
        return Order(**data)


    async def get_option_chain(self, symbol: str, contract_type: str = None, strike_count: int = None,
                              include_underlying_quote: bool = None, strategy: str = None,
                              strike_from_date: str = None, strike_to_date: str = None,
                              strike_from: float = None, strike_to: float = None,
                              expiration_month: str = None, option_type: str = None,
                              days_to_expiration: int = None, exp_month: str = None,
                              option_detail_flag: bool = None, 
                              entitlement: str = "np") -> Dict[str, Any]:
        """
        Get option chain for a symbol.
        
        Args:
            symbol: The underlying symbol for the option chain
            contract_type: Type of contracts (CALL, PUT, ALL)
            strike_count: Number of strikes to return
            include_underlying_quote: Include quote for underlying symbol
            strategy: Option strategy (SINGLE, ANALYTICAL, COVERED, VERTICAL, etc.)
            strike_from_date: From date for strike range (yyyy-MM-dd)
            strike_to_date: To date for strike range (yyyy-MM-dd)
            strike_from: From strike price
            strike_to: To strike price
            expiration_month: Expiration month (ALL, JAN, FEB, etc.)
            option_type: Option type (S for Standard, NS for Non-Standard, ALL)
            days_to_expiration: Days to expiration
            exp_month: Expiration month (ALL, JAN, FEB, etc.)
            option_detail_flag: Include additional option details
            entitlement: Entitlement level (np, npbo, retail)
            
        Returns:
            Dictionary containing option chain data
        """
        params = {
            "symbol": symbol,
            "entitlement": entitlement
        }
        
        # Add optional parameters
        if contract_type:
            params["contractType"] = contract_type
        if strike_count is not None:
            params["strikeCount"] = strike_count
        if include_underlying_quote is not None:
            params["includeUnderlyingQuote"] = include_underlying_quote
        if strategy:
            params["strategy"] = strategy
        if strike_from_date:
            params["strikeFromDate"] = strike_from_date
        if strike_to_date:
            params["strikeToDate"] = strike_to_date
        if strike_from is not None:
            params["strikeFrom"] = strike_from
        if strike_to is not None:
            params["strikeTo"] = strike_to
        if expiration_month:
            params["expirationMonth"] = expiration_month
        if option_type:
            params["optionType"] = option_type
        if days_to_expiration is not None:
            params["daysToExpiration"] = days_to_expiration
        if exp_month:
            params["expMonth"] = exp_month
        if option_detail_flag is not None:
            params["optionDetailFlag"] = option_detail_flag
            
        return await self._make_request("GET", "/marketdata/v1/chains", params=params)
    
    async def get_option_expiration_chain(self, symbol: str, 
                                         entitlement: str = "np") -> Dict[str, Any]:
        """
        Get option expiration dates for a symbol.
        
        Args:
            symbol: The underlying symbol
            entitlement: Entitlement level (np, npbo, retail)
            
        Returns:
            Dictionary containing expiration dates
        """
        params = {
            "symbol": symbol,
            "entitlement": entitlement
        }
        
        return await self._make_request("GET", "/marketdata/v1/expirationchain", params=params)

    
    async def _async_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the API.
        
        Args:
            endpoint: API endpoint
            params: Optional query parameters
            
        Returns:
            API response as dictionary
        """
        return await self._make_request("GET", endpoint, params=params)

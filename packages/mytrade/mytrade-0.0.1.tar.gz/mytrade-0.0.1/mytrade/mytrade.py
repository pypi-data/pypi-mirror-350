import ctypes
import os
from ctypes import c_char_p, c_double, c_int, POINTER
from typing import Union, Tuple, TypeVar, Type
from datetime import datetime

from dataclasses import dataclass, asdict

import json
from typing import Dict, Any, Optional

T = TypeVar('T')


@dataclass
class TradeOrder:
    contract_id: str  # 合同编号
    order_date: str  # 委托日期
    order_time: str  # 委托时间
    code: str  # 证券代码
    name: str  # 证券名称
    operation: str  # 操作
    remark: str  # 备注
    order_quantity: int  # 委托数量
    trade_quantity: int  # 成交数量
    cancel_quantity: int  # 撤销数量
    order_price: float  # 委托价格
    trade_price: float  # 成交价格/成交均价
    market: str  # 交易市场
    source_data: Dict[str, Any]

    def time(self) -> datetime:
        return datetime.strptime(f"{self.order_date} {self.order_time}", "%Y%m%d %H:%M:%S")

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(
            contract_id=data.get('contract_id', ''),
            order_date=data.get('order_date', ''),
            order_time=data.get('order_time', ''),
            code=data.get('code', ''),
            name=data.get('name', ''),
            operation=data.get('operation', ''),
            remark=data.get('remark', ''),
            order_quantity=data.get('order_quantity', 0),
            trade_quantity=data.get('trade_quantity', 0),
            cancel_quantity=data.get('cancel_quantity', 0),
            order_price=data.get('order_price', 0.0),
            trade_price=data.get('trade_price', 0.0),
            market=data.get('market', ''),
            source_data=data.get('source_data', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class TradeInfo:
    sequence: int  # 序号，例如 3
    contract_id: str  # 合同编号，例如 "201840"
    market: str  # 交易市场，例如 "深Ａ"
    market_id: str  # 市场ID，例如 "1"
    trade_date: str  # 成交日期，例如 "20250321"
    trade_time: str  # 成交时间，例如 "09:32:20"
    code: str  # 证券代码，例如 "123048"
    name: str  # 证券名称，例如 "应急转债"
    operation: str  # 操作，例如 "匹配成交卖出"
    trade_price: float  # 成交价格，例如 141.528
    trade_quantity: int  # 成交数量，例如 10
    trade_amount: float  # 成交金额，例如 1415.28
    account_id: str  # 股东账户，例如 "0340398883"
    trade_id: str  # 成交编号，例如 "0105000004132547"
    source_data: Dict[str, Any]

    def time(self) -> datetime:
        return datetime.strptime(f"{self.trade_date} {self.trade_time}", "%Y%m%d %H:%M:%S")

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(
            sequence=data.get('sequence', 0),
            contract_id=data.get('contract_id', ''),
            market=data.get('market', ''),
            market_id=data.get('market_id', ''),
            trade_date=data.get('trade_date', ''),
            trade_time=data.get('trade_time', ''),
            code=data.get('code', ''),
            name=data.get('name', ''),
            operation=data.get('operation', ''),
            trade_price=data.get('trade_price', 0.0),
            trade_quantity=data.get('trade_quantity', 0),
            trade_amount=data.get('trade_amount', 0.0),
            account_id=data.get('account_id', ''),
            trade_id=data.get('trade_id', ''),
            source_data=data.get('source_data', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class TradePosition:
    sequence: int  # 序号，例如 0
    code: str  # 证券代码，例如 "123025"
    name: str  # 证券名称，例如 "精测转债"
    frozen_qty: int  # 冻结数量，例如 0
    available_qty: int  # 可用余额，例如 0
    stock_balance: int  # 股票余额，例如 0
    actual_qty: int  # 实际数量
    market_price: float  # 市价，例如 142.512
    market_value: float  # 市值，例如 0.0001
    cost_price: float  # 成本价，例如 0
    profit_loss_rate: float  # 浮动盈亏比%，例如 0
    profit_loss: float  # 盈亏，例如 -2.01
    account_id: str  # 股东账户，例如 "0340398883"
    market_id: str  # 市场ID，例如 "1"
    market: str  # 交易市场，例如 "深Ａ"
    source_data: Dict[str, Any]

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(
            sequence=data.get('sequence', 0),
            code=data.get('code', ''),
            name=data.get('name', ''),
            frozen_qty=data.get('frozen_qty', 0),
            available_qty=data.get('available_qty', 0),
            stock_balance=data.get('stock_balance', 0),
            actual_qty=data.get('actual_qty', 0),
            market_price=data.get('market_price', 0.0),
            market_value=data.get('market_value', 0.0),
            cost_price=data.get('cost_price', 0.0),
            profit_loss_rate=data.get('profit_loss_rate', 0.0),
            profit_loss=data.get('profit_loss', 0.0),
            account_id=data.get('account_id', ''),
            market_id=data.get('market_id', ''),
            market=data.get('market', ''),
            source_data=data.get('source_data', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class AccountInfo:
    available_cash: float
    total_value: float
    source_data: Dict[str, Any]

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(
            available_cash=data.get('available_cash', 0.0),
            total_value=data.get('total_value', 0.0),
            source_data=data.get('source_data', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


class TradeClientError(Exception):
    """Custom exception for TradeClient errors."""

    def __init__(self, message: str, response: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.response = response


class TradeClient:
    """A Python class to interact with the trade.dylib shared library."""

    def __init__(self, ops: Optional[Dict[str, Any]] = None):
        """Initialize the TradeClient by loading the shared library.

        Args:
            ops: Optional connection parameters (e.g., API keys, server settings).
        """
        self._ops = ops  # Store connection parameters for later use
        self._client_id = None

        base_dir = os.path.dirname(__file__)
        lib_path = os.path.join(base_dir, "trade.so")

        try:
            self.lib = ctypes.CDLL(lib_path)
        except OSError as e:
            raise TradeClientError(f"Failed to load library {lib_path}: {e}")

        self._setup_functions()

    def __enter__(self):
        self.connect(self._ops)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


    def _setup_functions(self):
        """Configure the argument and return types for the library functions."""

        self.lib.Connect.argtypes = [c_char_p]
        self.lib.Connect.restype = c_char_p

        self.lib.Disconnect.argtypes = [c_char_p]
        self.lib.Disconnect.restype = c_char_p

        self.lib.Buy.argtypes = [c_char_p, c_char_p, POINTER(c_double), POINTER(c_int)]
        self.lib.Buy.restype = c_char_p

        self.lib.Sell.argtypes = [c_char_p, c_char_p, POINTER(c_double), POINTER(c_int)]
        self.lib.Sell.restype = c_char_p

        self.lib.CancelOrder.argtypes = [c_char_p, c_char_p, c_char_p]
        self.lib.CancelOrder.restype = c_char_p

        self.lib.AccountInfo.argtypes = [c_char_p]
        self.lib.AccountInfo.restype = c_char_p

        self.lib.GetOrder.argtypes = [c_char_p, c_char_p, c_char_p]
        self.lib.GetOrder.restype = c_char_p

        self.lib.GetOrders.argtypes = [c_char_p]
        self.lib.GetOrders.restype = c_char_p

        self.lib.GetOpenOrders.argtypes = [c_char_p]
        self.lib.GetOpenOrders.restype = c_char_p

        self.lib.GetOrdersHistory.argtypes = [c_char_p, POINTER(c_int), POINTER(c_int)]
        self.lib.GetOrdersHistory.restype = c_char_p

        self.lib.GetPositions.argtypes = [c_char_p]
        self.lib.GetPositions.restype = c_char_p

        self.lib.GetPosition.argtypes = [c_char_p, c_char_p]
        self.lib.GetPosition.restype = c_char_p

        self.lib.GetTrades.argtypes = [c_char_p]
        self.lib.GetTrades.restype = c_char_p

        self.lib.GetTradesHistory.argtypes = [c_char_p, POINTER(c_int), POINTER(c_int)]
        self.lib.GetTradesHistory.restype = c_char_p

    def _parse_response(self, result: Optional[bytes]) -> Tuple[Union[str, dict, list], Optional[str]]:
        """Parse the C function response into a Python dictionary.

        Args:
            result: The raw bytes response from the C library.

        Returns:
            The 'data' field from the response payload if code == 0.

        Raises:
            TradeClientError: If the response is empty, invalid JSON, or code != 0.
        """
        if not result:
            response = {
                "code": -1,
                "message": "Empty response from library",
                "client_id": "",
                "payload": {"data": {}, "error": "null_pointer"}
            }
            raise TradeClientError(response["message"], response)

        try:
            response = json.loads(result.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            response = {
                "code": -1,
                "message": f"Failed to parse response: {str(e)}",
                "client_id": "",
                "payload": {"data": {}, "error": "parse_error"}
            }
            raise TradeClientError(response["message"], response)

        # Check for error in response
        code = response.get("code", -1)
        if code != 0:
            message = response.get("message", "Unknown error")
            raise TradeClientError(message, response)

        # Ensure payload exists and has required fields
        payload = response.get("payload", {})
        if not isinstance(payload, dict):
            return {}, "invalid_payload_type"

        # print(result)
        # Ensure 'data' and 'error' fields exist with correct types
        data = payload.get("data")
        if data is None:
            raise KeyError("Key 'data' does not exist in payload")

        if not isinstance(data, (str, dict, list)):
            data = {}

        error = payload.get("error")
        if error is None:
            raise KeyError("Key 'error' does not exist in payload")

        # Convert various null/empty representations to None
        null_values = {"", "nil", "<nil>", "<null>", "null"}
        error = None if error in null_values else error

        return data, error

    def connect(self, ops: Optional[Dict[str, Any]] = None):
        """Initialize a new trading session with the given configuration."""
        ops = ops or {}
        result = self.lib.Connect(json.dumps(ops).encode('utf-8'))
        data, err = self._parse_response(result)
        if err not in (None, ""):  # Treat None or empty string as success
            raise TradeClientError(f"Failed to connect: {err}")

        self._client_id = data

    def disconnect(self):
        """Disconnect the trading session for the given client ID."""
        self.lib.Disconnect(self._client_id.encode('utf-8'))
        self._client_id = None

    def buy(self, code: str, price: float, qty: int):
        """Place a buy order for the given client ID, code, price, and quantity."""
        c_price = c_double(price)
        c_qty = c_int(qty)
        result = self.lib.Buy(self._client_id.encode('utf-8'), code.encode('utf-8'),
                              ctypes.byref(c_price), ctypes.byref(c_qty))
        order_id, error = self._parse_response(result)

        return order_id, error

    def sell(self, code: str, price: float, qty: int):
        """Place a sell order for the given client ID, code, price, and quantity."""
        c_price = c_double(price)
        c_qty = c_int(qty)
        result = self.lib.Sell(self._client_id.encode('utf-8'), code.encode('utf-8'),
                               ctypes.byref(c_price), ctypes.byref(c_qty))
        order_id, error = self._parse_response(result)
        return order_id, error

    def cancel_order(self, code: str, oid: str):
        """Cancel an order for the given client ID, code, and order ID."""
        result = self.lib.CancelOrder(self._client_id.encode('utf-8'), code.encode('utf-8'),
                                      oid.encode('utf-8'))
        _, error = self._parse_response(result)
        return oid, error

    def account_info(self):
        """Retrieve account information for the given client ID."""
        result = self.lib.AccountInfo(self._client_id.encode('utf-8'))
        account, error = self._parse_response(result)

        if error is None:
            account = AccountInfo.from_dict(account)

        return account, error

    def get_order(self, code: str, oid: str):
        """Retrieve a specific order for the given client ID, code, and order ID."""
        result = self.lib.GetOrder(self._client_id.encode('utf-8'), code.encode('utf-8'),
                                   oid.encode('utf-8'))
        order, error = self._parse_response(result)
        if error is None:
            order = TradeOrder.from_dict(order)
        return order, error

    def get_orders(self):
        """Retrieve all orders for the given client ID."""
        result = self.lib.GetOrders(self._client_id.encode('utf-8'))
        orders, error = self._parse_response(result)
        if error is None:
            orders = [TradeOrder.from_dict(order) for order in orders]
        return orders, error

    def get_open_orders(self):
        """Retrieve all open orders for the given client ID."""
        result = self.lib.GetOpenOrders(self._client_id.encode('utf-8'))
        orders, error = self._parse_response(result)
        if error is None:
            orders = [TradeOrder.from_dict(order) for order in orders]
        return orders, error

    def get_orders_history(self, start_date: int, end_date: int):
        """Retrieve order history for the given client ID and date range."""
        c_start_date = c_int(start_date)
        c_end_date = c_int(end_date)
        result = self.lib.GetOrdersHistory(self._client_id.encode('utf-8'),
                                           ctypes.byref(c_start_date), ctypes.byref(c_end_date))
        orders, error = self._parse_response(result)
        if error is None:
            orders = [TradeOrder.from_dict(order) for order in orders]
        return orders, error

    def get_positions(self):
        """Retrieve all positions for the given client ID."""
        result = self.lib.GetPositions(self._client_id.encode('utf-8'))
        positions, error = self._parse_response(result)
        if error is None:
            positions = [TradePosition.from_dict(pos) for pos in positions]
        return positions, error

    def get_position(self, code: str) -> Dict[str, Any]:
        """Retrieve a specific position for the given client ID and code."""
        result = self.lib.GetPosition(self._client_id.encode('utf-8'), code.encode('utf-8'))
        position, error = self._parse_response(result)
        if error is None:
            position = TradePosition.from_dict(position)
        return position, error

    def get_trades(self):
        """Retrieve all trades for the given client ID."""
        result = self.lib.GetTrades(self._client_id.encode('utf-8'))
        trades, error = self._parse_response(result)
        if error is None:
            trades = [TradeInfo.from_dict(trade) for trade in trades]
        return trades, error

    def get_trades_history(self, start_date: int, end_date: int):
        """Retrieve trade history for the given client ID and date range."""
        c_start_date = c_int(start_date)
        c_end_date = c_int(end_date)
        result = self.lib.GetTradesHistory(self._client_id.encode('utf-8'),
                                           ctypes.byref(c_start_date), ctypes.byref(c_end_date))
        trades, error = self._parse_response(result)
        if error is None:
            trades = [TradeInfo.from_dict(trade) for trade in trades]
        return trades, error


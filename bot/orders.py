"""
Order placement logic for Binance Futures Testnet.

Provides high-level functions that:
  1. Build the correct parameter payload for each order type.
  2. Call the client wrapper.
  3. Return a structured result dict for clean CLI display.
"""

from __future__ import annotations

import logging

from binance.client import Client  # only for constant references

from bot.client import BinanceTestnetClient
from bot.logging_config import setup_logging

logger = setup_logging().getChild("orders")


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _build_market_params(symbol: str, side: str, quantity: float) -> dict:
    return {
        "symbol": symbol,
        "side": side,
        "type": Client.FUTURE_ORDER_TYPE_MARKET,
        "quantity": quantity,
    }


def _build_limit_params(
    symbol: str, side: str, quantity: float, price: float
) -> dict:
    return {
        "symbol": symbol,
        "side": side,
        "type": Client.FUTURE_ORDER_TYPE_LIMIT,
        "quantity": quantity,
        "price": price,
        "timeInForce": Client.TIME_IN_FORCE_GTC,
    }


def _parse_response(response: dict) -> dict:
    """
    Extract the fields we care about from a raw Binance order response.
    Missing fields gracefully default to 'N/A'.
    """
    return {
        "orderId": response.get("orderId", "N/A"),
        "symbol": response.get("symbol", "N/A"),
        "side": response.get("side", "N/A"),
        "type": response.get("type", "N/A"),
        "status": response.get("status", "N/A"),
        "origQty": response.get("origQty", "N/A"),
        "executedQty": response.get("executedQty", "N/A"),
        "avgPrice": response.get("avgPrice", "N/A"),
        "price": response.get("price", "N/A"),
        "timeInForce": response.get("timeInForce", "N/A"),
        "updateTime": response.get("updateTime", "N/A"),
    }


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------


def place_order(
    client: BinanceTestnetClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict:
    """
    Place a MARKET or LIMIT futures order.

    Parameters
    ----------
    client      : BinanceTestnetClient instance
    symbol      : trading pair, e.g. 'BTCUSDT'
    side        : 'BUY' or 'SELL'
    order_type  : 'MARKET' or 'LIMIT'
    quantity    : order size in base asset units
    price       : limit price (required for LIMIT, ignored for MARKET)

    Returns
    -------
    dict with parsed order details
    """
    order_type = order_type.upper()

    if order_type == "MARKET":
        params = _build_market_params(symbol, side, quantity)
    elif order_type == "LIMIT":
        if price is None:
            raise ValueError("price must be provided for LIMIT orders.")
        params = _build_limit_params(symbol, side, quantity, price)
    else:
        raise ValueError(f"Unsupported order type: {order_type}")

    logger.info(
        "Placing %s %s order | symbol=%s qty=%s%s",
        side,
        order_type,
        symbol,
        quantity,
        f" price={price}" if price else "",
    )

    raw_response = client.place_futures_order(**params)
    parsed = _parse_response(raw_response)

    logger.info(
        "Order placed successfully | orderId=%s status=%s executedQty=%s avgPrice=%s",
        parsed["orderId"],
        parsed["status"],
        parsed["executedQty"],
        parsed["avgPrice"],
    )

    return parsed

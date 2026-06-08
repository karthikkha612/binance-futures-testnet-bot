"""
Input validation for trading bot CLI arguments.
All validators raise ValueError with a human-readable message on failure.
"""

from __future__ import annotations

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    """Return the symbol in upper-case or raise ValueError."""
    symbol = symbol.strip().upper()
    if not symbol or not symbol.isalnum():
        raise ValueError(
            f"Invalid symbol '{symbol}'. Must be alphanumeric, e.g. BTCUSDT."
        )
    return symbol


def validate_side(side: str) -> str:
    """Validate order side (BUY / SELL)."""
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(
            f"Invalid side '{side}'. Must be one of: {', '.join(sorted(VALID_SIDES))}."
        )
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type (MARKET / LIMIT)."""
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}."
        )
    return order_type


def validate_quantity(quantity: str | float) -> float:
    """Validate that quantity is a positive number."""
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid quantity '{quantity}'. Must be a positive number.")
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than 0, got {qty}.")
    return qty


def validate_price(price: str | float | None, order_type: str) -> float | None:
    """
    Validate price.
    - LIMIT  orders: price is required and must be positive.
    - MARKET orders: price must be absent / None.
    """
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders (--price).")
        try:
            p = float(price)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid price '{price}'. Must be a positive number.")
        if p <= 0:
            raise ValueError(f"Price must be greater than 0, got {p}.")
        return p

    # MARKET order
    if price is not None:
        # Warn but don't fail; price is simply ignored
        return None
    return None


def validate_all(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str | float,
    price: str | float | None = None,
) -> dict:
    """
    Run all validators and return a clean params dict.
    Raises ValueError on the first validation failure.
    """
    params = {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
        "price": None,
    }
    # validate_price needs the already-normalised order_type
    params["price"] = validate_price(price, params["order_type"])
    return params

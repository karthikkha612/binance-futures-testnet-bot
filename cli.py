#!/usr/bin/env python3
"""
cli.py – Command-line entry point for the Binance Futures Testnet trading bot.

Usage examples
--------------
# Market BUY
python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.001

# Limit SELL
python cli.py --symbol BTCUSDT --side SELL --order_type LIMIT --quantity 0.001 --price 100000
"""

from __future__ import annotations

import argparse
import sys

from dotenv import load_dotenv

from bot.client import BinanceTestnetClient
from bot.logging_config import setup_logging
from bot.orders import place_order
from bot.validators import validate_all

# Load .env before anything else so credentials are available
load_dotenv()

logger = setup_logging().getChild("cli")


# ------------------------------------------------------------------
# CLI helpers
# ------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet – place MARKET or LIMIT orders via CLI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cli.py --symbol BTCUSDT --side BUY  --order_type MARKET --quantity 0.001\n"
            "  python cli.py --symbol ETHUSDT --side SELL --order_type LIMIT  --quantity 0.01 --price 3500\n"
        ),
    )

    parser.add_argument(
        "--symbol",
        required=True,
        metavar="SYMBOL",
        help="Trading pair symbol, e.g. BTCUSDT",
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL"],
        type=str.upper,
        metavar="SIDE",
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--order_type",
        required=True,
        choices=["MARKET", "LIMIT"],
        type=str.upper,
        metavar="ORDER_TYPE",
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        metavar="QUANTITY",
        help="Order quantity in base asset units, e.g. 0.001 for BTC",
    )
    parser.add_argument(
        "--price",
        required=False,
        type=float,
        default=None,
        metavar="PRICE",
        help="Limit price (required for LIMIT orders, ignored for MARKET)",
    )

    return parser


def _print_separator(char: str = "─", width: int = 60) -> None:
    print(char * width)


def _print_order_summary(params: dict) -> None:
    """Pretty-print the order request summary."""
    _print_separator()
    print("  ORDER REQUEST SUMMARY")
    _print_separator()
    print(f"  Symbol     : {params['symbol']}")
    print(f"  Side       : {params['side']}")
    print(f"  Order Type : {params['order_type']}")
    print(f"  Quantity   : {params['quantity']}")
    if params.get("price"):
        print(f"  Price      : {params['price']}")
    _print_separator()


def _print_order_response(result: dict) -> None:
    """Pretty-print the order response details."""
    print("  ORDER RESPONSE")
    _print_separator()
    print(f"  Order ID     : {result['orderId']}")
    print(f"  Symbol       : {result['symbol']}")
    print(f"  Side         : {result['side']}")
    print(f"  Type         : {result['type']}")
    print(f"  Status       : {result['status']}")
    print(f"  Orig Qty     : {result['origQty']}")
    print(f"  Executed Qty : {result['executedQty']}")
    print(f"  Avg Price    : {result['avgPrice']}")
    if result.get("price") and result["price"] != "0":
        print(f"  Limit Price  : {result['price']}")
    if result.get("timeInForce") and result["timeInForce"] != "N/A":
        print(f"  Time-In-Force: {result['timeInForce']}")
    _print_separator()


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    # --- Validate inputs ---
    try:
        params = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        print(f"\n[ERROR] {exc}\n")
        return 1

    _print_order_summary(params)
    logger.info("Validated input: %s", params)

    # --- Initialise client ---
    try:
        client = BinanceTestnetClient()
    except EnvironmentError as exc:
        logger.error("Client init failed: %s", exc)
        print(f"\n[ERROR] {exc}\n")
        return 1

    # --- Place order ---
    try:
        result = place_order(
            client=client,
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
        )
    except Exception as exc:
        logger.error("Order placement failed: %s", exc)
        print(f"\n[FAILED] Order was NOT placed.\nReason: {exc}\n")
        return 1

    _print_order_response(result)
    print(f"  ✓ Order placed successfully! (orderId: {result['orderId']})")
    _print_separator()
    return 0


if __name__ == "__main__":
    sys.exit(main())

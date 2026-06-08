"""
Binance Futures Testnet client wrapper.

Wraps python-binance's Client with:
  - testnet base-URL injection
  - structured request / response logging
  - unified exception handling
"""

from __future__ import annotations

import logging
import os

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.logging_config import setup_logging

logger = setup_logging().getChild("client")

# Testnet base URLs (USDT-M futures)
FUTURES_TESTNET_BASE_URL = "https://testnet.binancefuture.com"


class BinanceTestnetClient:
    """
    Thin wrapper around python-binance's Client configured for
    Binance USDT-M Futures Testnet.
    """

    def __init__(self, api_key: str | None = None, api_secret: str | None = None):
        api_key = api_key or os.getenv("BINANCE_TESTNET_API_KEY", "")
        api_secret = api_secret or os.getenv("BINANCE_TESTNET_API_SECRET", "")

        if not api_key or not api_secret:
            raise EnvironmentError(
                "API credentials not found. "
                "Set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET "
                "in your .env file or environment."
            )

        logger.debug("Initialising Binance Futures Testnet client …")

        self._client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=True,  # activates testnet endpoints in python-binance ≥ 1.0.16
        )

        # Override the futures base URL explicitly so the testnet URL is always used
        self._client.FUTURES_URL = FUTURES_TESTNET_BASE_URL + "/fapi"

        logger.info("Binance Futures Testnet client ready (base: %s)", FUTURES_TESTNET_BASE_URL)

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def place_futures_order(self, **kwargs) -> dict:
        """
        Send a futures order to the testnet and return the raw response dict.

        Accepted kwargs mirror python-binance's futures_create_order():
            symbol, side, type, quantity, price, timeInForce, …

        Raises:
            BinanceAPIException  – exchange rejected the order
            BinanceRequestException – connectivity / HTTP error
            Exception            – unexpected error
        """
        logger.debug("Order request → %s", kwargs)

        try:
            response = self._client.futures_create_order(**kwargs)
            logger.debug("Order response ← %s", response)
            return response

        except BinanceAPIException as exc:
            logger.error(
                "Binance API error [code=%s]: %s",
                exc.code,
                exc.message,
            )
            raise

        except BinanceRequestException as exc:
            logger.error("Network / request error: %s", exc)
            raise

        except Exception as exc:
            logger.exception("Unexpected error while placing order: %s", exc)
            raise

    def get_account_info(self) -> dict:
        """Return futures account information (balance, positions, …)."""
        try:
            info = self._client.futures_account()
            logger.debug("Account info retrieved.")
            return info
        except BinanceAPIException as exc:
            logger.error("Could not fetch account info [%s]: %s", exc.code, exc.message)
            raise

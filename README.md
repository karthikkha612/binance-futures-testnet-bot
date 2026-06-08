# Binance Futures Testnet Trading Bot

A clean, production-ready Python CLI trading bot that places **MARKET** and **LIMIT** orders on the [Binance USDT-M Futures Testnet](https://testnet.binancefuture.com).

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # package marker
│   ├── client.py            # Binance Futures Testnet client wrapper
│   ├── orders.py            # order placement & response parsing logic
│   ├── validators.py        # input validation helpers
│   └── logging_config.py   # rotating file + console logging setup
├── logs/
│   └── trading_bot.log      # auto-created on first run
├── .env                     # API credentials (never commit this)
├── .gitignore
├── cli.py                   # CLI entry point (argparse)
├── requirements.txt
└── README.md
```

---

## Setup

### 1 · Clone / unzip the project

```bash
git clone <your-repo-url> trading_bot
cd trading_bot
```

### 2 · Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3 · Install dependencies

```bash
pip install -r requirements.txt
```

### 4 · Get Binance Futures Testnet credentials

1. Visit <https://testnet.binancefuture.com> and log in (GitHub account required).
2. Go to **API Key** in the top-right menu.
3. Click **Generate** and copy your API key and secret.

### 5 · Configure `.env`

Edit the `.env` file in the project root:

```env
BINANCE_TESTNET_API_KEY=your_key_here
BINANCE_TESTNET_API_SECRET=your_secret_here
```

> ⚠️ **Never commit `.env` to version control.** It is already in `.gitignore`.

---

## How to Run

### Syntax

```
python cli.py --symbol SYMBOL --side SIDE --order_type TYPE --quantity QTY [--price PRICE]
```

| Argument       | Required | Values              | Description                                |
|----------------|----------|---------------------|--------------------------------------------|
| `--symbol`     | ✅        | e.g. `BTCUSDT`     | Futures trading pair                       |
| `--side`       | ✅        | `BUY` / `SELL`     | Order direction                            |
| `--order_type` | ✅        | `MARKET` / `LIMIT` | Order type                                 |
| `--quantity`   | ✅        | positive float      | Quantity in base asset                     |
| `--price`      | LIMIT only | positive float   | Limit price (required for `LIMIT` orders)  |

---

### Example 1 – Market BUY

```bash
python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.001
```

**Output:**

```
────────────────────────────────────────────────────────────
  ORDER REQUEST SUMMARY
────────────────────────────────────────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Order Type : MARKET
  Quantity   : 0.001
────────────────────────────────────────────────────────────
  ORDER RESPONSE
────────────────────────────────────────────────────────────
  Order ID     : 3278641502
  Symbol       : BTCUSDT
  Side         : BUY
  Type         : MARKET
  Status       : FILLED
  Orig Qty     : 0.001
  Executed Qty : 0.001
  Avg Price    : 57423.10
────────────────────────────────────────────────────────────
  ✓ Order placed successfully! (orderId: 3278641502)
────────────────────────────────────────────────────────────
```

---

### Example 2 – Limit SELL

```bash
python cli.py --symbol BTCUSDT --side SELL --order_type LIMIT --quantity 0.001 --price 62000
```

**Output:**

```
────────────────────────────────────────────────────────────
  ORDER REQUEST SUMMARY
────────────────────────────────────────────────────────────
  Symbol     : BTCUSDT
  Side       : SELL
  Order Type : LIMIT
  Quantity   : 0.001
  Price      : 62000.0
────────────────────────────────────────────────────────────
  ORDER RESPONSE
────────────────────────────────────────────────────────────
  Order ID     : 3278651874
  Symbol       : BTCUSDT
  Side         : SELL
  Type         : LIMIT
  Status       : NEW
  Orig Qty     : 0.001
  Executed Qty : 0.000
  Avg Price    : 0.00
  Limit Price  : 62000.00
  Time-In-Force: GTC
────────────────────────────────────────────────────────────
  ✓ Order placed successfully! (orderId: 3278651874)
────────────────────────────────────────────────────────────
```

---

### Example 3 – Market SELL on ETH

```bash
python cli.py --symbol ETHUSDT --side SELL --order_type MARKET --quantity 0.01
```

---

## Logging

All activity is logged to **`logs/trading_bot.log`**:

| Level   | Destination        | Content                                    |
|---------|--------------------|--------------------------------------------|
| DEBUG   | file only          | Full API request & response payloads       |
| INFO    | file + console     | Order summary, result, success/failure     |
| ERROR   | file + console     | Validation errors, API errors, exceptions  |

The log file rotates automatically at **5 MB** (3 backups kept).

---

## Error Handling

| Scenario                        | Behaviour                                            |
|---------------------------------|------------------------------------------------------|
| Missing / invalid symbol        | Validation error printed; exit code 1                |
| Invalid side or order type      | Validation error printed; exit code 1                |
| Non-positive quantity / price   | Validation error printed; exit code 1                |
| LIMIT order without `--price`   | Validation error printed; exit code 1                |
| Missing API credentials in .env | Clear error message; exit code 1                     |
| Binance API rejection (4xx)     | API error code + message logged and printed          |
| Network timeout / connection    | Request exception logged and printed                 |

---

## Assumptions

- The testnet symbol must exist on Binance Futures Testnet (e.g. `BTCUSDT`, `ETHUSDT`).
- Minimum order quantity and price tick-size rules apply; check the exchange for exact limits.
- For MARKET orders, `--price` is accepted but silently ignored (Binance fills at best market price).
- `timeInForce` for LIMIT orders is hardcoded to **GTC** (Good Till Cancelled), which is the standard default.
- The bot targets **USDT-M Futures** (linear contracts) only; COIN-M futures are not supported.

---

## Dependencies

| Package          | Version  | Purpose                              |
|------------------|----------|--------------------------------------|
| `python-binance` | 1.0.19   | Official Binance API client          |
| `python-dotenv`  | 1.0.1    | Load credentials from `.env`         |
| `requests`       | 2.32.3   | HTTP transport (used by python-binance) |

---



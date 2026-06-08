import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv

load_dotenv()

from bot.client import BinanceTestnetClient
from bot.orders import place_order
from bot.validators import validate_all


class TradingBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binance Futures Testnet Bot")
        self.root.geometry("600x700")
        self.root.configure(bg="#111827")
        self.root.resizable(False, False)

        # Header
        tk.Label(
            root,
            text="Binance Futures Testnet",
            bg="#111827",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            root,
            text="Trading Bot",
            bg="#111827",
            fg="#9CA3AF",
            font=("Segoe UI", 11)
        ).pack()

        # Main Card
        card = tk.Frame(
            root,
            bg="#1F2937",
            padx=20,
            pady=20
        )
        card.pack(padx=20, pady=20, fill="x")

        # Style
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Dark.TCombobox",
            fieldbackground="#374151",
            background="#374151",
            foreground="white"
        )

        # Symbol
        tk.Label(
            card,
            text="Symbol",
            bg="#1F2937",
            fg="white"
        ).pack(anchor="w")

        self.symbol_entry = tk.Entry(
            card,
            bg="#374151",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.symbol_entry.insert(0, "BTCUSDT")
        self.symbol_entry.pack(fill="x", pady=(0, 10))

        # Side
        tk.Label(
            card,
            text="Side",
            bg="#1F2937",
            fg="white"
        ).pack(anchor="w")

        self.side_var = tk.StringVar(value="BUY")

        ttk.Combobox(
            card,
            textvariable=self.side_var,
            values=["BUY", "SELL"],
            state="readonly",
            style="Dark.TCombobox"
        ).pack(fill="x", pady=(0, 10))

        # Order Type
        tk.Label(
            card,
            text="Order Type",
            bg="#1F2937",
            fg="white"
        ).pack(anchor="w")

        self.order_type_var = tk.StringVar(value="MARKET")

        ttk.Combobox(
            card,
            textvariable=self.order_type_var,
            values=["MARKET", "LIMIT"],
            state="readonly",
            style="Dark.TCombobox"
        ).pack(fill="x", pady=(0, 10))

        # Quantity
        tk.Label(
            card,
            text="Quantity",
            bg="#1F2937",
            fg="white"
        ).pack(anchor="w")

        self.qty_entry = tk.Entry(
            card,
            bg="#374151",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.qty_entry.insert(0, "0.001")
        self.qty_entry.pack(fill="x", pady=(0, 10))

        # Price
        tk.Label(
            card,
            text="Price (LIMIT only)",
            bg="#1F2937",
            fg="white"
        ).pack(anchor="w")

        self.price_entry = tk.Entry(
            card,
            bg="#374151",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.price_entry.pack(fill="x", pady=(0, 20))

        # Button
        tk.Button(
            card,
            text="Place Order",
            command=self.place_order_ui,
            bg="#10B981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            pady=8
        ).pack(fill="x")

        # Results Card
        result_card = tk.Frame(
            root,
            bg="#1F2937",
            padx=15,
            pady=15
        )
        result_card.pack(
            padx=20,
            pady=(0, 20),
            fill="both",
            expand=True
        )

        tk.Label(
            result_card,
            text="Order Result",
            bg="#1F2937",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        self.result_text = tk.Text(
            result_card,
            bg="#111827",
            fg="white",
            height=15,
            relief="flat"
        )

        self.result_text.pack(fill="both", expand=True, pady=(10, 0))

    def place_order_ui(self):
        try:
            symbol = self.symbol_entry.get()
            side = self.side_var.get()
            order_type = self.order_type_var.get()
            quantity = self.qty_entry.get()

            price = self.price_entry.get().strip()
            if price == "":
                price = None

            validated = validate_all(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )

            client = BinanceTestnetClient()

            result = place_order(
                client=client,
                symbol=validated["symbol"],
                side=validated["side"],
                order_type=validated["order_type"],
                quantity=validated["quantity"],
                price=validated["price"]
            )

            output = (
                f"SUCCESS\n\n"
                f"Order ID      : {result['orderId']}\n"
                f"Symbol        : {result['symbol']}\n"
                f"Side          : {result['side']}\n"
                f"Type          : {result['type']}\n"
                f"Status        : {result['status']}\n"
                f"Executed Qty  : {result['executedQty']}\n"
                f"Average Price : {result['avgPrice']}\n"
            )

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, output)

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotUI(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

# Hardcoded stock prices
PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 2700,
    "AMZN": 3300,
    "MSFT": 310,
    "NFLX": 400,
    "NVDA": 900,
    "META": 350
}

class StockPortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("650x500")
        self.root.resizable(False, False)
        self.portfolio = {}
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Label(self.root, text="STOCK PORTFOLIO TRACKER", font=("Segoe UI", 20, "bold"), fg="#2d3436")
        header.pack(pady=15)
        subtitle = tk.Label(self.root, text="Track your investments with a professional touch!", font=("Segoe UI", 12), fg="#636e72")
        subtitle.pack(pady=2)

        # Stock input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=15)

        tk.Label(input_frame, text="Stock Symbol:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.stock_var = tk.StringVar()
        self.stock_entry = ttk.Combobox(input_frame, textvariable=self.stock_var, values=list(PRICES.keys()), font=("Segoe UI", 12), width=10)
        self.stock_entry.grid(row=0, column=1, padx=5, pady=5)
        self.stock_entry.set(list(PRICES.keys())[0])

        tk.Label(input_frame, text="Quantity:", font=("Segoe UI", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.qty_var = tk.StringVar()
        self.qty_entry = tk.Entry(input_frame, textvariable=self.qty_var, font=("Segoe UI", 12), width=10)
        self.qty_entry.grid(row=0, column=3, padx=5, pady=5)

        add_btn = tk.Button(input_frame, text="Add to Portfolio", font=("Segoe UI", 12, "bold"), bg="#0984e3", fg="white", command=self.add_stock)
        add_btn.grid(row=0, column=4, padx=10, pady=5)

        # Portfolio Table
        self.tree = ttk.Treeview(self.root, columns=("Stock", "Quantity", "Price", "Total"), show="headings", height=8)
        for col in ("Stock", "Quantity", "Price", "Total"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(pady=10)

        # Total investment label
        self.total_label = tk.Label(self.root, text="Total Investment: $0.00", font=("Segoe UI", 14, "bold"), fg="#00b894")
        self.total_label.pack(pady=10)

        # Save button
        save_btn = tk.Button(self.root, text="Save Portfolio", font=("Segoe UI", 12, "bold"), bg="#00b894", fg="white", command=self.save_portfolio)
        save_btn.pack(pady=5)

        # Creative touch: Show available stocks
        stocks_frame = tk.Frame(self.root)
        stocks_frame.pack(pady=5)
        tk.Label(stocks_frame, text="Available Stocks:", font=("Segoe UI", 10, "bold"), fg="#636e72").pack(side=tk.LEFT)
        tk.Label(stocks_frame, text=", ".join([f"{k} (${v})" for k, v in PRICES.items()]), font=("Segoe UI", 10), fg="#636e72").pack(side=tk.LEFT)

    def add_stock(self):
        stock = self.stock_var.get().strip().upper()
        qty_str = self.qty_var.get().strip()
        if stock not in PRICES:
            messagebox.showerror("Error", f"'{stock}' is not in the available stock list.")
            return
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer for quantity.")
            return
        if stock in self.portfolio:
            self.portfolio[stock] += qty
        else:
            self.portfolio[stock] = qty
        self.update_table()
        self.qty_var.set("")

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        total_investment = 0
        for stock, qty in self.portfolio.items():
            price = PRICES[stock]
            total = price * qty
            total_investment += total
            self.tree.insert("", tk.END, values=(stock, qty, price, total))
        self.total_label.config(text=f"Total Investment: ${total_investment:,.2f}")

    def save_portfolio(self):
        if not self.portfolio:
            messagebox.showinfo("Info", "Portfolio is empty. Add stocks before saving.")
            return
        filetypes = [("Text file", "*.txt"), ("CSV file", "*.csv")]
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=filetypes, title="Save Portfolio As")
        if not file:
            return
        total_investment = sum(PRICES[stock] * qty for stock, qty in self.portfolio.items())
        if file.endswith('.txt'):
            with open(file, 'w') as f:
                f.write("STOCK PORTFOLIO SUMMARY\n")
                f.write("="*40 + "\n")
                f.write(f"{'Stock':<10}{'Quantity':<10}{'Price':<10}{'Total':<10}\n")
                for stock, qty in self.portfolio.items():
                    price = PRICES[stock]
                    total = price * qty
                    f.write(f"{stock:<10}{qty:<10}{price:<10}{total:<10}\n")
                f.write("\n" + "-"*40 + "\n")
                f.write(f"TOTAL INVESTMENT: ${total_investment:,.2f}\n")
        elif file.endswith('.csv'):
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Stock", "Quantity", "Price", "Total"])
                for stock, qty in self.portfolio.items():
                    price = PRICES[stock]
                    total = price * qty
                    writer.writerow([stock, qty, price, total])
                writer.writerow([])
                writer.writerow(["TOTAL INVESTMENT", '', '', total_investment])
        messagebox.showinfo("Success", f"Portfolio saved as {file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockPortfolioApp(root)
    root.mainloop() 
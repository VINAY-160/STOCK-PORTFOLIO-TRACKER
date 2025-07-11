import csv
import sys

def print_header():
    print("=" * 60)
    print("{:^60}".format("STOCK PORTFOLIO TRACKER"))
    print("=" * 60)
    print("Welcome! Track your investments with a professional touch.\n")

def get_stock_input(prices):
    portfolio = {}
    while True:
        stock = input("Enter stock symbol (or 'done' to finish): ").strip().upper()
        if stock == 'DONE':
            break
        if stock not in prices:
            print(f"  [!] '{stock}' is not in our price list. Available: {', '.join(prices.keys())}")
            continue
        try:
            qty = int(input(f"  Enter quantity for {stock}: "))
            if qty < 0:
                print("  [!] Quantity cannot be negative.")
                continue
            if stock in portfolio:
                portfolio[stock] += qty
            else:
                portfolio[stock] = qty
        except ValueError:
            print("  [!] Please enter a valid integer for quantity.")
    return portfolio

def display_portfolio(portfolio, prices):
    print("\n" + "-" * 60)
    print("{:^60}".format("YOUR PORTFOLIO SUMMARY"))
    print("-" * 60)
    print(f"{'Stock':<10}{'Quantity':<15}{'Price':<15}{'Total':<15}")
    print("-" * 60)
    total_investment = 0
    for stock, qty in portfolio.items():
        price = prices[stock]
        total = price * qty
        total_investment += total
        print(f"{stock:<10}{qty:<15}{price:<15}{total:<15}")
    print("-" * 60)
    print(f"{'TOTAL INVESTMENT':<40}${total_investment:,.2f}")
    print("-" * 60)
    return total_investment

def save_to_file(portfolio, prices, total_investment):
    while True:
        choice = input("\nWould you like to save your portfolio? (y/n): ").strip().lower()
        if choice == 'n':
            print("Portfolio not saved. Exiting. Thank you!")
            return
        elif choice == 'y':
            filetype = input("Save as (1) .txt or (2) .csv? Enter 1 or 2: ").strip()
            if filetype == '1':
                filename = input("Enter filename (without extension): ").strip() + ".txt"
                with open(filename, 'w') as f:
                    f.write("STOCK PORTFOLIO SUMMARY\n")
                    f.write("="*40 + "\n")
                    f.write(f"{'Stock':<10}{'Quantity':<10}{'Price':<10}{'Total':<10}\n")
                    for stock, qty in portfolio.items():
                        price = prices[stock]
                        total = price * qty
                        f.write(f"{stock:<10}{qty:<10}{price:<10}{total:<10}\n")
                    f.write("\n" + "-"*40 + "\n")
                    f.write(f"TOTAL INVESTMENT: ${total_investment:,.2f}\n")
                print(f"Portfolio saved as {filename}")
                return
            elif filetype == '2':
                filename = input("Enter filename (without extension): ").strip() + ".csv"
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Stock", "Quantity", "Price", "Total"])
                    for stock, qty in portfolio.items():
                        price = prices[stock]
                        total = price * qty
                        writer.writerow([stock, qty, price, total])
                    writer.writerow([])
                    writer.writerow(["TOTAL INVESTMENT", '', '', total_investment])
                print(f"Portfolio saved as {filename}")
                return
            else:
                print("  [!] Invalid choice. Please enter 1 or 2.")
        else:
            print("  [!] Please enter 'y' or 'n'.")

def main():
    prices = {
        "AAPL": 180,
        "TSLA": 250,
        "GOOGL": 2700,
        "AMZN": 3300,
        "MSFT": 310,
        "NFLX": 400,
        "NVDA": 900,
        "META": 350
    }
    print_header()
    print("Available stocks and prices:")
    for stock, price in prices.items():
        print(f"  {stock}: ${price}")
    print("\nLet's build your portfolio!")
    portfolio = get_stock_input(prices)
    if not portfolio:
        print("No stocks entered. Exiting.")
        sys.exit()
    total_investment = display_portfolio(portfolio, prices)
    save_to_file(portfolio, prices, total_investment)
    print("\nThank you for using the Stock Portfolio Tracker! Have a great day.")

if __name__ == "__main__":
    main() 
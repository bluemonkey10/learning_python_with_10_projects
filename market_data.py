import yfinance as yf
from datetime import datetime
from snapshot import Snapshot
from snapshot_operations import save_snapshots

tickers = ["AAPL", "AMZN", "GOOG", "META", "NFLX"]

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    current_price = stock.info.get("currentPrice", "Data not found")
    return current_price

def view_current_prices():
    print("\n===CURRENT FAANG STOCK PRICES===\n")

    date_stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"Today's Date: {date_stamp}\n")


    for ticker in tickers:
        stock = yf.Ticker(ticker)
        current_price = get_stock_price(ticker)

        history = stock.history(period="5d")

        # Get yesterday's closing price 
        yesterday_close = history['Close'].iloc[-2] if len(history) >= 2 else None
        

        percent_change = ((current_price - yesterday_close) / yesterday_close) * 100 if yesterday_close else 0
        if percent_change > 0:
            print(f"{ticker} -> ${current_price:.2f} (▲ {percent_change:.2f}%)")
        else:
            print(f"{ticker} -> ${current_price:.2f} (▼ {abs(percent_change):.2f}%)") if percent_change < 0 else print(f"{ticker} -> ${current_price:.2f} (No change)")

def save_market_snapshot(snapshots):
    snapshot_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    stocks_and_prices = {}

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice", "Data not found")
        stocks_and_prices[ticker] = current_price
    
    snapshot = Snapshot(snapshot_date, stocks_and_prices)
    snapshot.display_snapshot()

    print("\nSaving snapshot...")

    snapshots.append(snapshot)
    save_snapshots(snapshots, "snapshots.json")


def view_historical_data(snapshots):
    print("\n===RECORDED SNAPSHOTS OF FAANG PRICES===\n")
    if not snapshots:
        print("No snapshots recorded yet.")
    
    for snapshot in snapshots:
        snapshot.display_snapshot()


def search_historical_data(snapshots):
    ticker_input = input("\nSearch for a specific stock, e.g. AAPL: ").upper()

    print(f"\n==={ticker_input} PRICE HISTORY===\n")

    found = False
    for snapshot in snapshots:
        if ticker_input in snapshot.stocks_and_prices:
            found = True
            price = snapshot.stocks_and_prices[ticker_input]
            print(f"{snapshot.date} -> ${price:.2f}")
    
    if not found:
        print(f"\nNo historical data found for {ticker_input}.\n")

def portfolio_simulator(snapshots):
    print("\n===PORTFOLIO SIMULATOR===\n")

    print("\nShares owned:\n")

    total_value = 0.0

    for ticker in tickers:
        while True:
            try:
                shares = int(input(f"{ticker}: "))
                if shares < 0:
                    print("Please enter a positive number of shares.")
                    continue
                total_value += (shares * get_stock_price(ticker))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number of shares.")
    
    print(f"\nTotal Portfolio Value: ${total_value:.2f}\n")


def exit_program(snapshots):
    save_snapshots(snapshots, "snapshots.json")
    print("Saving data and exiting the program...")


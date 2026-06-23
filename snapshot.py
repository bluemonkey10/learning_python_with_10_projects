class Snapshot:
    def __init__(self, date, stocks_and_prices):
        self.date = date
        self.stocks_and_prices = stocks_and_prices
    
    def display_snapshot(self):
        print(f"\nDate: {self.date}\n")
        
        for stock, price in self.stocks_and_prices.items():
            print(f"{stock} -> ${price:.2f}")

import yfinance as yf
import csv
from datetime import datetime

class StockData:
    def __init__(self):
        pass
    
    def get_historical_prices(self, symbol, period="1mo", save_to_csv=False):

        valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "ytd", "max"]
        
        if period not in valid_periods:
            raise ValueError("Invalid period. Please choose from: {}".format(", ".join(valid_periods)))
        
        # Create a Ticker object
        stock = yf.Ticker(symbol)
        
        # Get historical price data of the stock
        historical_data = stock.history(period=period)

        historical_data.columns = historical_data.columns.astype(str)
        
        if save_to_csv:
            # Get today's date
            today_date = datetime.today().strftime('%Y-%m-%d')
        
            # Generate file name
            file_name = f"{symbol}_{period}_{today_date}.csv"
        
            # Write data to CSV file
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
            
                # Write header with 'Date' as the first column
                header = ['Date'] + historical_data.columns.tolist()
                writer.writerow(header)
            
                # Write data rows
                for index, row in historical_data.iterrows():
                    writer.writerow([index.strftime('%Y-%m-%d')] + row.tolist())
        
        return historical_data

if __name__ == "__main__":
    stock_data = StockData()
    symbol = "AAPL"  # Stock symbol
    period = "1mo"   # Time period
    stock_data.get_historical_prices(symbol, period, False)

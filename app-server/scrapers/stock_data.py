import yfinance as yf
import csv
from datetime import datetime

class StockData:
    def __init__(self):
        pass
    
    def get_historical_prices(self, symbol, start_time, end_time, save_to_csv=False):
        stock = yf.Ticker(symbol)
        historical_data = stock.history(start=start_time, end=end_time)
        historical_data.columns = historical_data.columns.astype(str)
        
        if save_to_csv:
            file_name = f"{symbol}-PRICE-{start_time}-{end_time}.csv"
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                header = ['Date'] + historical_data.columns.tolist()
                writer.writerow(header)
                for index, row in historical_data.iterrows():
                    writer.writerow([index.strftime('%Y-%m-%d')] + row.tolist())
        
        return historical_data

if __name__ == "__main__":
    stock_data = StockData()
    symbol = "BABA"
    start_time = '2024-01-01'
    end_time = '2024-05-01'
    historical_data = stock_data.get_historical_prices(symbol, start_time, end_time, True)
    print(historical_data)


import yfinance as yf
import csv
from datetime import datetime

class StockData:
    def __init__(self):
        pass
    
    def get_historical_prices(self, symbol, start_time, end_time, save_to_csv=False):
        stock = yf.Ticker(symbol)
        historical_data = stock.history(start=start_time, end=end_time, interval="30m")
        historical_data.columns = historical_data.columns.astype(str)
        historical_data = historical_data.iloc[::-1]
        
        end_time_last_1 = (datetime.strptime(end_time, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        if save_to_csv:
            file_name = f"{symbol}-PRICE-60DAYS-{start_time}-{end_time_last_1}.csv"
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                header = ['Date'] + historical_data.columns.tolist()
                writer.writerow(header)
                for index, row in historical_data.iterrows():
                    writer.writerow([index.strftime('%Y-%m-%d %H:%M:%S')] + row.tolist())
        
        return historical_data

from datetime import timedelta

if __name__ == "__main__":
    end_time = datetime.now().strftime('%Y-%m-%d')
    start_time = (datetime.now() - timedelta(days=59)).strftime('%Y-%m-%d')
    symbol = "TSLA"

    stock_data = StockData()
    historical_data = stock_data.get_historical_prices(symbol, start_time, end_time, True)
    print(historical_data)


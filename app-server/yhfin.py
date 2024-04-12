import yfinance as yf
import json

def get_ticker_details(symbol):
    msft = yf.Ticker(symbol)
    msft_data = msft.info
    combined_data = {
        'symbol': symbol,
        'shortName': msft_data.get('shortName', ''), 
        'longName': msft_data.get('longName', '')
    }
    # result = json.dumps(combined_data)
    return combined_data

if __name__ == "__main__":
    print(get_ticker_details('AAPL'))
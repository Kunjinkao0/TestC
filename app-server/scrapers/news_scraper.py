import pandas as pd
import json
from datetime import datetime, timedelta
import finnhub
import json
import news_analysis

finnhub_client = finnhub.Client(api_key='co21o61r01qvggedq3dgco21o61r01qvggedq3e0')

class NewsData:
    def __init__(self):
        pass
    
    def get_company_news(self, symbol, start_date, end_date, analysis=False):
        company_news = self.call_finhub_api(symbol, start_date, end_date)
        refined = [
            {
                'id': item['id'],
                'datetime': datetime.fromtimestamp(item['datetime']).strftime('%Y-%m-%d %H:%M:%S'),
                'impact': 'n/a',
                'headline': item['headline'],
                'summary': item['summary'],
            } for item in company_news]
        if analysis: 
            print('Data prepared, pending to analysis.')
            analysor = news_analysis.Analysor()
            refined = analysor.analysis_news(refined)

        file_name = f"{symbol}-{start_date}-{end_date}.csv"
        df = pd.DataFrame(refined)
        df.to_csv(file_name, index=False)

        return True
    
    def call_finhub_api(self, symbol, start_date, end_date):
        full_data = []

        last_date = end_date
        while last_date >= start_date:
            print(f"Get news data [{symbol}] from[{start_date}] to [{last_date}]")
            response = finnhub_client.company_news(symbol, 
                                                   _from=start_date,
                                                   to=last_date)
            full_data.extend(response)
            last_item_date = datetime.fromtimestamp(response[-1]['datetime'])
            last_date = (last_item_date - timedelta(days=1)).strftime('%Y-%m-%d')

        return full_data
    
if __name__ == "__main__":
    news_data = NewsData()
    symbol = "NVDA"
    start_date = "2024-01-01"
    end_date = "2024-05-01"
    default_news = news_data.get_company_news(symbol, start_date, end_date, False)

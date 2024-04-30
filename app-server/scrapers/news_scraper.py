import yfinance as yf
import pandas as pd
import json
from datetime import datetime

import finnhub
import requests
import json
finnhub_client = finnhub.Client(api_key="co21o61r01qvggedq3dgco21o61r01qvggedq3e0")

class NewsData:
    def __init__(self):
        pass
    
    def get_default_news(self, symbol, start_date, end_date):
        company_news = finnhub_client.company_news(symbol, _from=start_date, to=end_date)
        refined = [
            {
                'id': item['id'],
                'datetime': datetime.utcfromtimestamp(item['datetime']).strftime('%Y-%m-%d %H:%M:%S'),
                'impact': 'n/a',
                'headline': item['headline'],
                'summary': item['summary'],
            } for item in company_news]
        # refined = refined[:12] # test
        # chunks = [refined[i:i+5] for i in range(0, len(refined), 5)]

        # for chunk in chunks:
        #     print(f"processing {chunk[0]['datetime']} - {chunk[-1]['datetime']}")
        #     dataset = json.dumps(chunk)
        #     result = self.analysis_news(dataset)
        #     self.combine_impact(result, chunk)

        # # flat map
        # chunks = [item for sublist in chunks for item in sublist]
        # refined = chunks

        file_name = f"{symbol}-{start_date}-{end_date}.csv"
        df = pd.DataFrame(refined)
        df.to_csv(file_name, index=False)

        json_data = json.dumps(refined)


        return json_data
    
    def combine_impact(self, json_data, dict_data):
        json_id_impact = {entry['id']: entry['impact'] for entry in json_data}
        
        for entry in dict_data:
            entry_id = entry['id']
            if entry_id in json_id_impact:
                entry['impact'] = json_id_impact[entry_id]
        
        return dict_data
    
    def analysis_news(self, dataset): 
        prompt = f"""
            Return a JSON array containing objects with the news ID and an index ranging from 0 to 1, where 0 represents a highly negative impact and 1 represents a highly positive impact.
            Remember, you don't need to explain anything just return me the json.
            Requirements:
            1. Check the 'headline' and 'summary' to determine if the news will influence the stock price.
            2. Consider the importance and timing of the news; assess whether it will have a short-term or long-term impact.
            3. Evaluate the Fear and Greed Index associated with the news and its potential effects.
            News dataset:
            ````
            {dataset}
            ````
        """
        # print(prompt)
        endpoint = "http://localhost:11434/api/generate"
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "options": {
                "seed": 123,
                "temperature": 0
            },
            "stream": False
        }
        llm_res = requests.post(endpoint, json=payload)
        response_str = llm_res.json()['response']

        try:
            return json.loads(response_str)
        except json.JSONDecodeError:
            return []

if __name__ == "__main__":
    news_data = NewsData()
    symbol = "TSLA"
    start_date = "2022-01-01"
    end_date = "2024-01-01"
    default_news = news_data.get_default_news(symbol, start_date, end_date)

    # with open('dataset1.json', 'r') as file:
    #     dataset = json.load(file)
    # news_data = NewsData()
    # result = news_data.analysis_news(dataset)
    # print(result)


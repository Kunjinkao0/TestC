import requests
import json

class Analysor:
    def __init__(self):
        pass

    def analysis_news(self, dataset, chunk_size=5):
        print(f"Total news: [{len(dataset)}] ")
        # do chunk to avoid large dataset
        chunks = [dataset[i:i+chunk_size] for i in range(0, len(dataset), chunk_size)]
        print(f"Chunk into {len(chunks)} parts per request.")
        print('--- --- ---')
        for index, chunk in enumerate(chunks):
            print(f"processing {index * chunk_size + 1}-{min((index + 1) * chunk_size, len(dataset))}")
            json_data = json.dumps(chunk)
            result = self.call_llm(json_data)
            self.combine_impact(chunk, result)

        # flat map
        refined = [item for sublist in chunks for item in sublist]
        return refined

    def call_llm(self, datasetJson): 
        prompt = f"""
            Return a JSON array containing objects with the news ID and an index ranging from 0 to 1, where 0 represents a highly negative impact and 1 represents a highly positive impact.
            Remember, you don't need to explain anything just return the json.
            Requirements:
            1. Check the 'headline' and 'summary' to determine if the news will influence the stock price.
            2. Consider the importance and timing of the news; assess whether it will have a short-term or long-term impact.
            3. Evaluate the Fear and Greed Index associated with the news and its potential effects.
            News dataset:
            ````
            {datasetJson}
            ````
        """
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
        
    def combine_impact(self, dataset, analysis_result):
        json_id_impact = {entry['id']: entry['impact'] for entry in analysis_result}
        
        for entry in dataset:
            entry_id = entry['id']
            if entry_id in json_id_impact:
                entry['impact'] = json_id_impact[entry_id]

        return dataset

import datetime  # Import datetime module to use current date

if __name__ == '__main__':
    news_analysis = Analysor()

    with open('dataset.json', 'r') as file:
        dataset = json.load(file)
    # dataset = dataset[:7] # test
    result = news_analysis.analysis_news(dataset)
    
    current_date = datetime.datetime.now()
    with open(f"parsed{current_date.strftime('%H:%M:%S')}.json", "w") as json_file:
        json_file.write(json.dumps(result))
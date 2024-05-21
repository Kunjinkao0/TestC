import requests
import json
import pandas as pd
import random
import os

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
            start_index = index * chunk_size
            end_index = min((index + 1) * chunk_size, len(dataset)) - 1
            print(f"processing {start_index}-{end_index}")
            result = self.call_llm(chunk)
            self.combine_impact(chunk, result)
            self.append_to_csv('temp.csv', chunk)

        # flat map
        refined = [item for sublist in chunks for item in sublist]
        return refined

    def call_llm(self, dataset): 
        # Make prompts
        prompts = []
        for item in dataset:
            prompt = f'''Instruction: What is the sentiment of this news? Please choose an answer from {{negative/neutral/positive}}\nInput: {item["headline"]}\nAnswer: '''
            prompts.append(prompt)
        # prompts = [item.replace('\xa0', '').replace('\n', '') for item in prompts]
        # Generate results
        # tokens = tokenizer(prompts, return_tensors='pt', padding=True, max_length=512)
        # res = model.generate(**tokens, max_length=512)
        # res_sentences = [tokenizer.decode(i) for i in res]
        # out_text = [o.split("Answer: ")[1].strip().replace("</s>", "") for o in res_sentences]
        # return out_text
        result = ['negative', 'neutral', 'positive']
        results = [random.choice(result) for _ in prompts]
        return results

    def call_llm0(self, datasetJson): 
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
        except Exception as e:
            ids = [item["id"] for item in json.loads(datasetJson)]
            print('Error:', e, 'IDs:', ids)
            print('Response:', response_str)
            return []

    def combine_impact0(self, dataset, analysis_result):
        json_id_impact = {entry['id']: entry['impact'] for entry in analysis_result}
        
        for entry in dataset:
            entry_id = entry['id']
            if entry_id in json_id_impact:
                entry['impact'] = json_id_impact[entry_id]

        return dataset
    
    def combine_impact(self, dataset, analysis_result):
        for index, entry in enumerate(dataset):
            entry['impact'] = analysis_result[index]

        return dataset
    
    def append_to_csv(self, file_path, rows_to_append):
        if not os.path.isfile(file_path):
            header = ['id', 'datetime', 'impact', 'headline', 'summary']
            pd.DataFrame(columns=header).to_csv(file_path, mode='w', header=True, index=False)
        
        # Use 'a' mode to append to the file
        with open(file_path, 'a') as f:
            # Create a CSV writer object
            for row in rows_to_append:
                pd.DataFrame([row]).to_csv(f, header=False, index=False)

import datetime  # Import datetime module to use current date

if __name__ == '__main__':
    news_analysis = Analysor()

    stock_data = pd.read_csv('/Users/willi/Workspace/fidchart/app-server/scrapers/AAPL-2024-01-01-2024-05-01.csv')
    dataset = stock_data.to_dict('records')
    dataset = dataset[:13]
    result = news_analysis.analysis_news(dataset)

    # with open('dataset.json', 'r') as file:
    #     dataset = json.load(file)
    # # dataset = dataset[:7] # test
    # result = news_analysis.analysis_news(dataset)
    
    # current_date = datetime.datetime.now()
    # with open(f"parsed{current_date.strftime('%H:%M:%S')}.json", "w") as json_file:
    #     json_file.write(json.dumps(result))
# import pandas as pd
import datetime

class NewsScraper:
    def __init__(self):
        pass
    
    def scrape_website(self, dateRange, website):
        test_json = {
            "test": 123,
            "abc": 123
        }
        # df = pd.DataFrame(test_json)
        current_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"news{current_stamp}.csv"
        # df.to_csv(f"../dataset/{file_name}", index=False)
        # df.to_csv('../dataset/news.csv', index=False)

        return f'{file_name}'
    
    def parse_content(self, content):
        pass

if __name__ == '__main__':
    scraper = NewsScraper()
    result = scraper.scrape_website('2020-01-01', 'https://www.google.com')
    print(result)

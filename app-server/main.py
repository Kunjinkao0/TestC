from flask import Flask, Blueprint, request
from scrapers.news_scraper import *
import json

app = Flask(__name__)
api_pre = Blueprint('api', __name__, url_prefix='/api')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@api_pre.route('/news-fetch', methods=['GET'])
def scrape_data():
    scraper_params = request.args.to_dict()
    scraper = NewsScraper()
    result = scraper.scrape_website(scraper_params['dateRange'], scraper_params['website'])
    parsed_result = json.dumps({"code": 1, "data": result})
    return parsed_result

app.register_blueprint(api_pre)

if __name__ == '__main__':
    app.run()
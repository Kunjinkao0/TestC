from flask import Flask, Blueprint, request, jsonify, render_template
from scrapers.news_scraper import *
from yhfin import *
import json

app = Flask(__name__)
app.template_folder = 'public'
app.static_folder = 'public'
api_pre = Blueprint('api', __name__, url_prefix='/api')

def format_response(response_data, message=None, code=1):
    return jsonify({"code": code, "data": response_data, "msg": message})

def res_formatter(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return format_response(result)
        except Exception as e:
            print(e)
            return format_response(None, str(e), code=0), 500
    return wrapper

@app.route('/')
def index():
    return render_template("index.html")

@api_pre.route('/news-fetch', methods=['GET'], endpoint="news-fetch")
@res_formatter
def scrape_data():
    scraper_params = request.args.to_dict()
    scraper = NewsScraper()
    result = scraper.scrape_website(scraper_params['dateRange'], scraper_params['website'])
    return result

@api_pre.route('/ticker-detail', methods=['GET'], endpoint="tickers")
@res_formatter
def get_stock_info():
    symbol = request.args.get('symbol')
    result = get_ticker_details(symbol)
    return result

@api_pre.route('/price-info', methods=['GET'], endpoint="price-info")
@res_formatter
def get_stock_info():
    symbol = request.args.get('symbol')
    with open('./dataset/aapl-c.json', 'r') as f:
        data = json.load(f)
        return data

app.register_blueprint(api_pre)
if __name__ == '__main__':
    app.run()
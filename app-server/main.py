from flask import Flask, Blueprint, request, jsonify, render_template
from scrapers.news_scraper import *

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
            return format_response(None, str(e), code=0), 500
    return wrapper

@app.route('/')
def index():
    return render_template("index.html")

@api_pre.route('/news-fetch', methods=['GET'])
@res_formatter
def scrape_data():
    scraper_params = request.args.to_dict()
    scraper = NewsScraper()
    result = scraper.scrape_website(scraper_params['dateRange'], scraper_params['website'])
    return result

app.register_blueprint(api_pre)

if __name__ == '__main__':
    app.run()
import crochet

crochet.setup()  # initialize crochet

import json
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scraper import ShopeeSpiderJSON
import os
import urllib.parse
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = 'myflaskshopeescraperjson'
crawl_runner = CrawlerRunner()  # requires the Twisted reactor to run
output_data = []  # store output
scrape_in_progress = False
scrape_complete = False
input_query = False  # set True after input query
start_url = ''


class InputProductForm(FlaskForm):
    product_query = StringField('Product Label:', validators=[DataRequired(), Length(min=3, max=100, message='Text Length: 3-100 Characters')])
    submit = SubmitField('Scrape')


@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'Shopi V1'
    form = InputProductForm()

    if form.validate_on_submit():
        kw = form.product_query.data
        keyword = urllib.parse.quote(kw, safe='')
        global start_url
        start_url = 'https://shopee.co.id/api/v2/search_items/?by=price&keyword={}&limit=20&newest=0&order=asc&page_type=search&version=2'.format(
            keyword)

        global input_query
        input_query = True

        global scrape_in_progress
        scrape_in_progress = True

        global output_data
        output_data = []

        # Remove existing output file
        if os.path.exists("output/outputjson.json"):
            os.remove("output/outputjson.json")

        return redirect(url_for('scrape'))  # Passing to the Scrape function

    else:
        return render_template('index.html', title=title, form=form)


@app.route('/scrape')
def scrape():
    title = 'Scraping Progress'
    """
    Process scrape data
    """
    global scrape_in_progress
    global scrape_complete
    global input_query

    if scrape_in_progress and input_query:
        # scrape_in_progress = True
        global output_data

        # log
        scrape_logging()

        # start the crawler and execute a callback when complete
        scrape_with_crochet(start_url, output_data)
        input_query = False  # set False after scraping in progress
        return render_template('scrape-progress.html', title=title)
    elif scrape_complete:
        return render_template('scrape-complete.html', title=title)
    else:
        return render_template('scrape-nojob.html', title=title)


@app.route('/result')
def get_result():
    title = 'Result'
    """
    Get the result only if a spider has result
    """
    global scrape_complete

    if scrape_complete and not output_data:
        return render_template('scrape-error.html', title=title)
    elif scrape_complete:
        return json.dumps(output_data)
    elif scrape_in_progress:
        return render_template('scrape-progress.html', title=title)
    else:
        return render_template('scrape-nojob.html', title=title)


@app.route('/about')
def about():
    title = 'About'
    return render_template('about.html', title=title)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@crochet.run_in_reactor
def scrape_with_crochet(_query, output):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(ShopeeSpiderJSON, query=_query, output_data=output)
    eventual.addCallback(finished_scrape)


# This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))


def finished_scrape(null):
    """
    """
    global scrape_complete
    scrape_complete = True


def scrape_logging():
    # configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log/scrapinglog.txt',
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        level=logging.WARNING
    )


if __name__ == '__main__':
    app.run(debug=True)

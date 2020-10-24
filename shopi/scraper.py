import scrapy
import json
# import urllib.parse
import datetime
import pytz
# from urllib.parse import parse_qs
# from scrapy.crawler import CrawlerProcess


# def query_search(query='mainan / bola'):
#     keyword = urllib.parse.quote(query, safe='')
#     return keyword

# def output_(urlstart='https://shopee.co.id/api/v2/search_items/?by=price&keyword=mainan%20%2F%20bola&limit=20&newest=0&order=asc&page_type=search&version=2'):
#     parsed = urllib.parse.urlparse(urlstart)
#     kwd = parse_qs(parsed.query)['keyword'][0]
#     kywd = urllib.parse.quote(kwd, safe='')
#     jkt_tz = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).date()
#     return 'output-{}-{}'.format(jkt_tz, kywd)


class ShopeeSpiderJSON(scrapy.Spider):
    # spider name
    name = 'my_shopee_spider_json'
    allowed_domains = ['shopee.co.id']

    start_url = ''

    # base URL
    # keyword = query_search()
    # start_url = 'https://shopee.co.id/api/v2/search_items/?by=price&keyword={}&limit=20&newest=0&order=asc&page_type=search&version=2'.format('mainan')

    # custom headers
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    #     'Referer': 'https://shopee.co.id/search?keyword=mainan&order=asc&page=0&sortBy=price',
    # }

    # parsed = urllib.parse.urlparse(url)
    # kwd = parse_qs(parsed.query)['keyword'][0]
    # kywd = urllib.parse.quote(kwd, safe='')

    # jkt_tz = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).date()
    # output_file = 'output/output-{}.json'.format(jkt_tz)
    # output_file = 'output/output-{}-{}.json'.format(jkt_tz, kywd)

    # custom settings
    custom_settings = {
        # uncomment below settings to slow down the scraper
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1,
        # 'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Referer': 'https://shopee.co.id/search?keyword=mainan&order=asc&page=0&sortBy=price',
        },
        # 'FEEDS': {output_file: {'format': 'json',
        #                      }
        #           },
        # 'LOG_ENABLED': False,
        # 'LOG_LEVEL': 'WARNING',
        # 'LOG_FILE': 'WARNING_LOG.txt',
    }

    def __init__(self, url_query='', **kwargs):  # The query variable will have the input URL.
        self.start_url = url_query
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        jsonresponse = json.loads(response.body.decode('utf-8'))
        for item in jsonresponse['items']:
            image = 'https://cf.shopee.co.id/file/' + item['image'] + '_tn'  # _tn for thumbnail
            yield {
                # 'image_url': image,
                # 'ads_keyword': item['ads_keyword'],
                'itemid': item['itemid'],
                'name': item['name'],
                'price': int(item['price'] / 100000),
                # 'price_before_discount': int(item['price_before_discount'] / 100000),
                # 'price_max': int(item['price_max'] / 100000),
                # 'price_max_before_discount': int(item['price_max_before_discount'] / 100000),
                # 'price_min': int(item['price_min'] / 100000),
                # 'price_min_before_discount': int(item['price_min_before_discount'] / 100000),
                # 'raw_discount': item['raw_discount'],
                # 'sold': item['sold'],
                # 'shopid': item['shopid'],
                # 'shop_location': item['shop_location'],
            }


# main driver
# if __name__ == '__main__':
#     starturl = 'https://shopee.co.id/api/v2/search_items/?by=price&keyword=mainan%20%2F%20bola&limit=20&newest=0&order=asc&page_type=search&version=2'
#     fpath = output_(starturl).replace('%', '-')
#     filepath = sanitize_filename(fpath)
#     filepath = 'output/{}.json'.format(filepath)
#
#     # run spider
#     process = CrawlerProcess(settings={
#         "FEEDS": {
#             filepath: {"format": "json"},
#         },
#     })
#
#     process.crawl(ShopeeSpiderJSON, start_url=starturl)
#     process.start()

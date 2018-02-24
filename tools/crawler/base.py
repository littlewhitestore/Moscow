import scrapy
import logging
from scrapy import signals


urls = {}

class BaseSpider(scrapy.Spider):

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_error, signal=signals.spider_error)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        return spider

    def spider_opened(spider):
        spider_name = spider.name
        urls[spider_name] = {
            "failed_url": [],
            "success_url": [],
        }

    def spider_closed(spider, reason):
        spider_name = spider.name
        message = '''
========================================
SPIDER: {spider}
TOTAL_COUNT: {total_count}
SUCCESS_COUNT: {success_count}
FAILED_COUNT: {failed_count}
FAILED: {failed_urls}
========================================
        '''.format(**{
            'spider': spider_name,
            'total_count': len(urls[spider_name]['success_url']) + len(urls[spider_name]['failed_url']), 
            'success_count': len(urls[spider_name]['success_url']), 
            'failed_count': len(urls[spider_name]['failed_url']),
            'failed_urls': "\r\n" + "\r\n".join(urls[spider_name]['failed_url']), 
        })
        logging.info(message) 

    def spider_error(failure, response, spider):
        spider_name = spider.name
        urls[spider_name]['failed_url'].append(response.request.url)

    def item_scraped(item, response, spider):
        spider_name = spider.name
        urls[spider_name]['success_url'].append(response.request.url)

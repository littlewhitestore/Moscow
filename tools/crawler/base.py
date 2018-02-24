import scrapy
import logging
from scrapy import signals


urls = {}

class BaseSpider(scrapy.Spider):

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_error, signal=signals.spider_error)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.request_scheduled, signal=signals.request_scheduled)
        return spider

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
            'total_count': len(urls[spider_name]['total_url']), 
            'success_count': len(urls[spider_name]['total_url']) - len(urls[spider_name]['failed_url']), 
            'failed_count': len(urls[spider_name]['failed_url']),
            'failed_urls': "\r\n" + "\r\n".join(urls[spider_name]['failed_url']), 
        })
        logging.info(message) 

    def spider_error(failure, response, spider):
        spider_name = spider.name
        if not urls.__contains__(spider_name):
            urls[spider_name] = {
                "failed_url": [],
                "total_url": [],
            }
        urls[spider_name]['failed_url'].append(response.request.url)

    def request_scheduled(request, spider):
        spider_name = spider.name
        if not urls.__contains__(spider_name):
            urls[spider_name] = {
                "failed_url": [],
                "total_url": [],
            }

        urls[spider_name]['total_url'].append(request.url)

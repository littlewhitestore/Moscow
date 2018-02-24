import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

from tools.crawler.alibaba.spider import Spider as SpiderAlibaba


SUPPLY_ALIBABA = '1688'
SPIDERS = {
    SUPPLY_ALIBABA: SpiderAlibaba
}


def crawl(supply):
    configure_logging(install_root_handler=False)
    logging.basicConfig(level=logging.INFO)

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    spider = SPIDERS[supply]
    process.crawl(spider)
    process.start()


# PYTHONPATH ="${PYTHONPATH}:{MOSCOW_PROJECT_PATH}"
# export PYTHONPATH

# run it in command
# cd tools/
# python crawl.py

if __name__ == "__main__":
    crawl(SUPPLY_ALIBABA)

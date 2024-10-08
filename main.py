from dotenv import load_dotenv
import os
from scrapy.crawler import CrawlerProcess

from amazonscraper.amazonscraper.spiders.amazonspider import AmazonspiderSpider

load_dotenv()

# from scrapy.utils.project import get_project_settings
# process = CrawlerProcess(settings={settings})

keyword = input("What is your input? ")

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "data_%(time)s.json": {
                "format": "json",
                "overwrite": False,
            }
        },
        "ITEM_PIPELINES": {
            "amazonscraper.amazonscraper.pipelines.AmazonscraperDataCleanPipeline": 300,
        },
        "ROBOTSTXT_OBEY": "False",
        "DOWNLOADER_MIDDLEWARES": {
            "amazonscraper.amazonscraper.middlewares.ScrapeOpsFakeBrowserHeadersMiddleware": 400
        },
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "FEED_EXPORT_ENCODING": "utf-8",
        "SCRAPEOPS_API_KEY": os.environ.get("SECRET_KEY"),
        "SCRAPEOPS_FAKE_HEADERS_ENABLED": "True",
    }
)

process.crawl(AmazonspiderSpider, keyword=keyword)
process.start()

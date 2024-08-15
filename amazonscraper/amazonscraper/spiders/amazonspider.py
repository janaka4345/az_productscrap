import scrapy
from amazonscraper.items import AmazonscraperItem


class AmazonspiderSpider(scrapy.Spider):

    name = "amazonspider"
    allowed_domains = ["amazon.com", "scrapeops.io"]
    scrapeops_commen_url = "https://proxy.scrapeops.io/v1/?api_key=*******************&url=https://www.amazon.com"
    commen_url_direct = "https://www.amazon.com"

    def __init__(self, keyword=None, jobid=None, *args, **kwargs):
        super(AmazonspiderSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.jobid = jobid

    def start_requests(self):
        amazon_search_url = f"{self.commen_url_direct}/s?k={self.keyword}"
        yield scrapy.Request(
            url=amazon_search_url,
            callback=self.all_products_divs,
        )

    def all_products_divs(self, response):
        all_products = response.xpath('//div[contains(@data-asin,"B")]')
        product_item = AmazonscraperItem()
        for product in all_products:
            product_item["title"] = product.xpath(".//h2/a/span/text()").get()
            product_item["image"] = product.xpath(
                './/div/div[contains(@class,"aok-relative")]//img/@src'
            ).get()
            product_item["price"] = product.xpath(
                './/div/a/span/span[contains(@class,"a-offscreen")]/text()'
            ).get()
            product_item["product_link"] = product.xpath(".//h2/a/@href").get()
            product_item["stars"] = product.xpath(".//i/span/text()").get()
            product_item["bought_in_past_month"] = product.xpath(
                './/div/span[contains(text(),"bought")]/text()'
            ).get()

            yield product_item

        next_page = response.xpath(
            '//span[contains(@class,"s-pagination-strip")]/a[last()]/@href'
        ).get()

        if next_page is not None:
            next_page_url = f"{self.commen_url_direct}{next_page}"

            yield response.follow(next_page_url, callback=self.all_products_divs)

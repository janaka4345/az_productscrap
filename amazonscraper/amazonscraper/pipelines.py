# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

base_url = "https://www.amazon.com"


class AmazonscraperDataCleanPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # remove null items
        if adapter.get("title") == None:
            raise DropItem("null item found")

        # convert price string to float
        if adapter.get("price"):
            price = adapter.get("price")
            new_price = price.replace("$", "")
            float_price = float(new_price)
            adapter["price"] = float_price

        # product link in full
        if adapter.get("product_link"):
            product_link = adapter.get("product_link")
            new_product_link = f"{base_url}{product_link}"
            adapter["product_link"] = new_product_link

        # convert start to numbers
        if adapter.get("stars"):
            stars_list = adapter.get("stars").split()
            star_rating = float(stars_list[0])
            adapter["stars"] = star_rating

        # convert start to numbers
        if adapter.get("bought_in_past_month"):
            bought_in_past_month = adapter.get("bought_in_past_month")
            new_bought_in_past_month = (
                bought_in_past_month.replace("bought in past month", "")
                .replace("+", "")
                .replace("K", "000")
                .strip()
            )
            new_bought_in_past_month_number = int(new_bought_in_past_month)
            adapter["bought_in_past_month"] = new_bought_in_past_month_number

        return item

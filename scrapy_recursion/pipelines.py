"""pipelines."""
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import tldextract
import os
from datetime import datetime
# from urllib.parse import urlparse


class ScrapyRecursionPipeline:
    """ScrapyRecursionPipeline."""

    def process_item(self, item, spider):
        """process_item."""
        return item


class LinksPipeline:
    """LinksPipeline."""

    def open_spider(self, spider):
        """open_spider."""
        self.visited_urls = set()
        # start_url = "".join(spider.start_urls)
        # domain = tldextract.extract(start_url).domain
        # date = "".join(str(datetime.now().date()).split('-')[1:])
        fid = spider.fid
        time_ = spider.time_
        now = datetime.now()
        date = now.strftime("%m%d")
        folder_name = f"test_{date}/recursion_{time_}/"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        self.file = open(f'test_{date}/recursion_{time_}/recursion_{fid}.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        """close_spider."""
        self.file.close()

    def process_item(self, item, spider):
        """process_item."""
        if item["url"] not in self.visited_urls:
            if tldextract.extract(item["url"]).domain == tldextract.extract("".join(spider.start_urls)).domain:
                self.visited_urls.add(item["url"])  # 將新 URL 添加到集合中
                self.file.write(item["url"] + '\n')  # 將 URL 寫入文件
        return item

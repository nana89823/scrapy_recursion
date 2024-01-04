# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import tldextract
from urllib.parse import urlparse


class ScrapyRecursionPipeline:
    def process_item(self, item, spider):
        return item

class LinksPipeline:

    def open_spider(self, spider):
        self.visited_urls = set()
        start_url = "".join(spider.start_urls)
        domain = tldextract.extract(start_url).domain
        self.file = open(f'{domain}_uniqueLinks.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item["url"] not in self.visited_urls:
            if urlparse(item["url"]).netloc == urlparse("".join(spider.start_urls)).netloc:
                self.visited_urls.add(item["url"])  # 將新 URL 添加到集合中
                self.file.write(item["url"] + '\n')  # 將 URL 寫入文件
        return item
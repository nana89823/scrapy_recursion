"""Main."""
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from .. import items
from urllib.parse import urlparse, urljoin
import logging

logger = logging.getLogger("mycustomlogger")  # 用python 的logging,這行為log取名


class MySpider(CrawlSpider):
    """MySpiser."""

    name = "recursion"
    allowed_domains = [
        "news.pts.org.tw",
        "www.don1don.com",
        "www.everydayobject.us",
        "www.ettoday.net",
        "www.dramaqueen.com.tw",
        "applianceinsight.com.tw",
        "easylife.tw",
        "e-creative.media",
        "ahui3c.com",
        "anntw.com",
        "www.ltn.com.tw",
        "www.businesstoday.com.tw",
        "www.businessweekly.com.tw",
        "csr.cw.com.tw",
        "news.cts.com.tw",
        "www.msn.com",
        "www.mirrormedia.mg",
        "www.cna.com.tw",
        "cnews.com.tw",
        "www.coolloud.org.tw",
        "www.cool3c.com",
        "www.cool-style.com.tw",
        "dailyview.tw",
        "www.thenewslens.com",
        "www.twreporter.org",
        "news.ttv.com.tw",
        "fongnews.net",
        "www.fiftyplus.com.tw",
        "fgblog.fashionguide.com.tw",
        "findnewstoday.net",
        "flipermag.com",
        "news.ebc.net.tw",
        "www.storm.mg",
        "udn.com",
    ]
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_recursion.middlewares.PerStartUrlTimeoutMiddleware": 543
        },
        "ITEM_PIPELINES": {"scrapy_recursion.pipelines.LinksPipeline": 500},
        "START_URL_TIMEOUT": 600,
    }
    rules = [Rule(LinkExtractor(), callback="parse_page", follow=True)]
    count = 0

    def __init__(self, *args, **kwargs):
        """init."""
        super().__init__(*args, **kwargs)
        self.url = kwargs.get("url")
        self.fid = kwargs.get("fid")
        self.time_ = kwargs.get("time")
        self.start_urls = [self.url]

    def parse_page(self, response):
        """parse_page."""
        links = LinkExtractor().extract_links(response)
        for link in links:
            self.count += 1
            item = items.urlItem()
            # item["url"] = link.url
            href = link.url.split("#")[0].lower().rstrip("/")
            try:
                parsed_href = urlparse(href)
            except Exception:
                continue
            if parsed_href.netloc:
                if not parsed_href.scheme:
                    continue
                if parsed_href.netloc != urlparse(response.url).netloc:
                    continue
            else:
                href = urljoin(response.url, href)
            item["url"] = href.split("?")[0]
            yield item

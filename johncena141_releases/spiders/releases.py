import dateparser
import re
import scrapy
import os

proxy_domain = os.environ["PROXY_URL_FOR_1337X"]
releases_domain = "1337x.to"
uploader_username = "johncena141"


class ReleasesSpider(scrapy.Spider):
    name = "releases"
    allowed_domains = [f"{proxy_domain}"]
    start_urls = [f"https://{proxy_domain}/{uploader_username}-torrents/1/"]
    scrape_pages = []

    def parse(self, response):
        last_page = (
            response.css(".last > a:nth-child(1)::attr(href)").get().split("/")[-2]
        )
        self.scrape_pages = [
            f"https://{proxy_domain}/{uploader_username}-torrents/{i}/"
            for i in range(1, int(last_page) + 1)
        ]
        for url in self.scrape_pages:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        for item in response.css("td.coll-1.name a:nth-child(2)"):
            torrent_url = f"https://{proxy_domain}{item.css('a::attr(href)').get()}"
            yield scrapy.Request(torrent_url, callback=self.parse_torrent)

    def parse_torrent(self, response):
        entry = {
            "name": (
                re.search(
                    "Download (.+?) Torrent | 1337x",
                    response.css("head > title::text").get(),
                ).group(1)
            ).strip(),
            "seeds": response.css(".seeds::text").get(),
            "leeches": response.css(".leeches::text").get(),
            "date": dateparser.parse(
                response.css(
                    "ul.list:nth-child(3) > li:nth-child(3) > span:nth-child(2)::text"
                ).get(),
                settings={"TO_TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": True},
            ).strftime("%a, %d %b %Y %H:%M:%S %z"),
            "size": response.css(
                ".no-top-radius > .clearfix > ul:nth-child(2) > li:nth-child(4) > span:nth-child(2)::text"
            ).get(),
            "url": response.url.replace(proxy_domain, releases_domain),
            "magnet": response.css(
                ".dropdown-menu li:nth-child(4) a::attr(href)"
            ).get(),
            "hash": response.css(".infohash-box p span::text").get(),
        }
        yield entry

import dateparser
import re
import scrapy

uploader_username = "johncena141"


class ReleasesSpider(scrapy.Spider):
    name = "releases"
    allowed_domains = ["1337x.to"]
    start_urls = [f"https://1337x.to/user/{uploader_username}/"]
    current_page = 0

    def parse(self, response):
        last_page = int(
            response.css(".last > a:nth-child(1)::attr(href)").get().split("/")[-2]
        )
        while self.current_page <= last_page:
            yield response.follow(
                f"/{uploader_username}-torrents/{self.current_page + 1}/",
                callback=self.parse_list,
            )

    def parse_list(self, response):
        self.current_page = int(response.url.split("/")[-2])
        torrents = response.css("td.coll-1.name a:nth-child(2)::attr(href)").getall()
        for item in reversed(torrents):
            yield response.follow(item, callback=self.parse_torrent)

    def parse_torrent(self, response):
        def process_description(desc):
            x = desc.replace('src="/images/profile-load.svg" ', "")
            x = x.replace("data-original=", "src=")
            x = x.replace(' class="img-responsive descrimg lazy"', "")
            return x

        def process_date(date):
            x = dateparser.parse(
                date, settings={"TO_TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": True}
            )
            x = x.strftime("%a, %d %b %Y %H:%M:%S %z")
            return x

        entry = {
            "id": response.url.split("/")[-3],
            "name": (
                re.search(
                    "Download (.+?) Torrent | 1337x",
                    response.css("title::text").get(),
                ).group(1)
            ).strip(),
            "seeds": response.css(".seeds::text").get(),
            "leeches": response.css(".leeches::text").get(),
            "date": process_date(
                response.css(
                    "ul.list:nth-child(3) > li:nth-child(3) > span:nth-child(2)::text"
                ).get()
            ),
            "size": response.css(
                ".no-top-radius > .clearfix > ul:nth-child(2) > li:nth-child(4) > span:nth-child(2)::text"
            ).get(),
            "url": response.url,
            "magnet": response.css(
                ".dropdown-menu li:nth-child(4) a::attr(href)"
            ).get(),
            "hash": response.css(".infohash-box p span::text").get(),
            "description": process_description(response.css("#description").get()),
        }
        yield entry

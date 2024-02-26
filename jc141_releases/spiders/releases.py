import scrapy
from ..items import Jc141ReleaseLoader, Jc141ReleaseItem

# username of the uploader
uploader_username = "johncena141"


class ReleasesSpider(scrapy.Spider):
    name = "releases"
    allowed_domains = ["l337xdarkkaqfwzntnfk5bmoaroivtl6xsbatabvlb52umg6v3ch44yd.onion"]
    start_urls = [f"http://{allowed_domains[0]}/user/{uploader_username}/"]
    current_page = 1  # 1337x works in strange ways..

    def parse(self, response):
        """Main parser"""

        # Fetching the last page number
        last_page = int(
            response.css(".last > a:nth-child(1)::attr(href)").get().split("/")[-2]
        )

        # HACK: Manually set total page number, for dev
        # last_page = 1

        while self.current_page <= last_page:
            yield response.follow(
                f"/{uploader_username}-torrents/{self.current_page}/",
                callback=self.parse_list,
            )
            self.current_page += 1  # update page number

    def parse_list(self, response):
        """Parses list of torrents on the page"""

        self.current_page = int(response.url.split("/")[-2])
        torrents = response.css("td.coll-1.name a:nth-child(2)::attr(href)").getall()
        for item in reversed(
            torrents
        ):  # for some reason, we need to have this reversed to work as intended
            yield response.follow(item, callback=self.parse_torrent)

    def parse_torrent(self, response):
        """Parses the required data from the full torrent page"""

        release = Jc141ReleaseLoader(item=Jc141ReleaseItem(), response=response)

        # actual ID will be assigned by item loader
        release.add_value("torrent_id", response.url)

        release.add_css("name", "title::text", re="Download (.+?) Torrent | 1337x")
        release.add_value("url", response.url)

        release.add_css(
            "upload_date",
            "ul.list:nth-child(3) > li:nth-child(3) > span:nth-child(2)::text",
        )
        release.add_css(
            "checked_date",
            "ul.list:nth-child(3) > li:nth-child(2) > span:nth-child(2)::text",
        )

        release.add_css("description", "#description")
        release.add_css(
            "total_size",
            ".no-top-radius > .clearfix > ul:nth-child(2) > li:nth-child(4) > span:nth-child(2)::text",
        )

        release.add_css("seeders", ".seeds::text")
        release.add_css("leechers", ".leeches::text")

        release.add_css("info_hash", ".infohash-box p span::text")
        release.add_css("magnet_link", ".dropdown-menu li:nth-child(4) a::attr(href)")

        # yield the processed item
        yield release.load_item()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader

from itemloaders.processors import TakeFirst, MapCompose

import re
import dateparser


class Jc141ReleaseLoader(ItemLoader):
    """Item Loader"""

    def get_absolute_date(date):
        """converts relative dates to absolute dates"""
        parsed_date = dateparser.parse(
            date, settings={"TO_TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": True}
        )
        date_string = parsed_date.strftime("%a, %d %b %Y %H:%M:%S %z")
        return date_string

    default_input_processor = MapCompose(str.strip)

    torrent_id_in = MapCompose(lambda x: x.split("/")[-3], str.strip)

    checked_date_in = MapCompose(get_absolute_date, str.strip)
    upload_date_in = MapCompose(get_absolute_date, str.strip)

    # Replace the onion domain with the public domain
    url_in = MapCompose(lambda x: x.replace(x.split("/")[-5], "1337x.to"), str.strip)

    default_output_processor = TakeFirst()


class Jc141ReleaseItem(scrapy.Item):
    """Item Model"""

    torrent_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    upload_date = scrapy.Field()
    checked_date = scrapy.Field()
    description = scrapy.Field()
    total_size = scrapy.Field()
    seeders = scrapy.Field()
    leechers = scrapy.Field()
    info_hash = scrapy.Field()
    magnet_link = scrapy.Field()

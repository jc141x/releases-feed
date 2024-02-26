# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem

# HTML Minifier
import minify_html_onepass

# Pony ORM for better DB handling syntax
from pony.orm import *

# Date and Time Handling
from datetime import datetime


class Jc141ReleaseDescriptionSanitizationPipeline:
    """Sanitize the description HTML (remove 1337x specific cruft)"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        description = adapter.get("description", None)
        if description is None:
            raise DropItem(f"No description in {item}")
        else:
            # Remove 1337x's placeholder spinner
            description = description.replace('src="/images/profile-load.svg" ', "")

            # Change attribute for image source
            description = description.replace("data-original=", "src=")

            # Switch to native lazy loading images
            description = description.replace(
                ' class="img-responsive descrimg lazy"', ' loading="lazy"'
            )

            # Strip unused attributes from the outer div tag
            description = description.replace(
                '<div role="tabpanel" class="tab-pane active" id="description">',
                "<div>",
            )

            # Strip outer p tag
            description = description.replace("<p>", "")
            description = description.replace("</p>", "")

            # better a href attributes
            description = description.replace(
                'target="_blank"', 'target="_blank" rel="noopener noreferrer"'
            )

            adapter["description"] = minify_html_onepass.minify(description)

            return item


class Jc141ReleaseSQLitePipeline:
    """Maintain a SQLite DB for deduplication and fixing issues"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Initializing SQLite DB and ORM
        db = Database()
        db.bind(provider="sqlite", filename="../releases.sqlite", create_db=True)

        # Releases "schema" for SQLite db
        # Make sure this matches the "Jc141ReleaseItem" class in items.py
        class Jc141ReleaseDBEntity(db.Entity):
            torrent_id = PrimaryKey(int)
            name = Required(str)
            url = Required(str)
            upload_date = Required(datetime)
            checked_date = Required(datetime)
            description = Required(LongUnicode)
            total_size = Required(str)
            seeders = Required(int)
            leechers = Required(int)
            info_hash = Required(str)
            magnet_link = Required(LongUnicode)

        # Mapping entities to the database tables
        db.generate_mapping(create_tables=True)

        # keeping datetime formats handy
        rss_datetime_format = "%a, %d %b %Y %H:%M:%S %Z"
        sqlite_datetime_format = "%Y-%m-%d %H:%M:%S%z"

        # Meat and Potatoes
        with db_session:
            # New release, add directly to DB
            if not Jc141ReleaseDBEntity.exists(torrent_id=adapter.get("torrent_id")):
                new_release = Jc141ReleaseDBEntity(
                    torrent_id=adapter.get("torrent_id"),
                    name=adapter.get("name"),
                    url=adapter.get("url"),
                    upload_date=datetime.strptime(
                        adapter.get("upload_date"), rss_datetime_format
                    ),
                    checked_date=datetime.strptime(
                        adapter.get("checked_date"), rss_datetime_format
                    ),
                    description=adapter.get("description"),
                    total_size=adapter.get("total_size"),
                    seeders=adapter.get("seeders"),
                    leechers=adapter.get("leechers"),
                    info_hash=adapter.get("info_hash"),
                    magnet_link=adapter.get("magnet_link"),
                )
            else:
                # Existing release, make sure the upload date does not change
                existing_release = Jc141ReleaseDBEntity[adapter.get("torrent_id")]
                if datetime.strptime(
                    existing_release.upload_date, sqlite_datetime_format
                ) <= datetime.strptime(adapter.get("upload_date"), rss_datetime_format):
                    adapter["upload_date"] = datetime.strptime(
                        existing_release.upload_date, sqlite_datetime_format
                    ).strftime(rss_datetime_format)

        return item

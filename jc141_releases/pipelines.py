# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem

# HTML Minifier
import minify_html

# Pony ORM for better DB handling syntax
from pony.converting import str2datetime
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

            # Strip away the weird spaces stuff
            description = description.replace("                      ", "")

            # Switch to native lazy loading images, also make it responsive
            description = description.replace(
                'class="img-responsive descrimg lazy"',
                'loading="lazy" style="width: 100%; height: auto"',
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

            adapter["description"] = minify_html.minify(
                description,
                minify_css=True,
                keep_spaces_between_attributes=True,
                remove_processing_instructions=True,
            )

            return item


class Jc141ReleaseSQLitePipeline:
    """Maintain a SQLite DB for deduplication and fixing issues"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Initializing SQLite DB and ORM
        db = Database()
        db.bind(provider="sqlite", filename="../releases.db", create_db=True)

        # Releases "schema" for SQLite db
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
        datetime_format_rss = "%a, %d %b %Y %H:%M:%S%z"
        datetime_format_sqlite = "%Y-%m-%d %H:%M:%S%z"

        # Meat and Potatoes
        with db_session:
            if not Jc141ReleaseDBEntity.exists(torrent_id=adapter.get("torrent_id")):
                # New release, add directly to DB
                new_release = Jc141ReleaseDBEntity(
                    torrent_id=adapter.get("torrent_id"),
                    name=adapter.get("name"),
                    url=adapter.get("url"),
                    upload_date=datetime.strptime(
                        adapter.get("upload_date"), datetime_format_rss
                    ),
                    checked_date=datetime.strptime(
                        adapter.get("checked_date"), datetime_format_rss
                    ),
                    description=adapter.get("description"),
                    total_size=adapter.get("total_size"),
                    seeders=adapter.get("seeders"),
                    leechers=adapter.get("leechers"),
                    info_hash=adapter.get("info_hash"),
                    magnet_link=adapter.get("magnet_link"),
                )
            else:
                # Existing release, make sure the upload date does not drift
                # ... unless there's a change in the description or title (edge case)
                existing_release = Jc141ReleaseDBEntity[adapter.get("torrent_id")]

                # Update the "last checked" value in the DB
                existing_release.set(
                    checked_date=datetime.strptime(
                        adapter.get("checked_date"), datetime_format_rss
                    )
                )

                # Update the "seeders" and "leechers" value in the DB
                existing_release.set(
                    seeders=adapter.get("seeders"),
                    leechers=adapter.get("leechers"),
                )

                if (existing_release.name != adapter.get("name")) or (
                    existing_release.description != adapter.get("description")
                ):
                    # Update the changes in the DB
                    existing_release.set(
                        name=adapter.get("name"),
                        url=adapter.get("url"),  # URL Changes with Name?
                        upload_date=datetime.strptime(
                            adapter.get("upload_date"), datetime_format_rss
                        ),
                        description=adapter.get("description"),
                    )
                else:
                    if datetime.strptime(
                        existing_release.upload_date, datetime_format_sqlite
                    ) <= datetime.strptime(
                        adapter.get("upload_date"), datetime_format_rss
                    ):
                        adapter["upload_date"] = datetime.strptime(
                            existing_release.upload_date, datetime_format_sqlite
                        ).strftime(datetime_format_rss)
        return item

<div align="center">
  <h1>Releases</h1>
</div>

<p align="center">
  All our releases scraped into various machine readable files (CSV, JSON, RSS)
</p>
<br>

### Recommended RSS client: [Fluent Reader](https://github.com/yang991178/fluent-reader)

 - The open externally button adds the torrents to your torrent client.

#### Keeping the reader up to date.

Previously we recommended Raven Reader but found out that it caches old articles/torrents and shows them without any mention that it does not match the current RSS listing anymore. This is not acceptable to our unique torrent per game practice which ensures a focus on quality.

Fluent Reader is a bit better by providing the user the option to clean up old articles in preferences. This enables users to use the search feature without finding duplicates. This action needs to be done manually so not quite ideal. We are looking for readers that handle this kind of requirements better.

## Links
* RSS feed: (add this one to RSS clients)
```
https://github.com/jc141x/releases-feed/releases/download/feeds/releases.rss
```
* JSON:
```
https://github.com/jc141x/releases-feed/releases/download/feeds/releases.json
```
* CSV:
```
https://github.com/jc141x/releases-feed/releases/download/feeds/releases.csv
```
* SQLite DB: (this is an archive and may contain deprecated data)
```
https://github.com/jc141x/releases-feed/releases/download/feeds/releases.sqlite
```

## Details

* an Actions cronjob will run the script and upload the feeds to the ["Releases"](https://github.com/jc141x/releases-feed/releases/latest) every 8 hours.

* In case 1337x.to goes down or scraping fails, you can check the latest ["Releases"](https://github.com/jc141x/releases-feed/releases/latest) for working files.

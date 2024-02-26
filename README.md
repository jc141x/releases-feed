<div align="center">
  <h1>Releases</h1>
  <p>All our releases scraped into various machine readable files (CSV, JSON, RSS, etc..)</p>
</div>

<br/>

### Recommended RSS clients:
- [Fluent Reader](https://github.com/yang991178/fluent-reader) (Desktop)
  - The open externally button adds the torrents to your torrent client.

#### Keeping the reader up to date.

Previously we recommended Raven Reader but found out that it caches old articles/torrents and shows them without any mention that it does not match the current RSS listing anymore. This is not acceptable to our unique torrent per game practice which ensures a focus on quality.

Fluent Reader is a bit better by providing the user the option to clean up old articles in preferences. This enables users to use the search feature without finding duplicates. This action needs to be done manually so not quite ideal. We are looking for readers that handle this kind of requirements better.

## Links
* RSS feed: (this one goes in your RSS reader apps)
```
https://github.com/jc141x/releases-feed/releases/download/feeds/releases.rss
```
* JSON:
```
https://github.com/jc141x/releases-feed/releases/download/feeds/releases.json
```
* JSON Lines: (JSON, [but better?](https://jsonlines.org/))
```
https://github.com/jc141x/releases-feed/releases/download/feeds/releases.jsonl
```
* CSV:
```
https://github.com/jc141x/releases-feed/releases/download/feeds/releases.csv
```
* SQLite DB: (used for archival purposes, contains superseded releases)
```
https://github.com/jc141x/releases-feed/releases/download/feeds/releases.sqlite
```

## Details

* an Actions cronjob will run the script and upload the feeds to the ["Releases"][releases] every 8 hours.

* In case 1337x.to goes down or scraping fails, you can check the latest ["Releases"][releases] for working files.

[releases]: https://github.com/jc141x/releases-feed/releases/latest

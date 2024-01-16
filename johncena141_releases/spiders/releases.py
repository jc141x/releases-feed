import random
import re
from time import time

import dateparser
import scrapy

uploader_username = "johncena141"


class ReleasesSpider(scrapy.Spider):
    name = "releases"

    allowed_domains = [
        "1337x.amazingspiderman.workers.dev",
        "1337x.antarctica.workers.dev",
        "1337x.april1424.workers.dev",
        "1337x.a-s.workers.dev",
        "1337x.a-t.workers.dev",
        "1337x.a-u.workers.dev",
        "1337x.a-v.workers.dev",
        "1337x.a-w.workers.dev",
        "1337x.a-y.workers.dev",
        "1337x.b-a.workers.dev",
        "1337x.b-c.workers.dev",
        "1337x.b-f.workers.dev",
        "1337x.bhadoo786.workers.dev",
        "1337x.b-h.workers.dev",
        "1337x.b-i.workers.dev",
        "1337x.b-j.workers.dev",
        "1337x.b-l.workers.dev",
        "1337x.b-m.workers.dev",
        "1337x.b-n.workers.dev",
        "1337x.b-o.workers.dev",
        "1337x.b-p.workers.dev",
        "1337x.b-q.workers.dev",
        "1337x.b-r.workers.dev",
        "1337x.b-s.workers.dev",
        "1337x.b-v.workers.dev",
        "1337x.b-w.workers.dev",
        "1337x.cdn-7.workers.dev",
        "1337x.cdn-8.workers.dev",
        "1337x.chatgpts1.workers.dev",
        "1337x.chennaicdn.workers.dev",
        "1337x.cloudflare-stream.workers.dev",
        "1337x.donnapaulson.workers.dev",
        "1337x.europecdn.workers.dev",
        "1337x.harveyspector.workers.dev",
        "1337x.hashaaliyah.workers.dev",
        "1337x.hashaaron.workers.dev",
        "1337x.hashabrahamlincoln.workers.dev",
        "1337x.hashadele.workers.dev",
        "1337x.hashadrienbrody.workers.dev",
        "1337x.hashaishwaryarai.workers.dev",
        "1337x.hashalberteinstein.workers.dev",
        "1337x.hashalfredhitchcock.workers.dev",
        "1337x.hashamsterdam.workers.dev",
        "1337x.hashangelababy.workers.dev",
        "1337x.hashangelinajolie.workers.dev",
        "1337x.hashanniehall.workers.dev",
        "1337x.hashantonio.workers.dev",
        "1337x.hasharnoldschwarzenegger.workers.dev",
        "1337x.hasharthurmiller.workers.dev",
        "1337x.hasharthur.workers.dev",
        "1337x.hashashleytisdale.workers.dev",
        "1337x.hashashley.workers.dev",
        "1337x.hashatlanta.workers.dev",
        "1337x.hashaustin.workers.dev",
        "1337x.hashavamax.workers.dev",
        "1337x.hashava.workers.dev",
        "1337x.hashbenaffleck.workers.dev",
        "1337x.hashberlin.workers.dev",
        "1337x.hashbeyonce.workers.dev",
        "1337x.hashbillclinton.workers.dev",
        "1337x.hashblakelively.workers.dev",
        "1337x.hashblake.workers.dev",
        "1337x.hashbollywoods.workers.dev",
        "1337x.hashbollywood.workers.dev",
        "1337x.hashboston.workers.dev",
        "1337x.hashbradpitts.workers.dev",
        "1337x.hashbradpitt.workers.dev",
        "1337x.hashbrandon.workers.dev",
        "1337x.hashbrooklyn.workers.dev",
        "1337x.hashbrunomars.workers.dev",
        "1337x.hashbryancranston.workers.dev",
        "1337x.hashbryan.workers.dev",
        "1337x.hashcaitlin.workers.dev",
        "1337x.hashcaitlynjenners.workers.dev",
        "1337x.hashcaitlynjenner.workers.dev",
        "1337x.hashcamerondiaz.workers.dev",
        "1337x.hashcameron.workers.dev",
        "1337x.hashcarrieunderwood.workers.dev",
        "1337x.hashcarrie.workers.dev",
        "1337x.hashcatherinezetajones.workers.dev",
        "1337x.hashcharliechaplin.workers.dev",
        "1337x.hashcher.workers.dev",
        "1337x.hashchicago.workers.dev",
        "1337x.hashchristianbale.workers.dev",
        "1337x.hashchristophernolan.workers.dev",
        "1337x.hashcristianoronaldo.workers.dev",
        "1337x.hashdavegrohls.workers.dev",
        "1337x.hashdavegrohl.workers.dev",
        "1337x.hashdemilovato.workers.dev",
        "1337x.hashdisney.workers.dev",
        "1337x.hashdwaynejohnson.workers.dev",
        "1337x.hashelizabethtaylor.workers.dev",
        "1337x.hashelonmusks.workers.dev",
        "1337x.hashelonmusk.workers.dev",
        "1337x.hasheltonjohn.workers.dev",
        "1337x.hashemilyblunt.workers.dev",
        "1337x.hasheminem.workers.dev",
        "1337x.hashemmawatsons.workers.dev",
        "1337x.hashemmawatson.workers.dev",
        "1337x.hashfrance.workers.dev",
        "1337x.hashfranksinatrs.workers.dev",
        "1337x.hashfranksinatr.workers.dev",
        "1337x.hashfreddiemercury.workers.dev",
        "1337x.hashgabrielgarciamarquez.workers.dev",
        "1337x.hashgeorgeclooney.workers.dev",
        "1337x.hashgeorgewashington.workers.dev",
        "1337x.hashgigihadidbhadoo.workers.dev",
        "1337x.hashgretathumberg.workers.dev",
        "1337x.hashhalleberry.workers.dev",
        "1337x.hashharrystyles.workers.dev",
        "1337x.hashhawaii.workers.dev",
        "1337x.hashheathledger.workers.dev",
        "1337x.hashhillaryclinton.workers.dev",
        "1337x.hashhindubhadoo.workers.dev",
        "1337x.hashhollywoods.workers.dev",
        "1337x.hashhollywood.workers.dev",
        "1337x.hashhowiemandel.workers.dev",
        "1337x.hashindia.workers.dev",
        "1337x.hashireneadler.workers.dev",
        "1337x.hashistanbul.workers.dev",
        "1337x.hashjadensmith.workers.dev",
        "1337x.hashjasonstathams.workers.dev",
        "1337x.hashjasonstatham.workers.dev",
        "1337x.hashjenniferlawrences.workers.dev",
        "1337x.hashjenniferlawrence.workers.dev",
        "1337x.hashjenniferlopez.workers.dev",
        "1337x.hashjennyslate.workers.dev",
        "1337x.hashjimcarey.workers.dev",
        "1337x.hashjustinbieber.workers.dev",
        "1337x.hashkeanureeves.workers.dev",
        "1337x.hashkendalljenner.workers.dev",
        "1337x.hashkimkardashian.workers.dev",
        "1337x.hashkyliejenner.workers.dev",
        "1337x.hashladygaga.workers.dev",
        "1337x.hashleonardodicaprio.workers.dev",
        "1337x.hashliamhemsworth.workers.dev",
        "1337x.hashlindsaylohan.workers.dev",
        "1337x.hashlondon.workers.dev",
        "1337x.hashlosangeles.workers.dev",
        "1337x.hashmerylstreep.workers.dev",
        "1337x.hashmichaeljackson.workers.dev",
        "1337x.hashmichelleobama.workers.dev",
        "1337x.hashmileycyrus.workers.dev",
        "1337x.hashmonicabellucci.workers.dev",
        "1337x.hashmorganfreeman.workers.dev",
        "1337x.hashmumbai.workers.dev",
        "1337x.hashneilarmstrong.workers.dev",
        "1337x.hashnewyork.workers.dev",
        "1337x.hashoprahwinfrey.workers.dev",
        "1337x.hashorlandobloom.workers.dev",
        "1337x.hashpamelaanderson.workers.dev",
        "1337x.hashparishilton.workers.dev",
        "1337x.hashparis.workers.dev",
        "1337x.hashprince.workers.dev",
        "1337x.hashqueenelizabethii.workers.dev",
        "1337x.hashqueenelizabeth.workers.dev",
        "1337x.hashrachelmcadams.workers.dev",
        "1337x.hashrobertdowneyjr.workers.dev",
        "1337x.hashrobinwilliams.workers.dev",
        "1337x.hashrome.workers.dev",
        "1337x.hashryanreynolds.workers.dev",
        "1337x.hashsalmahayek.workers.dev",
        "1337x.hashsanfrancisco.workers.dev",
        "1337x.hashscarlettjohansson.workers.dev",
        "1337x.hashseattle.workers.dev",
        "1337x.hashserenawilliams.workers.dev",
        "1337x.hashstevejobs.workers.dev",
        "1337x.hashstevenspielberg.workers.dev",
        "1337x.hashsydney.workers.dev",
        "1337x.hashtaylorswifts.workers.dev",
        "1337x.hashtaylorswift.workers.dev",
        "1337x.hashtokyo.workers.dev",
        "1337x.hashtomcruise.workers.dev",
        "1337x.hashtomhanks.workers.dev",
        "1337x.hashtoronto.workers.dev",
        "1337x.hashtravisbarker.workers.dev",
        "1337x.hashvladimirputin.workers.dev",
        "1337x.hashwashingtondc.workers.dev",
        "1337x.hashwaynerooney.workers.dev",
        "1337x.hashwillsmiths.workers.dev",
        "1337x.hashwillsmith.workers.dev",
        "1337x.hashwizkhalifa.workers.dev",
        "1337x.hashyahyaabdulmateeniibbhadoo.workers.dev",
        "1337x.hashzaynmalik.workers.dev",
        "1337x.i7cpu.workers.dev",
        "1337x.indiacdn.workers.dev",
        "1337x.indiadownloadserver3.workers.dev",
        "1337x.jammu.workers.dev",
        "1337x.kashmircdn.workers.dev",
        "1337x.lordshiva.workers.dev",
        "1337x.louislitt.workers.dev",
        "1337x.megha.workers.dev",
        "1337x.mikeross.workers.dev",
        "1337x.northkorea.workers.dev",
        "1337x.pakistancdn.workers.dev",
        "1337x.patrickjane.workers.dev",
        "1337x.piya.workers.dev",
        "1337x.resourcekey.workers.dev",
        "1337x.sharingpurposes.workers.dev",
        "1337x.southkoreacdn.workers.dev",
        "1337x.spstream1.workers.dev",
    ]

    start_urls = [f"https://{random.choice(allowed_domains)}/{int(time() * 1000)}/user/{uploader_username}/"]
    current_page = 0

    def parse(self, response):
        last_page = int(
            response.css(".last > a:nth-child(1)::attr(href)").get().split("/")[-2].strip()
        )

        while self.current_page <= last_page:
            yield response.follow(
                f"https://{random.choice(self.allowed_domains)}/{int(time() * 1000)}/{uploader_username}-torrents/{self.current_page + 1}/",
                callback=self.parse_list,
            )

    def parse_list(self, response):
        self.current_page = int(response.url.split("/")[-2])
        torrents = response.css("td.coll-1.name a:nth-child(2)::attr(href)").getall()
        for item in reversed(torrents):
            yield response.follow(f"https:{item}", callback=self.parse_torrent)

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
            "seeds": int(response.css(".seeds::text").get()),
            "leeches": int(response.css(".leeches::text").get()),
            "date": process_date(
                response.css(
                    "ul.list:nth-child(3) > li:nth-child(3) > span:nth-child(2)::text"
                ).get()
            ),
            "size": response.css(
                ".no-top-radius > .clearfix > ul:nth-child(2) > li:nth-child(4) > span:nth-child(2)::text"
            ).get(),
            "url": re.sub('https://1337x.+.workers.dev/(\d+)/', 'https://1337x.to/', response.url),
            "magnet": response.css(
                ".dropdown-menu li:nth-child(4) a::attr(href)"
            ).get().replace('[1337x.HashHackers.Com]', ''),
            "hash": response.css(".infohash-box p span::text").get(),
            "description": process_description(response.css("#description").get()),
        }
        yield entry

# -*- coding: utf-8 -*-
import scrapy
import re
import urlparse
import json
import urllib.request
from whjCrawler.items import WhjcrawlerItem
from whjCrawler.InvertedIndex import InvertedIndexvc

RESULTS_DIRECTORY = "CrawlerResults"


class WhjspiderSpider(scrapy.Spider):
    name = 'whjSpider'
    allowed_domains = ["lyle.smu.edu", "s2.smu.edu"]
    start_urls = ['http://lyle.smu.edu/~fmoore/']

    broken_links_status_list = [404]

    IMAGE_URL = []
    URL = []
    BROKEN_LINKS = []
    OUTGOING_LINKS = []
    DOCUMENT_LINKS = []

    doc_id = 0

    def parse(self, response):

        allUrl = response.url

        # All images
        image_links = response.xpath('//img/@src').extract()
        for image in image_links:
            item = WhjcrawlerItem()

            # get the full url with relative url
            if image.startswith('/'):
                image = '/'.join(allUrl.split('/')[0:3]) + image
            elif image.startswith('http') or image.startswith('www'):
                image = image
            else:
                if allUrl.endswith('/'):
                    image = allUrl + image
                else:
                    image = '/'.join(allUrl.split('/')[0:-1]) + '/' + image

            # eliminate duplicate
            if image not in self.IMAGE_URL:
                self.IMAGE_URL.append(image)
                self.URL.append(image)
                item['link'] = image
                yield item
            else:
                pass

        # All other links
        links = response.xpath('//a/@href').extract()

        # if response status is not 200 and the url will be a broken link
        if response.status == 200:
            for link_sel in links:
                item = WhjcrawlerItem()

                if link_sel.startswith('/'):
                    link_sel = '/'.join(allUrl.split('/')[0:3]) + link_sel
                elif link_sel.startswith('http') or link_sel.startswith('www'):
                    link_sel = link_sel
                else:
                    if allUrl.endswith('/'):
                        link_sel = allUrl + link_sel
                    else:
                        link_sel = '/'.join(allUrl.split('/')[0:-1]) + '/' + link_sel

                # judge if the url is in http://lyle.smu.edu/~fmoore (eliminate outgoing links)
                if re.match(r'^http(s?)://(lyle|s2)\.smu\.edu\/\~fmoore', link_sel):
                    if link_sel not in self.URL:
                        yield scrapy.Request(link_sel, callback=self.parse)

                        # find documents
                        try:
                            res = urllib.request.urlopen(link_sel)
                            type = res.getheader("Content-Type")
                            if type == "text/html":
                                item['id'] = self.doc_id
                                self.doc_id += 1
                                self.DOCUMENT_LINKS.append(link_sel)
                            else:
                                pass

                        except urllib.error.URLError as e:
                            print(e.reason)

                        self.URL.append(link_sel)

                        item['link'] = link_sel
                        yield item
                    else:
                        pass
                else:
                    self.OUTGOING_LINKS.append(link_sel)
        else:
            self.BROKEN_LINKS.append(allUrl)
        # print("\n\n\n" + str(self.doc_id) + "\n\n\n")
        def output_CrawlerResults(self, filename, dataset):
            with io.open(RESULTS_DIRECTORY + '/' + filename + '.txt', 'w', encoding='utf-8') as f:
                for item in dataset:
                    f.write(unicode("%s\n" % item))

        def outputCorpusTable(self):
            temp = sorted(self.table.corpus_dict(), key=operator.itemgetter(1), reverse=True)
            with io.open(RESULTS_DIRECTORY + '/Corpus.txt', 'w', encoding='utf-8') as f:
                for word in temp:
                    f.write(unicode("{1}\n", temp[w]))

        def outputTop20Words(self):
            with io.open(RESULTS_DIRECTORY + '/Top20Words.txt', 'w', encoding='utf-8') as f:
                for item in self.table.top20_w:
                    f.write(unicode("%s\n" % item))
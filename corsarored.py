# VERSION: 1.0
# AUTHORS: shamalaya

from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
import json
from urllib.parse import unquote
import cfscrape #bypass cf cookie (need https://pypi.org/project/cfscrape and nodejs installed)

class corsarored(object):
    url = 'https://corsaro.red/'
    name = 'Corsaro.red'
    supported_categories = {'all': '0', 'movies': '2', 'tv': '1', 'music': '3', 'games': '6', 'anime': '7', 'software': '5'}
    searchurl = url + 'api/search'
    limit = 20 # results per page

    def search(self, what, cat):
        try:
            scraper = cfscrape.create_scraper()
            for page in range(1,self.limit):
                data = {"term":unquote(what),"category": self.supported_categories[cat],"page":page}
                jsonresult = scraper.post(self.searchurl,data).content.decode('utf-8')
                json_object = json.loads(jsonresult)
                nitems = len(json_object['results'])
                if nitems == 0:
                    break
                else:
                    self.processJson(json_object)
        except Exception as e:
            print(e)

    def getSingleData(self):
        return {'name': '-1', 'seeds': '-1', 'leech': '-1', 'size': '-1', 'link': '-1', 'desc_link': '-1', 'engine_url': self.url}

    def processJson(self, json):
        itemData = self.getSingleData()
        for cur in json['results']:
            itemData['name'] = '{} {}'.format(cur['title'], cur['description'])
            itemData['desc_link'] = cur['link']
            itemData['seeds'] = cur['seeders']
            itemData['leech'] = cur['leechers']
            itemData['size'] = str(cur['size'])
            itemData['link'] = cur['magnet']
            prettyPrinter(itemData)

    def download_torrent(self, info):
        """ Downloader """
        print(download_file(info))


# script test
if __name__ == "__main__":
    cr = corsarored()
    cr.search('archlinux','all')
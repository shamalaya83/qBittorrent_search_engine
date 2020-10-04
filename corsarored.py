#VERSION: 1.1
#AUTHORS: shamalaya

#from helpers import download_file, retrieve_url
#from novaprinter import prettyPrinter
from helpers import retrieve_url
from helpers import download_file
from novaprinter import prettyPrinter

import json
from urllib.parse import unquote
import requests

class corsarored(object):
    url = 'https://corsaro.red/'
    name = 'Corsaro.red'
    supported_categories = {'all': '0', 'movies': '2', 'tv': '1', 'music': '3', 'games': '6', 'anime': '7', 'software': '5'}
    searchurl = url + 'api/search'
    limit = 20 # loop max 20 pages

    def search(self, what, cat):
        try:
            for page in range(1,self.limit):
                data = {"term":unquote(what),"category": self.supported_categories[cat],"page":page}
                json_object = requests.post(url=self.searchurl, data=data).json()
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

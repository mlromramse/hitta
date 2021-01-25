#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

try:
    from urllib import quote
    from urllib import urlencode
except ImportError:
    from urllib.parse import quote
    from urllib.parse import urlencode

import sys

from bs4 import BeautifulSoup
import requests as requests


class Hitta():

    def __init__(self):
        self.soup = None

    def hitta(self, word):
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
        if '/' in word:
            request = requests.get('https://www.hitta.se/{}'.format(quote(word)), headers=headers)
        else:
            request = requests.get('https://www.hitta.se/sök?vad={}'.format(quote(word)), allow_redirects=True, headers=headers)
        print('Url: {}'.format(request.url))
        html = request.content
        self.soup = BeautifulSoup(html, 'html.parser')
        # print(html)
        names = self.soup.select('span[class=display-name]')

        self.show_search_results(word)

        self.row('Title', 'title')
        self.row('Type', 'span.heading--subtle')
        self.row('Tel', 'h2[class^=Headings__H2SizedAsH3]', remove_start='Andra format av ')
        self.row('Unknown', 'h1.uknownNumber')
        self.row('Searches', 'div.triplets div h2')
        for item in names:
            print(item.string)
        names = self.soup.select('span.result-row__item-hover-visualizer')
        for item in names:
            print(item.string)

    def row(self, heading, selector, remove_start=''):
        all = self.soup.select(selector)
        for each in all:
            content = each.string
            if content is not None and content.startswith(remove_start):
                print(heading + ': ', content[len(remove_start):])

    def show_search_results(self, word):
        result_area = self.soup.select('ul[data-trackcat=search-result-row]')
        if len(result_area) == 0:
            result_area = self.soup.select("div[data-trackcat=nolltraff]")
        # print(result_area)
        if result_area is not None and len(result_area)>0:

            items = result_area[0].select("li a div.text-container")
            if len(items) == 0:
                items = result_area[0].select("div section.style_introContainer__22oP6")
            # print(items)

            for item in items:
                # print(item)
                name = item.select("h2 span[class=display-name]")
                if len(name) == 0:
                    name = item.select("h2")
                if len(name) == 0:
                    name = item.select("p")
                print(name[0].getText())
            exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1][:1] == '-':
        print('usage: hitta search_word [/personer|/företag]')
        exit(0)
    words = ' '.join(sys.argv[1:])
    Hitta().hitta(words)

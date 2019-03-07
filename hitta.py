#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import json
import urllib

from urllib import urlencode

import sys

from bs4 import BeautifulSoup
import requests as requests


class Hitta():

    def __init__(self):
        self.soup = None

    def hitta(self, word):
        if '/' in word:
            request = requests.get('http://hitta.se/{}'.format(urllib.quote(word)))
        else:
            request = requests.get('http://hitta.se/sök?vad={}'.format(urllib.quote(word)), allow_redirects=True)
        print 'Url: {}'.format(request.url)
        html = request.content
        self.soup = BeautifulSoup(html, 'html.parser')
        # print html
        names = self.soup.select('span[itemprop=name]')

        self.show_search_results(word)

        self.row('Title', 'title')
        self.row('Type', 'span.heading--subtle')
        self.row('Tel', 'h2[class^=Headings__H2SizedAsH3]', remove_start='Andra format av ')
        self.row('Unknown', 'h1.uknownNumber')
        self.row('Searches', 'div.triplets div h2')
        for item in names:
            print item.string
        names = self.soup.select('span.result-row__item-hover-visualizer')
        for item in names:
            print item.string

    def row(self, heading, selector, remove_start=''):
        all = self.soup.select(selector)
        for each in all:
            content = each.string
            if content is not None and content.startswith(remove_start):
                print heading + ': ', content[len(remove_start):]

    def show_search_results(self, word):
        result_tab_bar = self.soup.select('div.result-tab-bar')
        if result_tab_bar is not None and len(result_tab_bar)>0:
            data_bind = result_tab_bar[0]['data-bind'].encode('utf-8')
            tabs_data = data_bind.partition('tabs: ')[2]
            tabs_data = ''.join(tabs_data.rpartition(']')[:2])
            tabs_json = json.loads(tabs_data, encoding='utf-8')

            for tab in tabs_json:
                title = tab['title'].encode('utf-8')
                print '{} ({})'.format(title, tab['count'])
                if tab['count'] == 1:
                    print '\tSpecify search as: hitta {}/{}'.format(word, title.lower())
                elif tab['count'] > 1:
                    print 'Specify search with more data.'
            exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1][:1] == '-':
        print 'usage: hitta search_word [/personer|/företag]'
        exit(0)
    words = ' '.join(sys.argv[1:])
    Hitta().hitta(words)

#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

from bs4 import BeautifulSoup
import requests as requests


class Hitta():

    def __init__(self):
        self.soup = None

    def hitta(self, word):
        html = requests.get('http://hitta.se/sök?vad={}'.format(word)).content
        self.soup = BeautifulSoup(html, 'html.parser')
        # print html
        names = self.soup.select('span[itemprop=name]')
        self.row('Title', 'title')
        self.row('Type', 'span.heading--subtle')
        self.row('Tel', 'a.phone-numbers__link strong')
        for item in names:
            print item.string
        names = self.soup.select('span.result-row__item-hover-visualizer')
        for item in names:
            print item.string

    def row(self, heading, selector):
        all = self.soup.select(selector)
        for each in all:
            content = each.string
            print heading + ': ', content

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1][:1] == '-':
        print 'usage: hitta search_word'
        exit(0)
    Hitta().hitta(sys.argv[1])

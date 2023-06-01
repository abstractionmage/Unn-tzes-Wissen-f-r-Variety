#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
"""
Variety quotes plugin sourcing useless facts in German from https://uselessfacts.jsph.pl/
@author: p-ja
"""

import logging

from locale import gettext as _
from variety.plugins.IQuoteSource import IQuoteSource
from variety.Util import Util
from variety.Util import cache

logger = logging.getLogger("variety")

default_fact = {
    "text": "Der Mensch kann besser Entscheidungen treffen, wenn er dringend pinkeln muss.",
    "source": "NEON",
    "source_url": "http://www.neon.de/artikel/kaufen/produkte/der-mensch-kann-besser-entscheidungen-treffen-wenn-er-dringend-pinkeln-muss/994779",
    "language": "de",
    "permalink": "https://uselessfacts.jsph.pl/api/v2/facts/b4ecb56c53a80be8b504604e1f0bb925"
}

class UselessFactsSource(IQuoteSource):

    def __init__(self):
        super(IQuoteSource, self).__init__()

    @classmethod
    def get_info(cls):
        return {
            "name": "Unnützes Wissen",
            "description": _("Unnütze aber wahre Fakten"),
            "version": "0.1",
            "author": "p-ja"
        }

    def activate(self):
        if self.active:
            return
        super(UselessFactsSource, self).activate()
        self.active = True

    def deactivate(self):
        self.active = False

    def needs_internet(self):
        '''
        Normaly this plugin requires internet access,
        but it fails gracefully if the internet access
        is not granted.
        '''
        return False

    def supports_search(self):
        return False

    def get_random(self):
        fact = self._get_fact()
        return [
            {
                "quote": fact['text'],
                "author": fact.get('source', None),
                "sourceName": fact.get('source_url', None),
                "link": fact.get('permalink', None)
            }
        ]

    def _get_fact(self):
        if not Util.internet_enabled:
            return default_fact

        try:
            fact = self._fetch_fact()
        except Exception as err:
            logger.warning("Failed to fetch fact {}".format(err))
            return default_fact

        if not isinstance(fact, dict):
            return default_fact

        if 'text' not in fact:
            return default_fact

        return fact

    @cache(ttl_seconds=30, debug=True)
    def _fetch_fact(self):
        logger.debug("Fetching useless fact...")
        URL = "https://uselessfacts.jsph.pl/random.json?language=de"
        return Util.fetch_json(URL)

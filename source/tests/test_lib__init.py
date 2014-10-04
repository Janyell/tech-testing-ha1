#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import mock
from source import lib


class LibInitTestCase(unittest.TestCase):
    #to_unicode(val, errors='strict')
        #positive_tests
    def test_to_unicode_isinstance(self):
        val = 'val'
        self.assertEquals(val, lib.to_unicode(val))

    def test_to_unicode_else(self):
        val = 'значение'
        errors = 'ignore'
        self.assertEquals(val.decode('utf8', errors), lib.to_unicode(val, errors))

    #to_str(val, errors='strict')
        #positive_tests
    def test_to_str_isinstance(self):
        val = 'val'
        self.assertEquals(val.encode('utf8'), lib.to_str(val))

    def test_to_str_else(self):
        val = 'значение'
        self.assertEquals(val, lib.to_str(val))

    #get_counters(content)
        #positive_tests
    def test_get_counters_match(self):
        import rstr
        content = ''

        for counter_name, regexp in lib.COUNTER_TYPES:
            content += rstr.xeger(regexp)

        self.assertEquals(len(lib.COUNTER_TYPES), len(lib.get_counters(content)))

    def test_get_counters_else(self):
        content = ''

        self.assertEquals(0, len(lib.get_counters(content)))

    #check_for_meta(content, url)
        #positive_tests

    #fix_market_url(url)
    def test_fix_market_url_fixed_bug(self):
        url = "market://apps-url"
        return_url = 'http://play.google.com/store/apps/apps-url'

        self.assertEquals(return_url, lib.fix_market_url(url))

    def test_fix_market_url_not_market(self):
        url = "http://apps-url"

        self.assertEquals(url, lib.fix_market_url(url))


    #make_pycurl_request(url, timeout, useragent=None)
        #positive_tests

    #get_url(url, timeout, user_agent=None)
        #positive_tests

    #get_redirect_history(url, timeout, max_redirects=30, user_agent=None)
        #positive_tests

    #prepare_url(url)
        #positive_tests
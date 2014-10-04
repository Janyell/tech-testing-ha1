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
    def test_check_for_meta_not_result(self):
        content = """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body></body>
            </html>
        """
        url = 'url'

        self.assertEquals(None, lib.check_for_meta(content, url))

    def test_check_for_meta_not_content(self):
        content = """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8" />
                </head>
                <body></body>
            </html>
        """
        url = 'url'

        self.assertEquals(None, lib.check_for_meta(content, url))

    def test_check_for_meta_not_http_equiv(self):
        content = """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta name="refresh" content="content" />
                </head>
                <body></body>
            </html>
        """
        url = 'url'

        self.assertEquals(None, lib.check_for_meta(content, url))

    def test_check_for_meta_not_refresh(self):
        content = """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                </head>
                <body></body>
            </html>
        """
        url = 'url'

        self.assertEquals(None, lib.check_for_meta(content, url))

    def test_check_for_meta_len_splitted_not_equals_2(self):
        content = """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta http-equiv="ReFresh" content="5" />
                </head>
                <body></body>
            </html>
        """
        url = 'url'

        self.assertEquals(None, lib.check_for_meta(content, url))

    def test_check_for_meta_not_search_url(self):
        content = """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta http-equiv="refresh" content="5; url=">
                </head>
                <body></body>
            </html>
        """
        url = 'url'

        self.assertEquals(None, lib.check_for_meta(content, url))

    def test_check_for_meta(self):
        url = 'http://url.ru'
        redirect_url = 'http://redirect-url.ru'
        content = """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta http-equiv="refresh" content="5; url=""" + redirect_url + """">
                </head>
                <body></body>
            </html>
        """
        with mock.patch('source.lib.to_unicode', mock.Mock(return_value=redirect_url)):
            self.assertEquals(lib.urljoin(url, redirect_url), lib.check_for_meta(content, url))

    #fix_market_url(url)
        #positive_tests
    def test_fix_market_url_fixed_bug(self):
        url = 'market://apps-url'
        return_url = 'http://play.google.com/store/apps/apps-url'

        self.assertEquals(return_url, lib.fix_market_url(url))

    def test_fix_market_url_not_market(self):
        url = 'http://apps-url'

        self.assertEquals(url, lib.fix_market_url(url))

    #make_pycurl_request(url, timeout, useragent=None)
        #positive_tests
    def test_make_pycurl_request_redirect_url(self):
        url = 'http://url.ru'
        timeout = 30
        content = 'content'
        redirect_url = 'http://redirect-url.ru'
        useragent = 'useragent'
        buff = mock.MagicMock()
        buff.getvalue = mock.Mock(return_value=content)
        curl = mock.MagicMock()
        curl.setopt = mock.Mock()
        curl.perform = mock.Mock()
        curl.getinfo = mock.Mock(return_value=redirect_url)

        with mock.patch('source.lib.to_str', mock.Mock(return_value=url)):
            with mock.patch('source.lib.StringIO', mock.Mock(return_value=buff)):
                with mock.patch('pycurl.Curl', mock.Mock(return_value=curl)):
                    with mock.patch('source.lib.to_unicode', mock.Mock(return_value=redirect_url)):
                        self.assertEquals((content, redirect_url), lib.make_pycurl_request(url, timeout))
                        self.assertEquals((content, redirect_url), lib.make_pycurl_request(url, timeout, useragent))

    def test_make_pycurl_request_none(self):
        url = 'http://url.ru'
        timeout = 30
        content = 'content'
        useragent = 'useragent'
        buff = mock.MagicMock()
        buff.getvalue = mock.Mock(return_value=content)
        curl = mock.MagicMock()
        curl.setopt = mock.Mock()
        curl.perform = mock.Mock()
        curl.getinfo = mock.Mock(return_value=None)

        with mock.patch('source.lib.to_str', mock.Mock(return_value=url)):
            with mock.patch('source.lib.StringIO', mock.Mock(return_value=buff)):
                with mock.patch('pycurl.Curl', mock.Mock(return_value=curl)):
                    self.assertEquals((content, None), lib.make_pycurl_request(url, timeout))
                    self.assertEquals((content, None), lib.make_pycurl_request(url, timeout, useragent))

    #get_url(url, timeout, user_agent=None)
        #positive_tests
    def test_get_url(self):
        url = "http://url.ru"
        timeout = 30
        pass

    #get_redirect_history(url, timeout, max_redirects=30, user_agent=None)
        #positive_tests

    #prepare_url(url)
        #positive_tests
    def test_prepare_url_none(self):
        url = None

        self.assertEquals(url, lib.prepare_url(url))

    def test_prepare_url(self):
        url = 'https://netloc.com/path with%20space.php;qs=qs1 qs2'
        return_url = 'https://netloc.com/path%20with%20space.php;qs=qs1+qs2'

        self.assertEquals(return_url, lib.prepare_url(url))
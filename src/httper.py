#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
from pyquery import PyQuery as pq

from utils.pyecho import echo
from utils.helper import get_proxies, get_headers, save_failed_url

class Httper(object):
    """docstring for Httper"""
    def __init__(self, *args, **kwargs):
        super(Httper, self).__init__()
        self.url = args[0]
        self.method = kwargs.get('method', 'get')
        self.data = kwargs.get('data', {})
        # rtype: response type, text or json
        self.rtype = kwargs.get('rtype', 'text')
        # rkey: response key
        self.rkey = kwargs.get('rkey', '')
        # dtype: deal way, re or pq
        self.dtype = kwargs.get('dtype', '')
        self.rex = kwargs.get('rex', '')
        self.selector = kwargs.get('selector', '')
        self.attr = kwargs.get('attr', '')
        # request timeout, default timeout is 10s
        self.timeout = kwargs.get('timeout', 10)

    '''save failed request'''
    def request_failed(self):
        save_failed_url(
            'url': self.url,
            'method': self.method,
            'data': str(self.data),
            'rtype': self.rtype,
            'rkey': self.rkey,
            'dtype': self.dtype,
            'rex': self.rex,
            'selector': self.selector,
            'attr': self.attr
        )

    '''request'''
    def request(self):
        echo.info('Trying to get %s' % self.url)
        try:
            if self.method == 'get' or self.method == 'GET':
                r = requests.get(
                    self.url,
                    data = self.data,
                    headers = get_headers(),
                    proxies = get_proxies(),
                    timeout = self.timeout
                )
            elif self.method == 'post' or self.method == 'POST':
                r = requests.post(
                    self.url,
                    data = self.data,
                    headers = get_headers(),
                    proxies = get_proxies(),
                    timeout = self.timeout
                )
        except:
            echo.error('Get %s failed' % self.url)
            self.request_failed()
            return False, ''
        if r.status_code != 200:
            echo.error('%d %s' % (r.status_code, self.url))
            self.request_failed()
            return False, ''
        echo.success('Get %s successfully' % self.url)
        if self.rtype == 'text':
            return True, r.text
        elif self.rtype == 'json':
            if self.rkey:
                return True, r.json()[rkey]
            else:
                return True, r.json()

    '''get data'''
    def get_data(self):
        _, txt = self.request()
        # 如果请求成功了
        if _:
            # 如果是用正则模式
            if self.dtype == 're' and self.rex != '':
                return True, re.findall(rex, txt)
            # 如果是用选择器模式
            elif self.dtype == 'pq' and self.selector != '' and self.attr != '':
                d = pq(txt)
                elements = d(self.selector)
                # 如果选中的不是一个list，先变成list
                if not isinstance(elements, list):
                    elements = [elements]
                # 如果attr是text
                if self.attr == 'text' or self.attr == 'txt':
                    res = [d(x).text() for x in elements]
                else:
                    res = [d(x).attr(self.attr) for x in elements]
                return True, res
        return False, []

            


        


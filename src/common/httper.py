#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
from pyquery import PyQuery as pq

from .pyecho import echo
from .chameleon import chameleon
from .cache import mq_push

class Httper(object):
    """docstring for Httper"""
    def __init__(self, *args, **kwargs):
        super(Httper, self).__init__()
        # if request failed, retry 10 times
        self.remaining_retries = 20
        self.url = args[0] or kwargs.get('url', '')
        self.method = kwargs.get('method', 'get')
        self.data = kwargs.get('data', {})
        # rtype: response type, text or json
        self.rtype = kwargs.get('rtype', 'text')
        # rkey: response key
        self.rkey = kwargs.get('rkey', [''])
        # dtype: deal way, re or pq
        self.dtype = kwargs.get('dtype', '')
        self.rex = kwargs.get('rex', '')
        self.selector = kwargs.get('selector', '')
        self.attr = kwargs.get('attr', '')
        # request timeout, default timeout is 10s
        self.timeout = kwargs.get('timeout', 7)
        # 用来处理出错情况
        self.cache_key = kwargs.get('cache_key', 'mafengwo:default')
        self.cache_val = kwargs.get('cache_val', '1234')

        self.request()

    '''save failed request'''
    def request_failed(self):
        # if request failed, retry
        echo.error('Get %s failed' % self.url)
        echo.info('Remaining retries: %d' % self.remaining_retries)
        if self.remaining_retries > 0:
            self.remaining_retries -= 1
            self.request()
        else:
            mq_push(self.cache_key, self.cache_val)

    '''request'''
    def request(self):
        echo.info('Trying to get %s' % self.url)
        try:
            if self.method == 'get' or self.method == 'GET':
                r = requests.get(
                    self.url,
                    data = self.data,
                    headers = chameleon.get_headers(),
                    proxies = chameleon.get_proxies(),
                    timeout = self.timeout
                )
            elif self.method == 'post' or self.method == 'POST':
                r = requests.post(
                    self.url,
                    data = self.data,
                    headers = chameleon.get_headers(),
                    proxies = chameleon.get_proxies(),
                    timeout = self.timeout
                )
        except:
            return self.request_failed()
        # 如果状态不为200或数据为空或长度小于10
        if r.status_code != 200 or r.text is None or len(r.text) < 10:
            return self.request_failed()
        if self.rtype == 'text':
            self.result = r.text
        elif self.rtype == 'json':
            try:
                self.result = r.json()
            except:
                return self.request_failed()
        echo.success('Get %s successfully' % self.url)

    '''get data'''
    def get_data(self, **kwargs):
        dtype = kwargs.get('dtype', self.dtype)
        rex = kwargs.get('rex', self.rex)
        selector = kwargs.get('selector', self.selector)
        attr = kwargs.get('attr', self.attr)
        rkey = kwargs.get('rkey', self.rkey)
        txt = self.result

        # 支持从多级json中提取数据
        for rk in rkey:
            if rk:
                try:
                    txt = txt[rk]
                except:
                    self.request_failed()
                    return self.get_data(
                            dtype = dtype,
                            rex = rex,
                            selector = selector,
                            attr = attr,
                            rkey = rkey
                        )

        # 如果是用正则模式
        if dtype == 're' and rex != '':
            return re.findall(rex, txt)
        # 如果是用选择器模式
        elif dtype == 'pq' and selector != '' and attr != '':
            try:
                d = pq(txt)
            except:
                return self.request_failed()
            elements = d(selector)
            # 如果选中的不是一个list，先变成list
            if not isinstance(elements, list):
                elements = [elements]
            # 如果attr是text
            if attr == 'text' or attr == 'txt':
                res = [d(x).text() for x in elements]
            else:
                res = [d(x).attr(attr) for x in elements]
            return res

        echo.error('are you kidding me?')
        return ['']

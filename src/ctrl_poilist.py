#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import re
from common.pyecho import echo
from common.httper import Httper
from common.cache import push_poi_id

class PoilistCtrl(object):
    """docstring for PoilistCtrl"""
    def __init__(self, **kwargs):
        super(PoilistCtrl, self).__init__()
        self.url = 'http://www.mafengwo.cn/ajax/router.php'
        self.city_id = kwargs.get('city_id', '')
        self.page = kwargs.get('page', 1)
        self.total = kwargs.get('total', 2)

    def set_data(self):
        data = {
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            'iMddid': self.city_id,
            'iTagId': 0,
            'iPage': self.page
        }
        hr = Httper(
            self.url,
            method = 'post',
            data = data,
            rtype = 'json',
            rkey = ['data', 'list'],
            dtype = 'pq',
            selector = 'li a',
            attr = 'href'
        )
        # 如果是第一次请求那么获取总页数
        if self.page == 1:
            tmp_total = hr.get_data(
                rkey = ['data', 'page'],
                selector = '.count span',
                attr = 'text'
            )
            if tmp_total:
                self.total = int(tmp_total[0])
            else:
                self.total = 1
        self.poi_id_list = hr.get_data()

    def push_data(self):
        for poi_id in self.poi_id_list:
            pid = re.findall('\d+', poi_id)
            if pid:
                push_poi_id(pid[0])
                echo.info('Poi id %s pushed' % pid[0])

    def entry(self):
        self.set_data()
        self.push_data()
        

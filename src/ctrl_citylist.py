#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import re
from common.pyecho import echo
from common.models import Dest
from common.httper import Httper
from common.cache import push_city_id

class CitylistCtrl(object):
    """docstring for CitylistCtrl"""
    def __init__(self, **kwargs):
        super(CitylistCtrl, self).__init__()
        self.portal_id = kwargs.get('portal_id', '')
        self.page = kwargs.get('page', 1)
        self.total = kwargs.get('total', 2)
        self.url = 'http://www.mafengwo.cn/mdd/base/list/pagedata_citylist'
        self.city_id_list = []
        self.city_name_list = []

    def set_data(self):
        data = {
            'mddid': self.portal_id,
            'page': self.page
        }
        hr = Httper(
            self.url,
            method = 'post',
            data = data,
            rtype = 'json',
            dtype = 'pq'
        )
        # 在第一次请求时获取页面总数
        if self.page == 1:
            tmp_total = hr.get_data(
                rkey = ['page'],
                selector = '.pg-last',
                attr = 'data-page'
            )
            self.total = int(tmp_total[0])
        # 设置city id
        self.city_id_list = hr.get_data(
            rkey = ['list'],
            selector = '.item .img a',
            attr = 'data-id'
        )
        # 设置city name
        self.city_name_list = hr.get_data(
            rkey = ['list'],
            selector = '.item .title',
            attr = 'text'
        )

    def push_data(self):
        for city_id in self.city_id_list:
            push_city_id(city_id)
            echo.success('city id %s pushed' % city_id)

    def save_data(self):
        for city in zip(self.city_id_list, self.city_name_list):
            names = city[1].split(' ')
            if names[0]:
                Dest.create(
                    dest_id = uuid.uuid4(),
                    name = names[0],
                    m_dest_id = city[0],
                    m_parent_dest_id = self.portal_id
                )
                echo.success('city id %s name %s saved' % (city[0], names[0]))

    def entry(self):
        while self.page <= self.total:
            echo.info('mddid: %s, page: %s, total: %s' % (self.portal_id, self.page, self.total))
            self.set_data()
            self.push_data()
            self.save_data()
            self.page += 1

        
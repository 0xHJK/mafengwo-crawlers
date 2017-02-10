#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import re
from common.pyecho import echo
from common.models import Poi, Pimg
from common.httper import Httper
from common.cache import push_image_url

class PoidetailCtrl(object):
    """docstring for PoidetailCtrl"""
    def __init__(self, **kwargs):
        super(PoidetailCtrl, self).__init__()
        self.poi_id = uuid.uuid4()
        self.m_poi_id = kwargs.get('m_poi_id', '')
        self.url = 'http://www.mafengwo.cn/poi/%s.html' % self.m_poi_id

    def set_data(self):
        hr = Httper(
            self.url,
            method = 'get',
            rtype = 'text',
            dtype = 'pq'
        )
        self.poi_name = ''.join(hr.get_data(selector = 'h1', attr = 'text'))
        self.image_url_list = hr.get_data(selector = '.bd img', attr = 'src')
        self.summary = ''.join(hr.get_data(selector = '.summary', attr = 'text'))
        self.tel = ''.join(hr.get_data(selector = '.tel .content', attr = 'text'))
        self.website = ''.join(hr.get_data(selector = '.item-site .content a', attr = 'href'))
        self.expected_time = ''.join(hr.get_data(
            selector = '.item-time .content',
            attr = 'text'
        ))
        self.traffic = ''.join(hr.get_data(
            selector = '.container > div:nth-child(6) > div:nth-child(2) > dl:nth-child(3) > dd',
            attr = 'text'
        ))
        self.ticket = ''.join(hr.get_data(
            selector = '.container > div:nth-child(6) > div:nth-child(2) > dl:nth-child(4) > dd',
            attr = 'text'
        ))
        self.business_hours = ''.join(hr.get_data(
            selector = '.container > div:nth-child(6) > div:nth-child(2) > dl:nth-child(5) > dd',
            attr = 'text'
        ))
        comment_count = hr.get_data(
            selector = '#poi-navbar > ul > li:nth-child(3) > a > span',
            attr = 'text'
        )
        if comment_count:
            self.comment_count = ''.join(re.findall(r'\d+', str(comment_count)))
        else:
            self.comment_count = '0'
        sub_poi_href = ''.join(hr.get_data(
            selector = '.mod-innerScenic li > a',
            attr = 'href'
        ))
        if sub_poi_href:
            self.sub_poi_id = ','.join(re.findall('\d+', sub_poi_href))
        else:
            self.sub_poi_id = ''

    def push_data(self):
        for image_url in self.image_url_list:
            if image_url:
                image_url = image_url.split('?imageMogr2')[0]
                push_image_url(image_url)
                echo.info('image_url %s pushed' % image_url)

    def save_data(self):
        Poi.create(
            poi_id = self.poi_id,
            name = self.poi_name,
            summary = self.summary,
            tel = self.tel,
            website = self.website,
            expected_time = self.expected_time,
            traffic = self.traffic,
            ticket = self.ticket,
            business_hours = self.business_hours,
            comment_count = self.comment_count,
            sub_poi_id = self.sub_poi_id,
            m_poi_id = self.m_poi_id
        )
        for image_url in self.image_url_list:
            if image_url:
                Pimg.create(
                    poi_id = self.poi_id,
                    image_url = image_url.split('?imageMogr2')[0]
                )
        echo.info('%s %s saved' % (self.m_poi_id, self.poi_name))

    def entry(self):
        self.set_data()
        self.push_data()
        self.save_data()

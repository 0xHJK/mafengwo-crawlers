#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import re
from utils.pyecho import echo
from models import Dest, Poi, Pimg
from httper import Httper

class PoiCtrl(object):
    """docstring for PoiCtrl"""
    def __init__(self, **kwargs):
        super(PoiCtrl, self).__init__()
        self.url = 'http://www.mafengwo.cn/ajax/router.php'
        # dest uuid
        self.dest_id = kwargs.get('dest_id', '')
        # mafengwo mdd id
        self.m_dest_id = kwargs.get('m_dest_id', '')
        self.page = kwargs.get('page', 1)
        self.total = kwargs.get('total', 2)
        self.is_available = True

    def base_poi_list(self):
        data = {
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            'iMddid': self.m_dest_id,
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
        # send request
        hr.request()
        # get poi list
        self.is_available, poi_id_list = hr.get_data()
        _, poi_name_list = hr.get_data(attr = 'title')
        # get total page count
        if self.is_available:
            if self.page == 1:
                _, tmp_total = hr.get_data(
                    rkey = ['data', 'page'],
                    selector = '.count span',
                    attr = 'text'
                )
                if tmp_total:
                    self.total = int(tmp_total[0])
                else:
                    self.total = 1
        return zip(poi_id_list, poi_name_list)

    def save_poi_list(self, poi_id_name):
        if self.is_available:
            for poi in poi_id_name:
                print('saving...', poi)
                mp_id = re.findall('\d+', poi[0])
                poi = Poi.create(
                    poi_id = uuid.uuid4(),
                    name = poi[1],
                    m_poi_id = mp_id[0],
                    dest_id = self.dest_id
                )

    def read_poi_list(self):
        return Poi.select(Poi.poi_id, Poi.m_poi_id).where(Poi.is_over == False)

    def poi_list(self):
        while self.page <= self.total:
            echo.info('mddid: %s, uuid: %s, page: %s, total: %s' % (self.m_dest_id, self.dest_id, self.page, self.total))
            poi_id_name = self.base_poi_list()
            if self.is_available:
                self.save_poi_list(poi_id_name)
                self.page += 1
            else:
                break
        for dc in Dest.select().where(Dest.dest_id == self.dest_id):
            dc.is_poi_over = True
            dc.save()
            echo.success('%s %s is over' % (dc.name, dc.dest_id))


class PoiFullCtrl(object):
    """docstring for PoiFullCtrl"""
    def __init__(self, **kwargs):
        super(PoiFullCtrl, self).__init__()
        self.poi_id = kwargs.get('poi_id', '')
        self.m_poi_id = kwargs.get('m_poi_id', '')
        self.url = 'http://www.mafengwo.cn/poi/%s.html' % self.m_poi_id

    def save_full_poi(self, **kwargs):
        imgs = kwargs.get('imgs', [])
        for pc in Poi.select().where(Poi.poi_id == self.poi_id):
            pc.description = kwargs.get('description', '')
            pc.guidebook = kwargs.get('guidebook', '')
            pc.tel = kwargs.get('tel', '')
            pc.website = kwargs.get('website', '')
            pc.expected_time = kwargs.get('expected_time', '')
            pc.traffic = kwargs.get('traffic', '')
            pc.ticket = kwargs.get('ticket', '')
            pc.business_hours = kwargs.get('business_hours', '')
            pc.comment_count = kwargs.get('comment_count', 0)
            pc.comment_count_a = kwargs.get('comment_count_a', 0)
            pc.comment_count_b = kwargs.get('comment_count_b', 0)
            pc.comment_count_c = kwargs.get('comment_count_c', 0)
            pc.sub_poi_id = kwargs.get('sub_poi_id', '')
            pc.is_over = True
            pc.save()

        for img in imgs:
            if img:
                Pimg.create(poi_id = self.poi_id, image_url = img.split('?imageMogr2')[0])


    # def poi_comment_info(self, params, api):
    #     data = {
    #         'params': params,
    #         'api': api
    #     }
    #     hr = Httper(
    #         'http://www.mafengwo.cn/ajax/ajax_fetch_pagelet.php',
    #         method = 'get',
    #         data = data,
    #         rtype = 'json',
    #     )

    def full_poi_info(self):
        hr = Httper(
            self.url,
            method = 'get',
            rtype = 'text',
            dtype = 'pq'
        )
        hr.request()
        # imgs
        _, imgs = hr.get_data(
            selector = '.bd img',
            attr = 'src'
        )
        # description
        _, description = hr.get_data(
            selector = '.summary',
            attr = 'text'
        )
        # guidebook
        # tel
        _, tel = hr.get_data(
            selector = '.tel .content',
            attr = 'text'
        )
        # website
        _, website = hr.get_data(
            selector = '.item-site .content a',
            attr = 'href'
        )
        # expected_time
        _, expected_time = hr.get_data(
            selector = '.item-time .content',
            attr = 'text'
        )
        # traffic
        _, traffic = hr.get_data(
            selector = '.container > div:nth-child(6) > div:nth-child(2) > dl:nth-child(3) > dd',
            attr = 'text'
        )
        # ticket
        _, ticket = hr.get_data(
            selector = '.container > div:nth-child(6) > div:nth-child(2) > dl:nth-child(4) > dd',
            attr = 'text'
        )
        # business_hours
        _, business_hours = hr.get_data(
            selector = '.container > div:nth-child(6) > div:nth-child(2) > dl:nth-child(5) > dd',
            attr = 'text'
        )
        # comment_count
        _, comment_count = hr.get_data(
            selector = '#poi-navbar > ul > li:nth-child(3) > a > span',
            attr = 'text'
        )
        if not comment_count:
            comment_count = '0'
        # sub_poi_href
        _, sub_poi_href = hr.get_data(
            selector = '.mod-innerScenic li > a',
            attr = 'href'
        )
        sub_poi_href = ''.join(sub_poi_href)
        if sub_poi_href:
            sub_poi_id = ','.join(re.findall('\d+', sub_poi_href))
        else:
            sub_poi_id = ''

        self.save_full_poi(
            description = ''.join(description),
            tel = ''.join(tel),
            website = ''.join(website),
            expected_time = ''.join(expected_time),
            traffic = ''.join(traffic),
            ticket = ''.join(ticket),
            business_hours = ''.join(business_hours),
            comment_count = ''.join(re.findall(r'\d+', str(comment_count))),
            sub_poi_id = sub_poi_id,
            imgs = imgs
        )

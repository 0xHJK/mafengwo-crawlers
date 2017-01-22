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


        

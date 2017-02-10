#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import re
from common.pyecho import echo
from common.models import Dest
from common.httper import Httper
from common.cache import push_portal_id
from common.cache import push_city_id
from common.utils import get_full_province_name

class PortalCtrl(object):
    """docstring for PortalCtrl"""
    def __init__(self):
        super(PortalCtrl, self).__init__()
        self.url = 'http://www.mafengwo.cn/mdd/'

    def set_data(self):
        hr = Httper(
            self.url,
            rtype = 'text',
            dtype = 'pq'
        )
        portal_href_list = hr.get_data(
            selector = '.sub-title a',
            attr = 'href'
        )
        portal_name_list = hr.get_data(
            selector = '.sub-title a',
            attr = 'text'
        )
        city_href_list = hr.get_data(
            selector = '.bd-china > dl:nth-child(1) > dd > ul li a',
            attr = 'href'
        )
        city_name_list = hr.get_data(
            selector = '.bd-china > dl:nth-child(1) > dd > ul li a',
            attr = 'text'
        )
        self.portal_list = zip(portal_href_list, portal_name_list)
        self.city_list = zip(city_href_list, city_name_list)

    def save_data(self, href_name_list, area_type = 'province'):
        for href_name in href_name_list:
            mid = re.findall('\d+', href_name[0])
            if mid:
                name = get_full_province_name(href_name[1])
                m_dest_id = mid[0]
                if area_type == 'province':
                    province = name
                    city = ''
                    # push portal id
                    push_portal_id(m_dest_id)
                else:
                    province = ''
                    city = name
                    # push city id
                    push_city_id(m_dest_id)
                # save to database
                Dest.create(
                    dest_id = uuid.uuid4(),
                    name = name,
                    m_dest_id = m_dest_id,
                    province = province,
                    city = city
                )
                echo.info(m_dest_id + ' ' + name + ' saved')

    def entry(self):
        # 获取数据
        self.set_data()
        # 保存province数据
        self.save_data(self.portal_list)
        # 保存city数据
        self.save_data(self.city_list, 'city')


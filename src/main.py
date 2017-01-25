#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
from utils.helper import get_proxies, get_headers, save_failed_url
from httper import Httper
from models import Dest
from destctrl import DestCtrl, MainDestCtrl
from poictrl import PoiCtrl, PoiFullCtrl

def set_main_dest():
    mdc = MainDestCtrl()
    mdc.dest_list()

def get_main_dest():
    mdc = MainDestCtrl()
    return mdc.read_pvc_dest_list()

def get_area_dest():
    mdc = MainDestCtrl()
    return mdc.read_area_dest_list()

def get_poi_list():
    pc = PoiCtrl()
    return pc.read_poi_list()

def set_common_dest(mddid, province, parent_dest_id):
    dc = DestCtrl(
        mddid = mddid,
        province = province,
        parent_dest_id = parent_dest_id
    )
    dc.dest_list()

def set_common_dest_abort(mddid, province, parent_dest_id, page, total):
    dc = DestCtrl(
        mddid = mddid,
        province = province,
        parent_dest_id = parent_dest_id,
        page = page,
        total = total
    )
    dc.dest_list()

def set_basic_poi(dest_id, m_dest_id):
    pc = PoiCtrl(
        dest_id = dest_id,
        m_dest_id = m_dest_id
    )
    pc.poi_list()

def set_basic_poi_abort(dest_id, m_dest_id, page, total):
    pc = PoiCtrl(
        dest_id = dest_id,
        m_dest_id = m_dest_id,
        page = page,
        total = total
    )
    pc.poi_list()

def set_full_poi(poi_id, m_poi_id):
    pfc = PoiFullCtrl(
        poi_id = poi_id,
        m_poi_id = m_poi_id
    )
    pfc.full_poi_info()

if __name__ == '__main__':
    # 省／直辖市／特别行政区
    # set_main_dest()

    # 下属区域和城市
    # mdests = get_main_dest()
    # for dst in mdests:
    #     set_common_dest(dst.m_dest_id, dst.province, dst.dest_id)

    # failed dest request
    # set_common_dest_abort('14731', '湖北', 'cd4edbce-d05e-45a6-815d-78683bf68d77', 5, 10)


    # failed poi request
    # set_basic_poi_abort('0a648945-82d4-4121-a6fd-ba0acebb1d1c', '24998', 12, 41)


    # 获取景点ID和名字
    # adests = get_area_dest()
    # for dst in adests:
    #     set_basic_poi(dst.dest_id, dst.m_dest_id)

    # 获取景点ID
    pois = get_poi_list()
    for poi in pois:
        set_full_poi(poi.poi_id, poi.m_poi_id)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ctrl_poilist import PoilistCtrl
from common.cache import pop_city_id

if __name__ == '__main__':
    while True:
        city_id = pop_city_id()
        plc = PoilistCtrl(city_id = city_id)
        plc.entry()

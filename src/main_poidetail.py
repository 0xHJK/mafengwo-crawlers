#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ctrl_poidetail import PoidetailCtrl
from common.cache import pop_poi_id

if __name__ == '__main__':
    while True:
        m_poi_id = pop_poi_id()
        pdc = PoidetailCtrl(m_poi_id = m_poi_id)
        pdc.entry()
        
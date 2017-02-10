#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ctrl_citylist import CitylistCtrl
from common.cache import pop_portal_id

if __name__ == '__main__':
    while True:
        portal_id = pop_portal_id()
        print(portal_id)
        clc = CitylistCtrl(portal_id = portal_id)
        clc.entry()
        
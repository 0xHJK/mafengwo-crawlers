#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis

# r = redis.Redis(host = 'localhost')
r = redis.Redis(host = 'cache')

def mq_push(key, val, is_high = False):
    if is_high:
        r.rpush(key, val)
    else:
        r.lpush(key, val)

def mq_pop(key):
    return str(r.brpop(key)[1], encoding = 'utf-8')

def push_portal_id(val):
    mq_push('mafengwo:portal_id', val)

def pop_portal_id():
    return mq_pop('mafengwo:portal_id')

def push_city_id(val):
    mq_push('mafengwo:city_id', val)

def pop_city_id():
    return mq_pop('mafengwo:city_id')

def push_poi_id(val):
    mq_push('mafengwo:poi_id', val)

def pop_poi_id():
    return mq_pop('mafengwo:poi_id')

def push_image_url(val):
    mq_push('mafengwo:image_url', val)

def pop_image_url():
    mq_pop('mafengwo:image_url')

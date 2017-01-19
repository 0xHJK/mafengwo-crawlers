#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sqlite3

# TODO:
# restore txt and sqlite to redis

# get headers random
def get_headers():
    with open('headers.txt', 'r') as f:
        headers = [x.strip() for x in f.readlines()]
    return {'User-Agent': random.choice(headers)}

# get proxies random
def get_proxies():
    with open('proxies.txt', 'r') as f:
        proxies = [{'http': x.strip(), 'https': x.strip()} for x in f.readlines()]
    return random.choice(proxies)

def save_failed_url(**kwargs):
    url = kwargs.get('url', '')
    method = kwargs.get('method', '')
    data = kwargs.get('data', '')
    dtype = kwargs.get('dtype', '')
    rex = kwargs.get('rex', '')
    selector = kwargs.get('selector', '')
    attr = kwargs.get('attr', '')
    conn = sqlite3.connect('url.db')
    conn.excute(
        '''create table if not exists urls (
            id          integer     primary key,
            url         text,
            method      text,
            data        text,
            dtype       text,
            rex         text,
            selector    text,
            attr        text
        );'''
    )
    cur = conn.cursor()
    cur.excute('insert (url, method, data, dtype, rex, selector, attr) into urls values (?, ?, ?, ?, ?, ?, ?)', (url, method, data, dtype, rex, selector, attr))
    cur.commit()
    cur.close()
    conn.close()

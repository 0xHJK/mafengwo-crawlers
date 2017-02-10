#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *

db = MySQLDatabase('ayou', host = 'db', user = 'ayou', password = 'ayou', charset = 'utf8mb4')
db.connect()

class BaseModel(Model):
    class Meta:
        database = db

class Dest(BaseModel):
    dest_id = UUIDField(primary_key = True)
    name = CharField(max_length = 48, default = '')
    city = CharField(max_length = 48, default = '')
    province = CharField(max_length = 48, default = '')
    country = CharField(max_length = 48, default = '中国')
    parent_dest_id = CharField(max_length = 40, default = '')
    m_parent_dest_id = IntegerField(default = 0)
    m_dest_id = IntegerField(default = 0)
    # is_dest_over = BooleanField(default = False)
    # is_poi_over = BooleanField(default = False)


class Poi(BaseModel):
    poi_id = UUIDField(primary_key = True)
    name = CharField(max_length = 48, default = '')
    summary = TextField(default = '')
    # poi_address = TextField(default = '')
    # guidebook = TextField(default = '')
    tel = CharField(max_length = 255, default = '')
    website = CharField(default = '')
    expected_time = TextField(default = '')
    traffic = TextField(default = '')
    ticket = TextField(default = '')
    business_hours = TextField(default = '')
    comment_count = IntegerField(default = 0)
    # comment_count_a = IntegerField(default = 0)
    # comment_count_b = IntegerField(default = 0)
    # comment_count_c = IntegerField(default = 0)
    # parent_poi_id = CharField(max_length = 40, default = '')
    sub_poi_id = TextField(default = '')
    dest_id = CharField(max_length = 40, default = '')
    m_poi_id = IntegerField(default = 0)
    # is_over = BooleanField(default = False)


class Pimg(BaseModel):
    idx_id = PrimaryKeyField(primary_key = True)
    poi_id = CharField(max_length = 40, default = '')
    image_url = TextField(default = '')

# Only create the tables if they do not exist
db.create_tables([Dest, Poi, Pimg], safe=True)


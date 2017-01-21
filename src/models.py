#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *

db = MySQLDatabase('ayou', user = 'root', password = 'root', charset = 'utf8mb4')
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
    parent_dest_id = UUIDField(default = '')
    m_dest_id = IntegerField(default = 0)


class Poi(BaseModel):
    poi_id = UUIDField(primary_key = True)
    name = CharField(max_length = 48, default = '')
    description = TextField(default = '')
    poi_address = TextField(default = '')
    guidebook = TextField(default = '')
    tel = CharField(max_length = 20, default = '')
    website = CharField(default = '')
    expected_time = TextField(default = '')
    traffic = TextField(default = '')
    ticket = TextField(default = '')
    business_hours = TextField(default = '')
    comment_count = IntegerField(default = 0)
    comment_count_a = IntegerField(default = 0)
    comment_count_b = IntegerField(default = 0)
    comment_count_c = IntegerField(default = 0)
    parent_poi_id = UUIDField(default = '')
    dest_id = UUIDField(default = '')
    m_poi_id = IntegerField(default = 0)


class Pimg(BaseModel):
    idx_id = PrimaryKeyField(primary_key = True)
    poi_id = UUIDField(default = '')
    image_url = TextField(default = '')

# Only create the tables if they do not exist
db.create_tables([Dest, Poi, Pimg], safe=True)


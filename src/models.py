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
    name = CharField(max_length = 48)
    city = CharField(max_length = 48)
    province = CharField(max_length = 48)
    country = CharField(max_length = 48, default = '中国')
    parent_poi_id = UUIDField()
    m_dest_id = IntegerField()


class Poi(BaseModel):
    poi_id = UUIDField(primary_key = True)
    name = CharField(max_length = 48)
    description = TextField()
    poi_address = TextField()
    guidebook = TextField()
    tel = CharField(max_length = 20)
    website = CharField()
    expected_time = TextField()
    traffic = TextField()
    ticket = TextField()
    business_hours = TextField()
    comment_count = IntegerField()
    comment_count_a = IntegerField()
    comment_count_b = IntegerField()
    comment_count_c = IntegerField()
    parent_poi_id = UUIDField()
    dest_id = UUIDField()
    m_poi_id = IntegerField()


class Pimg(BaseModel):
    idx_id = PrimaryKeyField(primary_key = True)
    poi_id = UUIDField()
    image_url = TextField()

db.create_tables([Pimg])


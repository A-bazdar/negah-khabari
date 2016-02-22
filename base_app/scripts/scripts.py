#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("/root/ehsan/negah-khabari")
import json
from bson import ObjectId
from base_app.models.mongodb.base_model import MongodbModel
import dateutil.parser as d_parser


a = open("base_app/scripts/content.json", "r")
x = json.loads(a.read())
for i in x:
    i['_id'] = ObjectId(i['_id'])
    MongodbModel(collection="content", body=i).insert()
a.close()

a = open("base_app/scripts/subject.json", "r")
x = json.loads(a.read())
for i in x:
    i['_id'] = ObjectId(i['_id'])
    if "parent" in i.keys() and i['parent'] is not None:
        i['parent'] = ObjectId(i['parent'])
    else:
        i['parent'] = None
    MongodbModel(collection="subject", body=i).insert()
a.close()

a = open("base_app/scripts/category.json", "r")
x = json.loads(a.read())
for i in x:
    i['_id'] = ObjectId(i['_id'])
    MongodbModel(collection="category", body=i).insert()
a.close()

a = open("base_app/scripts/group.json", "r")
x = json.loads(a.read())
for i in x:
    i['_id'] = ObjectId(i['_id'])
    if "parent" in i.keys() and i['parent'] is not None:
        i['parent'] = ObjectId(i['parent'])
    else:
        i['parent'] = None
    MongodbModel(collection="group", body=i).insert()
a.close()

a = open("base_app/scripts/direction.json", "r")
x = json.loads(a.read())
for i in x:
    i['_id'] = ObjectId(i['_id'])
    MongodbModel(collection="direction", body=i).insert()
a.close()

a = open("base_app/scripts/geographic.json", "r")
x = json.loads(a.read())
for i in x:
    i['_id'] = ObjectId(i['_id'])
    if "parent" in i.keys() and i['parent'] is not None:
        i['parent'] = ObjectId(i['parent'])
    else:
        i['parent'] = None
    MongodbModel(collection="geographic", body=i).insert()
a.close()

a = open("base_app/scripts/agency.json", "r")
x = json.loads(a.read())
for i in x:
    i['_id'] = ObjectId(i['_id'])
    i['direction'] = ObjectId(i['direction'])
    i['category'] = ObjectId(i['category'])
    try:
        for l in i['links']:
            l['subject'] = ObjectId(l['subject'])
            l['group'] = ObjectId(l['group'])
            l['content'] = ObjectId(l['content'])
            l['geographic'] = ObjectId(l['geographic'])
            try:
                l['start_time'] = d_parser.parse(l['start_time'])
                l['end_time'] = d_parser.parse(l['end_time'])
            except:
                pass
    except:
        pass
    try:
        for r in i['rss_list']:
            r['subject'] = ObjectId(r['subject'])
            r['group'] = ObjectId(r['group'])
            r['content'] = ObjectId(r['content'])
            r['geographic'] = ObjectId(r['geographic'])
            try:
                r['start_time'] = d_parser.parse(r['start_time'])
                r['end_time'] = d_parser.parse(r['end_time'])
            except:
                pass
    except:
        pass
    try:
        for c in i['comparatives']:
            c['subject'] = ObjectId(c['subject'])
    except:
        pass
    MongodbModel(collection="agency", body=i).insert()
a.close()

a = open("base_app/scripts/setting.json", "r")
x = json.loads(a.read())
for i in x:
    i['_id'] = ObjectId(i['_id'])
    MongodbModel(collection="setting", body=i).insert()
a.close()
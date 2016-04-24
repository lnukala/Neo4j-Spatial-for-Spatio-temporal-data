from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
import requests
import json
import unicodedata
import urllib2
import urllib
#
# url = 'http://localhost:5000/withindist'
# payload = {"layer" : 'geom',  'lng':114.1080621, 'lat': 22.5426252, 'date' : '2015-08-17', 'distance':1}
# r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
# content = json.loads(r.content)
# print r.content
# sum = 0
# count = 0
# for object in content :
#     if 'value' in object['data']:
#         value = object['data'].get('value')
#         print(value)
#         sum += float(value)
#         count += 1
# print ("final value of the region is %f", sum/count)

# url = 'http://localhost:5000/boundingboxtemp'
# payload = {"start" : '2015-08-17', 'end' : '2015-08-20',  'maxlng':114.1080621, 'maxlat': 22.5426252, 'minlat' : 22.51, 'minlng' : 114.08}
# r = requests.post(url, data=json.dumps(payload))
# print r.status_code
# print r._content
# url = 'http://localhost:7474/db/data/cypher'
# payload = {"query" : "start node = node:cabfaibf('bbox:[113.79947662353516,114.12975311279297,22.522388566344084.22.655838847314328]') return node"}
# r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
# print r.content
# print r.status_code


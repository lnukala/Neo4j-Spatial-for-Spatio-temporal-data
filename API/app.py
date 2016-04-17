from flask import Flask
from flask_restful import  Resource, Api
import requests
import json


app = Flask(__name__)
api = Api(app)

#Run the within distance query and return the values in that circle
class WithinDistance (Resource):
    def get(self, lat, long, distance):
        url = 'http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/findGeometriesWithinDistance'
        payload = {"layer" : 'geom',  'pointX':lat, 'pointY': long, "distanceInKm" : distance}
        r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
        if r.status_code != 200:
            return r._content, r.status_code
        content = json.loads(r.content)
        sum = 0
        count = 0
        for object in content :
            if 'value' in object['data']:
                value = object['data'].get('value')
                print(value)
                sum += float(value)
                count += 1
        print ("final value of the region is %f", sum/count) #Take average
        return json.dumps({"value" : value})

class BBox (Resource):
    def get(self, minx , miny , maxx, maxy):
        url = 'http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/findGeometriesInBBox'
        payload = {"layer" : 'geom',  'miny':miny, 'maxy': maxy, 'minx':minx, 'maxx':maxx}
        r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
        if r.status_code != 200:
            return r._content, r.status_code
        content = json.loads(r.content)
        sum = 0
        count = 0
        for object in content :
            if 'value' in object['data']:
                value = object['data'].get('value')
                print(value)
                sum += float(value)
                count += 1
        print ("final value of the region is %f", sum/count) #Take average
        return json.dumps({"value" : value})


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
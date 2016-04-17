import csv
import requests
import json

headers = {'content-type': 'application/json'}

# Create geom index
url = "http://localhost:7474/db/data/index/node/"
payload= {
  "name" : "geom",
  "config" : {
    "provider" : "spatial",
    "geometry_type" : "point",
    "lat" : "lat",
    "lon" : "lon"
  }
}
r = requests.post(url, data=json.dumps(payload), headers=headers,  auth=('neo4j', '18843'))
if(r.status_code != 201):
    print "Error connecting to the index portal"

with open('gas_gps_150301_150331.csv', 'rU') as f:   # read data file
    reader = csv.reader(f)
    first = True
    datacount = 0
    for row in reader:
        #ignore the first entry
        if(first == True):
            first = False
            continue
        if(datacount >= 500):
            break

        # create pollution entry node
        url = "http://localhost:7474/db/data/node"
        payload = {'lon': float(row[8]), 'lat': float(row[9]), 'value': row[7]}
        print payload
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers, auth=('neo4j', '18843'))
            node = r.json()['self']
            print r.status_code
        except requests.ConnectionError:
            print "Error posting the data to the database"

        #add node to pollution index
        url = "http://localhost:7474/db/data/index/node/geom"
        payload = {'value': 'dummy', 'key': 'dummy', 'uri': node}
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers, auth=('neo4j', '18843'))
            print r.status_code
        except requests.ConnectionError:
            print "Error posting the data to the database"

        #add node to Spatial index
        url = "http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/addNodeToLayer"
        payload = {'layer': 'geom', 'node': node}
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers, auth=('neo4j', '18843'))
            print r.status_code
        except requests.ConnectionError:
            print "Error posting the data to the database"
        datacount = datacount + 1

    print "Completed data upload"
import csv
import requests
import json

file = raw_input('Enter name of file: ')
layer = file

headers = {'content-type': 'application/json'}

# Create geom index
url = "http://localhost:7474/db/data/index/node/"
payload= {
  "name" : layer,
  "config" : {
    "provider" : "spatial",
    "geometry_type" : "point",
    "lat" : "lat",
    "lon" : "lon",
    "co2" : "co2",
    "co"  : "co",
    "o3"  : "o3"
  }
}

lat_min = 22.4975
lon_min = 114.0025

co = []
co2 = []
o3 = []

r = requests.post(url, data=json.dumps(payload), headers=headers,  auth=('neo4j', '18843'))
if(r.status_code != 201):
    print "Error connecting to the index portal"

with open(file, 'rU') as f:   # read data file
    reader = csv.reader(f)
    first = True
    rowcount = 0
    for row in reader:
        column = 0
        while(column < 30):
            if rowcount < 20 :
                co.append(row[column])
            elif rowcount < 40 :
                co2.append(row[column])
            else:
                o3.append(row[column])
            column = column + 1
        rowcount = rowcount + 1

    index = 0;
    lat = lat_min
    count = 0
    for mono, dio, ozo in zip(co, co2, o3):
        if index % 30 == 0:
            lat = lat + 0.005
            lon = lon_min
         # create pollution entry node
        url = "http://localhost:7474/db/data/node"
        payload = {'lon': round(lon,5) , 'lat': round(lat,5), 'co' : mono, 'co2' : dio, 'o3' : ozo}
        count = count + 1
        lon = lon + 0.005
        index = index + 1

        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers, auth=('neo4j', '18843'))
            node = r.json()['self']
        except requests.ConnectionError:
           print "Error posting the data to the database"

        #add node to pollution index
        url = "http://localhost:7474/db/data/index/node/" + layer
        payload = {'value': 'dummy', 'key': 'dummy', 'uri': node}
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers, auth=('neo4j', '18843'))
        except requests.ConnectionError:
            print "Error posting the data to the database"

        #add node to Spatial index
        url = "http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/addNodeToLayer"
        payload = {'layer': layer, 'node': node}
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers, auth=('neo4j', '18843'))
        except requests.ConnectionError:
            print "Error posting the data to the database"

    print "Completed data upload"
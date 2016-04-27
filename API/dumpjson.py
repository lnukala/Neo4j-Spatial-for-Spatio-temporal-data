import json

payload = {"start" : '2015-08-17', 'end' : '2015-08-20',  'maxlng':114.1080621, 'maxlat': 22.5426252, 'minlat' : 22.51, 'minlng' : 114.08}
with open('boundingboxtemp.json', 'w') as outfile:
    json.dump(payload, outfile)
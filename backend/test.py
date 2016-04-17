import requests

r = requests.get("http://localhost:7474/db/data/", auth=('neo4j', '18843'))
print(r.text)
print(r.status_code)
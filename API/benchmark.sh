#!/bin/bash
ab -p boundingboxtemp.json -T application/json -c 1 -n 1 -H 'Authorization: Basic neo4j:18843' http://127.0.0.1:5000/boundingboxtemp/

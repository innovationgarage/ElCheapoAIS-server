#! /usr/bin/env python

import sys
import os
import json
import psycopg2

conn = psycopg2.connect(os.environ["DATABASE"])
cur = conn.cursor()

frequency = os.environ.get("FREQUENCY", 100)

for idx, line in enumerate(sys.stdin):
    line = json.loads(line)
    if not ("lat" in line and "lon" in line and "mmsi" in line):
        continue
    
    cur.execute("select count(*) from elcheapoais where mmsi=%s", (line["mmsi"],))
    if cur.fetchone()[0] > 0:
        cur.execute("update elcheapoais set the_geom=st_setsrid(st_point(%s, %s), 4326) where mmsi=%s",
                    (line["lon"], line["lat"], line["mmsi"]))
    else:
        cur.execute("insert into elcheapoais (mmsi, the_geom) VALUES (%s, st_setsrid(st_point(%s, %s), 4326))",
                    (line["mmsi"], line["lon"], line["lat"]))
    if idx % frequency == 0:
        print "commit"
        cur.execute("commit")
        
        

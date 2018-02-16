import os
import random
import string
import requests
import json

nativeURL = "http://localhost:5601/es_admin/.kibana/_mget"
HEADERS = {'Content-Type': 'application/json', 'kbn-xsrf': 'true', 'Host': 'localhost:5601',
'Connection': 'keep-alive', 'Accept': 'application/json'}

visURL = "http://localhost:5601/api/saved_objects/visualization?per_page=2000"

vis_list = requests.get(visURL, headers=HEADERS).json()['saved_objects']
oldName = input("Old index name: ")
newName = input("New index name: ")
for vis in vis_list:
    payload = "{\"docs\":[{\"_id\":\"" + vis['id'] + "\" ,\"_type\": \"visualization\"}]}"

    VIS = json.dumps(requests.post(nativeURL, json=json.loads(payload), headers=HEADERS).json())
    VIS = json.dumps(json.loads(VIS)['docs'][0]['_source']).replace(oldName, newName)

    POSTURL = "http://localhost:5601/es_admin/.kibana/visualization/" + vis['id']
    print("ERRORS: " + str(requests.post(POSTURL, json=json.loads(VIS), headers=HEADERS).raise_for_status()))


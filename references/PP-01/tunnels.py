import os
import json

with open('tunnel.json') as data_file:
    datajson = json.load(data_file)

for i in datajson['tunnels']:
    msg = i['public_url'] +'\n'
print(msg)
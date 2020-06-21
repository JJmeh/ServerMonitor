import os
import json
import subprocess
import sys

'''
check tunnel if it is up or not
arg use with either 4040 or 4041
script return False, ssh, or tcp
'''

a = sys.argv[1]

def curlTunnels(port):
    subprocess.call('curl -s http://localhost:{}/api/tunnels > Tunnel{}.json'.format(port, port), shell=True)
    return 'Tunnel{}.json'.format(port)

def loadData(file):
    if os.stat(file).st_size != 0:
        with open(file) as data_file:
            datajson = json.load(data_file)
        return datajson
    else:
        return None

def processData(data):
    if data != None:
        for i in data['tunnels']:
            b = i['public_url'].split('.')[2]
            if b == 'ap':
                return 'True.ssh'
            elif b == 'jp':
                return 'True.tcp'
            else:
                return 'error, {}'.format(b)
    else:
        return 'False.Empty'
        

if __name__ == "__main__":
    print(processData(loadData(curlTunnels(a))))
    subprocess.call('rm Tunnel{}.json'.format(a), shell=True)

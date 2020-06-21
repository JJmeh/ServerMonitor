import os
import json
import subprocess
import sys

'''
check if port [port_num] is used or not..
'''

def curlTunnels(port):
    subprocess.call('curl -s http://localhost:{}/api/tunnels > Tunnel{}.json'.format(port, port), shell=True)
    return 'Tunnel{}.json'.format(port)

def loadData(file):
    if os.stat(file).st_size != 0:
        return 'used'
    else:
        return None

def processData(data):
    if data != None:
        return 'False' # output this if port is used
    else:
        return 'True'
        

if __name__ == "__main__":
    print(processData(loadData(curlTunnels(4040))))
    subprocess.call('rm Tunnel{}.json'.format(4040), shell=True)

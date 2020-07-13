import subprocess
import sys
import time
import json


import google
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import json
from time import sleep

# Define the required scopes
scopes = [
  "https://www.googleapis.com/auth/userinfo.email",
  "https://www.googleapis.com/auth/firebase.database"
]

# Authenticate a credential with the service account
credentials = service_account.Credentials.from_service_account_file(
    "serviceAccountKey.json", scopes=scopes) #download the service account in firebase page, reference to firebase doc

# Use the credentials object to authenticate a Requests session.
authed_session = AuthorizedSession(credentials)

#response = authed_session.get("") // put server address here..

#testvar = json.loads(response.text)
#print(testvar)

serverAddr = "" #put server addr here

loop = True

f = open("config.txt", "r")
config = f.read().split('\n')
pwd = config[0].split(':')[1]
user = config[1].split(':')[1]
f.close()

#check if pwd file empty or not

if pwd == '':
    print('PASS value in config not filled')
    print('format: "PASS:YOURPASS"')
    sys.exit("exit code : 2")

#check if password is correct or not
m = subprocess.call('echo {} | sudo -S {}'.format(pwd, 'echo root'), shell=True)
if m == 1:
    print('wrong password, use correct password')
    sys.exit('exit code : 1')
elif m == 0:
    print("password correct")
else:
    sys.exit('meh, something must be wrong')

def getStatus():
    cpuPercentage = subprocess.getoutput("mpstat | awk '$12 ~ /[0-9.]+/ { print 100 - $12\"%\" }'")
    cpuTemp = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, 'tlp-stat -t | grep temp | awk \'{print $4}\''))
    storagePercent = subprocess.getoutput('df --output=pcent / | awk -F "%" "NR==2{print $1}"')
    batteryStatus = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, 'tlp-stat -b | grep status | awk \'{print $3 $4}\''))
    return cpuPercentage, cpuTemp, storagePercent, batteryStatus

while loop:
    print('')
    cpuPercentage, cpuTemp, storagePercent, batteryStatus = getStatus()
    cpuPercentage = cpuPercentage.split('%')[0].split(' ')[0]
    storagePercent = storagePercent.split('%')[0].split(' ')[1]
    print(cpuTemp, cpuPercentage, storagePercent, batteryStatus)
    data = {"temp": int(cpuTemp), "cpu": float(cpuPercentage), "batStatus": batteryStatus, "storage": float(storagePercent)}
    data = json.dumps(data)
    print(authed_session.patch(serverAddr, data=data))
    time.sleep(150) #change into 5 minute after finish
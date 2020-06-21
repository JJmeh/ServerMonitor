import os
import subprocess

from multiprocessing import Pool
import time
from firebase import firebase

# NOTE:
# add firebase database capability

firebase = firebase.FirebaseApplication('https://nyxserver-bb04f.firebaseio.com')

name = 'GNsMoN2koZWZKG7r2vJD'

webhook = 'https://nyxserverbot.herokuapp.com'
datawebhook = webhook + '/data'
pwd = '1910'


def sendData(data, webhook=datawebhook):
    subprocess.call("curl -X POST -H 'Content-type: application/text' --data '\"{}\"' {}".format(data, webhook), shell=True)
    
def tcpSend(url):
    print("\nSending tcp url to firebase database")
    result = firebase.put('/url', name, {"url": "{}".format(url)})
    return 'send done.. {}'.format(result)

def sshSend(url):
    sendData(url, 'http://localhost:5000/get')
    print('\nSending Url..')
    a = 'ap'
    c = url.split('.')[2]
    d = url.split(':')
    d1 = d[0]
    d2 = d[1]
    if c == 'jp':
        b = 'TCP'
    elif c == 'ap':
        b = 'SSH'
        print(c)
    else:
        return 'Error'
    sendData('{} -p {}'.format(d1, d2))

# -----------------------------------------

def startNgrok(port, region, port_num, name):
    print('\nStarting Ngrok....')
    url = subprocess.getoutput('./ngrokstart.sh {} {} {} {}'.format(port, region, port_num, name)).split('/')[-1]
    print('\nStart finish, url : ')
    print(url)
    return url

def killNgrokProcess(name):
    print('\nKilling Ngrok with name : {}'.format(name))
    subprocess.call("pkill -f {}".format(name), shell=True)

def killAllNgrok():
    print("\nKilling all ngrok process")
    subprocess.call("killall ngrok", shell=True)

def ngStart(port, region, port_num, name): #kill ngrok process, start ngrok, send ngrok link | every 8 hour
    print('\nSending Ngrok link and starting it..')
    if name == 'tcp':
        print('sending with tcpSend method')
        tcpSend(startNgrok(port, region, port_num, name))
    elif name == 'ssh':
        print('sending with sshSend method')
        sshSend(startNgrok(port, region, port_num, name))
    else:
        return 'it fucking broke again...'
    print('\nDone..')

# -----------------------------------------------

def rebootProcess():
    print('3 minutes..')
    sendData('3 minutes to reboot..')
    time.sleep(minuteTosecond(1))
    print('2 minutes..')
    time.sleep(minuteTosecond(1))
    print('1 minutes')
    time.sleep(minuteTosecond(1))
    sendData('rebooting server.')
    print('rebooting server..')
    subprocess.call('reboot', shell=True)


# -----------------------------------------------

def temp():
    temp = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, './tempCheck.sh'))
    return temp

def tempCheck():
    a = True
    while ( a == True ):
        temps = int(temp())
        if temps > 85:
            print('server is at > 75 degree')
            a = False
    print('Auto reboot in 3 minute...')
    rebootProcess()

#------------------------------------------------

def batStatus():
    status = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, './chargeStatus.sh'))
    return status

def checkBatStatus():
    status = batStatus()
    if status == 'Discharging':
        print('\nnot ok')
        return 'discharging'
    else:
        print('\nok')
        return 'charging'

def sendBatStatus():
    status = checkBatStatus()
    sendData(status)

# -----------------------------------

def checkIfPortOpen():
    a = subprocess.getoutput('python3 TunnelPortAvailable.py') #check if port 4040 is used or not
    if a == 'True':
        return 4040
    elif a == 'False':
        return 4041
    else:
        return a

# -----------------------------------

def checkIndividualNgrok(): # check each ngrok tunnel, if one is off, start it back up | run every 20 minute
    #check port 4040
    ap = 4040
    a = subprocess.getoutput('python3 CheckTunnels.py {}'.format(ap))
    a = a.split('.')
    # check port 4041
    bp = 4041
    b = subprocess.getoutput('python3 CheckTunnels.py {}'.format(bp))
    b = b.split('.')

    print(a)
    print(b)

    if a[0] == 'False':
        c = False
        print(c)
    else:
        c = True
        print(c)
    
    if b[0] == 'False':
        d = False
        print(d)
    else:
        d = True
        print(d)

    if c == True and d == True:
        return 'ok'
    elif c == True and d == False:
        #check what type of process is run in 4040
        if a[1] == 'ssh':
            #start TCP
            print('TCP')
            ngrokTCP()
        elif a[1] == 'tcp':
            #start ssh
            print('SSH')
            ngrokSSH()
        else:
            pass
    elif c == False and d == True:
        #check what type of process is run in 4041
        if b[1] == 'ssh':
            #start TCP
            print('TCP')
            ngrokTCP()
        elif b[1] == 'tcp':
            #start ssh
            print('SSH')
            ngrokSSH()
        else:
            pass
    elif c == False and d == False:
        print('BOTH')
        print('\nNgrok missing, starting it')
        ngStart(22, 'ap', 4040, 'ssh')
        print('\nSSH ngrok is UP..')
        ngStart(5000, 'jp', 4041, 'tcp')
        print('\nTCP ngrok is UP.....')
    else:
        print('ok')
        pass

    print(a, b, c, d)


def checkNgrok(): # check if ngrok is up or not | run every 30 minute
    status = str(subprocess.getoutput('./ngrokStatus.sh'))
    if status == '0':
        print('\nok')
        return 'ok'
    elif status == '1':
        print('\nNgrok missing, starting it')
        ngStart(22, 'ap', 4040, 'ssh')
        print('\nSSH ngrok is UP..')
        ngStart(5000, 'jp', 4041, 'tcp')
        print('\nTCP ngrok is UP.....')

def ngrokSSH(): # every 8 hour
    killNgrokProcess('ssh')
    ngStart(22, 'ap', checkIfPortOpen(), 'ssh')

def battery(): # every 15 minute
    status = checkBatStatus()
    if status == 'discharging':
        sendData("The server is {}, please plug it in.".format(status))

def ngrokTCP():
    killNgrokProcess('tcp')
    ngStart(5000, 'jp', checkIfPortOpen(), 'tcp')
    #add send to firebase database

# --------------------------------------------



def time_looper(a):
    while True:
        print('\nstarting function {} in {} sec on {}'.format(str(a[1]).split(' ')[1], a[0], time.ctime()))
        time.sleep(a[0]) # in second
        print('\nstarting function {}'.format(str(a[1]).split(' ')[1]))
        a[1]()
        print('\nfinish at {}'.format(time.ctime()))

def minuteTosecond(minute):
    second = minute * 60
    return second

def hourToSecond(hour):
    second = minuteTosecond(hour * 60)
    return second

def test1():
    print('TEST 1 done..')

def test2():
    print('TEST 2 done...')

def test3():
    print('TEST 3 done....')

def process_start(b):
    print('\nStarting function {} at {}'.format(str(b).split(' ')[1], time.ctime()))
    b()

def run_process(p):
    p[0](p[1])

def pool_handler():
    # this is final deploy timings.
    # a = minuteTosecond(30) | check ngrok
    # b = hourToSecond(8) | start ngrok ssh
    # c = minuteTosecond(10) | check battery
    # d = hourToSecond(8) | start ngrok tcp
    # e = minuteTosecond(5) | check individual tunnel

    #this is test timings
    a = hourToSecond(1)
<<<<<<< HEAD
<<<<<<< HEAD
    b = hourToSecond(4) + 10
=======
    b = hourToSecond(2) + 10
>>>>>>> 1c3a96c39b05c8287672b4b520f08e8d02d885d8
=======
    b = hourToSecond(8) + 10
>>>>>>> re stage
    c = minuteTosecond(10)
    d = hourToSecond(3)
    e = minuteTosecond(10)

    process = ([time_looper, [e, checkIndividualNgrok]], [time_looper, [d, ngrokTCP]], [time_looper, [a, checkNgrok]], [time_looper, [b, ngrokSSH]], [time_looper, [c, battery]], [process_start, tempCheck]) # in order = checkngrok, ngrok, battery 
    p = Pool(6)
    p.map(run_process, process)

if __name__ == "__main__":
    pool_handler()

import ntplib

import os
import time

timeDelta = None
isInitialized = False

def getTimestamp():
    global timeDelta, isInitialized
    if not isInitialized:
        raise Exception('You should initialize it first')

    return int(os.times().elapsed + timeDelta)


def updateTime():
    global timeDelta, isInitialized
    if os.times().elapsed == 0:
        print("Sorry, your platform isn't supported")
        exit(1)

    # get time from internet
    # maybe it needs to be repeated it in thread
    while timeDelta is None:
        try:
            if not os.path.exists('.last_timestamp'):
                with open('.last_timestamp', 'w') as f:
                    f.write(str(0))

            with open('.last_timestamp') as f:
                lastTimestamp = int(float(f.readline()))

            ntpClient = ntplib.NTPClient()
            ntpResponse = ntpClient.request('europe.pool.ntp.org')
            ntpTimestamp = ntpResponse.tx_time
            timeDelta = int(ntpTimestamp - os.times().elapsed)

            if int(ntpTimestamp) < lastTimestamp:
                print('some shit happened')
                exit(1)

            with open('.last_timestamp', 'w') as f:
                f.write(str(int(ntpTimestamp)))
        except Exception as ex:
            print('Error during getting time from NTP')
            raise ex
            time.sleep(1)

    print('time delta is ' + str(timeDelta))


def init():
    global timeDelta, isInitialized
    updateTime()
    isInitialized = True
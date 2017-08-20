import stem.process
from stem.util import term
import socket
import io
import pycurl
import random


class TorProcess:
    process = None
    port = 0
    controlPort = 0

    def __init__(self, process, port, controlPort):
        self.process = process
        self.port = port
        self.controlPort = controlPort

    def changeIP(self):
        try:
            tor_c = socket.create_connection(
                ('127.0.0.1', self.controlPort))
            tor_c.send('AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\n'.encode())
            response = tor_c.recv(1024)
            if response.decode() != '250 OK\r\n250 OK\r\n':
                print('Unexpected response from Tor control port: {}\n'
                      .format(response))
        except Exception as ex:
            # print('unable to change ip: ' + repr(ex))
            raise Exception('unable to change ip' + repr(ex))
        except:
            # print('some bad shit when changing ip')
            raise Exception('unable to change ip')


def printBootstrapLines(line):
    if "Bootstrapped " in line:
        print(term.format(line, term.Color.BLUE))


def spawnTorProcesses(
        count,
        startPort=30000,
        initMsgHandler=printBootstrapLines):

    if count < 1 or count > 10000 or startPort > 50000:
        raise Exception("count must be positive value \
                        or some other shit happened")

    processes = []

    for i in range(count):
        print('\\ port: ' + str(startPort))
        torProcess = stem.process.launch_tor_with_config(
            config={
                'SocksPort': str(startPort),
                'ControlPort': str(startPort+count),
                'DataDir': '/tmp/tor_' + str(startPort),
            },
            init_msg_handler=initMsgHandler,
            take_ownership=True
        )
        processes.append(TorProcess(torProcess, startPort, startPort + count))

        startPort += 1

    return processes


def query(url, port):
    output = io.BytesIO()

    query = pycurl.Curl()
    query.setopt(pycurl.URL, url)
    query.setopt(pycurl.PROXY, 'localhost')
    query.setopt(pycurl.PROXYPORT, port)
    query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
    query.setopt(pycurl.WRITEFUNCTION, output.write)
    try:
        query.perform()
        return output.getvalue()
    except pycurl.error as exc:
        raise Exception('error during making query: ' + url + ' ' + exc)
        # return "Unable to reach %s (%s)" % (url, exc)


NUMBER_OF_WORKERS = 0
threads = []
torProcesses = []
i = 0


def get(url, forceIpChanging=False):
    global NUMBER_OF_WORKERS, threads, torProcesses, i
    torProcess = torProcesses[i % NUMBER_OF_WORKERS]
    result = query(url, torProcess.port)
    if forceIpChanging or random.randint(0, 100) < 30:
        torProcess.changeIP()
    i += 1
    return result


def init(numberOfWorkers, startPort):
    global NUMBER_OF_WORKERS, threads, torProcesses, i
    NUMBER_OF_WORKERS = numberOfWorkers
    torProcesses = spawnTorProcesses(numberOfWorkers, startPort)


def clean(self):
    global NUMBER_OF_WORKERS, threads, torProcesses, i
    for item in self.torProcesses:
        item.process.kill()

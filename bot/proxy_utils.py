import requests
import re

PROXY_VALIDATE_REGEX = \
r'^(?P<protocol>[a-z0-9]+)://((?P<login>[a-zA-Z0-9_\.]+):(?P<password>[a-zA-Z0-9_\.]+)@)?(?P<domain>([a-z0-9_]+\.)+[a-z0-9_]+):(?P<port>[0-9]{1,5})/?$'

def getProxyDict(proxy):
    matches = re.match(PROXY_VALIDATE_REGEX, proxy)
    protocol = matches.group('protocol')
    rawProxy = matches.group('domain') + ':' + matches.group('port')
    proxiesTypesList = {
        'http': {
            'http': 'http://' + rawProxy,
            'https': 'https://' + rawProxy
        },
        'socks5': {
            'http': 'socks5://' + rawProxy,
            'https': 'socks5://' + rawProxy
        },
        'socks4': {
            'http': 'socks4://' + rawProxy,
            'https': 'socks4://' + rawProxy
        },
        'socks': {
            'http': 'socks://' + rawProxy,
            'https': 'socks://' + rawProxy
        }
    }
    try:
        return proxiesTypesList[protocol]
    except:
        return proxiesTypesList['http']


def getRandomUserAgent():
    # TODO: do it
    return 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'

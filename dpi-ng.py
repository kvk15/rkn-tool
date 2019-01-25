#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from urllib.parse import quote, urlsplit, urlunsplit
from xml.etree import cElementTree as ET

# Logging
logging.basicConfig(filename='dpi-ng.log', level=logging.ERROR)
log = logging.getLogger("log")


try:
    tree = ET.ElementTree(file='dump.xml')
    log.info('Try open file "dump.xml"')
except IOError:
    print('cannot open file')
    log.error('Cannot open file')
    exit(1)

IP=set()
NET=set()
Domain=set()
URL=set()
SSLURL=set()

root = tree.getroot()

for content in tree.findall('content'):
    blockType = content.get('blockType')
    # block ip and subnet
    if blockType == 'ip':
        for ip in content.findall('ip'):
            IP.add(ip.text)
    if blockType == 'ip':
        for net in content.findall('ipSubnet'):
            NET.add(net.text)
    # block domain
    elif blockType == 'domain':
        for name in content.findall('domain'):
            name = name.text.encode('idna').decode("utf-8")
            Domain.add(name)
    # block domain-mask
    elif blockType == 'domain-mask':
        for name in content.findall('domain'):
            name = name.text.encode('idna').decode("utf-8")
            Domain.add(name)
    else:
        for url in content.findall('url'):
            u=urlsplit(str(url.text))
            if u.scheme == 'http':
                usrc = url.text.replace('http://','')
                usrc = usrc.rsplit('#')[0]
                usrc = usrc.replace('\\','/')
                usrc = usrc.replace('"','')
                URL.add(usrc.encode().decode())
                uloc = u.netloc.encode('idna').decode("utf-8")
                upath = quote(str(u.path))
                uquery = quote(str(u.query))
                url = urlunsplit((u.scheme, uloc.lower(), upath, uquery, ''))
                url = url.rsplit('#')[0]
                url = url.replace('http://','')
                url = url.rstrip('.')
                url = url.replace('\\','/')
                url = url.replace('"','')
                url = url.replace('./','/')
                url = url.replace('/.','/')
                URL.add(url)
                #log.info(u.scheme)
            if u.scheme == 'https':
                log.info(u.scheme)
                log.info(u.netloc)
                SSLURL.add(u.netloc.encode('idna').decode("utf-8"))

#File
fIP=open('conf/ip','w')
fNet=open('conf/net','w')
fDomain=open('conf/domain', 'w')
fUrl=open('conf/url', 'w')
fSSLUrl=open('conf/sslurl', 'w')
fNet.write('ipset flush block_net\n')

for ip in IP:
    fIP.write(ip+'\n')
for net in NET:
    fNet.write('ipset add block_net '+net+'\n')
for domain in Domain:
    fDomain.write(domain+'\n')
    fSSLUrl.write(domain+'\n')
for url in URL:
    fUrl.write(url+'\n')
for ssl in SSLURL:
    fSSLUrl.write(ssl+'\n')

fUrl.close()
fSSLUrl.close()
fDomain.close()
fIP.close()
fNet.close()

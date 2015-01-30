#!/usr/bin/env python

import urllib3
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
import time

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs="/etc/ssl/certs/ca-certificates.crt"
)

host="www.google.nl"

pool = http.connection_from_host(host, scheme='https')
r = pool.urlopen('GET', '/')
print(pool)
print(http)
print(r.data)

print("========================================================================")
http2 = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs="/etc/ssl/certs/ca-certificates.crt"
)

time.sleep(5)
r = http.urlopen('GET', 'https://' + host + '/')
print(pool)
print(http)
print(r.data)

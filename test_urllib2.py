#!/usr/bin/env python

import httplib
import urllib2
import ssl
import pyopenssl

class CertValidatingHTTPSConnection(httplib.HTTPConnection):
    default_port = httplib.HTTPS_PORT

    def __init__(self, host, port=None, key_file=None, cert_file=None,
                             ca_certs=None, strict=None, **kwargs):
        httplib.HTTPConnection.__init__(self, host, port, strict, **kwargs)
        self.key_file = key_file
        self.cert_file = cert_file
        self.ca_certs = ca_certs
        self.cert_reqs = ssl.CERT_REQUIRED

    def connect(self):
        httplib.HTTPConnection.connect(self)
        hostname = self.host.split(':', 0)[0]
        self.sock = pyopenssl.ssl_wrap_socket(self.sock, keyfile=self.key_file,
                                    ssl_version=ssl.PROTOCOL_SSLv23,
                                    server_hostname=hostname,
                                    certfile=self.cert_file,
                                    cert_reqs=self.cert_reqs,
                                    ca_certs=self.ca_certs)
        cert = self.sock.getpeercert()
        if not cert or not cert.get('subjectAltName', ()):
            self.sock.close()
            print('Certificate has no `subjectAltName`');
            return None

class VerifiedHTTPSHandler(urllib2.HTTPSHandler):
    def __init__(self, **kwargs):
        urllib2.HTTPSHandler.__init__(self)
        self._connection_args = kwargs

    def https_open(self, req):
        def http_class_wrapper(host, **kwargs):
            full_kwargs = dict(self._connection_args)
            full_kwargs.update(kwargs)
            return CertValidatingHTTPSConnection(host, **full_kwargs)

        return self.do_open(http_class_wrapper, req)


if __name__ == "__main__":
    url = 'https://google.com'
    handler = VerifiedHTTPSHandler(ca_certs="/etc/ssl/certs/ca-certificates.crt")
    opener = urllib2.build_opener(handler, urllib2.ProxyHandler())
    a=opener.open(url).read()
    print(a)
    a=opener.open(url).read()
    print(a)


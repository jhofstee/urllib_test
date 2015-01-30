#!/usr/bin/env python

#import settings
from OpenSSL import SSL
import socket

def verify(conn, cert, errnum, depth, ok):
    # This obviously has to be updated
    print 'Got certificate: %s' % cert.get_subject()
    return ok

def password_callback(maxlen, verify, extra):
        print (maxlen, verify, extra)
        return settings.DEPOSIT_CODE

context = SSL.Context(SSL.SSLv23_METHOD)
context.set_verify(SSL.VERIFY_NONE, verify)
context.set_passwd_cb(password_callback)
#context.use_certificate_file(settings.CLIENT_CERT_FILE)
#context.use_privatekey_file(settings.PEM_FILE)

sock = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
sock.connect(("ccgxlogging.victronenergy.com", 443))

http_get_request = """
GET / HTTP/1.1


"""
sock.write(http_get_request)
print sock.recv(1000)

# 
#Connection.get_session()
#    Get a Session instance representing the SSL session in use by the connection, or None if there is no session.
#
#    New in version 0.14.
#Connection.set_session(session)
#
#    Set a new SSL session (using a Session instance) to be used by the connection.
#    New in version 0.14.


session = sock.get_session()


# again
sock = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
sock.set_session(session)
sock.connect(("ccgxlogging.victronenergy.com", 443))

http_get_request = """
GET / HTTP/1.1


"""
sock.write(http_get_request)
print sock.recv(1000)

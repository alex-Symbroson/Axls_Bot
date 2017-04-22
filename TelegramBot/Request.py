
from _socket import getaddrinfo, error as SocketError
from socket import socket as SOCKET
from ssl import SSLSocket
from json import loads
from Modules import ranint
try: from urllib.parse import urlencode
except: from urllib import urlencode

    # make multipart-formdata of dict with (file)tuples
def encode_multipart(fields):
    bnd = ''.join((lambda:'abcdefghijklmnopqrstuvwxyz0123456789'[ranint(36)])() for _ in range(32))
    s = ''
    
    for field in fields:
        s += '--%s\r\n' % bnd
        if type(fields[field]) == tuple:
            s += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (field, fields[field][0])
            s += 'Content-Type: text/plain\r\n\r\n%s\r\n' % fields[field][1].decode('latin-1')
        else: s += 'Content-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (field, fields[field])
    
    return ('%s--%s--\r\n' % (s, bnd)).encode('latin-1'), ('Content-Type', str('multipart/form-data; boundary=%s' % bnd))

    # class for http-requests
class Requests:
        # {host:socket} dict
    sockets = {}

        # send message to host
    def send(self, method, host, path='', asset={}):
        socket = self.sockets.get(host) or Request.createSocket(host)
        socket.requests += 1
        
            # if no (file)tuple in fields
        if asset and not any(type(v)==tuple for v in asset.values()):
                # add args to url: url?param1=value1&param2=value2...
            path += '?' + urlencode(asset)
            asset = {}

        body, header = encode_multipart(asset) if asset else ({}, ())

        socket.send(('%s /%s HTTP/1.1\r\nHost:%s' % (method, path, host) + 
                    ('\r\nContent-Length:%s' % len(body) if body else '') + # add body length if exists
                    ('\r\n%s:%s' % header if header else '') +              # add header if exists
                     '\r\n\r\n').encode('latin-1')
                    )

    
        if body: socket.send(body)
        
        fp = socket.makefile('rb') # create smth like a file to read the response
        length = None
        while True:
            line = fp.readline().replace(b'\r', b'').split(b':', 1)
            if line[0] in [b'\n', b'']: break                      # break because response content begins here
            if line[0] == b'Content-Length': length = int(line[1]) # needed because prog freezes when reading after eof
    
        response = fp.read(length).decode('latin-1') # read response
        del fp

            # reload socket because otherwise BrokenPipe error occures
        if socket.requests == 100:
            del socket
            socket = self.createSocket(host)
        return response

        # returns new socket
    def createSocket(self, host):
        try:
                # get available addresses from host
            conns = getaddrinfo(host, 443)
                # append for me working connection
            conns.append((2, 1, 6, '', ('149.154.167.199', 443)))
        except: raise Exception('No internet connection or wrong host')

            # try to make a socket with one of the connections
        for res in conns:
            try:
                af, socktype, proto, canonname, sa = res 
                socket = SOCKET(af, socktype, proto)
                socket.setsockopt(6, 1, 1)
                socket.connect(sa)
                    # save and return socket if successfully built
                if socket:
                    self.sockets[host] = SSLSocket(socket)
                    self.sockets[host].requests = 0
                    return self.sockets[host]
            except:
                pass
            # raise exception if none of the connections worked            
        if not 'sock' in locals(): raise Exception('no sockets available')

Request = Requests()

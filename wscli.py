#!/usr/bin/python
print "*Innus Ali* - THE CERTIFIED INFORMATION SECURITY EXPERT"
import sys
from twisted.application import strports 
from twisted.application import service
from twisted.internet    import protocol
from twisted.python      import log
from twisted.web.server  import Site
from twisted.web.static  import File

from txws import WebSocketFactory 

class Protocol(protocol.Protocol):
    def connectionMade(self):
        from twisted.internet import reactor
        log.msg("Launch a new process ")
        self.pp = ProcessProtocol()
        self.pp.factory = self
        reactor.spawnProcess(self.pp, sys.executable,
                             [sys.executable, '-u', 'client.py'])
    def dataReceived(self, data):
        log.msg("Redirect received Input ' password: %r" % data)
        self.pp.transport.write(data)
    def connectionLost(self, reason):
        self.pp.transport.loseConnection()

    def _send(self, data):
        self.transport.write(data) 


class ProcessProtocol(protocol.ProcessProtocol):
    def connectionMade(self):
        log.msg("connectionMade")

  
        log.msg("processExited")
    def processEnded(self, reason):
        log.msg("processEnded")

    def _sendback(self, data):
        self.factory._send(data)


application = service.Application("ws-cli")

_echofactory = protocol.Factory()
_echofactory.protocol = Protocol
strports.service("tcp:8076:interface=127.0.0.1",
                 WebSocketFactory(_echofactory)).setServiceParent(application)

resource = File('.') 
strports.service("tcp:8080:interface=127.0.0.1",
                 Site(resource)).setServiceParent(application)

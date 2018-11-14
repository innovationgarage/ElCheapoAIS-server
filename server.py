"""The most basic chat protocol possible.

run me with twistd -y chatserver.py, and then connect with multiple
telnet clients to port 1025
"""
from __future__ import print_function

from twisted.protocols import basic
import json
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import protocol
from twisted.application import service, internet


class MyChat(basic.LineReceiver):
    delimiter = '\n'
    
    def connectionMade(self):
        print("Got new client!")
        self.client_mode = None
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Lost a client!")
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        print("received", repr(line))
        answer = None
        try:
            if line.startswith("?"):
                cmd = json.loads(line[1:])
                try:
                    res = getattr(self, "cmd_" + cmd["method"])(**cmd["params"])
                    if "id" in cmd:
                        answer = {"id": cmd["id"], "result": res}
                except Exception as e:
                    if "id" in cmd:
                        answer = {"id": cmd["id"], "error": {"code": -32603, "message": unicode(e)}}
                    else:
                        answer = {"error": {"code": -32603, "message": unicode(e)}}
            else:
                if self.client_mode != "sender":
                    answer = {"error": {"message": "Not in sending mode"}}
                else:
                    for c in self.factory.clients:
                        if c.client_mode == "receiver":
                            c.message(line)
        except Exception as e:
            answer = {"error": {"code": -32603, "message": unicode(e)}}

        if answer is not None:
            self.message('?' + json.dumps(answer))
            
    def message(self, message):
        self.transport.write(message + b'\n')

    def cmd_mode(self, mode=None):
        self.client_mode = mode
        return True
        
    def cmd_connect(self, host, port):
        TCP4ClientEndpoint(reactor, host, port).connect(self.factory.client_factory)
        return True

factory = protocol.ServerFactory()
factory.protocol = MyChat
factory.clients = []
factory.client_factory = protocol.ClientFactory()
factory.client_factory.protocol = MyChat
factory.client_factory.clients = factory.clients

application = service.Application("chatserver")
internet.TCPServer(1025, factory).setServiceParent(application)

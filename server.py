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
import twisted.application.strports
import json


class FileOutput(object):
    def __init__(self, filename):
        self.file = open(filename, "w")
        self.client_mode = "receiver"
        
    def sendLine(self, line):
        self.file.write(line + "\n")
        self.file.flush()

    def __delete__(self):
        self.file.close()
    
class Multiplexer(basic.LineReceiver):
    delimiter = '\n'
    
    def connectionMade(self):
        print("Got new client!")
        self.client_mode = None
        self.factory.server.clients.append(self)

    def connectionLost(self, reason):
        print("Lost a client!")
        self.factory.server.clients.remove(self)

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
                    for c in self.factory.server.clients:
                        if c.client_mode == "receiver":
                            c.sendLine(line)
        except Exception as e:
            answer = {"error": {"code": -32603, "message": unicode(e)}}

        if answer is not None:
            self.sendLine('?' + json.dumps(answer))
            
    def cmd_mode(self, mode=None):
        self.client_mode = mode
        return True

class Server(object):
    def __init__(self):
        self.clients = []

with open("config.json") as f:
    config = json.load(f)

server = Server()
factory = protocol.ServerFactory()
factory.protocol = Multiplexer
factory.server = server

#client_factory = protocol.ClientFactory()
#client_factory.protocol = Multiplexer
#client_factory.server = server

application = service.Application("chatserver")
for conn in config["connections"]:
    if conn["type"] == "connect":
        twisted.application.internet.ClientService(
            twisted.internet.endpoints.clientFromString(
                reactor, str(conn["connect"])
            ), factory).setServiceParent(application)
    elif conn["type"] == "listen":
        twisted.application.strports.service(
            str(conn["listen"]), factory
        ).setServiceParent(application)
    elif conn["type"] == "file":
        server.clients.append(FileOutput(conn["filename"]))

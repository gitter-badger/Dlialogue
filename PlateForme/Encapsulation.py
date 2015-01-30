#-*- coding:utf-8 -*-
__author__ = 'baptiste'
import zmq
import time
from ServicesWeb import ServiceWebInput, ServiceWebOutput
from threading import Thread

#ports are meant to finally be in the directory
hubPort = "2000"
outputPort = "2001"

class Kanban :
    def __init__(self,orchestrationName):
        '''should initiate state thanks to the orchestrationName'''
        self.orchestrationName = orchestrationName
        self.state = ""
        self.idMessage = ""

class Encapsulateur:
    """Encapsulateur -- abstract"""
    pass

class EncapsulateurLocal(Encapsulateur):
    """Encapsule une fonction locale"""
    def __init__(self,context, port, worker):
      self.context = context
      socket = context.socket(zmq.PAIR)
      socket.bind("tcp://*:%s" % port)
    pass

class EncapsulateurExempleInput(Thread):
    """Encapsule une fonction input qui pourrait être un service web"""

    def __init__(self,context, port):
        Thread.__init__(self)
        self.context = context
        self.socket = context.socket(zmq.PUSH)
        self.socket.connect("tcp://127.0.0.1:%s" % hubPort)

    def run(self):
        print("coucou input")
        for lettre in "chaine":
            message = ServiceWebInput.main()
            print(message)
            self.socket.send(message.encode('utf8'))
            time.sleep(5)

class EncapsulateurExempleOutput(Thread):
    """Encapsule une fonction output qui pourrait être un service web"""

    def __init__(self,context, port):
        Thread.__init__(self)
        self.context = context
        self.socket = context.socket(zmq.PULL)
        self.socket.bind("tcp://127.0.0.1:%s" % outputPort)

    def run(self):
        # self.socket.bind("tcp://localhost:5557")
        while True:
            print ("Pret à recevoir")
            message = self.socket.recv()
            ServiceWebOutput.main(message)
        pass

class Hub(Thread):
    """Hub : Crossroad for the messages between carrefour encapsulators, then between workers. The hub is unique for a
       given context, then for an orchestration. Its port is 2000."""

    def __init__(self,context,orchestration,directory):
        Thread.__init__(self)

        self.orchestration = orchestration #the scxml file
        self.directory = directory #{} #directory : worker/port

        self.context = context

        self.universalInputSocket = context.socket(zmq.PULL)
        self.universalInputSocket.bind("tcp://127.0.0.1:%s" % hubPort)
        #self.universalInputSocket.bind("127.0.0.1:%s" % self.port)

        #temp : just a static unique port accessing an encapsulator
        self.outputSocket = context.socket(zmq.PUSH)
        self.outputSocket.connect("tcp://127.0.0.1:%s" % outputPort)


    def run(self):
        while True:
            message = self.universalInputSocket.recv()
            #shunt of the message : for now it's static
            self.outputSocket.send(message)








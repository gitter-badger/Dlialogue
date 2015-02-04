#-*- coding:utf-8 -*-
from Workers import ServiceWebInput

__author__ = 'baptiste'
import zmq
import time
from Workers import ServiceWebOutput
from threading import Thread

class Kanban :
    def __init__(self,orchestrationName):
        '''should initiate state thanks to the orchestrationName'''
        self.orchestrationName = orchestrationName
        self.idDialogue = ""
        self.state = ""
        self.idMessage = ""


class EncapsulatorWithInitiative(Thread):


    pass

class EncapsulatorWithoutInitiative(Thread):
    def __init__(self, context, hubPort, port, workerAddress):
        Thread.__init__(self)
        self.context = context
        self.listeningSocket = context.socket(zmq.PULL)
        self.listeningSocket.bind("tcp://127.0.0.1:%s" % port)
        self.sendingSocket = context.socket(zmq.PUSH)
        self.sendingSocket.connect("tcp://127.0.0.1:%s" % hubPort)
        self.workerAddress = workerAddress

    def run(self):
        print (self.workerAddress + " : Ready to work !")
        while True:
            message = self.listeningSocket.recv()

            #to be continued

            self.sendingSocket.send(message)
        pass

    pass

class EncapsulateurExempleInput(Thread):
    """Encapsule une fonction input qui pourrait être un service web"""

    def __init__(self,contexte, port):
        Thread.__init__(self)
        self.contexte = contexte
        self.socket = contexte.socket(zmq.PUSH)
        self.socket.connect("tcp://127.0.0.1:%s" % port)
        # self.socket.bind("tcp://localhost:%s" % port)

    def run(self):
        print("coucou input")
        for i in "chaine":
            message = ServiceWebInput.main()
            print("Input sending : ", message)
            self.socket.send(message.encode('utf8'))
            time.sleep(2)

class EncapsulateurExempleOutput(Thread):
    """Encapsule une fonction output qui pourrait être un service web"""
    def __init__(self,contexte, port):
        Thread.__init__(self)
        self.contexte = contexte
        self.socket = contexte.socket(zmq.PULL)
        self.socket.bind("tcp://127.0.0.1:%s" % port)
        # self.socket.bind("tcp://localhost:%s" % 1234)

    def run(self):
        print ("Output : Ready to receive")
        # self.socket.bind("tcp://localhost:5557")
        while True:
            message = self.socket.recv()
            print ("Output receiving : ", message)
            ServiceWebOutput.main(message)
        pass

class Hub(Thread):
    """Hub : Crossroad for the messages between carrefour encapsulators, then between workers. The hub is unique for a
       given context, then for an orchestration."""

    def __init__(self,context,orchestration,directory):
        Thread.__init__(self)

        self.orchestration = orchestration #the scxml file
        self.directory = directory #{} #directory : worker/port

        self.context = context

        self.universalInputSocket = context.socket(zmq.PULL)
        self.universalInputSocket.bind("tcp://127.0.0.1:%s" % directory["Exemple-Hub"])
        #self.universalInputSocket.bind("127.0.0.1:%s" % self.port)

        #temp : just a static unique port accessing an encapsulator
        self.outputSocket = context.socket(zmq.PUSH)
        self.outputSocket.connect("tcp://127.0.0.1:%s" % directory["Exemple-Output"])


    def run(self):
        #print (self.directory())
        while True:
            message = self.universalInputSocket.recv()
            #shunt of the message : for now it's static
            self.outputSocket.send(message)


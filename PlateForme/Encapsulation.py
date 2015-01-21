#-*- coding:utf-8 -*-
__author__ = 'baptiste'
import zmq
import time
from ServicesWeb import ServiceWebInput, ServiceWebOutput
from threading import Thread


class Encapsulateur:
    """Encapsulateur -- abstract"""
    pass

class EncapsulateurLocal(Encapsulateur):
    """Encapsule une fonction locale"""
    def __init__(self,contexte, port, worker):
      self.contexte = contexte
      socket = contexte.socket(zmq.PAIR)
      socket.bind("tcp://*:%s" % port)
    pass

class EncapsulateurExempleInput(Thread):
    """Encapsule une fonction input qui pourrait être un service web"""

    def __init__(self,contexte, port):
        Thread.__init__(self)
        self.contexte = contexte
        self.socket = contexte.socket(zmq.PAIR)
        self.socket.bind("tcp://127.0.0.1:%s" % 1235)
        # self.socket.bind("tcp://localhost:%s" % port)

    def run(self):
        print("coucou input")
        while True:
            message = ServiceWebInput.main()
            print(message)
            self.socket.send(message.encode('utf8'))
            time.sleep(5)

class EncapsulateurExempleOutput(Thread):
    """Encapsule une fonction output qui pourrait être un service web"""
    def __init__(self,contexte, port):
        Thread.__init__(self)
        self.contexte = contexte
        self.socket = contexte.socket(zmq.PAIR)
        self.socket.connect("tcp://127.0.0.1:%s" % 1235)
        # self.socket.bind("tcp://localhost:%s" % 1234)

    def run(self):
        # self.socket.bind("tcp://localhost:5557")
        while True:
            print ("Pret à recevoir")
            message = self.socket.recv()
            ServiceWebOutput.main(message)
        pass




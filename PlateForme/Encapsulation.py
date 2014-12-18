__author__ = 'baptiste'
import zmq
import time
from ServicesWeb import ServiceWebInput, ServiceWebOutput


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

class EncapsulateurExempleInput(Encapsulateur):
    """Encapsule une fonction input qui pourrait être un service web"""

    def __init__(self,contexte, port):
      self.contexte = contexte
      self.socket = contexte.socket(zmq.PAIR)
      self.socket.bind("tcp://*:%s" % port)

    def run(self):
        while True:
            message = ServiceWebInput.main()
            self.socket.send(message)
            time.sleep(5000)
        pass

class EncapsulateurExempleOutput(Encapsulateur):
    """Encapsule une fonction output qui pourrait être un service web"""
    def __init__(self,contexte, port):
      self.contexte = contexte
      self.socket = contexte.socket(zmq.PAIR)
      self.socket.bind("tcp://*:%s" % port)

    def run(self):
        while True:
            message = self.socket.recv()
            ServiceWebOutput.main(message)
        pass




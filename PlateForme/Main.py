__author__ = 'baptiste'
#-*- coding:utf-8 -*-
import zmq
from threading import Thread
from PlateForme.Encapsulation import EncapsulateurExempleOutput, EncapsulateurExempleInput, Hub

orchestrations = {}

class orchestration :
    '''orchestration defined with its state chart and its unique name as id'''
    def __init__(self,orchestrationStateChart,orchestrationName):
        self.orchestrationStateChart = orchestrationStateChart
        self.orchestrationName = orchestrationName #unique
        self.directory = {} #directory : worker/port
        #self.context ??

#Orchestrations Management : add/check/modify/delete

#Local Services Management : add/check/modify/delete

#Local Enconders Management : add/check/modify/delete

#Orchestrations Launcher : start/stop, threads management
def StartOrchestration(orchestration):
    pass

def StopOrchestration(orchestration):
    pass

def DemarrageProcessusExemple():
    '''as long as the orchestration management is not dynamic and the orchestration unique, this function will exist'''
    try:
        context = zmq.Context()

        print("salut les copains")

        #Instanciation du (d'un) point de sortie
        portOutput = "5557"
        # output = EncapsulateurExempleOutput(context, portOutput)
        threadOutput = EncapsulateurExempleOutput(context, portOutput)
        # Thread(target=output.run(), args=())

        #Instanciation de la suite du processus : PUSH PULL
        #Fusion/Fission -> zmq.PUB/SUB

        # #Instanciation du (d'un) point d'entrée
        portInput = "5556"
        # input = EncapsulateurExempleInput(context, portInput)
        threadInput = EncapsulateurExempleInput(context, portInput)
            # Thread(target=input.run(), args=())

        #Instanciation d'un hub
        threadHub = Hub(context,"","")

        #Démarrage des threads
        threadOutput.start()
        threadHub.start()
        threadInput.start()


        # Attend que les threads se terminent
        threadInput.join()
        threadOutput.join()

    except (RuntimeError, TypeError, NameError):
        print ("bringing down zmq device")
        pass

DemarrageProcessusExemple()





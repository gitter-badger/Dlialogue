__author__ = 'baptiste'
#-*- coding:utf-8 -*-
import zmq
import json
from collections import defaultdict
from threading import Thread
from PlateForme.Encapsulation import EncapsulateurExempleOutput, EncapsulateurExempleInput, Hub

#Orchestrations Management : add/check/modify/delete
#Local Services Management : add/check/modify/delete
#Local Enconders Management : add/check/modify/delete
#Orchestrations Launcher : start/stop, threads management

global idDialogueIncrement
idDialogueIncrement = 0
orchestrations = {"orchestrationName":"json"}

directory = {"encapsulationName":"address"}
forbiddenPorts = ["8080"]

idDialogueOrchestration = {"idDialogue":"orchestrationName"}
dialogueStates = {"idDialogue":"state"}


threads = {"orchestrationName":["thread1","thread2"]}

blackBoard = {"idDialogue":{"idTurn":{"attribut":"valeur"}}}

def initialization():
    '''reads folders, finds id max for idDialogueIncrement, checks that '''

    orchestrationName = "firstExample"
    path = "../Orchestrations/"+orchestrationName+".json"
    json_data=open(path).read()
    orchestration = json.loads(json_data)
    orchestrations.update ({orchestrationName : orchestration})
    # print(orchestrations[orchestrationName])


def getOrchestration(orchestrationName):
    path = "../Orchestrations/"+orchestrationName+".json"
    json_data=open(path).read()
    orchestration = json.loads(json_data)
    return orchestration

def addressPorts(orchestration):
    if "Hub" not in orchestrations :
        directory["Hub"] = "273"
    print (directory["Hub"])
    for state in orchestration["states"]:
            print (state)
            for substate in orchestration["states"][state]["parallelSubstates"]:
                print (substate)

def StartOrchestration(orchestration):
    print ("start")
    listeWorkers
    pass
def StopOrchestration(orchestration):
    pass

def LaunchingExample(orchestrationName):
    try:
        print("Launching static example")

        context = zmq.Context()

        path = "../Orchestrations/"+orchestrationName+".json"
        json_data=open(path).read()
        orchestration = json.loads(json_data)

        for state in orchestration["states"]:
            print (state)
            for substate in orchestration["states"][state]["parallelSubstates"]:
                print (substate)

        directory = {"Exemple-Hub":"4500", "Exemple-Output":"5556"}
        # output = EncapsulateurExempleOutput(context, portOutput)
        threadOutput = EncapsulateurExempleOutput(context, directory["Exemple-Output"])
        # Thread(target=output.run(), args=())
        #Instanciation de la suite du processus : PUSH PULL
        #Fusion/Fission -> zmq.PUB/SUB
        # input = EncapsulateurExempleInput(context, portInput)
        threadInput = EncapsulateurExempleInput(context, directory["Exemple-Hub"])
            # Thread(target=input.run(), args=())
        #Instanciation d'un hub
        threadHub = Hub(context,"",directory)
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

#     DemarrageProcessusExemple()
# orchestration = getOrchestration("firstExample")
# addressPorts(orchestration)
# LaunchingExample(orchestration)


initialization()
StartOrchestration(orchestrations["firstExample"])

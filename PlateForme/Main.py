__author__ = 'baptiste'
#-*- coding:utf-8 -*-
import zmq
import json
from collections import defaultdict
from threading import Thread
from PlateForme.Encapsulation import EncapsulatorWithoutInitiative, EncapsulatorWithInitiative, Hub

#Orchestrations Management : add/check/modify/delete
#Local Services Management : add/check/modify/delete
#Local Enconders Management : add/check/modify/delete
#Orchestrations Launcher : start/stop, threads management

forbiddenPorts = ["8080","80","22"]
global idDialogueIncrement
idDialogueIncrement = int()
orchestrations = {}
#orchestrations = {"orchestrationName":"jsonOrchestrationObject"}
threadsByOrchestration = {"orchestrationName":["threads"]}

directory = defaultdict(tuple)
#directory = {"encapsulator":"port"}
directory = {('_', 'ServiceWebOutput.py', ''):273}
print(list(directory.keys()))
print(list(directory.values()))


idDialogueOrchestration = {"idDialogue":"orchestrationName"}
dialogueStates = {"idDialogue":"state"}


threads = {"orchestrationName":["thread1","thread2"]}

blackBoard = {"idDialogue":{"idTurn":{"attribut":"valeur"}}}

def initialization():
    '''reads orc folder, finds id max for idDialogueIncrement. checks that ... ??'''
    #TODO : automatically get all json files in the Orchestrations folder
    path = "../Orchestrations/firstExample.json"
    json_data=open(path).read()
    orchestration = json.loads(json_data)
    orchestrationName = orchestration["orchestrationName"]
    orchestrations.update ({orchestrationName : orchestration})
    idDialogueIncrement = 0

def giveNewEncapsulatorsPorts(orchestrationEncapsulatorsDefaultDict):
    '''Ports not already in the global directory are added to it'''
     #arbitrary port
    # givenPort = "273"
    # for encapsulator in orchestrationEncapsulatorsDefaultDict :
    #     if encapsulator not in directory :
    #         while (givenPort in list(directory.values) or givenPort in forbiddenPorts):
    #             print(givenPort)
    #             givenPort+=1
    #             print(givenPort)
    #         directory[encapsulator] = givenPort

def createEncapsulatorsDict(orchestration):
    '''gives this orchestration's encapsulators dict with triplet [conversionIn,address,conversionOut]  and boolean
    saying if it has initiative'''
    encapsulatorsDict = defaultdict(tuple) #with triplet [conversionIn,address,conversionOut]  and boolean saying if it has initiative
    for state in orchestration["states"]:
        #the encapsulator tuple (=name) is created here : conversionIn/address/conversionOut
        workerAddress = orchestration["states"][state]["worker"]["address"]
        if 1 :
            conversionIn = "_"
        else:
            conversionIn = "_"
        conversionOut = "_"
        encapsulatorTuple = (conversionIn,workerAddress,conversionOut)
        if 'initiate' in orchestration["states"][state]["worker"]["type"]:
            encapsulatorsDict[encapsulatorTuple] = True
        else:
            encapsulatorsDict[encapsulatorTuple] = False
            pass
    return encapsulatorsDict

def StartOrchestration(orchestration):
    context = zmq.Context()
    encapsulatorsDict = createEncapsulatorsDict(orchestration)
    giveNewEncapsulatorsPorts(encapsulatorsDict)

    print(list(directory.keys()))
    print(list(directory.values()))

    #Threads Creation

    directoryV1 = {}
    directoryV1["hub"]=1
    directoryV1["semi"]=2
    directoryV1["semo"]=3
    directoryV1["dmanStart"]=4
    directoryV1["dmanUpdate"]=5
    directoryV1["dmanStop"]=6
    directoryV1["clientWeb"]=7
    orchestrationThreads = set()
    hubThread = Hub(context,orchestration,directoryV1)
    semiThread = EncapsulatorWithoutInitiative(context, directoryV1["hub"], directoryV1["semi"], "semiAddress")
    semoThread = EncapsulatorWithoutInitiative(context, directoryV1["hub"], directoryV1["semo"], "semoAddress")
    dmanStartThread = EncapsulatorWithoutInitiative(context, directoryV1["hub"], directoryV1["dmanStart"], "dmanStartAddress")
    dmanUpdateThread = EncapsulatorWithoutInitiative(context, directoryV1["hub"], directoryV1["dmanUpdate"], "dmanUpdateAddress")
    dmanStopThread = EncapsulatorWithoutInitiative(context, directoryV1["hub"], directoryV1["dmanStop"], "dmanStopAddress")
    clientWebThread = EncapsulatorWithInitiative(context, directoryV1["hub"], directoryV1["clientWeb"], "clientWebAddress")

    #Threads launching, hub first, initiative last


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

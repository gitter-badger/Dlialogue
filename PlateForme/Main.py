__author__ = 'baptiste'
#-*- coding:utf-8 -*-
import zmq
from threading import Thread
from PlateForme.Encapsulation import EncapsulateurExempleOutput, EncapsulateurExempleInput

def DemarrageProcessusExemple():
    try:
        contexte = zmq.Context()

        print("salut les copains")

        #Instanciation du (d'un) point de sortie
        portOutput = "5557"
        # output = EncapsulateurExempleOutput(contexte, portOutput)
        threadOutput = EncapsulateurExempleOutput(contexte, portOutput)
        # Thread(target=output.run(), args=())

        #Instanciation de la suite du processus : PUSH PULL
        #Fusion/Fission -> zmq.PUB/SUB

        # #Instanciation du (d'un) point d'entrée
        portInput = "5556"
        # input = EncapsulateurExempleInput(contexte, portInput)
        threadInput = EncapsulateurExempleInput(contexte, portInput)
            # Thread(target=input.run(), args=())

        #Démarrage des threads
        threadInput.start()
        threadOutput.start()

        # Attend que les threads se terminent
        threadInput.join()
        threadOutput.join()

    except (RuntimeError, TypeError, NameError):
        print ("bringing down zmq device")
        pass

# def main():
#     '''Moteur de threads'''
#
#     # Thread Ajout/suppression de config
#     # Pour l'instant, inexistant
#
#     # Thread de Démarrage/Arret d'une config
#     # Pour l'instant, démarrage simple ICI d'une fonction processus donné en exemple
#
#     DemarrageProcessusExemple()

DemarrageProcessusExemple()






#
# if __name__ == "__main__":
#     main()


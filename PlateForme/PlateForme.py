__author__ = 'baptiste'
import zmq
import threading
from PlateForme.Encapsulation import EncapsulateurExempleOutput, EncapsulateurExempleInput

#
#         thread.start()


def DemarrageProcessusExemple():
    try:
        contexte = zmq.Context()

        #Instanciation du (d'un) point de sortie
        portOutput = "5557"
        output = EncapsulateurExempleOutput(contexte, portOutput)
        thread = threading.Thread(target=output.run(), args=())

        #Instanciation de la suite du processus : PUSH PULL

        # #Instanciation du (d'un) point d'entrée
        portInput = "5556"
        input = EncapsulateurExempleInput(contexte, portInput)
        thread = threading.Thread(target=input.run(), args=())

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
#     # Pour l'instant, démarrage simple ici d'une fonction processus donné en exemple
#
#     DemarrageProcessusExemple()

DemarrageProcessusExemple()






#
# if __name__ == "__main__":
#     main()


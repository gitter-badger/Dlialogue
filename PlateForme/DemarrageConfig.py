__author__ = 'baptiste'

    #Instanciation dynamique de contexte : un par point d'entrée (et par processus si cela s'avérait pertinent)

    try:
        contexte = zmq.Context()

    #Instanciation point d'entrée
        worker1 = plateForme.encapsulateurLocalSWInput(contexte, 5556, "")





    #Instanciation de la suite du processus : PUSH PULL

    #Instanciation du (d'un) point de sortie

    except (RuntimeError, TypeError, NameError):
        print ("bringing down zmq device")
        pass

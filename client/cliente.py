from __future__ import print_function
import logging

import grpc
import socket
import time

import helloworld_pb2
import helloworld_pb2_grpc
import threading

# ----------------- VARIABLES GOLBALES DE CADA USUARIO ------------------------

index = []              # para acceder a variable global desde funciones
index.append(0)         # [0] numero actual 
index.append("")        # [1] nombre
index.append(False)     # [2] terminar procesos, True = terminar
index.append(-1)        # [3] ID asignado por servidors
index.append(0)         # [4] ID ultimo mensaje

# ----------------- --------------------------------- ------------------------
#--------------------------------   SEPARADOR    ------------------------------

def separador(oracion):             
    lista = oracion.split("$$##$$")
    final = ""
    for frase in lista:
        final = final + frase + "\n"
    return final[:-2]

# ----------------- --------------------------------- ------------------------
# ----------------- --------------------------------- ------------------------
# ----------------- --------THREAD 1 Hablar --------- ------------------------

def hablar():
    print("Bienvenido, por favor, escribe tu nombre:")

    while index[3] == -1:
        nombre = input()
        index[1] = nombre
        mensaje = ""
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = helloworld_pb2_grpc.GreeterStub(channel)
            joining = "El usuario " + nombre + " quiere unirse al chat" 
            response = stub.SayHello(helloworld_pb2.HelloRequest(name=nombre, mensaje=joining))

                # NOMBRE INCORRECTO
            if response.message == "ya existe usuario con ese nombre, vuelva a intentarlo":
                print("nombre ya escogido. Debe escoger otro nombre")

            else:     # Buen nombre

                index[3] = int(response.message)
                print("Puede comenzar a escribir  (@historial: Ver tus mensajes / @users: Ver usuarios conectados / @salir: Para cerrar)")

    #   Primer ciclo. Autentificacion 

    while True:
        
        mensaje = input()
        mensaje = nombre +": " + mensaje
        if mensaje != nombre + ": @salir":

                    #Funcion Historial

            if mensaje == nombre + ": @historial":      
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = helloworld_pb2_grpc.GreeterStub(channel)
                    response = stub.talk(helloworld_pb2.HelloRequest(name=nombre, mensaje = "$$historial$$", idmensaje = index[4]))
                    index[4] = index[4] + 1
                    print("-----------------------------------")
                    print("\nEste es tu historial\n")
                    print(separador(response.message))

                    #Funcion Todos los usuarios

            if mensaje == nombre + ": @users":      
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = helloworld_pb2_grpc.GreeterStub(channel)
                    response = stub.talk(helloworld_pb2.HelloRequest(name=nombre, mensaje = "$$users$$", idmensaje = index[4]))
                    index[4] = index[4] + 1
                    print("-----------------------------------")
                    print("\nUsuarios en servidor \n")
                    print(separador(response.message))

                    # mensaje NORMAL
            else:
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = helloworld_pb2_grpc.GreeterStub(channel)
                    response = stub.talk(helloworld_pb2.HelloRequest(name=nombre, mensaje = mensaje, idmensaje = index[4]))
                    index[4] = index[4] + 1

                    # mensaje SALIR
        else:
            print("hasta la proxima!")
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = helloworld_pb2_grpc.GreeterStub(channel)
                response = stub.talk(helloworld_pb2.HelloRequest(name=nombre, mensaje = "salio de la conversacion", idmensaje = index[4]))
                index[4] = index[4] + 1
                index[2] = True
                break

# ----------------- --------------------------------- ------------------------
# ----------------- --------------------------------- ------------------------
# ----------------- --------THREAD 2 Escuchar --------- ------------------------

def escuchar():
    while index[1] == "":
        time.sleep(0.1)
    name = index[1]
    namelong = len(name)

    while True:
        if index[2]:        # terminar procesos, cambia cuando escriben "salir"
            break   
        
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = helloworld_pb2_grpc.GreeterStub(channel)
            time.sleep(1)                           #para que no imprima infinitamente
            response= stub.answering(helloworld_pb2.ultimoLeido(numeroMensaje = index[0]))
            auxIndex = index[0]                     #ultimo mensaje escuchado por usuario
            auxMensaje = str(response)              # se pasa mensaje string(no se en que tipo de dato viene)
            msm = auxMensaje.split("###")           
            index[0] = auxIndex + int(msm[1][:-2])       #msm = lista, 1ro mensaje, 2do nuevo valor index[0] (ultimo valor leido)
            mostrar = str(msm[0][17:])
            if int(msm[1][:-2]) != 0:
                final = separador(mostrar)
                if final[:namelong] != name:
                    print(final)

# ----------------- --------------------------------- ------------------------
# ----------------- --------------------------------- ------------------------
# ----------------- --------------------------------- ------------------------
# ----------------- --------------------------------- ------------------------

if __name__ == '__main__':
    logging.basicConfig()
    threadingHablar = threading.Thread(target=hablar)
    threadingHablar.start()

    threadingEscuchar = threading.Thread(target=escuchar)
    threadingEscuchar.start()

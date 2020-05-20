from concurrent import futures
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc
from datetime import datetime

# --------- VARIABLES GLOBALES DE SERVIDOR ---------
# -------------------------------------------------

mensajes = []
totalMensajes = 0
usuariosID = []

# -------------------------------------------------
# -------------------------------------------------

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    # ----------------------- BIENVENIDA A USUARIO ---------------------------------------

    def SayHello(self, request, context):
        print(request.mensaje)
        log = open("log.txt","a") 
        log.write(request.mensaje + "\n" )
        log.close()
        mensajes.append(request.mensaje)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if request.name not in usuariosID:
            usuariosID.append(request.name)
            numeroUsuario = str(usuariosID.index(request.name))
            print ("el usuario " + request.name + " se ha unido al chat")
            log = open("log.txt","a") 
            log.write("el usuario " + request.name + " se ha unido al chat         TIME: "+ current_time + "\n")
            log.close()
            return helloworld_pb2.HelloReply(message = numeroUsuario)
        else:
            print ("el usuario " + request.name + " NO ENTRO")
            log = open("log.txt","a") 
            log.write("el usuario " + request.name + " No entro al chat         TIME: "+ current_time +"\n")
            log.close()
            return helloworld_pb2.HelloReply(message="ya existe usuario con ese nombre, vuelva a intentarlo")
            
    # ----------------------- RECEPCION MENSAJES / FUNCIONES ESPECIALES  ---------------------------------------

    def talk(self, request, context):
        print(request.mensaje)
        log = open("log.txt","a") 
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        mensajeid =  str(usuariosID.index(request.name)) +"."+ str(request.idmensaje)
        print(mensajeid)
        log.write(request.mensaje + "        ID:" + str(mensajeid)+ "       TIME: " +current_time+"\n" )
        log.close()

            #Funcion HISTORIAL

        if request.mensaje == "$$historial$$":
            historial = ""
            nombre = request.name
            largo = len(nombre)
            for texto in mensajes:
                if texto[:largo] == nombre:
                    historial = historial + texto + "$$##$$"
            return helloworld_pb2.HelloReply(message= historial )

            #Funcion Todos los usuario

        elif request.mensaje == "$$users$$":
            todosUsuarios = ""
            for u in usuariosID:
                todosUsuarios = todosUsuarios + "*Usuario: " + u + "    *ID: " + str(usuariosID.index(u)) + "$$##$$"
            return helloworld_pb2.HelloReply(message= todosUsuarios )


            #Mensaje normal

        else:
            mensajes.append(request.mensaje)
            return helloworld_pb2.HelloReply(message='%s: %s' % (request.name , request.mensaje))


    # ----------------------- RESPUESTAS ---------------------------------------

    def answering(self, request, context):
        respuesta = ""
        diferencia  = len(mensajes)  - request.numeroMensaje
        if diferencia != 0:
            for linea in range(0,diferencia):
                respuesta = respuesta + mensajes[(request.numeroMensaje + linea)] + "$$##$$"
        return helloworld_pb2.respuestaLeido(actualizarChat = '%s###%s' % (respuesta, diferencia))
        
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

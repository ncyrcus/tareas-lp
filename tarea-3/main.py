#!/usr/bin/env python
from instagram_api import InstagramAPI
from gui import Login, Search, Profile, Photo
from fetcher import WebFetch
from gui import *
import webbrowser

#WebFetch lo que hace es descargar cualquier tipo de archivo al disco
#f = WebFetch()
#f.retrieve(<urldelaimagen>)
# retrieve retorna la ruta absoluta a una imagen por ejemplo
# retrieve tiene algo especial, es que si ya existe una imagen en el disco
# y retrieve sabe que ya existe, entonces no la va a volver a descargar
# durante la ejecucion del programa por supuesto

# InstagramAPI funciona llamando a call_resource
# call_resource(contexto, query, parametros, info_adicional ...)
# contexto y query deben ser strings (vease la implementacion)
# el contexto es la seccion de la api, si pertenece a usuario o media o comentario, etc
# query es el llamado dentro del contexto, que necesita saber de ese contexto
# parametros debe ser un diccionario clave: valor
# donde cada set key-value deben coincidir con los parametros de la api de instagram
# info_adicional es **kwargs (argumentos keyword), se asignan clave=valor, de preferencia deben ser string
# esto es para ciertos valores que van en la url con %(clave)s
# deben ser completados siempre! a menos que la url no lo pida

#OJO: InstagramAPI solo debe ser instanciado 1 vez por programa
#porque no pueden existir varios codigos corriendo simultaneamente
#es una limitacion de seguridad que impone Instagram

#el code-decode json esta implicito, no hay para que tocarlo
#call_resource retorna todo en diccionario, decodificado y listo para servir

#ESTAN TODAS LAS HERRAMIENTAS, USELAS CON RESPONSABILIDAD!


#Se puede ejecutar este ejemplo para ver como funciona todo
if __name__ == '__main__':
        #NOTA: Al principio se vera este codigo en la terminal
        #hay que loguearse (o estar logueado) en Instagram
        #e ir a la direccion y copiar y pegar el codigo en la terminal
        #(para eso esta el raw_input)
        
        url = 'https://instagram.com/oauth/authorize/?client_id=b4a37965871b48f79e5365fa097f8e24&scope=relationships&redirect_uri=http://neopixel.org&response_type=code'
        webbrowser.open(url,new=2)

        root = Tk()
        root.geometry("550x450+150+150")
        app = Login(root)
        root.mainloop()  

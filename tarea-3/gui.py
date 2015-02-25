#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from Tkinter import RAISED, BOTH, LEFT, END, RIGHT
from ttk import Frame, Style, Label, Button, Entry
from PIL import Image, ImageTk
from instagram_api import InstagramAPI
from fetcher import WebFetch

GlobalID = ''


class Login(Frame):
    """******** Funcion: __init__ **************
    Descripcion: Constructor de Login
    Parametros:
    self Login
    parent Tk
    Retorno: void
    *****************************************************"""
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()


    """******** Funcion: initUI **************
    Descripcion: Inicia la interfaz grafica de un Login,
                para ello hace uso de Frames y Widgets.
    Parametros:
    self Login
    Retorno: void
    *****************************************************"""
    def initUI(self):
        self.parent.title("Pythagram: Login")
        self.style = Style()
        self.style.theme_use("default")

        self.frame = Frame(self, relief=RAISED)
        self.frame.pack(fill=BOTH, expand=1)
        self.instructions = Label(self.frame,text="A new Web Browser window will open, you must log-in and accept the permissions to use this app.\nThen you have to copy the code that appears and paste it on the next text box.")
        self.instructions.pack(fill=BOTH, padx=5,pady=5)
        self.codeLabel = Label(self.frame,text="Code:")
        self.codeLabel.pack(fill=BOTH, padx=5,pady=5)
        self.codeEntry = Entry(self.frame)
        self.codeEntry.pack(fill=BOTH, padx=5,pady=5)
        self.pack(fill=BOTH, expand=1)

        self.closeButton = Button(self, text="Cancel", command=self.quit)
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)
        self.okButton = Button(self, text="OK", command=self.login)
        self.okButton.pack(side=RIGHT)

    """******** Funcion: login **************
    Descripcion: Luego que el usuario ingresa su codigo de acceso, hace
                la solicitud al servidor para cargar su cuenta en una
                ventana de tipo Profile
    Parametros:
    self
    Retorno: Retorna...
    *****************************************************"""
    def login(self):
        code = self.codeEntry.get()
        api = InstagramAPI(code)
        raw = api.call_resource('users', 'info', user_id='self')
        data = raw['data']
        self.newWindow = Toplevel(self.parent)
        global GlobalID
        GlobalID = data['id']
        p = Profile(self.newWindow,api,data['id'])

class Profile(Frame):
    """******** Funcion: __init__ **************
    Descripcion: Constructor de Profile
    Parametros:
    self Profile
    parent Tk
    api InstagramAPI
    id str
    Retorno: void
    *****************************************************"""
    def __init__(self,parent,api,id):
        Frame.__init__(self, parent)
        self.parent = parent
        self.api = api
        self.id = id
        raw = self.api.call_resource('users', 'info', user_id=self.id)
        data = raw['data']
        self.initUI(data['username'],data['bio'],data['profile_picture'],data['full_name'],data['counts']['followed_by'],data['counts']['follows'])

    """******** Funcion: initUI **************
    Descripcion: Funcion que inicia un perfil de usuario de Instagram,
                muestra su foto de perfil nombre y bio, botones para ir a sus 
                seguidores o a quien sigue, botones para seguir o dejar
                de hacerlo (si no es el mismo usuario), un listado con
                el nombre de cada una de sus fotos y un boton de busqueda.
    Parametros:
    self Profile
    name str
    prof_picture str
    full_name str
    followed str
    follows str
    Retorno: void
    *****************************************************"""
    def initUI(self,name,bio,prof_picture,full_name,followed,follows):
        self.parent.title("Pythagram: "+name)
        self.style = Style()
        self.style.theme_use("default")

        headerFrame = Frame(self,relief=RAISED)
        headerFrame.pack(fill=BOTH, expand=1)

        #Profile Picture
        f = WebFetch()
        prof_picture = "http://images.ak.instagram.com/profiles/" + prof_picture.replace('http:http://images.ak.instagram.comimages.ak.instagram.com/profilesprofiles/','')

        profpict = Image.open(f.retrieve(prof_picture))
        profilePicture = ImageTk.PhotoImage(profpict)
        label2 = Label(headerFrame, image=profilePicture)
        label2.image = profilePicture
        label2.pack(side=LEFT,padx=5, pady=5)

        #ProfileName
        FullName = Label(headerFrame, text=full_name)
        FullName.pack(side=LEFT)
        
        #PersonalInfo
        bioFrame = Frame(self,relief=RAISED)
        bioFrame.pack(fill=BOTH, expand=1)
        bio = Label(bioFrame, text=bio)
        bio.pack(side=LEFT, padx=5, pady=5)

        #Followers/Following
        followFrame = Frame(self,relief=RAISED)
        followFrame.pack(fill=BOTH, expand=1)
        followersButton = Button(followFrame, text="Followers: "+str(followed), command=self.followed)
        followingButton = Button(followFrame, text="Following: "+str(follows), command=self.follows)
        followersButton.pack(side=LEFT, padx=5, pady=5)
        followingButton.pack(side=LEFT, padx=5, pady=5)

        #Follow/Unfollow
        global GlobalID
        if (self.id != GlobalID):
            joinFrame = Frame(self,relief=RAISED)
            joinFrame.pack(fill=BOTH, expand=1)
            if (self.api.call_resource('users','relationship', user_id=self.id)['data']['outgoing_status'] == "none"):
                followButton = Button(joinFrame, text="Follow", command=self.follow)
                followButton.pack(side=LEFT, padx=5, pady=5)
            else:
                unfollowButton = Button(joinFrame, text="Unfollow", command=self.unfollow)
                unfollowButton.pack(side=LEFT, padx=5, pady=5)

        #Photo List
        photoFrame = Frame(self,relief=RAISED)
        photoFrame.pack(fill=BOTH, expand=1)
        raw = self.api.call_resource('users', 'recent', user_id=self.id)
        data = raw['data']
        lb = Listbox(photoFrame, width=100)
        self.photos = []
        for element in data:
            try:
                lb.insert(END, element['caption']['text'])
            except:
                continue
            self.photos.append(element['id'])
        lb.bind("<<ListboxSelect>>", self.onSelect)
        lb.pack(side=LEFT, padx=5, pady=5)

        self.pack(fill=BOTH, expand=1)

        searchButton = Button(self, text="Search", command=self.search)
        searchButton.pack(side=RIGHT, padx=5, pady=5)


    """******** Funcion: follow **************
    Descripcion: Realiza la petición al servidor de seguir el
                perfil actual
    Parametros:
    self Profile
    Retorno: void
    *****************************************************"""
    def follow(self):
        p = { "action": "follow" }
        request = self.api.call_resource('users','relationship', user_id=self.id, params=p, apimethod='post')


    """******** Funcion: unfollow **************
    Descripcion: Realiza la petición al servidor de dejar seguir al
                perfil actual
    Parametros:
    self Profile
    Retorno: void
    *****************************************************"""
    def unfollow(self):
        p = { "action": "unfollow" }
        request = self.api.call_resource('users','relationship', user_id=self.id, params=p, apimethod='post')

    """******** Funcion: followed **************
    Descripcion: crea una nueva ventana con los seguidores
                de la cuenta actual
    Parametros:
    self Profile
    Retorno: void
    *****************************************************"""
    def followed(self):
        self.newWindow = Toplevel(self.parent)
        f = Follow(self.newWindow,"followed-by",self.api,self.id)
        
    """******** Funcion: follows **************
    Descripcion: crea una nueva ventana con las personas
                a las que sigue la cuenta actual
    Parametros:
    self Profile
    Retorno: void
    *****************************************************"""
    def follows(self):
        self.newWindow = Toplevel(self.parent)
        f = Follow(self.newWindow,"follows",self.api,self.id)

    """******** Funcion: onSelect **************
    Descripcion: crea una nueva accion cuando un elemento
                de la lista de fotos es presionado y lo muestra
                en una nueva ventana
    Parametros:
    self Profile
    val
    Retorno: void
    *****************************************************"""
    def onSelect(self,val):
        sender = val.widget
        idx = sender.curselection()
        self.newWindow = Toplevel(self.parent)
        p = Photo(self.newWindow,self.api,self.photos[int(idx[0])])

    """******** Funcion: search **************
    Descripcion: crea una nueva ventana para buscar a personas
                por su nombre o nick
    Parametros:
    self Profile
    Retorno: void
    *****************************************************"""
    def search(self):
        self.newWindow = Toplevel(self.parent)
        s = Search(self.newWindow,self.api,self.id)


class Search(Frame):
    """******** Funcion: __init__ **************
    Descripcion: Constructor de Search
    Parametros:
    self Search
    parent Tk
    api InstagramAPI
    id str
    Retorno: void
    *****************************************************"""
    def __init__(self,parent,api,id):
        Frame.__init__(self, parent)
        self.parent = parent
        self.api = api
        self.id = id
        self.anySearch = False
        self.initUI()

    """******** Funcion: initUI **************
    Descripcion: Crea una nueva ventana de busqueda con un
                text box y un boton
    Parametros:
    self Search
    Retorno: void
    *****************************************************"""
    def initUI(self):
        self.parent.title("Pythagram: Search")
        self.style = Style()
        self.style.theme_use("default")

        self.frame = Frame(self,relief=RAISED)
        self.frame.pack(fill=BOTH, expand=1)
        searchLabel = Label(self.frame, text="Search")
        self.searchEntry = Entry(self.frame)
        searchLabel.pack(fill=BOTH, padx=5,pady=5)
        self.searchEntry.pack(fill=BOTH, padx=5,pady=5)
        self.pack(fill=BOTH, expand=1)

        okButton = Button(self, text="OK", command=self.search)
        okButton.pack(side=RIGHT, padx=5, pady=5)

    """******** Funcion: search **************
    Descripcion: realiza la busqueda en el servidor segun el
                texto ingresado en el campo de texto
    Parametros:
    self Search
    Retorno: void
    *****************************************************"""
    def search(self):
        if (self.anySearch):
            self.lb.pack_forget()
        query = self.searchEntry.get()
        p = { "q": query}
        raw = self.api.call_resource('users', 'search', params=p)
        data = raw['data']
        self.results = []
        self.lb = Listbox(self.frame, width=100)
        for element in data:
            try:
                self.lb.insert(END, "@{0}: {1}".format(element['username'],element['full_name']))
            except:
                continue
            self.results.append(element['id'])
        self.lb.bind("<<ListboxSelect>>", self.onSelect)
        self.lb.pack(side=LEFT, padx=5, pady=5)
        self.pack(fill=BOTH, expand=1)
        self.anySearch = True

    """******** Funcion: onSelect **************
    Descripcion: abre una nueva ventana con el perfil seleccionado
                en la lista de resultados
    Parametros:
    self Profile
    val
    Retorno: void
    *****************************************************"""
    def onSelect(self,val):
        sender = val.widget
        idx = sender.curselection()
        self.newWindow = Toplevel(self.parent)
        p = Profile(self.newWindow,self.api,self.results[int(idx[0])])



class Follow(Frame):
    """******** Funcion: __init__ **************
    Descripcion: Constructor de Follow
    Parametros:
    self Follow
    parent Tk
    api InstagramAPI
    id str
    Retorno: void
    *****************************************************"""
    def __init__(self,parent,tipo,api,id):
        Frame.__init__(self, parent)
        self.parent = parent
        self.api = api
        self.id = id
        self.initUI(tipo)

    """******** Funcion: initUI **************
    Descripcion: crea una nueva ventana con los seguidores
                o a quienes sigue la cuenta actual, para ello
                se hace uso de una lista con todos ellos.
    Parametros:
    self Follow
    tipo str
    Retorno: void
    *****************************************************"""
    def initUI(self,tipo):
        if (tipo == "followed-by"):
            self.parent.title("Pythagram: Followers")
        else:
            self.parent.title("Pythagram: Follows")
        self.style = Style()
        self.style.theme_use("default")

        profilesFrame = Frame(self,relief=RAISED)
        profilesFrame.pack(fill=BOTH, expand=1)
        raw = self.api.call_resource('users', tipo, user_id=self.id)
        data = raw['data']
        self.follows = []
        lb = Listbox(profilesFrame, width=100)
        for element in data:
            try:
                lb.insert(END, "@{0}: {1}".format(element['username'],element['full_name']))
            except:
                continue
            self.follows.append(element['id'])
        lb.bind("<<ListboxSelect>>", self.onSelect)
        lb.pack(side=LEFT, padx=5, pady=5)

        self.pack(fill=BOTH, expand=1)

    """******** Funcion: onSelect **************
    Descripcion: abre el perfil de la persona seleccionada
                en la lista de seguidores o personas a las
                que sigue la cuenta
    Parametros:
    self Follow
    val
    Retorno: void
    *****************************************************"""
    def onSelect(self,val):
        sender = val.widget
        idx = sender.curselection()
        self.newWindow = Toplevel(self.parent)
        p = Profile(self.newWindow,self.api,self.follows[int(idx[0])])


class Photo(Frame):
    """******** Funcion: __init__ **************
    Descripcion: constructor de Photo
    Parametros:
    self Photo
    parent Tk
    api InstagramAPI
    id str
    Retorno: void
    *****************************************************"""
    def __init__(self, parent, api, id):
        Frame.__init__(self, parent)
        self.parent = parent
        self.id = id
        self.api = api
        self.initUI()

    """******** Funcion: initUI **************
    Descripcion: inicializa la ventana con la foto segun su id,
                la muestra en la parte superior y abajo de ella
                la descripcion y las personas que le han dado like.
    Parametros:
    self Photo
    Retorno: void
    *****************************************************"""
    def initUI(self):
        self.parent.title("Pythagram: Photo")
        self.style = Style()
        self.style.theme_use("default")

        raw = self.api.call_resource('media', 'info', media_id=self.id)
        data = raw['data']

        #Photo
        f = WebFetch()
        photoFrame = Frame(self, relief=RAISED)
        photoFrame.pack(fill=BOTH, expand=1)
        photoUrl = "http://photos-d.ak.instagram.com/hphotos-ak-frc/" + data['images']['thumbnail']['url'].replace("http:http://origincache-frc.fbcdn.netorigincache-frc.fbcdn.net/","")
        profpict = Image.open(f.retrieve(photoUrl))
        profilePicture = ImageTk.PhotoImage(profpict)
        label2 = Label(photoFrame, image=profilePicture)
        label2.image = profilePicture
        label2.pack(padx=5, pady=5)

        #Photo info
        infoFrame = Frame(self,relief=RAISED)
        infoFrame.pack(fill=BOTH, expand=1)
        try:
            info = Label(infoFrame, text=data['caption']['text'])
        except:
            info = Label(infoFrame, text="")
        info.pack(side=LEFT, padx=5, pady=5)

        #People who liked
        likesFrame = Frame(self,relief=RAISED)
        likesFrame.pack(fill=BOTH, expand=1)
        likeLabel = Label(likesFrame, text="Likes:")
        likeLabel.pack()
        proto_likes = data['likes']['data']
        self.likes = []
        lb = Listbox(likesFrame, width=100)
        for element in proto_likes:
            try:
                lb.insert(END, "@{0}: {1}".format(element['username'],element['full_name']))
            except:
                continue
            self.likes.append(element['id'])
        lb.bind("<<ListboxSelect>>", self.onSelect)
        lb.pack(side=LEFT, padx=5, pady=5)

        self.pack(fill=BOTH, expand=1)

    """******** Funcion: onSelect **************
    Descripcion: Abre el perfil de la persona que se selecciono
                en la lista de likes.
    Parametros:
    self Photo
    val
    Retorno: void
    *****************************************************"""
    def onSelect(self,val):
        sender = val.widget
        idx = sender.curselection()
        self.newWindow = Toplevel(self.parent)
        p = Profile(self.newWindow,self.api,self.likes[int(idx[0])])

#!/usr/bin/env python
import hashlib
import urllib
import os.path
from urlparse import urlparse

class WebFetch(object):
	"""******** Clase: WebFetch **************
	Descripcion: Clase wrapper para obtener recursos de internet
	Herencia: objeto
	Retorno: metodos
	*****************************************************"""
	def __init__(self):
		"""******** Metodo: __init__ **************
		Descripcion: constructor de la clase que inicializa algunas variables
		Parametros: self
		Retorno: objeto
		*****************************************************"""
		self.cache_path = os.path.abspath('cache')
		if not os.path.exists(self.cache_path):
			raise Exception("No existe la ruta: %s" % self.cache_path)
		self.cached_files = {}
		self._retriever = urllib.urlretrieve

	def save(self, url, directory=None):
		"""******** Metodo: save **************
		Descripcion: metodo que guarda el contenido descargado en una carpeta
		Hashea el nombre para posibles alcances de nombres
		Parametros: self, url, directory
		Retorno: retorna la ruta a la imagen en el disco
		*****************************************************"""
		m = hashlib.md5()
		m.update(url)
		hashname = m.hexdigest()
		filename, ext = os.path.splitext(os.path.basename(urlparse(url).path))
		savepath = '%s/%s%s' % (self.cache_path, hashname, ext)
		if directory is None:
			self._retriever(url, savepath)
		else:
			self._retriever(url, savepath)
		self.cached_files[url] = savepath
		urllib.urlcleanup()
		return savepath

	def retrieve(self, url, directory=None):
		"""******** Metodo: retrieve **************
		Descripcion: metodo wrapper de save, agrega posibilidad de cache para aumentar tiempos de respuesta
		Parametros: self, url, directory
		Retorno: el retorno del metodo save
		*****************************************************"""
		if url not in self.cached_files:
			return self.save(url, directory)
		return self.cached_files[url]
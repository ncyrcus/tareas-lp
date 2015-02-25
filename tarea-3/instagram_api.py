#!/usr/bin/env python
import urllib2
import urllib
import jregex as json
from pprint import pprint

#obtener codigo de acceso en esta url y pasarla por argv 1
# https://instagram.com/oauth/authorize/?client_id=b4a37965871b48f79e5365fa097f8e24&redirect_uri=http://neopixel.org&scope=likes+comments+relationships&response_type=code

ENDPOINTS = {
	'users': {
		'base_url': '/users',
		'info': '/%(user_id)s',
		'feed': '/self/feed',
		'recent': '/%(user_id)s/media/recent',
		'liked': '/self/media/liked',
		'search': '/search',
		'follows': '/%(user_id)s/follows',
		'followed-by': '/%(user_id)s/followed-by',
		'requested-by': '/self/requested-by',
		'relationship': '/%(user_id)s/relationship',
	},
	'media': {
		'base_url': '/media',
		'info': '/%(media_id)s',
		'search': '/search',
		'popular': '/popular',
		'get-comment': '/%(media_id)s/comments',
		'post-comment': '/%(media_id)s/comments',
		'delete-comment': '/%(media_id)s/comments/%(comment_id)s',
		'get-likes': '/%(media_id)s/likes',
		'post-like': '/%(media_id)s/likes',
		'delete-like': '/%(media_id)s/likes',
	},
	'tags': {
		'base_url': '/tags',
		'get': '/%(tag_name)s',
		'recent': '/%(tag_name)s/media/recent',
		'search': '/search'
	},
	'locations': {
		'base_url': '/locations',
		'get': '/%(location_id)s',
		'recent': '/%(location_id)s/media/recent',
		'search': '/search'
	},
	'geographies': {
		'base_url': '/geographies',
		'recent': '/%(geo_id)s/media/recent'
	}
}

class InstagramAPI(object):
	"""******** Clase: InstagramAPI **************
	Descripcion: Clase wrapper de la api de instagram
	Herencia: objeto
	Retorno: metodos
	*****************************************************"""
	def __init__(self, code):
		"""******** Metodo: __init__ **************
		Descripcion: metodo encargado de inicializar variables
		Parametros: self, code
		Retorno: object
		*****************************************************"""
		self.jsondecoder = json.loads
		self.uriencode = urllib.urlencode
		self.baseapi_uri = 'https://api.instagram.com/v1'
		self.session_info = 'https://api.instagram.com/oauth/access_token'
		self.req_params = {
			'code': '',
			'client_secret': '3f0f335f1cf648a7b0de9ecbbb55941b',
			'client_id': 'b4a37965871b48f79e5365fa097f8e24',
			'grant_type': 'authorization_code',
			'redirect_uri': 'http://neopixel.org'
		}
		self.set_code(code)
		self.loadcache()

	def call_resource(self, resource, command, params=None, apimethod='get', **kwargs):
		"""******** Metodo: call_resource **************
		Descripcion: metodo que ejecuta una consulta de un ambito en especifico a instagram
		Parametros: self, resource, command, params, apimethod, kwargs
		Retorno: codigo json parseado
		*****************************************************"""
		res = ENDPOINTS[resource]
		base_url = res['base_url']
		if command == 'base_url':
			raise Exception
		raw_query = res[command]
		try:
			prep_q = (raw_query % kwargs)
		except KeyError:
			raise Exception("Not enough arguments for query")
		prep_url = '%s%s%s' % (self.baseapi_uri, base_url, prep_q)
		if params is not None:
			modparams = dict(params)
		else:
			modparams = {}
		modparams['access_token'] = self.sess_token()
		r = self.fetch(prep_url, modparams, method=apimethod)
		decoded = self.decodejson(r)
		r.close()
		return decoded

	def loadcache(self):
		"""******** Metodo: loadcache **************
		Descripcion: metodo que carga metadata inicial de sesion
		Parametros: self
		Retorno: None
		*****************************************************"""
		try:
			r = self.fetch(self.session_info, self.req_params, method='post')
		except Exception:
			raise Exception("Bad request, use a newer code")
		self.profile_cache = self.decodejson(r)
		r.close()

	def sess_token(self):
		"""******** Metodo: sess_token **************
		Descripcion: metodo que entrega el token de sesion guardado en el cache de metadata
		Parametros: self
		Retorno: un token de sesion en string
		*****************************************************"""
		return self.profile_cache['access_token']

	def fetch(self, uri, data=None, method='get'):
		"""******** Metodo: fetch **************
		Descripcion: metodo que permite hacer una consulta post o get a instagram
		Parametros: self, uri, data, method
		Retorno: un stream que contiene texto de respuesta
		*****************************************************"""
		if data is None:
			r = urllib2.urlopen(uri)
		else:
			d = data
			if type(data) != str:
				try:
					d = urllib.urlencode(data)
				except Exception:
					pass
			if method == 'post':
				r = urllib2.urlopen(uri, d)
			elif method == 'get':
				r = urllib2.urlopen(uri + '?' + d)
			else:
				#Unrecognized method
				raise Exception
		return r


	def decodejson(self, stream):
		"""******** Metodo: decodejson **************
		Descripcion: wrapper de decodificacion json
		Parametros: self, stream
		Retorno: json decodificado
		*****************************************************"""
		if hasattr(stream, 'read'):
			s = stream.read()
		else:
			s = stream
		return self.jsondecoder(s)

	def set_code(self, code):
		"""******** Metodo: set_code **************
		Descripcion: puede setear un codigo de sesion en runtime
		Parametros: self, code
		Retorno: None
		*****************************************************"""

		if type(code) == str:
			self.req_params['code'] = code
		else:
			raise Exception

#!/usr/bin/env python

import re

ws = r'[ \t\n\r]*'
wsp = re.compile(ws)

rtranslator = {
    '"': '"', '\\': u'\u005c', '/': '/',
    'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t',
}

stringp = re.compile(ur'(.*?)([\\"\u0000-\u001F])')
numberp = re.compile(ur'''
	(?P<number> #represents the whole number (int/float)
		-?(?:0|[1-9][0-9]*) #integer part
		(?P<dot>[.][0-9]+)? #dot followed by numbers
		(?P<exp>[eE][+-]?[0-9]+)? #exponent of float
	)''', re.VERBOSE)

def parseString(string, start):
	"""******** Funcion: parseString **************
	Descripcion: funcion que parsea un string en formato json
	 y lo convierte a un string de python
	Parametros: string, start
	Retorno: un string resultante y un numero correspondiente al indice,
	 donde ocurrio el final del string
	*****************************************************"""
	outarr = []
	endindex = start
	
	if string[endindex:endindex+1] != '"':
		raise Exception

	endindex += 1
	while True:
		chunk = stringp.match(string, endindex)
		if chunk is None:
			raise Exception
		content, ender = chunk.groups()
		endindex = chunk.end()
		if content:
			outarr.append(content)
		if ender == '"':
			break
		elif ender != '\\':
			raise Exception
		outarr.append(content)
		esc_char = string[endindex]
		if esc_char == 'u':
			uniesc = string[endindex+2:endindex+6]
			if len(uniesc) != 4 and uniesc[1:2] != 'X' and uniesc[1:2] != 'x':
				try:
					uni = int(uniesc, 16)
				except ValueError:
					raise Exception
			#uno para \u mas cuatro para hex
			endindex += 5
		else:
			try:
				translatedchar = rtranslator[esc_char]
			except Exception:
				raise Exception
			outarr.append(translatedchar)
			endindex += 1
	return ''.join(outarr), endindex


def parseNumber(string, pos):
	"""******** Funcion: parseNumber **************
	Descripcion: funcion que parsea un numero en formato json y lo convierte a tipo float o int en python
	Parametros: string, pos
	Retorno: numero correspondiente al resultado y un indice que senala el final del numero en el string
	*****************************************************"""
	chunk = numberp.match(string, pos)
	if chunk is None:
		raise Exception
	endindex = chunk.end()
	gd = chunk.groupdict()
	if gd['dot'] or gd['exp']:
		num = float(gd['number'])
	else:
		num = int(gd['number'])
	return num, endindex

def parseObject(string, pos):
	"""******** Funcion: parseObject **************
	Descripcion: funcion que parsea un objeto en formato json y lo convierte en un diccionario de python
	Parametros: string, pos
	Retorno: un diccionario con el contenido resultante y un indice senalando el final del objeto en el string
	*****************************************************"""
	outobj = {}
	m = wsp.match(string, pos)
	if m is None:
		raise Exception
	endindex = m.end()
	begin_obj = string[endindex:endindex+1]
	
	if begin_obj != '{':
		raise Exception
	endindex += 1

	while True:	
		m = wsp.match(string, endindex)
		if m is None:
			raise Exception
		endindex = m.end()
		
		if string[endindex:endindex+1] == '"':
			key, endindex = parseString(string, endindex)
		elif string[endindex:endindex+1] == '}':
			endindex += 1
			break
		else:
			raise Exception
		
		m = wsp.match(string, endindex)
		if m is None:
			raise Exception

		endindex = m.end()
		objsep = string[endindex:endindex+1]
		if objsep == ':':
			endindex += 1
			m = wsp.match(string, endindex)
			if m is None:
				raise Exception
			endindex = m.end()
			value, endindex = selectValue(string, endindex)
		else:
			raise Exception
		m = wsp.match(string, endindex)
		if m is None:
			raise Exception
		endindex = m.end()
		if string[endindex:endindex+1] == ',':
			endindex += 1
			outobj[key] = value
		elif string[endindex:endindex+1] == '}':
			endindex += 1
			outobj[key] = value
			break
		else:
			#object structure not ended correctly
			raise Exception
	
	return outobj, endindex

def parseArray(string, pos):
	"""******** Funcion: parseArray **************
	Descripcion: funcion que parsea un arreglo en formato json y lo convierte a una lista en python
	Parametros: string, pos
	Retorno: una lista de python con el contenido asociado
	y un numero correspondiente al indice en donde se termina el arreglo en el string json
	*****************************************************"""
	outarr = []
	m = wsp.match(string, pos)
	if m is None:
		raise Exception
	endindex = m.end()
	if string[pos:pos+1] != '[':
		raise Exception
	endindex += 1
	while True:
		m = wsp.match(string, endindex)
		if m is None:
			raise Exception
		endindex = m.end()
		if string[endindex:endindex+1] == ']':
			endindex += 1
			break
		else:
			value, endindex = selectValue(string, endindex)
		m = wsp.match(string, endindex)
		if m is None:
			raise Exception
		endindex = m.end()
		if string[endindex:endindex+1] == ',':
			endindex += 1
			outarr.append(value)
		elif string[endindex:endindex+1] == ']':
			endindex += 1
			outarr.append(value)
			break
		else:
			#array structure not ended correctly
			raise Exception
	return outarr, endindex



def parseNull(string, pos):
	"""******** Funcion: parseNull **************
	Descripcion: funcion que parsea un tipo null de json a un None de python
	Parametros: string, pos
	Retorno: None y la posicion donde termina null en el string
	*****************************************************"""
	if string[pos:pos+4] == 'null': 
		pos += 4
		return None, pos
	else:
		raise Exception

def parseTrue(string, pos):
	"""******** Funcion: parseTrue **************
	Descripcion: funcion que parsea un tipo true en json y lo mapea a un tipo True en python
	Parametros: string, pos
	Retorno: retorna True y la posicion donde termina true de json en el string
	*****************************************************"""
	if string[pos:pos+4] == 'true': 
		pos += 4
		return True, pos
	else:
		raise Exception

def parseFalse(string, pos):
	"""******** Funcion: parseFalse **************
	Descripcion: funcion que parsea un tipo false en json y lo transforma a un tipo False en Python
	Parametros: string, pos
	Retorno: False y la posicion donde termina el tipo false en el string
	*****************************************************"""
	if string[pos:pos+5] == 'false': 
		pos += 5
		return False, pos
	else:
		raise Exception

def selectValue(string, pos):
	"""******** Funcion: selectValue **************
	Descripcion: funcion que analiza el string en busqueda de posibles matches de tipo json. 
	Luego redirecciona el flujo a una de estas funciones, generando un parseo en profundidad
	Parametros: string, pos
	Retorno: el valor de la funcion que fue llamada (dinamico)
	*****************************************************"""
	inichar = string[pos:pos+1]
	if inichar == 't':
		_parser = parseTrue
	elif inichar == 'f':
		_parser = parseFalse
	elif inichar == 'n':
		_parser = parseNull
	elif inichar == '"':
		_parser = parseString
	elif inichar == '{':
		_parser = parseObject
	elif inichar == '[':
		_parser = parseArray
	else:
		_parser = parseNumber
	return _parser(string, pos)

def loads(string):
	"""******** Funcion: loads **************
	Descripcion: funcion helper de las funciones anteriores
	Parametros: string
	Retorno: tipos mixtos con el resultado del parseo
	 (dict, array, str, int, float, True, False, None)
	*****************************************************"""
	return selectValue(string, 0)[0]


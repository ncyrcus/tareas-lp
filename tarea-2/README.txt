README
 
info = "Se omiten tildes para compatibilidad por problemas de codificacion";
 
integrantes[0] = new Integrante({
 Nombre: Ignacio Tolosa
 Rol: 201273548-3
});
 
integrantes[1] = new Integrante({
 Nombre: Daniel Morales
 Rol: 201273596-3
});
 
new Documentacion({
		"Forma de jugar BlockCrush":
	"""
		El juego inicia la interfaz grafica. Ahi se juega haciendo intercambio de bloques de colores.
		Para intercambiar bloques se selecciona uno con un clic y luego se selecciona otro adyacente, con lo que
		se destruiran las tripletas de colores, si es que existen, si no, no se podra hacer el cambio.
		El juego termina cuando una cantidad determinada de bloques ha sido destruido.
	"""
})
 
new Observaciones({
	"""
		*Las animaciones estan, 
		el problema... es que ocurren a la velocidad a la luz
		y el ojo humano no es capaz de percibirlo*
	""",
	"""
		La funcion setDummy marca los bloques para su destruccion, que es lo que llama destruirBloque.
		La tarea de eliminacion definitiva del espacio de memoria sera delegada al malvado (GC) GarbageCollector, 
		quien asesinara a los indefensos bloques cuando sea necesario, ya que 
		no tendran mas referencias en memoria.
	"""
})
package tarea2lp;

public class ColorCreator extends AbstractCreator {

	/******** Funcion: crearBloque **************
	Descripcion: Crea un nuevo bloquecolor
	Parametros:
	Retorno: retorna la referencia del bloque
	************************************************/
	@Override
	public BloqueColor crearBloque() {
		return new BloqueColor();
	}
}

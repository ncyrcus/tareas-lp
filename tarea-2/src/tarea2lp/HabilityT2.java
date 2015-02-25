package tarea2lp;

public class HabilityT2 implements HabilityBehavior {
	private BloqueComodin block;
	private GameEngine engine;
	
	/******** Funcion: HabilityT2 **************
	Descripcion: Constructor de HabilityT2
	Parametros:
	Retorno: 
	************************************************/
	public HabilityT2(BloqueComodin block, Object o) {
		this.block = block;
		this.engine = (GameEngine) o;
	}

	/******** Funcion: setBlock **************
	Descripcion: Setea el bloquecomodin correspondiente
	Parametros:
	Retorno: void
	************************************************/
	public void setBlock(BloqueComodin block) {
		this.block = block;
	}

	/******** Funcion: Habilidad **************
	Descripcion: Borra toda la columna donde esta el bloque
	Parametros:
	Retorno: void
	************************************************/
	@Override
	public void Habilidad(){
		//Borra toda la fila
		for (int y=0;y<15;y++){
			engine.boardGrid[y][block.x].destruirBloque();
		}
	}
}


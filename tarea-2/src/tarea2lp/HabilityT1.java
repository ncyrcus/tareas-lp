package tarea2lp;

public class HabilityT1 implements HabilityBehavior {
	private BloqueComodin block;
	private GameEngine engine;
	
	/******** Funcion: HabilityT1 **************
	Descripcion: Constructor de HabilityT1
	Parametros:
	Retorno: 
	************************************************/
	public HabilityT1(BloqueComodin block, Object o) {
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
	Descripcion: Borra toda la fila donde esta el bloque
	Parametros:
	Retorno: void
	************************************************/
	@Override
	public void Habilidad(){
		//Borra toda la fila
		for (int x=0;x<15;x++){
			engine.boardGrid[block.y][x].destruirBloque();
			for (int y=block.y;y>0;y--){
				engine.swapWhite(engine.boardGrid[y][x],engine.boardGrid[y-1][x]);
			}
		}
	}
}

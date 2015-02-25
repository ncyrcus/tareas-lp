package tarea2lp;


import java.awt.Color;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.util.Random;

import javax.swing.JLabel;



public class GameEngine implements ActionListener {
	Bloque[][] boardGrid;
	int breakPercent = 95;
	private static final ColorCreator colorFactory = new ColorCreator();
	private static final ComodinCreator comodinFactory = new ComodinCreator();
	private Bloque prevBlock;
	private Boolean blockSelected;
	private int height;
	private int width;
	private GUIEngine gui;
	
	// Estadisticas de juego
	private static Integer[] estadisticas = {0,0,0,0,0};//R,B,O,G,Y
	private static JLabel[] estadisticasLabel = new JLabel[5];
	private static Integer restantes = 300;
	private static JLabel restantesLabel = new JLabel("L: "+restantes.toString());

	/******** Funcion: createBlock **************
	Descripcion: Crea un nuevo bloque que luego sera ingresado al tablero
	Parametros:
	Retorno: void
	************************************************/
	public Bloque createBlock() {
		int percentage = randInt(0, 100);
		if (percentage <= breakPercent) {
			return colorFactory.crearBloque();
		} else {
			return comodinFactory.crearBloque();
		}
	}
	
	/******** Funcion: getGrid **************
	Descripcion: retorna el tablero de bloques
	Parametros:
	Retorno: retorna la referencia al arreglo de bloques
	************************************************/
	public Bloque[][] getGrid() {
		return boardGrid;
	}
	
	/******** Funcion: setGrid **************
	Descripcion: Setea el valor de BoardGrid
	Parametros:
	Retorno: void
	************************************************/
	public void setGrid(Bloque[][] g) {
		boardGrid = g;
	}
	
	/******** Funcion: initEstadisticasLabel **************
	Descripcion: Inicia las estadistias en pantalla
	Parametros:
	Retorno: void
	************************************************/
	private void initEstadisticasLabel() {
		estadisticasLabel[0] = new JLabel("R: "+estadisticas[0]);
		estadisticasLabel[1] = new JLabel("B: "+estadisticas[1]);
		estadisticasLabel[2] = new JLabel("O: "+estadisticas[2]);
		estadisticasLabel[3] = new JLabel("G: "+estadisticas[3]);
		estadisticasLabel[4] = new JLabel("Y: "+estadisticas[4]);
		gui.addComponent(estadisticasLabel);
		gui.addComponent(restantesLabel);
	}
	
	/******** Funcion: setEstadisticasLabel **************
	Descripcion: Cambia el valor de las estadisticas del juego en pantalla
	Parametros:
	Retorno: void
	************************************************/
	private void setEstadisticasLabel(){
		estadisticasLabel[0].setText("R: "+estadisticas[0]);
		estadisticasLabel[1].setText("B: "+estadisticas[1]);
		estadisticasLabel[2].setText("O: "+estadisticas[2]);
		estadisticasLabel[3].setText("G: "+estadisticas[3]);
		estadisticasLabel[4].setText("Y: "+estadisticas[4]);
		restantesLabel.setText("L: "+restantes.toString());
	}
	
	/******** Funcion: GameEngine **************
	Descripcion: Constructor de GameEngine
	Parametros:
	Retorno:
	************************************************/
	public GameEngine() {
		height = 15;
		width = 15;
		
		boardGrid = new Bloque[height][width];
		gui = new GUIEngine();
		Bloque.setListener(this);
		int y, x;
		y = 0; x = 0;
		for (y = 0; y < height; y++) {
			for ( x = 0; x < width; x++) {
				boardGrid[y][x] = createBlock();
				boardGrid[y][x].setCoords(x, y);	
			}
		}
		gui.loadGrid(boardGrid);
		initEstadisticasLabel();
		gui.updateGrid();
		blockSelected = false;
	}
	
	/******** Funcion: checkSwap **************
	Descripcion: Chequea si los dos bloques presionados son contiguos y pueden hacer swap,
				comparando el anterior en tal caso
	Parametros:
	Bloque bloque
	Retorno: void
	************************************************/
	public void checkSwap(Bloque bloque){
		if (!blockSelected) {
			prevBlock = bloque;
			blockSelected = true;
		} else if (((Math.abs(bloque.x-prevBlock.x)== 1) && (bloque.y == prevBlock.y)) ||
			((Math.abs(bloque.y-prevBlock.y) == 1) && (bloque.x == prevBlock.x))) {
			swapButton(bloque, prevBlock);
			blockSelected = false;
			prevBlock = null;
		} else {
			blockSelected = false;
			prevBlock = null;
		}
	}
	
	/******** Funcion: swapButton **************
	Descripcion: Cambia dos bloques de posicion
	Parametros:
	Bloque bloque 1
	Bloque bloque 2
	Retorno: void
	************************************************/
	public void swapButton(Bloque bloque1, Bloque bloque2) {
		int auxX, auxY;
		boardGrid[bloque1.y][bloque1.x] = bloque2;
		boardGrid[bloque2.y][bloque2.x] = bloque1;
	
		auxX = bloque1.x; auxY = bloque1.y;
		bloque1.setCoords(bloque2.x, bloque2.y);
		bloque2.setCoords(auxX, auxY);
		
		BlockButton button1 = bloque1.getButton();
		BlockButton button2 = bloque2.getButton();
		
		Color auxbackground = button1.getBackground();
		String auxtext = button1.getText();
		
		button1.setText(button2.getText());
		button1.setBackground(button2.getBackground());
		button2.setText(auxtext);
		button2.setBackground(auxbackground);
		auxX = button1.xCoord;
		auxY = button1.yCoord;
		button1.xCoord = button2.xCoord;
		button1.yCoord = button2.yCoord;
		button2.xCoord = auxX;
		button2.yCoord = auxY;
		
		bloque1.setButton(button2);
		bloque2.setButton(button1);
		
		if (clearButtons(bloque1) || clearButtons(bloque2)){
			for (int y=0;y<height;y++){
				for (int x=0;x<width;x++){
					if ((boardGrid[y][x].getColor().equals("-")) || 
						(boardGrid[y][x].getColor().equals("$")) || 
						(boardGrid[y][x].getColor().equals("&"))) {
						continue;
					}
					clearButtons(boardGrid[y][x]);
				}
			}

			fillWhites();
			gui.updateGrid();
			if (restantes <= 0){
				gui.msgbox("Congratulations! You WIN!");
				System.exit(0);
			}
			else{
				if (isGameOver()){
					gui.msgbox("Re-making the board!");
					renewBoard();
				}
			}
		}
		else{
			fakeSwapButton(bloque1,bloque2);
		}
	}
	
	/******** Funcion: fakeSwapButton **************
	Descripcion: Realiza el rollback de un swapButton cuando este no origina ninguna destruccion
	Parametros:
	Bloque bloque 1
	Bloque bloque 2
	Retorno: void
	************************************************/
	public void fakeSwapButton(Bloque bloque1, Bloque bloque2) {
		int auxX, auxY;
		boardGrid[bloque1.y][bloque1.x] = bloque2;
		boardGrid[bloque2.y][bloque2.x] = bloque1;
		

		auxX = bloque1.x; auxY = bloque1.y;
		bloque1.setCoords(bloque2.x, bloque2.y);
		bloque2.setCoords(auxX, auxY);
		
		BlockButton button1 = bloque1.getButton();
		BlockButton button2 = bloque2.getButton();
		
		Color auxbackground = button1.getBackground();
		String auxtext = button1.getText();
		
		button1.setText(button2.getText());
		button1.setBackground(button2.getBackground());
		button2.setText(auxtext);
		button2.setBackground(auxbackground);
		auxX = button1.xCoord;
		auxY = button1.yCoord;
		button1.xCoord = button2.xCoord;
		button1.yCoord = button2.yCoord;
		button2.xCoord = auxX;
		button2.yCoord = auxY;
		
		bloque1.setButton(button2);
		bloque2.setButton(button1);
		gui.updateGrid();
	}
	
	/******** Funcion: swapWhite **************
	Descripcion: cambia un bloque blanco con uno normal
	Parametros:
	Bloque bloque1
	Bloque bloque2
	Retorno: void
	************************************************/
	public void swapWhite(Bloque bloque1, Bloque bloque2){

		int auxX, auxY;
		

		boardGrid[bloque1.y][bloque1.x] = bloque2;
		boardGrid[bloque2.y][bloque2.x] = bloque1;
		
		auxX = bloque1.x; auxY = bloque1.y;
		bloque1.setCoords(bloque2.x, bloque2.y);
		bloque2.setCoords(auxX, auxY);
		
		BlockButton button1 = bloque1.getButton();
		BlockButton button2 = bloque2.getButton();
		
		button1.setText(button2.getText());
		button1.setBackground(button2.getBackground());
		button2.setText("-");
		bloque2.color = "-";
		button2.setBackground(Color.WHITE);
		auxX = button1.xCoord;
		auxY = button1.yCoord;
		button1.xCoord = button2.xCoord;
		button1.yCoord = button2.yCoord;
		button2.xCoord = auxX;
		button2.yCoord = auxY;
		
		bloque1.setButton(button2);
		bloque2.setButton(button1);
		
		
		
		gui.updateGrid();
	}
	
	/******** Funcion: randInt **************
	Descripcion: Retorna un entero aleatorio
	Parametros:
	Bloque bloque1
	Bloque bloque2
	Retorno: entero aleatorio
	************************************************/
	public static int randInt(int min, int max) {
	    Random rand = new Random();
	    int randomNum = rand.nextInt((max - min) + 1) + min;
	    return randomNum;
	}
	
	/******** Funcion: fillWhites **************
	Descripcion: Crea un nuevo bloque en los campos en blanco
	Parametros:
	int min
	int max
	Retorno: void
	************************************************/
	public void fillWhites() {
		Bloque newBloque, bloque;
		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				if (boardGrid[y][x].getButton().getText().equals("-")){
					newBloque = createBlock();
					bloque = boardGrid[y][x];
					BlockButton button1 = bloque.getButton();
					BlockButton button2 = newBloque.getButton();
					button1.setText(button2.getText());
					button1.setBackground(button2.getBackground());
					newBloque.setButton(button1);
					newBloque.setCoords(x,y);
					boardGrid[y][x] = newBloque;
				}
			}
		}
	}
	
	/******** Funcion: renewBoard **************
	Descripcion: Crea un nuevo tablero cuando no hay mas movimientos
	Parametros:
	Retorno: void
	************************************************/
	public void renewBoard() {
		Bloque newBloque, bloque;
		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				newBloque = createBlock();
				bloque = boardGrid[y][x];
				BlockButton button1 = bloque.getButton();
				BlockButton button2 = newBloque.getButton();
				button1.setText(button2.getText());
				button1.setBackground(button2.getBackground());
				newBloque.setButton(button1);
				newBloque.setCoords(x,y);
				boardGrid[y][x] = newBloque;
			}
		}
	}
	
	/******** Funcion: isGameOver **************
	Descripcion: Chequea en todo el tablero si existen mas jugadas
	Parametros:
	Retorno: void
	************************************************/
	public Boolean isGameOver(){
		for (int y=14;y>=0;y--){
			for (int x=0;x<15;x++){
				Bloque aux = boardGrid[y][x];
				if (aux.getColor().equals("-")){
					continue;
				}
				
				//Revisar siguiente
				if (x+1 < 15){
					if (aux.getColor().equals(boardGrid[y][x+1].getColor())){
						if (x+3 < 15){ // Sub-subsiguiente
							if (aux.getColor().equals(boardGrid[y][x+3].getColor()))
								return false;
						}
						if (x-2 >= 0){ // Ante-anterior
							if (aux.getColor().equals(boardGrid[y][x-2].getColor()))
								return false;
						}
						if ((x+2 < 15) && (y-1 >= 0)){ //Subsiguiente-arriba
							if (aux.getColor().equals(boardGrid[y-1][x+2].getColor()))
								return false;
						}
						if ((x+2 < 15) && (y+1 < 15)){ //Subsiguiente-abajo
							if (aux.getColor().equals(boardGrid[y+1][x+2].getColor()))
								return false;
						}
						if ((x-1 >= 0) && (y-1 >= 0)){ //Anterior-arriba
							if (aux.getColor().equals(boardGrid[y-1][x-1].getColor()))
								return false;
						}
						if ((x-1 >= 0) && (y+1 < 15)){//Anterior-abajo
							if (aux.getColor().equals(boardGrid[y+1][x-1].getColor()))
								return false;
						}
					}
				}
				
				//Revisar arriba
				if (x+1 < 15){
					if (aux.getColor().equals(boardGrid[y][x+1].getColor())){
						if (y-3 >= 0){ // Sup-supsuperior
							if (aux.getColor().equals(boardGrid[y-3][x].getColor()))
								return false;
						}
						if (y+2 < 15){ // Inf-inferior
							if (aux.getColor().equals(boardGrid[y+2][x].getColor()))
								return false;
						}
						if ((y-2 >= 0) && (x+1 < 15)){ //Sup-superior-derecha
							if (aux.getColor().equals(boardGrid[y-2][x+1].getColor()))
								return false;
						}
						if ((y-2 >= 0) && (x-1 >= 0)){ //Sup-superior-izquierda
							if (aux.getColor().equals(boardGrid[y-2][x-1].getColor()))
								return false;
						}
						if ((y+1 < 15) && (x+1 < 15)){ //Inferior-derecha
							if (aux.getColor().equals(boardGrid[y+1][x+1].getColor()))
								return false;
						}
						if ((y+1 < 15) && (x-1 >= 0)){//Inferior-izquierda
							if (aux.getColor().equals(boardGrid[y+1][x-1].getColor()))
								return false;
						}
					}
				}
				
				//Revisar sub siguiente
				if (x+2 < 15){
					if (aux.getColor().equals(boardGrid[y][x+2].getColor())){
						if ((y-1 >= 0) && (x+1 < 15)){ // derecha-arriba
							if (aux.getColor().equals(boardGrid[y-1][x+1].getColor()))
								return false;
						}
						if ((y+1 < 15) && (x+1 < 15)){ // derecha-abajo
							if (aux.getColor().equals(boardGrid[y+1][x+1].getColor()))
								return false;
						}
					}
				}
				
				//Revisar sup superior
				if (y-2 >= 0){
					if (aux.getColor().equals(boardGrid[y-2][x].getColor())){
						if ((y-1 >= 0) && (x+1 < 15)){ // arriba-derecha
							if (aux.getColor().equals(boardGrid[y-1][x+1].getColor()))
								return false;
						}
						if ((y-1 >= 0) && (x-1 >= 0)){ // arriba-izquerda
							if (aux.getColor().equals(boardGrid[y-1][x-1].getColor()))
								return false;
						}
					}
				}
				
			}
		}
		return true;
	}
	
	/******** Funcion: clearButtons **************
	Descripcion: Elimina todos los bloques que puedan estar contiguos de 3 o mas
	Parametros:
	Bloque bloque
	Retorno: void
	************************************************/
	public Boolean clearButtons(Bloque bloque){
		// Chequear iguales
		// En X:
		String colour = bloque.getColor();
		String bonus1 = "1";
		String bonus2 = "2";
		int xplus = bloque.x, xminus = bloque.x;
		int yplus = bloque.y, yminus = bloque.y;
		for (int y1=(bloque.y+1);y1<height;y1++){
			if ((boardGrid[y1][bloque.x].getColor().equals(bonus1)) || (boardGrid[y1][bloque.x].getColor().equals(bonus2))){
				BloqueComodin auxblock = (BloqueComodin) boardGrid[y1][bloque.x];
				auxblock.habilidad.Habilidad();
				yplus = 14;
				break;
			}
			if (boardGrid[y1][bloque.x].getColor().equals(bloque.getColor())){
				yplus = y1;
			}
			else{
				break;
			}
		}
		for (int y2=(bloque.y-1);y2>=0;y2--){
			if ((boardGrid[y2][bloque.x].getColor().equals(bonus1)) || (boardGrid[y2][bloque.x].getColor().equals(bonus2))){
				BloqueComodin auxblock = (BloqueComodin) boardGrid[y2][bloque.x];
				auxblock.habilidad.Habilidad();
				yminus = 0;
				break;
			}
			if (boardGrid[y2][bloque.x].getColor().equals(bloque.getColor())){
				yminus = y2;
			}
			else{
				break;
			}
		}
		// En Y:		
		for (int x1=(bloque.x+1);x1<height;x1++){
			if ((boardGrid[bloque.y][x1].getColor().equals(bonus1)) || (boardGrid[bloque.y][x1].getColor().equals(bonus2))){
				BloqueComodin auxblock = (BloqueComodin) boardGrid[bloque.y][x1];
				auxblock.habilidad.Habilidad();
				xplus = 14;
				break;
			}
			if (boardGrid[bloque.y][x1].getColor().equals(bloque.getColor())){
				xplus = x1;
			}
			else{
				break;
			}
		}
		for (int x2=(bloque.x-1);x2>=0;x2--){
			if ((boardGrid[bloque.y][x2].getColor().equals(bonus1)) || (boardGrid[bloque.y][x2].getColor().equals(bonus2))){
				BloqueComodin auxblock = (BloqueComodin) boardGrid[bloque.y][x2];
				auxblock.habilidad.Habilidad();
				xminus = 0;
				break;
			}
			if (boardGrid[bloque.y][x2].getColor().equals(bloque.getColor())){
				xminus = x2;
			}
			else{
				break;
			}
		}
		// Eliminar iguales
		Integer total = 0;
		Boolean check = false;
		
		// En X:
		if (xplus-xminus>=2){
			for (int i = xminus; i <= xplus; i++){
				boardGrid[bloque.y][i].destruirBloque();
				for (int r=bloque.y;r>0;r--){
					if(boardGrid[r-1][i].getColor().equals("-"))
						break;
					swapWhite(boardGrid[r][i],boardGrid[r-1][i]); 
				}
			}
			total += (xplus-xminus) + 1;
			check = true;
		}
		// En Y:
		if (yplus-yminus>=2){
			for (int i = yminus; i <= yplus; i++){
				boardGrid[i][bloque.x].destruirBloque();
				for (int r=i;r>0;r--){
					if(boardGrid[r-1][bloque.x].getColor().equals("-"))
						break;
					
					swapWhite(boardGrid[r][bloque.x],boardGrid[r-1][bloque.x]);
				}	
			}
			total += (yplus-yminus) + 1;
			check = true;
		}
		
		//R,B,O,G,Y
		if (colour.equals("red")){
			estadisticas[0] += total;
		}
		else if (colour.equals("blue")){
			estadisticas[1] += total;
		}
		else if (colour.equals("orange")){
			estadisticas[2] += total;
		}
		else if (colour.equals("green")){
			estadisticas[3] += total;
		}
		else if (colour.equals("yellow")){
			estadisticas[4] += total;
		}
		restantes -= total;
		setEstadisticasLabel();
		return check;
	}

	/******** Funcion: actionPerformed **************
	Descripcion: Realiza una accion cuando un boton es presionado
	Parametros:
	ActionEvent
	Retorno: void
	************************************************/
	@Override
	public void actionPerformed(ActionEvent e) {
		BlockButton button = (BlockButton) e.getSource();
		Bloque bloque = boardGrid[button.yCoord][button.xCoord];
		checkSwap(bloque);
	}

}
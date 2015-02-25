package tarea2lp;

import javax.swing.JButton;

@SuppressWarnings("serial")
public class BlockButton extends JButton {
	public int xCoord;
	public int yCoord;
	
	/******** Funcion: BlockButton **************
	Descripcion: constructor, crea un boton con nombre name
	Parametros:
	String name
	Retorno: nada
	************************************************/
	public BlockButton(String name) {
		super(name);
	}
	
}

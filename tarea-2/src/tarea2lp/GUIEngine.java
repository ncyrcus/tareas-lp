package tarea2lp;

import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.GridLayout;

import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.UIManager;
import javax.swing.border.CompoundBorder;
import javax.swing.border.EmptyBorder;
import javax.swing.JOptionPane;

public class GUIEngine {
	JFrame frame = new JFrame();
	private int height;
	private int width;
	
	/******** Funcion: loadGrid **************
	Descripcion: Carga todos los bloques en la pantalla
	Parametros:
	Bloque[][] grid
	Retorno: void
	************************************************/
	public void loadGrid(Bloque[][] grid) {
		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				frame.add(grid[y][x].getButton());
			}
		}
	}
	
	/******** Funcion: updateGrid **************
	Descripcion: Actualiza lo que aparece en la pantalla
	Parametros:
	Retorno: void
	************************************************/
	public void updateGrid() {
		frame.pack();
		frame.setVisible(true);
	}
	
	/******** Funcion: addComponent **************
	Descripcion: Anade un nuevo componente a la pantalla
	Parametros:
	Component comp
	Retorno: void
	************************************************/
	public void addComponent(Component comp) {
		frame.add(comp);
	}
	
	/******** Funcion: removeComponent **************
	Descripcion: Remueve un componente de la pantalla
	Parametros:
	Component comp
	Retorno: void
	************************************************/
	public void removeComponent(Component comp) {
		frame.remove(comp);
	}
	
	/******** Funcion: addComponent **************
	Descripcion: Similar a la anterior pero con un arreglo de JLabels
	Parametros:
	JLabel[] comp
	Retorno: void
	************************************************/
	public void addComponent(JLabel[] comp) {
		for (JLabel c : comp) {
			addComponent(c);
		}
	}
	
	/******** Funcion: msgbox **************
	Descripcion: Muestra una alerta por pantalla con un texto definido
	Parametros:
	String s
	Retorno: void
	************************************************/
	public void msgbox(String s){
		JOptionPane.showMessageDialog(null, s);
	}
	
	/******** Funcion: GUIEngine **************
	Descripcion: Constructor de GUIEngine
	Parametros:
	Retorno:
	************************************************/
	public GUIEngine() {
		height = 15;
		width = 15;
		
		try {
			//temas de compatibilidad para los botones
			UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
		} catch (Exception e) { }
		
		//presets para los bordes de botones de bloques
		Bloque.baseBorder = new EmptyBorder(10, 10, 10, 10);
		Bloque.lineBorder = BorderFactory.createLineBorder(Color.BLACK);
		Bloque.customBorder = new CompoundBorder(Bloque.lineBorder, Bloque.baseBorder); 
		
		frame.setLayout(new GridLayout(height+1, width));
		
		//loadGrid(initialGrid);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.pack();
		frame.setVisible(true);
		frame.setPreferredSize(new Dimension(600, 640));
	}

}

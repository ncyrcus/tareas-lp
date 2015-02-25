package tarea2lp;

import java.awt.Color;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.Random;


public class BloqueComodin extends Bloque implements HabilityBehavior{
	public HabilityBehavior habilidad;
	
	@SuppressWarnings("serial")
	protected static final HashMap <String, Object[]> buttons = new HashMap<String, Object[]>() {
		{
			put("1", new Object[] {"$", Color.CYAN});
			put("2", new Object[] {"&", Color.MAGENTA});
		};
	};

	/******** Funcion: getHabilidad **************
	Descripcion: Retorna la habilidad de un bloque comodin
	Parametros:
	Retorno: Retorna un HabilityBehavior con la habilidad
	************************************************/
	public HabilityBehavior getHabilidad() {
		return habilidad;
	}

	/******** Funcion: setHabilidad **************
	Descripcion: Asigna una habilidad a un bloquecolor
	Parametros:
	HabilityBehavior habilidad
	Retorno: void
	************************************************/
	public void setHabilidad(HabilityBehavior habilidad) {
		this.habilidad = habilidad;
	}

	/******** Funcion: Habilidad **************
	Descripcion: Llama a la habilidad del bloque
	Parametros:
	Retorno: void
	************************************************/
	@Override
	public void Habilidad() {
		this.habilidad.Habilidad();
	}
	/******** Funcion: getColor **************
	Descripcion: Retorna el color de un bloque
	Parametros:
	Retorno: Retorna el color de un bloque
	************************************************/
	public String getColor() {
		return color;
	}
	
	/******** Funcion: setButton **************
	Descripcion: Le asigna un boton a un bloque
	Parametros:
	BlockButton b
	Retorno: void
	************************************************/
	public void setButton(BlockButton b) {
		innerButton = b;
	}
	
	/******** Funcion: getButton **************
	Descripcion: Retorna el boton de n bloque
	Parametros:
	Retorno: void
	************************************************/
	public BlockButton getButton() {
		return innerButton;
	}
	
	/******** Funcion: setColor **************
	Descripcion: Asigna un color al bloque
	Parametros:
	String color
	Retorno: void
	************************************************/
	public void setColor(String color) {
		try {
			Object[] values = buttons.get(color);
			innerButton.setText((String) values[0]);
			innerButton.setBackground((Color) values[1]);
			this.color = color;
		} catch (Exception e) {
		}
	}

	/******** Funcion: setCoords **************
	Descripcion: Asigna coordenadas a un bloque
	Parametros:
	int x
	int y
	Retorno: void
	************************************************/
	public void setCoords(int x, int y) {
		this.x = x;
		this.y = y;
		innerButton.xCoord = x;
		innerButton.yCoord = y;
	}

	/******** Funcion: getX **************
	Descripcion: retorna la coordenada x del bloque
	Parametros:
	Retorno: int con la coordenada x
	************************************************/
	public int getX() {
		return this.x;
	}
	
	/******** Funcion: getY **************
	Descripcion: retorna la coordenada y del bloque
	Parametros:
	Retorno: int con la coordenada y
	************************************************/
	public int getY() {
		return this.y;
	}
	
	protected String randKey(HashMap<String, Object[]> hm) {
		Random rand = new Random();
		Object[] keys = hm.keySet().toArray();
		String randomKey = (String) keys[rand.nextInt(keys.length)];
		return randomKey;
	}
	
	/******** Funcion: BloqueComodin **************
	Descripcion: constructor de un bloque comodin
	Parametros:
	Retorno: 
	************************************************/
	public BloqueComodin() {
		String colorName = randKey(buttons);
		
		try {
			Object[] values = buttons.get(colorName);
			innerButton = new BlockButton((String) values[0]);
			innerButton.setBackground((Color) values[1]);
			this.color = colorName;
		} catch (Exception e) {
		}
		if (colorName.equals("1")){
			this.habilidad = new HabilityT1(this,actionlistener);
		}
		else{
			this.habilidad = new HabilityT2(this,actionlistener);
		}
		innerButton.addActionListener((ActionListener) actionlistener);
		innerButton.setOpaque(true);
		innerButton.setBorder(customBorder);
	}
	
	/******** Funcion: destruirBloque **************
	Descripcion: crea un bloque en blanco para ser eliminado por el grid
	Parametros:
	Retorno: void
	************************************************/
	@Override
	public void destruirBloque() {
		innerButton.setText("-");
		innerButton.setBackground(Color.WHITE);
		color = "-";
	}
}

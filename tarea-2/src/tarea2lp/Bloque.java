package tarea2lp;

import javax.swing.border.Border;
import java.util.HashMap;

public abstract class Bloque {
	protected static Border baseBorder;
	protected static Border lineBorder;
	protected static Border customBorder;
	public static Object actionlistener;

	//no static
	protected String color;
	protected static HashMap<String, Object[]> buttons;
	protected BlockButton innerButton;
	protected int x;
	protected int y;
	
	public static void setListener(Object o){
		actionlistener = o;
	}
	
	public abstract String getColor();
	public abstract void setButton(BlockButton b) ;
	public abstract BlockButton getButton() ;
	public abstract void setColor(String color);
	public abstract void setCoords(int x, int y);
	public abstract int getX();
	public abstract int getY();
	protected abstract String randKey(HashMap<String, Object[]> hm);

	public abstract void destruirBloque();
}

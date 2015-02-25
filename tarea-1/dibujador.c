#include <stdio.h>
#include <stdlib.h>
#include <ncurses.h>
#include "dibujador.h"

/************* Funcion: init_settings ************
Descripcion: Inicializa el uso de colores de la
            libreria ncurses
Parametros: 
void
Retorno: void
************************************************/
void init_settings()
{
    savetty();

    pair_id = 10;
    color_id = 10;

    if (!initscr()) {
        printf("Error initializing screen.\n");
        exit(1);
    }

    if (has_colors() == FALSE) {
        endwin();
        printf("Your terminal does not support color\n");
        exit(1);
    }

    start_color();
    use_default_colors();
}

/************* Funcion: finalize *****************
Descripcion: Finaliza la ejecucion de la ventana
            usada con la libreria ncurses
Parametros: 
void
Retorno: void
************************************************/
void finalize()
{
    endwin();
    resetty();
}

/************* Funcion: printblock *****************
Descripcion: Imprime en pantalla un bloque del color
            ingresado con el ancho de la pantalla y
            una fraccion del alto
Parametros: 
self dibujante
c color
Retorno: void
************************************************/
void printblock(dibujante *self, color *c) {
    int x, y;

    int margin_left = 3;
    int margin_right = 3;
    int width = self->maxcoords.x-(margin_left+margin_right);
    char labeltxt[30];
    char name[1024];
    strcpy(name,c->nombre);
    int red = c->red;
    int green = c->green;
    int blue = c->blue;
    
    //inicia la impresion del bloque de color
    init_color(color_id, red, green, blue);
    init_pair(pair_id, DEFAULT_ID, color_id); //asigna fondo
    attron(COLOR_PAIR(pair_id)); //pair_id es la mezcla
    
    move(++self->cursor.y, self->cursor.x+margin_left);
    for (y = 0; y < self->height-1; y++) {
        move(self->cursor.y++, self->cursor.x+margin_left);
        //printw("%d %d", self->cursor.y, self->cursor.x);
        for (x = 0; x < width; x++) {
            printw(" "); //pinta con la mezcla
        }

        printw("\n");
    }
    
    attroff(COLOR_PAIR(pair_id));

    //inicia la impresion de la etiqueta
    init_pair(2, COLOR_BLACK, COLOR_WHITE);
    attron(COLOR_PAIR(2));
    move(self->cursor.y, self->cursor.x+margin_left);
    self->cursor.y++;
    sprintf(labeltxt, "%s (%d, %d, %d)", name, red, green, blue);
    printw("%*s\n", width, labeltxt);
    
    attroff(COLOR_PAIR(2));
    refresh();

    //evita que se repitan los colores por id
    color_id = (color_id+1) % 256;
    pair_id++;
}

/************* Funcion: printgrid *****************
Descripcion: Imprime un color definido en una
            fraccion del ancho de la pantalla y 
            otra del alto.
Parametros: 
self dibujante
c color
Retorno: void
************************************************/
void printgrid(dibujante *self, color *c) {
    int x, y;

    int margin_left = 3;
    int margin_right = 3;
    int minwidth = 30;
    int width = (self->maxcoords.x-(2+margin_left+margin_right))/4;
    char labeltxt[30];
    char name[1024];
    strcpy(name,c->nombre);
    int red = c->red;
    int green = c->green;
    int blue = c->blue;
    
    //inicia la impresion del bloque de color
    init_color(color_id, red, green, blue);
    init_pair(pair_id, DEFAULT_ID, color_id); //asigna fondo
    attron(COLOR_PAIR(pair_id)); //pair_id es la mezcla
    
    //move(((self->cursor.y)/3)*self->height, (((pair_id-10) % 3)*width)+1);
    self->cursor.y = (((self->count) / 4) * (self->height+1)) + 1;
    self->cursor.x = (((self->count) % 4) * (width+margin_left-1)) + 1;

    for (y = 0; y < self->height-1; y++) {
        move(self->cursor.y++, self->cursor.x);
        //printw("%d %d", self->cursor.y, self->cursor.x);
        for (x = 0; x < width; x++) {
            printw(" "); //pinta con la mezcla
        }
    }
    
    attroff(COLOR_PAIR(pair_id));

    //inicia la impresion de la etiqueta
    init_pair(2, COLOR_BLACK, COLOR_WHITE);
    attron(COLOR_PAIR(2));

    self->cursor.y = ((self->count / 4) * (self->height+1)) + self->height;
    self->cursor.x = ((self->count % 4) * (width+margin_left-1)) + 1;
    move(self->cursor.y, self->cursor.x);
    sprintf(labeltxt, "%s (%d, %d, %d)", name, red, green, blue);
    printw("%*s\n", width, labeltxt);
    
    attroff(COLOR_PAIR(2));
    refresh();

    //evita que se repitan los colores por id
    color_id = (color_id+1) % 256;
    pair_id++;

    self->count++;
}

/************* Funcion: newDibujante *****************
Descripcion: Crea un nuevo dibujante requiriendo la 
            memoria de un struct dibujante
Parametros: 
void
Retorno: Retorna un puntero a la direccion del struct
        creado
*****************************************************/
dibujante *newDibujante(void) {
    dibujante *self = (dibujante *) malloc(sizeof(dibujante));
    if (self == NULL) return NULL;
    self->DrawList = DrawList;
    self->DrawGrid = DrawGrid;
    self->cursor.x = 0;
    self->cursor.y = 0;
    self->maxcoords.x = 0;
    self->maxcoords.y = 0;
    self->height = 3;
    self->count = 0;
    return self;
}

/************* Funcion: delDibujante *****************
Descripcion: Libera la memoria utilizada por un struct
            dibujante
Parametros: 
self dibujante
Retorno: void
*****************************************************/
void delDibujante(dibujante *self) {
    free((void *) self);
}

/************* Funcion: DrawList *****************
Descripcion: Imprime todos los colores existentes
            en el sistema a partir de la lista de
            colores haciendo uso para ello de la 
            funcion printBlock, ademas la funcion
            soporta uso de ventanas de 5 colores 
            por cada una
Parametros: 
self dibujante
L llist
Retorno: void
************************************************/
void DrawList(dibujante *self, llist *L)
{
    initscr();
    init_settings();
    int y, x, i, j;
    color *c;

    listMoveToStart(L);
    
    if (!can_change_color()) {
        printw("ALERTA: tu terminal no soporta ncurses\n");
    }

    int h, w;
    getmaxyx(stdscr, h, w);
    int length = listLength(L);

    self->maxcoords.x = w;
    self->maxcoords.y = h;

    int cou = 0;
    int page = 0;
    int key, move;
    keypad(stdscr, TRUE);
    
    for (i = 0; i <= length; i++) {
        if ((cou == 5) || (i == length)) {
            printw("presione una tecla para continuar...");
            key = getch();
            clear();
            if (key == KEY_LEFT){
                listMoveToStart(L);
                for (move = 0; move < 5*(page-1); move++){
                    listMoveNext(L);
                }
                i = 5*(page-1) - 1;
                self->cursor.x = 0;
                self->cursor.y = 0;
                page--;
                cou = 0;
                continue;
            }
            else{
                if (i == length){
                    break;
                }
                self->cursor.x = 0;
                self->cursor.y = 0;
                page++;
                cou = 0;
            }
        }
        
        c = listGetItem(L);
        printblock(self, c);
        listMoveNext(L);
        cou++;
    }
    printw("presione una tecla para salir...");
    getch();
    endwin();
    exit(EXIT_SUCCESS);
}


/************* Funcion: DrawGrid *****************
Descripcion: Imprime en pantalla todos los colores
            del sistema en forma de grid de 4x5 en
            cada ventana utilizada
Parametros: 
self dibujante
L llist
Retorno: void
************************************************/
void DrawGrid(dibujante *self, llist *L)
{
    initscr();
    init_settings();
    int y, x, i, j;
    color *c;

    listMoveToStart(L);

    if (!can_change_color()) {
        printw("ALERTA: tu terminal no soporta ncurses\n");
    }

    int h, w;
    getmaxyx(stdscr, h, w);

    self->maxcoords.x = w;
    self->maxcoords.y = h;
    
    int cou = 0;
    int page = 0;
    int key, move;
    keypad(stdscr, TRUE);
    
    for (i = 0; i <= listLength(L); i++) {
        if ((cou == 20) || (i == listLength(L))) {
            printw("presione una tecla para continuar...");
            key = getch();
            clear();
            self->cursor.x = 0;
            self->cursor.y = 0;
            self->count = 0;
            if (key == KEY_LEFT){
                listMoveToStart(L);
                for (move = 0; move < 5*(page-1); move++){
                    listMoveNext(L);
                }
                i = 5*(page-1) - 1;
                page--;
                cou = 0;
                continue;
            }
            else{
                if (i == listLength(L)){
                    break;
                }                
                page++;
                cou = 0;
            }
        }
        
        c = listGetItem(L);
        printgrid(self, c);
        listMoveNext(L);
        cou++;
    }
    printw("presione una tecla para salir...");
    getch();
    endwin();
    exit(EXIT_SUCCESS);

    return;
}

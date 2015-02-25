#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "color.h"

#define FALSE   0
#define TRUE    1


/************* Funcion: checkn *****************
Descripcion: Chequea que el valor ingresado en RGB
             este entre 0 y 1000
Parametros: 
n entero
Retorno: Retorna 1 si no esta dentro del rango y 0
        en el caso contrario.
************************************************/
int checkn(int n)
{
    return !(n >= 0 && n <= 1000);
}

/************* Funcion: addColor *****************
Descripcion: Anade un color al archivo colors.txt
            desde el struct.
Parametros: 
self color
Retorno: void
************************************************/
void addColor(color *self)
{   
    //Anadir al archivo:
    int r, g, b;
    int exists = FALSE;
    string aux_nombre;

    FILE *output;
    output = fopen("colors.txt", "r+");

    rewind(output);

    while (fscanf(output, "%s\n%d\n%d\n%d\n", aux_nombre, &r, &g, &b) > 0) {
        if (strcmp(self->nombre, aux_nombre) == 0)
            exists = TRUE;
    }

    fclose(output);

    if (!exists) {
        output = fopen("colors.txt", "a+");
        if (output == NULL) return;
        fprintf(output, "%s\n%d\n%d\n%d\n", self->nombre, self->red, self->green, self->blue);
        fclose(output);
    }
    return;
}

/************* Funcion: rmColor *****************
Descripcion: Remueve un color del archivo colors
            a partir del struct
Parametros: 
self color
Retorno: void
************************************************/
void rmColor(color *self)
{
    FILE *input = fopen("colors.txt", "r");
    FILE *output = fopen(".colors.tmp", "w");

    if (input == NULL || output == NULL) {
        return;
    }

    string nombre;
    int r, g, b;

    while (fscanf(input, "%s\n%d\n%d\n%d\n", nombre, &r, &g, &b) != EOF) {
        if (strcmp(self->nombre, nombre)) fprintf(output, "%s\n%d\n%d\n%d\n", nombre, r, g, b);
    }

    fclose(input);
    fclose(output);
    remove("colors.txt");
    rename(".colors.tmp", "colors.txt");
}

/*************** Funcion: newColor *****************
Descripcion: Crea un nuevo color en el sistema, para
            ello se solicita memoria para un struct
            color
Parametros: 
s string
r entero
g entero
b entero
Retorno: Puntero a struct color
****************************************************/
color *newColor(char *s, int r, int g, int b) {
    if (checkn(r) || checkn(g) || checkn(b)) return NULL;
    color *self = (color *) malloc(sizeof(color));
    if (self == NULL) return NULL;
    strcpy(self->nombre, s);
    self->red = r;
    self->green = g;
    self->blue = b;
    self->addColor = addColor;
    self->rmColor = rmColor;
    return self;
}

/************* Funcion: delColor *****************
Descripcion: Remueve un color del sistema a partir
            del struct color
Parametros: 
self color
Retorno: void
************************************************/
void delColor(color *self) {
    free((void *) self);
    self = NULL;
}
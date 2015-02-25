#include <stdio.h>
#include <stdlib.h>

typedef char string[30];

typedef struct _color{
	string nombre;
	int red;
	int green;
	int blue;
	void (*addColor)(struct _color *);
	void (*rmColor)(struct _color *);
} color;

void addColor(color *);
void rmColor(color *);
void delColor(color *);
color *newColor(char *, int, int, int);
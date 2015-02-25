#include <stdio.h>
#include <stdlib.h>
#include <ncurses.h>
#include <string.h>
#include "list.h"

#define DEFAULT_ID  -1

int pair_id;
int color_id;

typedef struct curr {
	int x;
	int y;
} Cursor;

typedef struct _dibujante {
	Cursor cursor;
	Cursor maxcoords;
	int height;
	int count;
	void (*DrawGrid) (struct _dibujante *, llist *);
	void (*DrawList) (struct _dibujante *, llist *);
} dibujante;

void DrawGrid(dibujante *, llist *);
void DrawList(dibujante *, llist *);
dibujante *newDibujante(void);
void delDibujante(dibujante *);
void printblock(dibujante *, color *);

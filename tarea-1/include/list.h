#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "color.h"

typedef struct _lnode {
	struct _lnode *next;
	color *data;
} lnode;

typedef struct _llist {
	struct _lnode *nil;
	struct _lnode *tail;
	struct _lnode *curr;
	int length;
	int index;
} llist;

void initList(llist *);
void listAppend(llist *, color *);
void listMoveNext(llist *);
void listMoveToStart(llist *);
void listMoveToEnd(llist *);
void listInsert(llist *, color *);
int listLength(llist *);
void listRemove(llist *);
void listDelete(llist *);
color *listGetItem(llist *);
int listInTail(llist *);
color *listSearch(llist *, char *);
void loadColors(llist *);
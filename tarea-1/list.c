#include "list.h"

/************* Funcion: initList *****************
Descripcion: Inicializa una nueva lista y le asigna
            la memoria requerida
Parametros: 
list *llist
Retorno: void
************************************************/
void initList(llist *list)
{
    list->index = -1;
    list->length = 0;
    list->nil = (struct _lnode *) malloc(sizeof(struct _lnode));
    list->tail = list->nil;
    list->curr = list->nil;
}

/************* Funcion: listAppend *****************
Descripcion: Inserta un nuevo elemento en la lista
Parametros: 
list *llist
item *color
Retorno: void
************************************************/
void listAppend(llist *list, color *item)
{
    struct _lnode *tmp;
    tmp = (struct _lnode *) malloc(sizeof(struct _lnode));
    if (tmp == NULL) return;
    tmp->next = NULL;
    tmp->data = item;
    list->tail->next = tmp;
    list->tail = tmp;
    if (list->length == 0) list->nil->next = list->curr = tmp;
    list->length++;
}

/************* Funcion: listMoveNext *****************
Descripcion: Avanza el puntero de elementos de la lista
            al siguiente que actualmente apunta.
Parametros: 
list *llist
Retorno: void
************************************************/
void listMoveNext(llist *list)
{
    if (list->curr->next == NULL) return;
    list->curr = list->curr->next;
    (list->index)++;
}

/************* Funcion: listMoveToStart *****************
Descripcion: Mueve el puntero de elementos de la lista
            hacia el comienzo de esta
Parametros: 
list *llist
Retorno: void
************************************************/
void listMoveToStart(llist *list)
{
    if (list->curr == list->nil) return;
    list->curr = list->nil->next;
    list->index = 0;
}

/************* Funcion: listMoveToEnd *****************
Descripcion: Mueve el puntero de elementos de la lista
            hacia el final de esta
Parametros: 
list *llist
Retorno: void
************************************************/
void listMoveToEnd(llist *list)
{
    list->curr = list->tail;
    list->index = (list->length) - 1;
}

/************* Funcion: listInsert *****************
Descripcion: Inserta un elemento en la lista en la
            posicion siguiente a la apuntada por el
            puntero de elementos de la lista
Parametros: 
list *llist
item *color
Retorno: void
************************************************/
void listInsert(llist *list, color *item)
{
    struct _lnode *tmp;
    tmp = list->curr->next;
    list->curr->next = (struct _lnode *) malloc(sizeof(struct _lnode));
    list->curr->next->next = tmp;
    list->curr->data = item;
    list->curr = list->curr->next;
    (list->index)++;
    (list->length)++;
}

/************* Funcion: listLength *****************
Descripcion: Retorna el tamano de la lista
Parametros: 
list *llist
Retorno: Entero con el tamano de la lista
************************************************/
int listLength(llist *list)
{
    return list->length;
}

/************* Funcion: listRemove *****************
Descripcion: Elimina el elemento apuntado de la lista
Parametros: 
list *llist
Retorno: void
************************************************/
void listRemove(llist *list)
{
    if (list->curr == NULL) return;
    int i;
    struct _lnode *tmp;
    tmp = list->curr;
    listMoveToStart(list);
    for (i = 0; i < list->index; i++) {
        if (list->curr->next == tmp) {
            list->curr->next = tmp->next;
            if (list->tail == tmp) {
                list->tail = list->curr;
            }
            list->index--;
            list->length--;
            free((void *) tmp);
            break;
        }
        listMoveNext(list);
    }
}

/************* Funcion: listDelete *****************
Descripcion: Elimina la lista y todos sus elementos
            de la memoria
Parametros: 
list *llist
Retorno: void
************************************************/
void listDelete(llist *list)
{
    if (list->curr == NULL) return;
    int i;
    listMoveToEnd(list);
    for (i = 0; i < listLength(list); i++) {
        listRemove(list);
    }
    free(list->nil);
    list->index = -1;
    list->length = 0;
    list->nil = NULL;
    list->tail = NULL;
    list->curr = NULL;
}

/************* Funcion: listSearch *****************
Descripcion: Busca un elemento dentro de la lista
            segun su nombre
Parametros: 
list *llist
s string
Retorno: retorna un puntero al color buscado o bien
        NULL si no se encuentra en la lista
************************************************/
color *listSearch(llist *list, char *s) {
    color *item;
    int i;
    listMoveToStart(list);
    for (i = 0; i < listLength(list); i++) {
        item = listGetItem(list);
        printf("%s", item->nombre);
        if (strcmp(item->nombre, s) == 0) {
            return item;
        }
        listMoveNext(list);
    }
    return NULL;
}

/************* Funcion: listGetItem *****************
Descripcion: Retorna el elemento actualmente apuntado
            por la lista
Parametros: 
list *llist
Retorno: Retorna un puntero al valor actual de la lista
        o NULL si la lista esta vacia
************************************************/
color *listGetItem(llist *list)
{
    if (list->curr == list->nil) return NULL;
    return list->curr->data;
}

/************* Funcion: loadColors *****************
Descripcion: Inserta todos los colores del archivo
            colors.txt en una lista
Parametros: 
list *llist
Retorno: void
************************************************/
void loadColors(llist *L) {
    int r, g, b;
    string nombre;
    color *tmpcolor;

    FILE *input;
    input = fopen("colors.txt", "r+");
    if (input == NULL) return;
    rewind(input);

    while (fscanf(input, "%s\n%d\n%d\n%d\n", nombre, &r, &g, &b) > 0) {
        tmpcolor = newColor(nombre, r, g, b);
        if (tmpcolor == NULL) return;
        listAppend(L, tmpcolor);
    }

    fclose(input);
}
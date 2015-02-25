#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ncurses.h>
#include "dibujador.h"

int main(int argc, char **argv)
{
    color *c;
    llist l;
    initList(&l);
    dibujante *d = newDibujante();
    
    if (argc == 2) {
    	loadColors(&l);
        if (strcmp(argv[1], "-grid") == 0) {
            d->DrawGrid(d, &l);
        } else if (strcmp(argv[1], "-list") == 0) {
            d->DrawList(d, &l);
        } else {
            printf("usage: %s -grid OR %s -list\n", argv[0], argv[0]);
        }
    } else if (argc == 3) {
    	loadColors(&l);
        if (strcmp(argv[1], "-d") == 0) {
	        c = listSearch(&l, argv[2]);
	        if (c == NULL) return 1;
	        c->rmColor(c);
	        listRemove(&l);
	    }
	    //printf("usage: %s -d <nombre_color>\n", argv[0]);
    } else if (argc == 6) {
        if (strcmp(argv[1], "-i") == 0) {
            c = newColor(argv[2], atoi(argv[3]), atoi(argv[4]), atoi(argv[5]));

            c->addColor(c);
            delColor(c);
        } else {
            printf("usage: %s -i <nombre_color> <num red> <num green> <num blue>\n", argv[0]);
        }
    } else {
        printf("Invalid argument\n");
    }
    listDelete(&l);
    return 0;
}

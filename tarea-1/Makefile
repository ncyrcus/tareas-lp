IDIR =include
CC=gcc
CFLAGS=-I$(IDIR)

ODIR=obj
#LDIR =../lib

LIBS=-lncurses

_DEPS = color.h list.h dibujador.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = color.o list.o dibujador.o main.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core main
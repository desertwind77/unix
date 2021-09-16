INCDIR = include
SRCDIR = src
OBJDIR = obj
BINDIR = bin

CC = gcc
CPP = g++
CFLAGS = -I$(INCDIR)
LFLAGS = -lm

SOURCES := $(wildcard $(SRCDIR)/*.cc) 
INCLUDE := $(wildcard $(INCDIR)/*.h)
OBJECT  := $(SOURCES:$(SRCDIR)/%.cc=$(OBJDIR)/%.o)
TARGET  := $(patsubst $(SRCDIR)/%.cc, %, $(SOURCES))
DEPS = $(INCLUDE)

all: $(TARGET)

$(OBJDIR)/%.o: $(SRCDIR)/%.cc $(DEPS)
	mkdir -p $(OBJDIR)
	$(CPP) -c -o $@ $< $(CFLAGS)

# There is a problem here. each binary depends on all objects.
$(TARGET): $(OBJECT) 
	mkdir -p $(BINDIR)
	$(CPP) -o $(BINDIR)/$@ $< 

.PHONY: clean

clean:
	rm -rf core *~ $(OBJDIR) $(INCDIR)/*~ $(BINDIR)

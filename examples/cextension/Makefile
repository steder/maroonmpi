########################
# Mike Steder
# University of Chicago
# 2006
########################

########################
# *IMPORTANT*
# Look over the following variables.
# Edit the values so that they are appropriate
# for your system.
CC=mpicc

# Debugging Options
CCOPTS=-fPIC -g -Wall -ansi #-pedantic 
# Release Options
#CCOPTS=-fPIC -O2

# Libraries and Include Files:
PYTHON=python2.4
PYTHON_INCLUDE=/usr/include/python2.4
# Use this variable to point to your libpython2.x and libmpich
LIBRARY_PATH=
# LIBRARY_PATH=-L/usr/lib -L/usr/local/mympich/lib

OS=$(shell uname -s)

ifeq ($(OS),Linux)
	LD_FLAGS=-shared
endif
ifeq ($(OS),Darwin)
	LD_FLAGS=-bundle -flat_namespace -undefined suppress
endif

# *OPTIONAL*
# Edit these variables to suit your taste:
RM=rm         # command executed to delete make products
CP=cp -rv     # copy command for building tar archive
CD=cd
MV=mv
MKDIR=mkdir      # make directory command for building tar archive
TAR=tar -zcf     # command for creating a tar archive
BZTAR=tar -jcf  # command for creating a tar archive
ZIP=zip -rq 

########################
# Do NOT edit variables below this line 
# (It shouldn't be necessary).
NAME=mikempi
MINOR_NUMBER=$(shell svnversion .)
VERSION=1.0.$(MINOR_NUMBER)
ARCHIVE=$(NAME)-$(VERSION)
TARBALL=$(ARCHIVE).tar.gz
BZTARBALL=$(ARCHIVE).tar.bz2
ZIPFILE=$(ARCHIVE).zip
FILES=Makefile *.c *.py *.h SConstruct *.cfg *.txt 

#MPI:
NAME=simplempi
LIB=_$(NAME).so
LIBRARIES=$(LIBRARY_PATH) -l$(PYTHON)
SRC=$(wildcard *.c)
HEADERS=$(wildcard *.h)
OBJ=$(SRC:.c=.o)
PYBC=$(wildcard *.pyc) $(wildcard mpi/*.pyc)
INTERFACE=$(wildcard *.i)
SWIG_CRUFT=$(wildcard *_wrap.c) $(NAME).py 
### Targets ###

default: $(LIB) 

#$(CC) -Wall -g  -fPIC -I$(PYTHON_INCLUDE)  -c mmpi_module.c -o mmpi_module.o

$(LIB): $(OBJ)
	$(CC) $(LD_FLAGS) $(OBJ) -o $(LIB) $(LIBRARIES)

test.exe: $(OBJ) 
	$(CC) -o test.exe test.o $(LIBRARIES)

$(OBJ): $(HEADERS)

.SUFFIXES: .o .c

.c.o: 
	$(CC) $(CCOPTS) -I$(PYTHON_INCLUDE) -c $< -o $@

swig:
	swig -python $(INTERFACE)

clean:
#@echo "I will clean:" $(OBJ) $(LIB) $(PYBC)
	-$(RM) $(OBJ) $(PYBC) $(LIB) $(SWIG_CRUFT)


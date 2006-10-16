########################
# Mike Steder
# University of Chicago
# 2005
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
#PYTHONLIB=$(PYTHON)

# Defaults:
#PYTHON_INCLUDES=-I/usr/include/python2.4
# Use this variable to point to your libpython2.x and libmpich
#LIBRARY_PATH=
#INCLUDES=

# Mac OS X.4:
PYTHONLIB=python
PYTHON_INCLUDES=-I/Library/Frameworks/Python.framework/Versions/2.4/include/python2.4/ -I/Library/Frameworks/Python.framework/Versions/2.4/include/python2.4/Numeric
LIBRARY_PATH=-L/Library/Frameworks/Python.framework/Versions/2.4/lib/python2.4/ -L/usr/lib/ 
INCLUDES=-I/usr/include/

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
NAME=maroonmpi
MINOR_NUMBER=$(shell svnversion .)
VERSION=1.1.$(MINOR_NUMBER)
ARCHIVE=$(NAME)-$(VERSION)
TARBALL=$(ARCHIVE).tar.gz
BZTARBALL=$(ARCHIVE).tar.bz2
ZIPFILE=$(ARCHIVE).zip
FILES=Makefile *.c *.py *.h SConstruct *.cfg *.txt 

#MPI:
LIBMPI=_mpi.so
LIBMPI_SERIAL=_mpiserial.so
LIBRARIES=$(LIBRARY_PATH) -l$(PYTHONLIB)
LIBRARIES_SERIAL= $(LIBRARY_PATH) -lmpi-serial -l$(PYTHONLIB)
SRC=src/mmpi_module.c
HEADERS=$(wildcard src/mmpi_*.h)
OBJ=$(SRC:.c=.o)
PYBC=$(wildcard *.pyc) $(wildcard mpi/*.pyc)

#MPE:
LIBMPE=_mpe.so
MPESRC=$(wildcard src/mpe_*.c)
MPEHEADERS=$(wildcard src/mpe_*.h)
MPEOBJ=$(MPESRC:.c=.o)
MPELIBRARIES=$(LIBRARIES) -lmpe

#MPI-IO:
IOSRC=src/mmpi_io.c
IOHEADERS=

### Targets ###

default: $(LIBMPI) 
mpe: $(LIBMPE)
serial: $(LIBMPI_SERIAL)

#$(CC) -Wall -g  -fPIC -I$(PYTHON_INCLUDE)  -c mmpi_module.c -o mmpi_module.o

$(LIBMPI): $(OBJ)
	$(CC) $(LD_FLAGS) $(OBJ) -o $(LIBMPI) $(LIBRARIES)
	mv $(LIBMPI) mpi/

$(LIBMPI_SERIAL): $(OBJ)
	${MAKE} src/mpi-serial 
	$(CC) $(LD_FLAGS) $(OBJ) -o $(LIBMPI_SERIAL) -Lsrc/mpi-serial/ $(LIBRARIES_SERIAL)
	mv $(LIBMPI_SERIAL) mpi/$(LIBMPI)

$(LIBMPE): $(MPEOBJ)
	$(CC) $(LD_FLAGS) $(MPEOBJ) -o $(LIBMPE) $(MPELIBRARIES)
	mv $(LIBMPE) mpi/

test.exe: $(OBJ) 
	$(CC) -o test.exe test.o $(LIBRARIES)

$(OBJ): $(HEADERS)

.SUFFIXES: .o .c

.c.o: 
	$(CC) $(CCOPTS) $(INCLUDES) $(PYTHON_INCLUDES) -c $< -o $@

clean:
#@echo "I will clean:" $(OBJ) $(LIBMPI) $(PYBC)
	-$(RM) $(OBJ) $(PYBC) $(LIBMPI) $(LIBMPE) test.exe mpi/$(LIBMPI) mpi/$(LIBMPE) mpi/$(LIBMPI_SERIAL)

distclean:
	-$(RM) dist/*

doc:
	@echo running "epydoc --html --output docs/ --url http://www.penzilla.net/mmpi/ --top http://www.penzilla.net/mmpi/docs/top.shtml mpi"
	@epydoc --html --output docs/ --url http://www.penzilla.net/mmpi/ --top http://www.penzilla.net/mmpi/docs/top.shtml mpi

dist: tar bztar zip

tar: clean 
	svn export . $(ARCHIVE)
	$(TAR) $(TARBALL) $(ARCHIVE)
	$(RM) -rf $(ARCHIVE)
	$(MV) $(TARBALL) dist
	ln -fs $(TARBALL) dist/$(NAME)-current.tar.gz

bztar: clean 
	svn export . $(ARCHIVE)
	$(BZTAR) $(BZTARBALL) $(ARCHIVE)
	$(RM) -rf $(ARCHIVE)
	$(MV) $(BZTARBALL) dist
	ln -fs $(BZTARBALL) dist/$(NAME)-current.tar.bz2		

zip: clean 
	svn export . $(ARCHIVE)
	$(ZIP) $(ZIPFILE) $(ARCHIVE)
	$(RM) -rf $(ARCHIVE)
	$(MV) $(ZIPFILE) dist
	ln -fs $(ZIPFILE) dist/$(NAME)-current.zip

#windows:
#C:\Documents and Settings\steder\Desktop\mikempi>python setup.py build_ext --include-dirs="C:\Program Files\MPICH2\include" -cmingw32 --with-mpicc=gcc --library
#-dirs="C:\Program Files\MPICH2\lib" --libraries="mpi" bdist --formats=wininst
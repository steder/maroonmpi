#FC=g77
AR=ar rv
CC=cc

SHELL		= /bin/sh

# SOURCE FILES

MODULE		= mpi-serial

#SRCS_F90	= fort.F90

SRCS_C		= mpi.c \
		  send.c \
		  recv.c \
		  collective.c \
		  req.c \
		  list.c \
		  handles.c \
                  comm.c \
                  group.c \
                  time.c


OBJS_ALL	= $(SRCS_C:.c=.o) #\
#		  $(SRCS_F90:.F90=.o)


###############################

#include ../Makefile.conf

#
# The values used from Makefile.conf
#

ALLCFLAGS= -DFORTRAN_UNDERSCORE_
# ALLCFLAGS= -DFORTRAN_SAME
# ALLCFLAGS= -DFORTRAN_CAPS




###############################

# TARGETS

default: lib

examples: ctest #ftest


#MPIFH= mpif.$(FORT_SIZE).h

#fort.o: mpif.h

lib:
#	@if [ ! "$(FORT_SIZE)" ] ; \
#           then echo "Please setenv FORT_SIZE (e.g. real4double8 or real8double16)"; \
#                exit 1; fi
#	@if [ ! -r $(MPIFH) ] ; \
#           then echo "Error: there is no $(MPIFH) -" \
#                      "check the environment value of FORT_SIZE" ; \
#                exit 1; fi
#	cp -f $(MPIFH) mpif.h
#	chmod -w mpif.h
	$(MAKE) $(LIB)



lib$(MODULE).a: $(OBJS_ALL)
	echo $(OBJS_ALL)
	$(RM) $@
	$(AR) $@ $(OBJS_ALL)


LIB	= lib$(MODULE).a



###############################
#RULES

.SUFFIXES:
.SUFFIXES: .F90 .c .o

.c.o:
	$(CC) -c $(ALLCFLAGS) $*.c

.f90.o:
	$(FC) -c $(INCPATH) $(DEFS) $(FCFLAGS) $(F90FLAGS) $(MPEUFLAGS) $*.F90

MYF90FLAGS=$(INCPATH) $(DEFS) $(FCFLAGS) $(F90FLAGS) $(MPEUFLAGS)

.F90.o:
	$(FPP) $(DEFS) $(FPPFLAGS) $*.F90 $*.f90 
	$(FC) -c $(INCPATH) $(FCFLAGS) $(F90FLAGS) $(MPEUFLAGS) $*.f90
	$(RM) $*.f90


clean:
	/bin/rm -f *.o ctest ftest $(LIB) mpif.h


install: lib
	$(MKINSTALLDIRS) $(libdir) $(includedir)
	$(INSTALL) lib$(MODULE).a -m 644 $(libdir)
	$(INSTALL) mpi.h -m 644 $(includedir)
	$(INSTALL) mpif.h -m 644 $(includedir)

###############################

#
# test programs
#


ctest: lib ctest.c
	$(CC) $(ALLCFLAGS) -o $@ ctest.c -L. -lmpi-serial

ftest: lib ftest.F90
	$(FC) $(MYF90FLAGS) -o $@ ftest.F90 -L. -lmpi-serial


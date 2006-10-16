/*
  simplempi.h

  This file contains a set of simple MPI functions 
  that will be used to illustrate that C-extensions 
  work properly from within the MMPI environment.
 */
#ifndef SIMPLEMPI_H
#define SIMPLEMPI_H

#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>

int getrank()
{
  int errorcode, rank;
  errorcode = MPI_Comm_rank( MPI_COMM_WORLD, &rank );
  return rank;
}

int getsize()
{
  int errorcode, size;
  errorcode = MPI_Comm_size( MPI_COMM_WORLD, &size );
  return size;
}

int getrankfromcomm( MPI_Comm comm )
{
  int errorcode, rank;
  errorcode = MPI_Comm_rank( comm, &rank );
  return rank;
}

int getsizefromcomm( MPI_Comm comm )
{
  int errorcode, size;
  errorcode = MPI_Comm_size( comm, &size );
  return size;
}

#endif

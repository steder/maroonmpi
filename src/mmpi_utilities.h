/*MMPI - MPI Interface for Python
Copyright (C) 2005 Michael Steder(steder@gmail.com)

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/
/*
  mmpi_utilities.h:

  This header defines functions needed in several other C files.
*/

#ifndef MPIMODULE_UTILITIES_H
#define MPIMODULE_UTILITIES_H

#include "Python.h"
#include "arrayobject.h"
#include "mmpi_globals.h"

#ifndef PyArray_BYTE
#define BYTE PyArray_SBYTE
#else
#define BYTE PyArray_BYTE
#endif

/* This function translates an MPI Type into a Python Type. */
int getPythonType(MPI_Datatype mpitype)
{
  /* Please take note of the shortcutting here when reorganizing 
     For instance, MPI_LONG and MPI_UNSIGNED_LONG both
     drop through to the same return PyArray_LONG; 
   */
    if (mpitype == MPI_BYTE)
    	return BYTE;/* Or PyArray_UBYTE (signed / unsigned) */
    if (mpitype == MPI_CHAR)
      return PyArray_CHAR;
    if (mpitype == MPI_SHORT)
      return PyArray_SHORT;
    if (mpitype == MPI_INT)
      return PyArray_INT;
    if (mpitype == MPI_LONG)
      return PyArray_LONG;
    if (mpitype == MPI_FLOAT)
      return PyArray_FLOAT;
    if (mpitype == MPI_DOUBLE)
      return PyArray_DOUBLE;

    #warning "TODO: the default case in getPythonType should probably throw an exception (TypeError,ValueError) or something rather then just print a warning.\n"
    /* Set an exception handler and return ?? */
    printf("*** Unknown MPI Type -- (Assuming MPI_INT)! ***\n");
    return PyArray_INT;
}

#endif

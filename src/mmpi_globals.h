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
#ifndef MPIMODULE_GLOBALS_H
#define MPIMODULE_GLOBALS_H

/* Standard Header files */
#include "Python.h"
#include "mpi.h"

/* 
msteder: I don't believe this define and com_ray are necessary any longer.
    #define com_ray_size 20
    MPI_Comm com_ray[com_ray_size];
*/


MPI_Status status;

/* ierror is a global that holds the error code of the most
   recent MPI function call.

   If ierror is non-zero an error a MPI error has occured.
 */
long ierror;
static PyObject *mpiException;

/* For mmpi_error.h */
int global_mpi_error_length = 0;
char global_mpi_error_string[MPI_MAX_ERROR_STRING];


#endif

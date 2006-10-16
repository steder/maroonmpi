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

#ifndef MPIMODULE_ERROR_H
#define MPIMODULE_ERROR_H

/* Standard Header files */
#include "Python.h"
#include "arrayobject.h"
#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "mmpi_globals.h"
#include "mmpi_defines.h"
/* Define Error Messages for Error Codes here */

/* Prototypes */
static PyObject *mmpi_abort(PyObject * self, PyObject *args );
static PyObject *mmpi_error(PyObject * self, PyObject * args);
void get_error_string(char *str);
static PyObject *mmpi_error_string(PyObject * self, PyObject * args);
/* I'm shelving this function for now, I don't believe that the error class
   will be useful at the Python level. */
/* SHELVED:

static PyObject *mmpi_error_class(PyObject * self, PyObject * args);

*/

/* Definitions */

#define MPI_ABORT_DOC "\
errorcode = mpi_abort( communicator, errorcode )\n\n\
Terminates MPI execution environment.\n"
static PyObject *mmpi_abort(PyObject * self, PyObject *args )
{
  MPI_Comm comm;
  long errorcode = ierror;
  if(!PyArg_ParseTuple(args, "l|l", &comm, &errorcode ))
    return NULL;

  ierror = MPI_Abort( comm, errorcode );
  return PyInt_FromLong((long)ierror);
}

/* 
   Returns mpi error code from most recent MPI call.
 */
#define MPI_ERROR_DOC "\
errorcode = mpi_error()\n\n\
Returns current error/status code."
static PyObject *mmpi_error(PyObject * self, PyObject * args)
{
    return PyInt_FromLong((long) ierror);
}

/* 
   Returns mpi error message from most recent MPI call.
 */
void set_error_string(void)
{
    MPI_Error_string(ierror, global_mpi_error_string,
		     &global_mpi_error_length);
    return;
}

#define MPI_ERROR_STRING_DOC "\
string = mpi_error_string()\n\n\
Returns a string corresponding to the current error code."
static PyObject *mmpi_error_string(PyObject * self, PyObject * args)
{
    set_error_string();
    return Py_BuildValue("s", global_mpi_error_string);
}
#endif

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
  mmpi_asynchronous.h

  This file defines basic Non-blocking MPI Calls
*/

#ifndef MPIMODULE_ASYNCHRONOUS_H
#define MPIMODULE_ASYNCHRONOUS_H

/* Standard Header files */
#include "mpi.h"
#include "Python.h"
#include "arrayobject.h"
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Include our own code: */
#include "mmpi_defines.h"
#include "mmpi_globals.h"
#include "mmpi_error.h"
#include "mmpi_utilities.h"	/* Includes typedefs and getPythonType() */

/* Prototypes */
static PyObject *mmpi_iprobe(PyObject * self, PyObject * args);
static PyObject *mmpi_test(PyObject * self, PyObject * args);
static PyObject *mmpi_wait(PyObject * self, PyObject * args);
static PyObject *mmpi_isend(PyObject * self, PyObject * args);
static PyObject *mmpi_irecv(PyObject * self, PyObject * args);

/* not yet defined */
static PyObject *mmpi_cancel(PyObject * self, PyObject * args);
static PyObject *mmpi_testall(PyObject * self, PyObject * args);
static PyObject *mmpi_testany(PyObject * self, PyObject * args);
static PyObject *mmpi_testsome(PyObject * self, PyObject * args);
static PyObject *mmpi_test_cancelled(PyObject * self, PyObject * args);
static PyObject *mmpi_waitall(PyObject * self, PyObject * args);
static PyObject *mmpi_waitany(PyObject * self, PyObject * args);
static PyObject *mmpi_waitsome(PyObject * self, PyObject * args);

#define MPI_IPROBE_DOC "flag = iprobe(source, tag, comm)\n\nNonblocking test for a message\n\nSee probe"

static PyObject *mmpi_iprobe(PyObject * self, PyObject * args)
{
    /* int MPI_Iprobe( int source, int tag, MPI_Comm comm, int *flag, MPI_Status *status ) */
    int source, tag, flag;
    MPI_Comm comm;

    if (!PyArg_ParseTuple(args, "iil", &source, &tag, &comm))
	return NULL;
    MPI_Iprobe(source, tag, (MPI_Comm) comm, &flag, &status);
    return PyInt_FromLong((long) flag);
}

#define MPI_TEST_DOC "integer_flag = test( request )\n\nTests for the completion of any previously initiated communications"

static PyObject *mmpi_test(PyObject * self, PyObject * args)
{
/* int MPI_Test (MPI_Request  *request,int *flag, MPI_Status *status) 
 * 
 * The request is the only variable passed in from python.  
 * The flag is the return value.  
 * Status can just be used internally.  If someone were really interested
 * we could return the status information as well.
 */
    MPI_Request req;
    int flag;


    if (!PyArg_ParseTuple(args, "l", &req))
	return NULL;
    /* printf("mpi_test: req = %ld\n",(long)req); */
    ierror = MPI_Test(&req, &flag, &status);

    return PyInt_FromLong((long) flag);
}

#define MPI_WAIT_DOC "status = wait( request )\n\nWaits for an MPI send or receive to complete"
static PyObject *mmpi_wait(PyObject * self, PyObject * args)
{
    /* int MPI_Wait (MPI_Request  *request, MPI_Status *status) */

    MPI_Request request;

    /* Allocate a 3 element array to contain the current status info */
    PyArrayObject *current_status;
    int dimensions[1], statray[3];

    dimensions[0] = 3;
    current_status =
	(PyArrayObject *) PyArray_FromDims(1, dimensions, PyArray_INT);
    /*printf("MPI_Wait does not work yet\n"); */

    if (!PyArg_ParseTuple(args, "l", &request))
	return NULL;

    ierror = MPI_Wait(&request, &status);

    /* Return the current status */
    statray[0] = status.MPI_SOURCE;
    statray[1] = status.MPI_TAG;
    statray[2] = status.MPI_ERROR;
    memcpy((void *) (current_status->data), (void *) statray,
	   (size_t) (12));

    return PyArray_Return(current_status);
}

#define MPI_ISEND_DOC "request = isend( send_buffer, count, datatype, destination, tag, comm )\n\nSends data in buffer to destination in comm.\nThis is a non-blocking send.\n\nSee send"
static PyObject *mmpi_isend(PyObject * self, PyObject * args)
{
/* int MPI_Isend( void *buf, int count, MPI_Datatype datatype, int dest, int tag,MPI_Comm comm, MPI_Request *request ) */

    int count, dest, tag;
    MPI_Datatype datatype;
    MPI_Comm comm;
    int i, n;
    PyObject *input;
    PyArrayObject *array;
    MPI_Request request;
    char *aptr;

    /*printf("this routine is underconstruction\n"); */
    /*printf("Parsing isend arguments...\n"); */
    if (!PyArg_ParseTuple(args, "Oiliil", &input, &count, &datatype, &dest, &tag, &comm)) {
      printf("Error parsing isend arguments...\n");
      return NULL;
    }
    array = (PyArrayObject *) PyArray_ContiguousFromObject(input,
						       getPythonType(datatype), 0, 0);

    if (array == NULL) {
      printf("Error creating input array...\n");
      return NULL;
    }
    n = 1;
    for (i = 0; i < array->nd; i++)
      n *= array->dimensions[i];
    
    if (n < count) {
      printf("Error: n < count ( %d < %d )\n",n, count);
      return NULL;
    }
    aptr = (char *) (array->data);
    
    ierror = MPI_Isend(aptr, count, datatype, dest, tag,comm, &request);
    
    return PyInt_FromLong((long) request);
}

#define MPI_IRECV_DOC "request_id, buffer = irecv( count, datatype, source, tag, comm )\n\nReceive a message into buffer. \n'request_id' represents a handle to use to check on the status of this operation.\nThis is a non-blocking receive.\n\nSee recv"
static PyObject *mmpi_irecv(PyObject * self, PyObject * args)
{
/* int MPI_Irecv( void *buf, int count, MPI_Datatype datatype, int source, int tag, MPI_Comm comm, MPI_Request *request ) */
    /*printf("MPI_Irecv does not work yet\n"); */
    char *array_pointer;
    int dimensions[1];
    long count, source, tag;
    PyArrayObject *buffer;

    MPI_Datatype datatype;
    MPI_Comm comm;
    MPI_Request request_id;

    if (!PyArg_ParseTuple
	(args, "lllll", &count, &datatype, &source, &tag, &comm))
	return NULL;

    dimensions[0] = count;
    buffer = (PyArrayObject *) PyArray_FromDims(1, dimensions,
					   getPythonType(datatype));
    array_pointer = (char *) (buffer->data);
    ierror =
	MPI_Irecv(array_pointer, count, datatype, source, tag, comm,
		  &request_id);

    /* printf("Request_Id = %ld\n",(long)request_id); */
    /* Return Tuple containing Buffer and Request_ID */
    return Py_BuildValue("lO", (long) request_id, PyArray_Return(buffer));
}

#endif

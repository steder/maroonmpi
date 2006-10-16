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
#ifndef MMPI_SYNCHRONOUS_H
#define MMPI_SYNCHRONOUS_H

/* Standard Header files */
#include "Python.h"
#include "arrayobject.h"
#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Include our own code: */
#include "mmpi_defines.h"
#include "mmpi_globals.h"
#include "mmpi_error.h"
#include "mmpi_timing.h"
#include "mmpi_utilities.h"	/* Includes typedefs and getPythonType() */

/* Contains Functions: */

static PyObject *mmpi_send(PyObject * self, PyObject * args);
static PyObject *mmpi_recv(PyObject * self, PyObject * args);
static PyObject *mmpi_barrier(PyObject * self, PyObject * args);
static PyObject *mmpi_status(PyObject * self, PyObject * args);
static PyObject *mmpi_probe(PyObject * self, PyObject * args);
static PyObject *mmpi_get_count(PyObject * self, PyObject * args);

/* Not yet implemented */
static PyObject *mmpi_sendrecv(PyObject * self, PyObject * args);

/* Definitions */

#define MPI_BARRIER_DOC "errorcode = barrier( communicator )\n\nCauses \
all processors in 'communicator' to synchronize at this point\nbefore continuing."
static PyObject *mmpi_barrier(PyObject * self, PyObject * args)
{
    /* int MPI_Barrier ( MPI_Comm comm ) */
    MPI_Comm comm;

    if (!PyArg_ParseTuple(args, "l", &comm))
	return NULL;

    ierror = MPI_Barrier(comm);

    return PyInt_FromLong((long) ierror);
}


#define MPI_SEND_DOC "errorcode = send( buffer, count, datatype, destination, \
tag, communicator )\n\nSends a message to destination in communicator.\nThis \
is a blocking send.\n\nSee isend"
static PyObject *mmpi_send(PyObject * self, PyObject * args)
{
    /* int MPI_Send( void *buf, int count, MPI_Datatype datatype, int dest, int tag, MPI_Comm comm ) */
    int count, dest, tag;
    MPI_Datatype datatype;
    MPI_Comm comm;
    int i, n;
    PyObject *input;
    PyArrayObject *array;
    char *sendbuf;
    
    if (!PyArg_ParseTuple
	(args, "Oiliil", &input, &count, &datatype, &dest, &tag, &comm))
	return NULL;
    array = (PyArrayObject *) PyArray_ContiguousFromObject(input,
						       getPythonType(datatype), 0, 0);
    if (array == NULL)
	return NULL;
    
    if (array->nd == 0)
	n = 1;
    else {
	n = 1;
	for (i = 0; i < array->nd; i++)
	    n = n * array->dimensions[i];
    }

    sendbuf = (char *) (array->data);
    
    ierror = MPI_Send(sendbuf, count, datatype, dest, tag, comm);

    /*printf("Leaving C-MPI_Send...\n"); */
    return PyInt_FromLong((long) ierror);
}

#define MPI_RECV_DOC "result = recv( count, type, source, tag, comm )\
\n\nReceives a message from source in comm.\n\
This is a blocking receive.\n\nSee irecv"
static PyObject *mmpi_recv(PyObject * self, PyObject * args)
{
    /* int MPI_Recv( void *buf, int count, MPI_Datatype datatype, int source, int tag, MPI_Comm comm, MPI_Status *status ) */
    int count, source, tag;
    MPI_Datatype datatype;
    MPI_Comm comm;
    PyArrayObject *result;
    int dimensions[1];
    char *buffer;

    if (!PyArg_ParseTuple(args, "iliil", &count, &datatype, &source, &tag, &comm))
      return NULL;
    dimensions[0] = count;
    result = (PyArrayObject *) PyArray_FromDims(1, dimensions,
					   getPythonType(datatype));
    buffer = (char *) (result->data);
    ierror =
	MPI_Recv(buffer, count, (MPI_Datatype) datatype, source, tag,
		 (MPI_Comm) comm, &status);

    return PyArray_Return(result);
}

#define MPI_STATUS_DOC "status_array = status()\n\nReturns an array of 3 integers.\
\n\tstatus_array[0] -> SOURCE of a recent MPI call\
\n\tstatus_array[1] -> TAG of a recent MPI call\
\n\tstatus_array[2] -> ERROR code from a recent MPI call."
static PyObject *mmpi_status(PyObject * self, PyObject * args)
{
    PyArrayObject *result;
    int dimensions[1], statray[3];

    dimensions[0] = 3;
    result =
	(PyArrayObject *) PyArray_FromDims(1, dimensions, PyArray_INT);
    statray[0] = status.MPI_SOURCE;
    statray[1] = status.MPI_TAG;
    statray[2] = status.MPI_ERROR;
    memcpy((void *) (result->data), (void *) statray, (size_t) (12));
    return PyArray_Return(result);
}

#define MPI_PROBE_DOC "error_code = probe( source, tag, comm )\
\n\nTests to see if a message has been received.\
\nThis is a blocking test for a message.\
\n\nSee iprobe"
static PyObject *mmpi_probe(PyObject * self, PyObject * args)
{
    /* int MPI_Probe( int source, int tag, MPI_Comm comm, MPI_Status *status ) */
    int source, tag;
    MPI_Comm comm;

    if (!PyArg_ParseTuple(args, "iil", &source, &tag, &comm))
	return NULL;
    ierror = MPI_Probe(source, tag, (MPI_Comm) comm, &status);
    
    return PyInt_FromLong((long) ierror);
}

#define MPI_GET_COUNT_DOC "count = get_count( datatype )\
\n\nChecks on the number of elements waiting to be received."
static PyObject *mmpi_get_count(PyObject * self, PyObject * args)
{
    /* int MPI_Get_count( MPI_Status *status, MPI_Datatype datatype, int *count ) */
    MPI_Datatype datatype;
    int count;

    if (!PyArg_ParseTuple(args, "l", &datatype))
	return NULL;
    ierror = MPI_Get_count(&status, (MPI_Datatype) datatype, &count);

    return PyInt_FromLong((long) count);
}

#endif

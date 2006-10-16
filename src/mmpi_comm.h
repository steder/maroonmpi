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

#ifndef MMPI_COMM_H
#define MMPI_COMM_H

/* Standard Header files */
#include "mpi.h"
#include "Python.h"
#include "arrayobject.h"

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/time.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Include our own code: */
#include "mmpi_defines.h"
#include "mmpi_globals.h"
#include "mmpi_error.h"
#include "mmpi_timing.h"
#include "mmpi_utilities.h"	/* Includes typedefs and getPythonType() */

/* Prototypes */
static PyObject *mmpi_comm_compare(PyObject * self, PyObject * args);
static PyObject *mmpi_comm_free(PyObject * self, PyObject * args);
static PyObject *mmpi_comm_size(PyObject * self, PyObject * args);
static PyObject *mmpi_comm_rank(PyObject * self, PyObject * args);
static PyObject *mmpi_group_rank(PyObject * self, PyObject * args);
static PyObject *mmpi_group_incl(PyObject * self, PyObject * args);
static PyObject *mmpi_comm_group(PyObject * self, PyObject * args);
static PyObject *mmpi_comm_dup(PyObject * self, PyObject * args);
static PyObject *mmpi_comm_create(PyObject * self, PyObject * args);
static PyObject *mmpi_comm_split(PyObject * self, PyObject * args);

/* Definitions */
#define MPI_COMM_COMPARE_DOC "result = comm_compare( communicator1, communicator2 )\n\nResult indicates whether communicators 1 and 2 are:\nMPI_IDENT - context and group are the same for both groups\nMPI_CONGRUENT - different contexts but identical groups\nMPI_SIMILAR - different contexts and similar groups\nMPI_UNEQUAL - different contexts and groups are considered unequal and return this status.\n\nCare should be taken when using this routine to check the result against the specific MPI types, otherwise it is possible that all 4 integer results will be interpreted as True.  Using this routine in a boolean context doesn't make sense (although it might seem reasonable to define this method as TRUE if it returns MPI_IDENT and FALSE otherwise)."
static PyObject *mmpi_comm_compare(PyObject * self, PyObject * args)
{
  MPI_Comm comm1,comm2;
  int flag;
  
  if (!PyArg_ParseTuple(args, "ll", &comm1, &comm2))
    return NULL;
  ierror = MPI_Comm_compare( comm1, comm2, &flag );
  return PyInt_FromLong((long) flag);
}

#define MPI_COMM_FREE_DOC "errorcode = comm_free( communicator )\n\nMarks a communicator object for deallocation."
static PyObject *mmpi_comm_free(PyObject * self, PyObject * args)
{
  MPI_Comm comm;
    
  
  if (!PyArg_ParseTuple(args, "l", &comm))
    return NULL;
  ierror = MPI_Comm_free(&comm);
  return PyInt_FromLong((long) ierror);
}

#define MPI_COMM_SIZE_DOC "sizeofcomm = comm_size( communicator )\n\nDetermines the size of the group associated with a communicator"
static PyObject *mmpi_comm_size(PyObject * self, PyObject * args)
{
    MPI_Comm comm;
    int numprocs;

    if (!PyArg_ParseTuple(args, "l", &comm))
	return NULL;
    ierror = MPI_Comm_size((MPI_Comm) comm, &numprocs);
    return PyInt_FromLong((long) numprocs);
}

#define MPI_COMM_RANK_DOC "rankInComm = comm_rank( communicator )\n\nDetermines the rank of the calling process in the communicator"
static PyObject *mmpi_comm_rank(PyObject * self, PyObject * args)
{
    MPI_Comm comm;
    int rank;

    if (!PyArg_ParseTuple(args, "l", &comm))
	return NULL;
    ierror = MPI_Comm_rank((MPI_Comm) comm, &rank);
    return PyInt_FromLong((long) rank);
}

#define MPI_GROUP_RANK_DOC "groupRank = group_rank( group )\n\nReturns the rank of this process in the given group"
static PyObject *mmpi_group_rank(PyObject * self, PyObject * args)
{
    /* int MPI_Group_rank ( MPI_Group group, int *rank ) */
    long in_group;
    int rank;
    MPI_Group group;

    if (!PyArg_ParseTuple(args, "l", &in_group))
	return NULL;
    group = (MPI_Group) in_group;
    ierror = MPI_Group_rank(group, &rank);
    if (ierror != MPI_SUCCESS) {
	printf("MPI Error code %ld occured in mpi_group_rank\n", ierror);
    }
    return PyInt_FromLong((long) rank);
}

#define MPI_GROUP_INCL_DOC "newGroup = group_incl( group, n, ranks )\n\nProduces a group by reording an existing group and taking only listed members"
static PyObject *mmpi_group_incl(PyObject * self, PyObject * args)
{
    /* int MPI_Group_incl ( MPI_Group group, int n, int *ranks, MPI_Group *group_out ) */
    long in_group;
    int *ranks, n;
    MPI_Group group, out_group;
    PyObject *ranks_obj;
    PyArrayObject *array;

    if (!PyArg_ParseTuple(args, "liO", &in_group, &n, &ranks_obj))
	return NULL;
    group = (MPI_Group) in_group;
    array =
	(PyArrayObject *) PyArray_ContiguousFromObject(ranks_obj,
						       PyArray_INT, 1, 1);
    if (array == NULL)
	return NULL;
    if (array->dimensions[0] < n)
	return NULL;
    ranks = (int *) malloc((size_t) (n * sizeof(int)));
    memcpy((void *) ranks, (void *) (array->data),
	   (size_t) (n * sizeof(int)));
    ierror = MPI_Group_incl((MPI_Group) group, n, ranks, &out_group);
    return PyInt_FromLong((long) out_group);
}

#define MPI_COMM_GROUP_DOC "group = comm_group( communicator )\n\nAccesses the group associated with the given communicator"
static PyObject *mmpi_comm_group(PyObject * self, PyObject * args)
{
    /* int MPI_Comm_group ( MPI_Comm comm, MPI_Group *group ) */
    MPI_Group group;
    MPI_Comm comm;

    if (!PyArg_ParseTuple(args, "l", &comm))
	return NULL;
    if ((sizeof(MPI_Group) != sizeof(long))
	&& (sizeof(MPI_Group) != sizeof(int)))
	printf("can not return MPI_Group as long or int sizes %ld %ld %ld",
	       (long) sizeof(MPI_Group), (long) sizeof(long),
	       (long) sizeof(int));
    ierror = MPI_Comm_group((MPI_Comm) comm, &group);
    return PyInt_FromLong((long) group);
}

#define MPI_COMM_DUP_DOC  "newcomm = comm_dup( original_comm )\n\nDuplicates an existing communicator with all its cached information"
static PyObject *mmpi_comm_dup(PyObject * self, PyObject * args)
{
    /* int MPI_Comm_dup ( MPI_Comm comm, MPI_Comm *comm_out ) */

    long tmpcomm;
    MPI_Comm incomm, outcomm;

    if (!PyArg_ParseTuple(args, "l", &tmpcomm))
      return NULL;
    incomm = (MPI_Comm) tmpcomm;
    ierror = MPI_Comm_dup((MPI_Comm) incomm, (MPI_Comm *) & outcomm);
    return PyInt_FromLong((long) outcomm);
}

#define MPI_COMM_CREATE_DOC "newcomm = comm_create( original_comm, group )\n\nCreates a new communicator"
static PyObject *mmpi_comm_create(PyObject * self, PyObject * args)
{
    /* int MPI_Comm_create ( MPI_Comm comm, MPI_Group group, MPI_Comm *comm_out ) */
    MPI_Comm incomm, outcomm;
    long group;

    if (!PyArg_ParseTuple(args, "ll", &incomm, &group))
      return NULL;
    ierror =
	MPI_Comm_create((MPI_Comm) incomm, (MPI_Group) group,
			(MPI_Comm *) & outcomm);
    return PyInt_FromLong((long) outcomm);
}

#define MPI_COMM_SPLIT_DOC "new_comm = comm_split( original_comm, color, key )\n\nCreates a new communicator based on color and keys\nColor and Key are integers.  Processors that call comm_split with the same color\nwill belong to the same new_comm.  The value of Key determines the order the processors\nwill have in new_comm.  If you don't know you need a key value it can just be set to 0"
static PyObject *mmpi_comm_split(PyObject * self, PyObject * args)
{
    /* int MPI_Comm_split ( MPI_Comm comm, int color, int key, MPI_Comm *comm_out ) */

    int color, key;
    MPI_Comm incomm, outcomm;

    if (!PyArg_ParseTuple(args, "lii", &incomm, &color, &key))
	return NULL;
    ierror =
	MPI_Comm_split((MPI_Comm) incomm, color, key,
		       (MPI_Comm *) & outcomm);
    return PyInt_FromLong((long) outcomm);
}

#endif

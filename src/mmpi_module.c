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
/*!
mmpi_module.c

This file actually defines and initializes the Python Extension
Module.  Essentially the "main" of the module is here.
*/


#define MMPI_MODULE_DOC "A C Extension module that defines low level interfaces \
to the Message Passing Interface (MPI).\n\nThis module provides functions for accessing \
the state of the MPI environment as well as wrapped versions of MPI calls.\n\nMike Steder\
 2005 (steder@gmail.com)"
/*
"module _mpi\n\nThis module contains Python versions of the following MPI functions:\n\tmpi_barrier\n\tmpi_send\n\tmpi_recv\n\tmpi_status\n\tmpi_probe\n\tmpi_get_count\n\tmpi_initialized\n\tmpi_init\n\tmpi_start\n\tmpi_finalize\n\tmpi_iprobe\n\tmpi_test\n\tmpi_wait\n\tmpi_isend\n\tmpi_irecv\n\tmpi_bcast\n\tmpi_scatterv\n\tmpi_gatherv\n\tmpi_scatter\n\tmpi_gather\n\tmpi_reduce\n\tmpi_allreduce\n\tmpi_alltoall\n\tmpi_alltoallv\n\tmpi_comm_size\n\tmpi_comm_rank\n\tmpi_group_rank\n\tmpi_group_incl\n\tmpi_comm_group\n\tmpi_comm_dup\n\tmpi_comm_create\n\tmpi_comm_split\n\tmpi_error\n\tmpi_error_string\n\tmpi_wtick\n\tmpi_wtime\n\n"
*/

/* Standard Header files */
#include "Python.h"
/* Python2.5 64-bit Hack for older python versions */
#if PY_VERSION_HEX < 0x02050000 && !defined(PY_SSIZE_T_MIN)
typedef int Py_ssize_t;
#define PY_SSIZE_T_MAX INT_MAX
#define PY_SSIZE_T_MIN INT_MIN
#endif
#include "arrayobject.h"
#include "mpi.h"
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
#include "mmpi_globals.h"/* Variables defined in globals.h
   MPI_Status status;
   int ierror;
   static PyObject *mpiException;
*/

#include "mmpi_utilities.h"	/* Includes typedefs and getPythonType() */
/* Wrapped MPI Functions */
#include "mmpi_timing.h"
#include "mmpi_synchronous.h"
#include "mmpi_asynchronous.h"
#include "mmpi_cartesian.h"
#include "mmpi_collective.h"
#include "mmpi_comm.h"
#include "mmpi_intercomm.h"
#include "mmpi_error.h"
#include "mmpi_graph.h"
#include "mmpi_types.h"


/* Function Prototypes */

/* Adds many integer constants to the module */
void AddIntConstants(PyObject * m);

/* MPI Prototypes */

static PyObject *mmpi_initialized(PyObject * self, PyObject * args);
static PyObject *mmpi_init(PyObject * self, PyObject * args);
static PyObject *mmpi_finalize(PyObject * self, PyObject * args);
static PyObject *mmpi_get_processor_name(PyObject * self, PyObject * args);
static PyObject *mmpi_get_version(PyObject * self, PyObject * args);

/* Definitions */

#define MPI_INITIALIZED_DOC "is_initialized = initialized()\
\n\nReturns true if 'init' has already been called."
static PyObject *mmpi_initialized(PyObject * self, PyObject * args)
{
    int flag;
    ierror = MPI_Initialized(&flag);

    return PyInt_FromLong((long) flag);
}
#define MPI_INIT_DOC "rank,size = init( len(sys.argv), sys.argv )\
\nOR:\nrank,size = init()\
\n\nThis function must be called before any other MPI calls\n(besides 'initialized')\
\nThis is the MPICH version of 'start'.\
\n\nSee initialized, start"
static PyObject *mmpi_init(PyObject * self, PyObject * args)
{
    
    int initialized;
    int myargc = 1;
    char **myargv;
    /* Add one for the NULL at the end  */
    myargv = calloc(myargc + 1, sizeof(char *));
    myargv[0] = strdup("maroonmpi");
    myargv[myargc] = NULL;
    
    ierror = MPI_Init(&myargc, &myargv);

    free( myargv[1] );
    free( myargv[0] );
    free( myargv );

    return PyInt_FromLong((long) ierror);
}

#define MPI_FINALIZE_DOC "finalize()\
\n\nThis function should be called in any program that uses 'init' or 'start'.\
\nThis shuts down the MPI environment and cleans up.\
\nNot calling 'finalize' is considered an error in MPI programs." 
static PyObject *mmpi_finalize(PyObject * self, PyObject * args)
{
    /* int MPI_Finalize() */

    return PyInt_FromLong((long) MPI_Finalize());
}

#define MPI_GET_PROCESSOR_NAME_DOC "get_processor_name()\n\n\
Returns the unique name of the calling processor as a string."
static PyObject *mmpi_get_processor_name(PyObject * self, PyObject * args)
{
  Py_ssize_t length;
  char name[MPI_MAX_PROCESSOR_NAME];
  
  ierror = MPI_Get_processor_name( name, &length );
  return PyString_FromStringAndSize( name, length );
}


#define MPI_GET_VERSION_DOC "get_version()\n\n\
Returns the MPI version as a tuple of integers (majorversion, minorversion)."
static PyObject *mmpi_get_version(PyObject * self, PyObject * args)
{
  int version, subversion;
  
  ierror = MPI_Get_version( &version, &subversion );
  return Py_BuildValue("ll", version, subversion );
}

/* 
   A list of all methods to be included in "_mpi"
   
   Acceptable values for the 3rd element of each entry are:
METH_VARARGS - Typical Case
    The function expects two PyObject* values. The first one is the self object for methods; for module functions, it has the value given to Py_InitModule4() (or NULL if Py_InitModule() was used). The second parameter (often called args) is a tuple object representing all arguments. This parameter is typically processed using PyArg_ParseTuple() or PyArg_UnpackTuple. 

METH_KEYWORDS - Define Functions with Keyword Arguments
    The function expects three parameters: self, args, and a dictionary of all the keyword arguments. The flag is typically combined with METH_VARARGS, and the parameters are typically processed using PyArg_ParseTupleAndKeywords(). 

METH_NOARGS - Optimized No Argument Case
    Methods without parameters don't need to check whether arguments are given if they are listed with the METH_NOARGS flag. When used with object methods, the first parameter is typically named self and will hold a reference to the object instance. In all cases the second parameter will be NULL. 

METH_O - Optimized Single Argument Case
    Methods with a single object argument can be listed with the METH_O flag, instead of invoking PyArg_ParseTuple() with a "O" argument. They have the type PyCFunction, with the self parameter, and a PyObject* parameter representing the single argument. 
 
*/

static PyMethodDef mpiMethods[] = {
  {"mpi_abort",mmpi_abort, METH_VARARGS, MPI_ABORT_DOC},
  {"mpi_allgather",mmpi_allgather, METH_VARARGS, MPI_ALLGATHER_DOC},
  {"mpi_allgatherv",mmpi_allgatherv, METH_VARARGS, MPI_ALLGATHERV_DOC},
  {"mpi_allreduce", mmpi_allreduce, METH_VARARGS, MPI_ALLREDUCE_DOC},
  {"mpi_alltoall", mmpi_alltoall, METH_VARARGS, MPI_ALLTOALL_DOC},
  {"mpi_alltoallv", mmpi_alltoallv, METH_VARARGS, MPI_ALLTOALLV_DOC},
  {"mpi_barrier", mmpi_barrier, METH_VARARGS, MPI_BARRIER_DOC},
  {"mpi_bcast", mmpi_bcast, METH_VARARGS, MPI_BCAST_DOC},
  {"mpi_comm_compare",mmpi_comm_compare, METH_VARARGS, MPI_COMM_COMPARE_DOC},
  {"mpi_comm_create", mmpi_comm_create, METH_VARARGS, MPI_COMM_CREATE_DOC},
  {"mpi_comm_dup", mmpi_comm_dup, METH_VARARGS, MPI_COMM_DUP_DOC},
  {"mpi_comm_free",mmpi_comm_free, METH_VARARGS, MPI_COMM_FREE_DOC},
  {"mpi_comm_group", mmpi_comm_group, METH_VARARGS, MPI_COMM_GROUP_DOC},
  {"mpi_comm_rank", mmpi_comm_rank, METH_VARARGS, MPI_COMM_RANK_DOC},
  {"mpi_comm_size", mmpi_comm_size, METH_VARARGS, MPI_COMM_SIZE_DOC},
  {"mpi_comm_split", mmpi_comm_split, METH_VARARGS, MPI_COMM_SPLIT_DOC},
  {"mpi_error", mmpi_error, METH_NOARGS, MPI_ERROR_DOC},
  {"mpi_error_string", mmpi_error_string, METH_NOARGS, MPI_ERROR_STRING_DOC},
  {"mpi_finalize", mmpi_finalize, METH_NOARGS, MPI_FINALIZE_DOC},
  {"mpi_gather", mmpi_gather, METH_VARARGS, MPI_GATHER_DOC},
  {"mpi_gatherv", mmpi_gatherv, METH_VARARGS, MPI_GATHERV_DOC},
  {"mpi_get_count", mmpi_get_count, METH_VARARGS, MPI_GET_COUNT_DOC},
  {"mpi_get_processor_name",mmpi_get_processor_name,METH_NOARGS,MPI_GET_PROCESSOR_NAME_DOC},
  {"mpi_get_version",mmpi_get_version,METH_NOARGS,MPI_GET_VERSION_DOC},
  {"mpi_group_incl", mmpi_group_incl, METH_VARARGS, MPI_GROUP_INCL_DOC},
  {"mpi_group_rank", mmpi_group_rank, METH_VARARGS, MPI_GROUP_RANK_DOC},
  {"mpi_init", mmpi_init, METH_VARARGS, MPI_INIT_DOC},
  {"mpi_initialized", mmpi_initialized, METH_NOARGS, MPI_INITIALIZED_DOC},
  {"mpi_iprobe", mmpi_iprobe, METH_VARARGS, MPI_IPROBE_DOC},
  {"mpi_irecv", mmpi_irecv, METH_VARARGS, MPI_IRECV_DOC},
  {"mpi_isend", mmpi_isend, METH_VARARGS, MPI_ISEND_DOC},
  {"mpi_probe", mmpi_probe, METH_VARARGS, MPI_PROBE_DOC},
  {"mpi_recv", mmpi_recv, METH_VARARGS, MPI_RECV_DOC},
  {"mpi_reduce", mmpi_reduce, METH_VARARGS, MPI_REDUCE_DOC},
  {"mpi_scan", mmpi_scan, METH_VARARGS, MPI_SCAN_DOC},
  {"mpi_scatter", mmpi_scatter, METH_VARARGS, MPI_SCATTER_DOC},
  {"mpi_scatterv", mmpi_scatterv, METH_VARARGS, MPI_SCATTERV_DOC},
  {"mpi_send", mmpi_send, METH_VARARGS, MPI_SEND_DOC},
  {"mpi_status", mmpi_status, METH_NOARGS, MPI_STATUS_DOC},
  {"mpi_test", mmpi_test, METH_VARARGS, MPI_TEST_DOC},
  {"mpi_wait", mmpi_wait, METH_VARARGS, MPI_WAIT_DOC},
  {"mpi_wtick", mmpi_wtick, METH_NOARGS, MPI_WTICK_DOC},
  {"mpi_wtime", mmpi_wtime, METH_NOARGS, MPI_WTIME_DOC},
  {NULL, NULL, 0, NULL}	/* Sentinel */
};

/* defines and initializes module "_mpi" */
void init_mpi(void)
{
    PyObject *m;		/*, *d; */
    /*PyObject *tmp; */
    import_array();
    m = Py_InitModule3("_mpi", mpiMethods, MMPI_MODULE_DOC);
    mpiException = PyErr_NewException("mpi.Exception", NULL, NULL);
    Py_INCREF(mpiException);
    PyModule_AddObject(m, "MpiException", mpiException);

    /* Add a lot of MPI constants */
    AddIntConstants(m);

    return;
}

void AddIntConstants(PyObject * m)
{
    PyModule_AddIntConstant(m, "MPI_CHAR", (long) MPI_CHAR);
    PyModule_AddIntConstant(m, "MPI_BYTE", (long) MPI_BYTE);
    PyModule_AddIntConstant(m, "MPI_SHORT", (long) MPI_SHORT);
    PyModule_AddIntConstant(m, "MPI_INT", (long) MPI_INT);
    PyModule_AddIntConstant(m, "MPI_LONG", (long) MPI_LONG);
    PyModule_AddIntConstant(m, "MPI_FLOAT", (long) MPI_FLOAT);
    PyModule_AddIntConstant(m, "MPI_DOUBLE", (long) MPI_DOUBLE);
    /*
      These types are supported, but it is unclear what an MPI_UNSIGNED is.  
      Also the utility of UNSIGNED versions of more of these types is unclear.

      Many of these, like MPI_LONG_INT, are really tuples of a LONG and an INT.  
      While these could be useful they are not currently supported.

    PyModule_AddIntConstant(m, "MPI_UNSIGNED_CHAR",(long) MPI_UNSIGNED_CHAR);
    PyModule_AddIntConstant(m, "MPI_UNSIGNED_SHORT",(long) MPI_UNSIGNED_SHORT);
    PyModule_AddIntConstant(m, "MPI_UNSIGNED", (long) MPI_UNSIGNED);
    PyModule_AddIntConstant(m, "MPI_UNSIGNED_LONG",(long) MPI_UNSIGNED_LONG);
    PyModule_AddIntConstant(m, "MPI_LONG_DOUBLE", (long) MPI_LONG_DOUBLE);
    PyModule_AddIntConstant(m, "MPI_FLOAT_INT", (long) MPI_FLOAT_INT);
    PyModule_AddIntConstant(m, "MPI_LONG_INT", (long) MPI_LONG_INT);
    PyModule_AddIntConstant(m, "MPI_SHORT_INT", (long) MPI_SHORT_INT);
    PyModule_AddIntConstant(m, "MPI_2INT", (long) MPI_2INT);    
    PyModule_AddIntConstant(m, "MPI_LONG_DOUBLE_INT",(long) MPI_LONG_DOUBLE_INT);
    PyModule_AddIntConstant(m, "MPI_DOUBLE_INT", (long) MPI_DOUBLE_INT);
    PyModule_AddIntConstant(m, "MPI_LONG_LONG_INT",(long) MPI_LONG_LONG_INT);
    */
    PyModule_AddIntConstant(m, "MPI_PACKED", (long) MPI_PACKED);
    /* Additonal Types Defined within this module for use with Python.
        These types do not exist in MPI and are not specified in the MPI 
        standard.  This is an extension to support some special Python types
        more directly.
     
        Because these types need additional work to implement
       I'm going to stop exporting them for now so that the user doesn't
       stumble on to them by mistake.
    
    PyModule_AddIntConstant(m, "MPI_OBJECT", (long) MMPI_OBJECT);
    PyModule_AddIntConstant(m, "MPI_COMPLEX_FLOAT", (long) MMPI_COMPLEX_FLOAT);
    PyModule_AddIntConstant(m, "MPI_COMPLEX_DOUBLE", (long) MMPI_COMPLEX_DOUBLE);
    PyModule_AddIntConstant(m, "MPI_NOTYPE", (long) MMPI_NOTYPE);
    */
    PyModule_AddIntConstant(m, "MPI_UB", (long) MPI_UB);
    PyModule_AddIntConstant(m, "MPI_LB", (long) MPI_LB);
    PyModule_AddIntConstant(m, "MPI_MAX", (long) MPI_MAX);
    PyModule_AddIntConstant(m, "MPI_MIN", (long) MPI_MIN);
    PyModule_AddIntConstant(m, "MPI_SUM", (long) MPI_SUM);
    PyModule_AddIntConstant(m, "MPI_PROD", (long) MPI_PROD);
    PyModule_AddIntConstant(m, "MPI_LAND", (long) MPI_LAND);
    PyModule_AddIntConstant(m, "MPI_BAND", (long) MPI_BAND);
    PyModule_AddIntConstant(m, "MPI_LOR", (long) MPI_LOR);
    PyModule_AddIntConstant(m, "MPI_BOR", (long) MPI_BOR);
    PyModule_AddIntConstant(m, "MPI_LXOR", (long) MPI_LXOR);
    PyModule_AddIntConstant(m, "MPI_BXOR", (long) MPI_BXOR);
    PyModule_AddIntConstant(m, "MPI_MINLOC", (long) MPI_MINLOC);
    PyModule_AddIntConstant(m, "MPI_MAXLOC", (long) MPI_MAXLOC);
    PyModule_AddIntConstant(m, "MPI_COMM_NULL", (long) MPI_COMM_NULL);
    PyModule_AddIntConstant(m, "MPI_OP_NULL", (long) MPI_OP_NULL);
    PyModule_AddIntConstant(m, "MPI_GROUP_NULL", (long) MPI_GROUP_NULL);
    PyModule_AddIntConstant(m, "MPI_DATATYPE_NULL",
			    (long) MPI_DATATYPE_NULL);
    PyModule_AddIntConstant(m, "MPI_REQUEST_NULL",
			    (long) MPI_REQUEST_NULL);
    PyModule_AddIntConstant(m, "MPI_ERRHANDLER_NULL",
			    (long) MPI_ERRHANDLER_NULL);
    PyModule_AddIntConstant(m, "MPI_MAX_PROCESSOR_NAME",
			    (long) MPI_MAX_PROCESSOR_NAME);
    PyModule_AddIntConstant(m, "MPI_MAX_ERROR_STRING",
			    (long) MPI_MAX_ERROR_STRING);
    PyModule_AddIntConstant(m, "MPI_UNDEFINED", (long) MPI_UNDEFINED);
    PyModule_AddIntConstant(m, "MPI_KEYVAL_INVALID",
			    (long) MPI_KEYVAL_INVALID);
    PyModule_AddIntConstant(m, "MPI_BSEND_OVERHEAD",
			    (long) MPI_BSEND_OVERHEAD);
    PyModule_AddIntConstant(m, "MPI_PROC_NULL", (long) MPI_PROC_NULL);
    PyModule_AddIntConstant(m, "MPI_ANY_SOURCE", (long) MPI_ANY_SOURCE);
    PyModule_AddIntConstant(m, "MPI_ANY_TAG", (long) MPI_ANY_TAG);
    PyModule_AddIntConstant(m, "MPI_BOTTOM", (long) MPI_BOTTOM);
    PyModule_AddIntConstant(m, "MPI_COMM_WORLD", (long) MPI_COMM_WORLD);
    PyModule_AddIntConstant(m, "MPI_SUCCESS", (long) MPI_SUCCESS);
    /* For MPI_Comm_compare */
    PyModule_AddIntConstant(m, "MPI_IDENT", (long) MPI_IDENT);
    PyModule_AddIntConstant(m, "MPI_CONGRUENT", (long) MPI_CONGRUENT);
    PyModule_AddIntConstant(m, "MPI_SIMILAR", (long) MPI_SIMILAR);
    PyModule_AddIntConstant(m, "MPI_UNEQUAL", (long) MPI_UNEQUAL);

    return;
}

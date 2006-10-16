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

#ifndef MMPI_MPE_H
#define MMPI_MPE_H

#define MPE_MODULE_DOC "A C Extension module that defines low level interfaces \
to the MPE logging library.\n\nThis module provides functions for accessing \
the state of the MPE environment as well as wrapped versions of MPE calls.\n\nMike Steder\
 2006 (steder@gmail.com)"

/* Standard Header files */
#include "mpi.h"
#include "mpe.h"
#include "Python.h"
#include "arrayobject.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Our headers */
#include "mmpi_globals.h"
#include "mmpi_defines.h"

/* global */
static PyObject *mpeException;

/* Prototypes */
static PyObject *mmpi_mpe_init_log(PyObject * self, PyObject * args);
static PyObject *mmpi_mpe_finish_log(PyObject * self, PyObject * args);

static PyObject *mmpi_mpe_log_event(PyObject * self, PyObject * args);
static PyObject *mmpi_mpe_describe_event(PyObject * self, PyObject * args);
static PyObject *mmpi_mpe_describe_state(PyObject * self, PyObject * args);

static PyObject *mmpi_mpe_start_log(PyObject * self, PyObject * args);
static PyObject *mmpi_mpe_stop_log(PyObject * self, PyObject * args);


/* Definitions */
/* Comment */
#define MPE_INIT_LOG_DOC "errorcode = mpe_init_log()\n\n \
Initializes the MPE Event Log.\n"
static PyObject *mmpi_mpe_init_log(PyObject * self, PyObject * args)
{
  int errorcode;
  errorcode = MPE_Init_log();
  return Py_BuildValue("i",errorcode);
}

#define MPE_FINISH_LOG_DOC "errorcode = mpe_finish_log( char *filename )\n\n \
Finalizes the MPE Event Log and writes it to disk.\n"
static PyObject *mmpi_mpe_finish_log(PyObject * self, PyObject * args)
{
  int errorcode;
  char *logfilename;
  if (!PyArg_ParseTuple(args, "s", &logfilename))
    return NULL;
  errorcode = MPE_Finish_log(logfilename);
  return Py_BuildValue("i",errorcode);
}

#define MPE_LOG_EVENT_DOC "errorcode = mpe_log_event( int event, int intdata, \
char *chardata )\n\n Create and log an event. \n\
The first integer argument is the *user defined* type of the event.\n\
The second integer argument is essentially for optional data about the event.\n\
The last argument, a string, can be used to describe this specific event.\n"
static PyObject *mmpi_mpe_log_event(PyObject *self, PyObject *args)
{
  int errorcode;
  int eventtype;
  int eventid;
  char *eventdata;
  if (!PyArg_ParseTuple(args,"iis", &eventtype, &eventid, &eventdata))
    return NULL;
  errorcode = MPE_Log_event( eventtype, eventid, eventdata );
  return Py_BuildValue("i",errorcode);
}

#define MPE_DESCRIBE_EVENT_DOC "errorcode = mpe_describe_event( int event, char *description, char *color)\n\n \
This function defines a more indepth description of all events of a given\n \
integer type.  The color string is used by log viewing utilities.\n"
static PyObject *mmpi_mpe_describe_event(PyObject *self, PyObject *args)
{
  int errorcode;
  int eventtype;
  char *description, *color;
  if (!PyArg_ParseTuple(args,"iss", &eventtype, &description, &color))
    return NULL;
  errorcode = MPE_Describe_event( eventtype, description, color );
  return Py_BuildValue("i",errorcode);
}

#define MPE_DESCRIBE_STATE_DOC "errorcode = mpe_describe_state( int start, \
int end, char *name, char *color )\n\n \
A state is represented by the interval between the start and end events.\n \
You can name the state with a string and provide a color string for log\n \
viewers to use to display that event.\n"
static PyObject *mmpi_mpe_describe_state(PyObject *self, PyObject *args)
{
  int errorcode;
  int start,end;
  char *description,*color;
  if (!PyArg_ParseTuple(args,"iiss", &start,&end,&description,&color))
    return NULL;
  errorcode = MPE_Describe_state(start,end,description,color);
  return Py_BuildValue("i",errorcode);
}

#define MPE_START_LOG_DOC "errorcode = mpe_start_log()\n\n \
Used to dynamically turn logging on.  Corresponds to mpe_stop_log.\n"
static PyObject *mmpi_mpe_start_log(PyObject *self, PyObject *args)
{
  int errorcode;
  errorcode = MPE_Start_log();
  return Py_BuildValue("i",errorcode);
}
#define MPE_STOP_LOG_DOC "errorcode = mpe_stop_log()\n\n \
Used to dynamically turn logging off.  Corresponds to mpe_start_log.\n"
static PyObject *mmpi_mpe_stop_log(PyObject *self, PyObject *args)
{
  int errorcode;
  errorcode = MPE_Stop_log();
  return Py_BuildValue("i",errorcode);
}

static PyMethodDef mpeMethods[] = {
  {"mpe_init_log",mmpi_mpe_init_log, METH_NOARGS, MPE_INIT_LOG_DOC},
  {"mpe_finish_log",mmpi_mpe_finish_log, METH_VARARGS, MPE_INIT_LOG_DOC},
  {"mpe_log_event",mmpi_mpe_log_event, METH_VARARGS, MPE_LOG_EVENT_DOC},
  {"mpe_describe_event",mmpi_mpe_describe_event, METH_VARARGS, MPE_DESCRIBE_EVENT_DOC},
  {"mpe_describe_state",mmpi_mpe_describe_state, METH_VARARGS, MPE_DESCRIBE_STATE_DOC},
  {"mpe_start_log",mmpi_mpe_start_log, METH_NOARGS, MPE_START_LOG_DOC},
  {"mpe_stop_log",mmpi_mpe_stop_log, METH_NOARGS, MPE_STOP_LOG_DOC},
  {NULL, NULL, 0, NULL}	/* Sentinel */
};

/* defines and initializes module "_mpe" */
void init_mpe(void)
{
    PyObject *m;		/*, *d; */
    /*PyObject *tmp; */
    import_array();
    m = Py_InitModule3("_mpe", mpeMethods, MPE_MODULE_DOC);
    mpeException = PyErr_NewException("mpe.Exception", NULL, NULL);
    Py_INCREF(mpeException);
    PyModule_AddObject(m, "mpeException", mpeException);

    /* MPE Error Codes */

    PyModule_AddIntConstant(m, "MPE_LOG_OK", (long) MPE_LOG_OK);
    PyModule_AddIntConstant(m, "MPE_LOG_LOCKED_OUT", (long) MPE_LOG_LOCKED_OUT);
    PyModule_AddIntConstant(m, "MPE_LOG_FILE_PROB", (long) MPE_LOG_FILE_PROB);
    PyModule_AddIntConstant(m, "MPE_LOG_NOT_INITIALIZED", (long) MPE_LOG_NOT_INITIALIZED);
    PyModule_AddIntConstant(m, "MPE_LOG_PACK_FAIL", (long) MPE_LOG_PACK_FAIL);
    PyModule_AddIntConstant(m, "MPE_LOG_NO_MEMORY", (long) MPE_LOG_NO_MEMORY);
    
    return;
}

#endif

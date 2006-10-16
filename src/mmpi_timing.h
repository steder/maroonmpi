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

#ifndef MMPI_TIMING_H
#define MMPI_TIMING_H

/* Standard Header files */
#include "mpi.h"
#include "Python.h"
#include "arrayobject.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Our headers */
#include "mmpi_globals.h"
#include "mmpi_defines.h"

/* Prototypes */
static PyObject *mmpi_wtick(PyObject * self, PyObject * args);
static PyObject *mmpi_wtime(PyObject * self, PyObject * args);

/* Definitions */
/*
  MPI_Wtick
  double MPI_Wtick(void)

  Returns the resolution of MPI_Wtime
*/

#define MPI_WTICK_DOC "\
resolution = mpi_wtick()\n\n\
Returns the resolution of mpi_wtime.\n"
static PyObject *mmpi_wtick(PyObject * self, PyObject * args)
{
    double resolution;

    resolution = MPI_Wtick();

    return Py_BuildValue("d", resolution);
}

/*
  MPI_Wtime 
  double MPI_Wtime(void)
  
  Returns an elapsed time on the calling processor
*/
#define MPI_WTIME_DOC "\
elapsedtime = mpi_wtime()\n\n\
Returns elapsed time on the calling processor.\n"
static PyObject *mmpi_wtime(PyObject * self, PyObject * args)
{
    double elapsed_time;

    elapsed_time = MPI_Wtime();

    return Py_BuildValue("d", elapsed_time);
}

#endif

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

#ifndef MMPI_TYPES_H
#define MMPI_TYPES_H

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

#warning "TODO: Implement MPI type creation and manipulation routines."
#warning "TODO: Define flags for building MPI1 and MPI2 functions based on what is available at compile time."

/* Prototypes */


/* Functions that may need to be defined: */
static PyObject *mmpi_pack(PyObject *self, PyObject *args);
static PyObject *mmpi_unpack(PyObject *self, PyObject *args);
static PyObject *mmpi_pack_size(PyObject *self, PyObject *args);
static PyObject *mmpi_type_commit(PyObject *self, PyObject *args);
static PyObject *mmpi_type_contiguous(PyObject *self, PyObject *args);
static PyObject *mmpi_type_create_hindexed(PyObject *self, PyObject *args);
static PyObject *mmpi_type_create_hvector(PyObject *self, PyObject *args);
static PyObject *mmpi_type_create_struct(PyObject *self, PyObject *args);
static PyObject *mmpi_type_get_extent(PyObject *self, PyObject *args);
static PyObject *mmpi_type_size(PyObject *self, PyObject *args);

/* Deprecated: MPICH1 (MPICH2 versions defined above) 
 For example:
  MPI1 version: mmpi_type_extent
  MPI2 version: mmpi_type_get_extent
*/
static PyObject *mmpi_type_extent(PyObject *self, PyObject *args);
static PyObject *mmpi_type_hindexed(PyObject *self, PyObject *args);
static PyObject *mmpi_type_hvector(PyObject *self, PyObject *args);
static PyObject *mmpi_type_indexed(PyObject *self, PyObject *args);
static PyObject *mmpi_type_lb(PyObject *self, PyObject *args);/* lb -> LB -> Lowerbound */

static PyObject *mmpi_type_struct(PyObject *self, PyObject *args);
static PyObject *mmpi_type_ub(PyObject *self, PyObject *args);/* ub -> UB -> Upperbound */
static PyObject *mmpi_type_vector(PyObject *self, PyObject *args);

/* Definitions */

#endif

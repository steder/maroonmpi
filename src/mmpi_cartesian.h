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
  mmpi_cartesian.h

  This file will define the MPI_Cart_* functions.  
  These functions can be used to create and use cartesian communicators.
*/

#ifndef MMPIMODULE_CARTESIAN_H
#define MMPIMODULE_CARTESIAN_H

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
#warning "TODO: Implement Cartesian Communicator Support"
/*static PyObject *mmpi_cart_coords(PyObject * self, PyObject * args);
static PyObject *mmpi_cart_create(PyObject * self, PyObject * args);
static PyObject *mmpi_cart_get(PyObject * self, PyObject * args);
static PyObject *mmpi_cart_map(PyObject * self, PyObject * args);
static PyObject *mmpi_cart_rank(PyObject * self, PyObject * args);
static PyObject *mmpi_cart_shift(PyObject * self, PyObject * args);
static PyObject *mmpi_cart_sub(PyObject * self, PyObject * args);
static PyObject *mmpi_cartdim_get(PyObject * self, PyObject * args);
static PyObject *mmpi_dims_create(PyObject * self, PyObject * args);
static PyObject *mmpi_topo_test(PyObject * self, PyObject * args);
*/
/* Definitions */

#endif

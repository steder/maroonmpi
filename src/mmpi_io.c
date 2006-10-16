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
mmpi_io.c

*/

#define MMPI_IO_DOC ""
/*
"module _mpiio\n
*/
/* Standard Header files */
#include "Python.h"
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

/*
  MPI_FILE_C2F
  MPI_FILE_CALL_ERRHANDLER (fh, errorcode)
  MPI_FILE_CLOSE(fh)
  MPI_FILE_CREATE_ERRHANDLER(function, errhandler)
  MPI_FILE_DELETE(filename, info)
  MPI_FILE_F2C
  MPI_FILE_GET_AMODE(fh, amode)
  MPI_FILE_GET_ATOMICITY(fh, flag)
  MPI_FILE_GET_BYTE_OFFSET(fh, offset, disp)
  MPI_FILE_GET_ERRHANDLER(file, errhandler)
  MPI_FILE_GET_GROUP(fh, group)
  MPI_FILE_GET_INFO(fh, info_used)
  MPI_FILE_GET_POSITION(fh, offset)
  MPI_FILE_GET_POSITION_SHARED(fh, offset)
  MPI_FILE_GET_SIZE(fh, size)
  MPI_FILE_GET_TYPE_EXTENT(fh, datatype, extent)
  MPI_FILE_GET_VIEW(fh, disp, etype, filetype, datarep)
  MPI_FILE_IREAD(fh, buf, count, datatype, request)
  MPI_FILE_IREAD_AT(fh, offset, buf, count, datatype, request)
  MPI_FILE_IREAD_SHARED(fh, buf, count, datatype, request)
  MPI_FILE_IWRITE(fh, buf, count, datatype, request)
  MPI_FILE_IWRITE_AT(fh, offset, buf, count, datatype, request)
  MPI_FILE_IWRITE_SHARED(fh, buf, count, datatype, request)
  MPI_FILE_OPEN(comm, filename, amode, info, fh)
  MPI_FILE_PREALLOCATE(fh, size)
  MPI_FILE_READ(fh, buf, count, datatype, status)
  MPI_FILE_READ_ALL(fh, buf, count, datatype, status)
  MPI_FILE_READ_ALL_BEGIN(fh, buf, count, datatype)
  MPI_FILE_READ_ALL_END(fh, buf, status)
  MPI_FILE_READ_AT(fh, offset, buf, count, datatype, status)
  MPI_FILE_READ_AT_ALL(fh, offset, buf, count, datatype, status)
  MPI_FILE_READ_AT_ALL_BEGIN(fh, offset, buf, count, datatype)
  MPI_FILE_READ_AT_ALL_END(fh, buf, status)
  MPI_FILE_READ_ORDERED(fh, buf, count, datatype, status)
  MPI_FILE_READ_ORDERED_BEGIN(fh, buf, count, datatype)
  MPI_FILE_READ_ORDERED_END(fh, buf, status)
  MPI_FILE_READ_SHARED(fh, buf, count, datatype, status)
  MPI_FILE_SEEK(fh, offset, whence)
  MPI_FILE_SEEK_SHARED(fh, offset, whence)
  MPI_FILE_SET_ATOMICITY(fh, flag)
  MPI_FILE_SET_ERRHANDLER(file, errhandler)
  MPI_FILE_SET_INFO(fh, info)
  MPI_FILE_SET_SIZE(fh, size)
  MPI_FILE_SET_VIEW(fh, disp, etype, filetype, datarep, info)
  MPI_FILE_SYNC(fh)
  MPI_FILE_WRITE(fh, buf, count, datatype, status)
  MPI_FILE_WRITE_ALL(fh, buf, count, datatype, status)
  MPI_FILE_WRITE_ALL_BEGIN(fh, buf, count, datatype)
  MPI_FILE_WRITE_ALL_END(fh, buf, status)
  MPI_FILE_WRITE_AT(fh, offset, buf, count, datatype, status)
  MPI_FILE_WRITE_AT_ALL(fh, offset, buf, count, datatype, status)
  MPI_FILE_WRITE_AT_ALL_BEGIN(fh, offset, buf, count, datatype)
  MPI_FILE_WRITE_AT_ALL_END(fh, buf, status)
  MPI_FILE_WRITE_ORDERED(fh, buf, count, datatype, status)
  MPI_FILE_WRITE_ORDERED_BEGIN(fh, buf, count, datatype)
  MPI_FILE_WRITE_ORDERED_END(fh, buf, status)
  MPI_FILE_WRITE_SHARED(fh, buf, count, datatype, status)
*/

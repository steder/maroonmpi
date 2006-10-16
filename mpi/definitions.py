"""
MMPI - MPI Interface for Python
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
"""

"""
file: definitions.py

---

 Hackery:  importing the constants from the _mpi
 module and making them appear in this namespace.
 So, instead of mpi._mpi.MPI_COMM_WORLD
 you can type:  mpi.MPI_COMM_WORLD
 And MPI_COMM_WORLD can be used directly in this module.

 This allows us to hide the _mpi functions that are undocumented
 in _mpi, and only expose the documented versions I'm defining here.
"""

import _mpi

__import_list = dir(_mpi)
__constants = [ x for x in __import_list if (x.find("MPI")>=0) ]
__attributes = {}
for x in __constants:
    __attributes[x] = getattr(_mpi,x)

__self__ = vars()
for x in __attributes.keys():
    __self__[ x ] = __attributes[x]

del __import_list, __constants, __attributes, x, __self__        

"""
The default MPI Exception Type.  If any exceptions are thrown by the
C Extension module _mpi, they will be of type mpi.Exception.
"""
from _mpi import mpiException

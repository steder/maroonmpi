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
Package MPI

When the MPI package is imported this __init__.py sets up the
default MMPI world.

Other MPI syntaxes are defined in the pympi module.
"""

from core import *

# Use Communicator Objects
# Overwrites a few (comm_split, comm_dup) functions in core.
from communicator import *

# Use Request Objects for Non-blocking Communications
# This overwrites previous imports from the core module.
from request import *

"""
Redefine MPI_COMM_WORLD as a Communicator object
"""
MPI_COMM_WORLD=Communicator( MPI_COMM_WORLD )

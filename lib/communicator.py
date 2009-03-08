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
communicator.py

Defines the Communicator class and provides overloaded methods
of all comm* functions that return communicators when called.  The
overloaded methods wrap their return values into Communicator objects.

Communicator objects provide a default conversion to an integer
(the _mpi functions expect communicators to be passed in as integers).
"""
import core

def comm_dup( comm ):
    """
    new_comm = comm_dup( comm )
    
    Simply makes a copy of comm.
    """
    newcomm = core.comm_dup( comm )
    return Communicator( newcomm )
    
def comm_create(comm, processor_list):
    """
    new_comm = comm_create(comm, processor_list)
    
    processor_list: simple python list specifying all the processors
    to put into the new communicator.
    """
    oldGroup = core.comm_group( comm )
    newGroup = core.group_incl( oldGroup, len(processor_list), processor_list )
    new_comm = core.comm_create( comm, newGroup )
    if new_comm == core.MPI_COMM_NULL:
        return None
    return Communicator( new_comm )
    
def comm_split(comm, color, key=0):
    """
    new_comm = comm_split( comm, color, key )

    color:  all processors that call comm_split with the same color will be put
                into the same communicator.
    key:  determines the order of the processors in the new communicator
    """
    new_comm = core.comm_split( comm, color, key )
    if new_comm == core.MPI_COMM_NULL:
        return None
    return Communicator( new_comm )
    
class Communicator:
    """
        Communicator objects encapsulate integer communicator handles 
    """
    def __init__(self, id):
        self.id = id
        return

    def __del__(self):
        return 

    def __len__(self):
        return self.size()
    
    def __int__(self):
        """
        """
        return self.id

    def __str__(self):
        s = "<communicator#: "
        s += str(self.id)
        s += ",size:" + str(self.size())
        s += ",rank:" + str(self.rank())
        s += ">"
        return s

    def __repr__(self):
        return self.__str__()

    def __getitem__(self,key):
        """
        Implements a pyMPI style slicing cability for Communicators.
        """
        # Create a list from 0 to size - 1:
        myranks = range( self.size() )
        return myranks[key]

    def rank(self):
        """
        rank = comm.rank()

        Returns the rank (processor ID) of the calling processor.
        """
        return core.comm_rank( self.id )
    
    def size(self):
        """
        size = comm.size()

        Returns the size of the communicator
        """
        return core.comm_size( self.id )

    def dup( self ):
        """
        new_comm = old_comm.dup( )
        
        Simply makes a copy (dup->duplicate) of comm.
        """
        return comm_dup( self.id )
    
    def create(self, processor_list):
        """
        new_comm = comm_create(comm, processor_list)
        
        processor_list: simple python list specifying all the processors
        to put into the new communicator.
        """
        return comm_create( self.id, processor_list )
    
    def split(self, color, key=0):
        """
        new_comm = comm_split( comm, color, key )
        
        color:  all processors that call comm_split with the same color will be put
                    into the same communicator.
        key:  determines the order of the processors in the new communicator
        """
        return comm_split( self.id, color, key )

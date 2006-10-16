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
file: pympi.py

------

This module defines an interface similar to PyMPI's. 
"""

import sys,atexit
import pickle
import _mpi, core

"""
 Hackery:  importing the constants from the _mpi
 module and making them appear in this namespace.
 So, instead of mpi._mpi.MPI_COMM_WORLD
 you can type:  mpi.MPI_COMM_WORLD
 And MPI_COMM_WORLD can be used directly in this module.

 This allows us to hide the _mpi functions that are undocumented
 in _mpi, and only expose the documented versions I'm defining here.
"""

import core

# Overloaded Constants
__import_list = dir(_mpi)
__constants = [ x for x in __import_list if (x.find("MPI")>=0) ]
__attributes = {}
for x in __constants:
    __attributes[x] = getattr(_mpi,x)

__self__ = vars()
for x in __attributes.keys():
    # PyMPI drops the "MPI_" from the beginning of it's constants
    part = x.split("_")[1:]
    s = "_".join( part )
    __self__[ s ] = __attributes[x]

del __import_list, __constants, __attributes, x, part, s, __self__        

from _mpi import mpiException as MPIError

# Initialization and Finalization
# PyMPI does this at interpreter startup
# We'll just do it at import time 
rank, size = core.init(len(sys.argv),sys.argv)
# Register a handler for when the interpreter quits
atexit.register( core.finalize )

# Use Communicator Objects
# Overwrites a few (comm_split, comm_dup) functions in core.
import communicator
import request
class Communicator(communicator.Communicator):
    def __init__(self,id):
        communicator.Communicator.__init__(self,int(id))
        self.size = core.comm_size(self.id)
        self.rank = core.comm_rank(self.id)

    def __len__(self):
        return self.size
        
    def __str__(self):
        s = "<communicator#: "
        s += str(self.id)
        s += ",size:" + str(self.size)
        s += ",rank:" + str(self.rank)
        s += ">"
        return s    
        
    def send(self, message, destination, tag=0):
        """
        comm.send( message, destination[, tag(defaults to 0)])

        Sends message to destination with tag (default tag is 0).

        This method will serialize message and send it as an array of characters.
        This method trades efficency for generality: i.e. It takes extra time and bandwidth
        to serialize and transmit the serialized object.  However, any Python object
        that can be Pickled can be sent.

        Currently this method uses the python pickle module(rather then cPickle).
        """
        s = pickle.dumps( message )
        errorcode = core.send( s, len(s), core.MPI_CHAR, destination, tag, self.id )
        return None    

    def isend(self, message, destination, tag=0):
        """
        request = comm.isend( message, destination[, tag(defaults to 0)])

        Sends message to destination with tag (default tag is 0).

        This is a NON-Blocking send, meaning that it does not wait for the send to
        complete before moving on to perform other computations.

        This method will serialize message and send it as an array of characters.
        This method trades efficency for generality: i.e. It takes extra time and bandwidth
        to serialize and transmit the serialized object.  However, any Python object
        that can be Pickled can be sent.

        Currently this method uses the python pickle module(rather then cPickle).
        """
        s = pickle.dumps( message )
        return request.isend( s, len(s), core.MPI_CHAR, destination, tag, self.id )
    

    def recv(self, source=ANY_SOURCE, tag=ANY_TAG ):
        """
        message = comm.recv( [destination(defaults to ANY_SOURCE), tag(defaults to ANY_TAG)])

        Receives a message from any source and tag by default, or from specified source
        and tag.

        This method receives messages as arrays of characters.
        This method trades efficency for generality: i.e. It takes extra time and bandwidth
        to serialize and transmit the serialized object.  However, any Python object
        that can be Pickled can be received.

        Currently this method uses the python pickle module(rather then cPickle).
        """
        core.probe( source, tag, WORLD )
        count = core.get_count( core.MPI_CHAR )
        data = core.recv( count, core.MPI_CHAR, source, tag, self.id )
        message = pickle.loads( data )
        return message

    def irecv( self, source=ANY_SOURCE, tag=ANY_TAG ):
        """
        message,request = comm.recv( [destination(defaults to ANY_SOURCE), tag(defaults to ANY_TAG)])
        if( test(request) ):
            print 'Received message:', message


        Receives a message from any source and tag by default, or from specified source
        and tag.

        This is a NON-Blocking receive, meaning this process will not wait for the data if it is not
        yet ready.  The call will return immediately and you will want to call wait or test on
        the request object before actually using the 'message' object returned by this call.

        This method receives messages as arrays of characters.
        This method trades efficency for generality: i.e. It takes extra time and bandwidth
        to serialize and transmit the serialized object.  However, any Python object
        that can be Pickled can be received.

        Currently this method uses the python pickle module(rather then cPickle).
        """
        core.probe( source, tag, WORLD )
        count = core.get_count( core.MPI_CHAR )
        req, data = request.irecv( count, core.MPI_CHAR, source, tag, self.id )
        message = pickle.loads( data )
        return message,req

    def bcast( self, message, root=0 ):
        """
        """
        s = pickle.dumps( message )
        length = int(core.bcast(len(s),1,core.MPI_INT,root,self.id))
        data = core.bcast( s, length, core.MPI_CHAR, root, self.id )
        newmessage = pickle.loads(data)
        return newmessage

    def gather( self, message, root = 0 ):
        """
        """
        rank = core.comm_rank( self.id )
        size = core.comm_size( self.id )
        #raise NotImplementedError
        s = pickle.dumps(message)

        recvlengths = core.gather(len(s),1,core.MPI_INT,
                                  1, core.MPI_INT,
                                  root, self.id)
        #if(rank==root):
        #    print "recvlengths:",recvlengths

        displacements = [0]
        displ = 0
        for rl in recvlengths[:-1]:
            displacements.append( displ+rl )
            displ += rl
            
        #if(rank==root):
        #    print "displacements:",displacements
            
        data = core.gatherv(s, len(s), core.MPI_CHAR,
                           recvlengths, displacements, core.MPI_CHAR,
                           root, self.id)
        if rank==root:
            data = data.tostring()
        #    print data
        #    print "length of data:",len(data)
            i,n=0,0
        #    print recvlengths
            realdata = []

            for length in recvlengths:
                n += length
        #        print "i,n=%d,%d"%(i,n)
        #        print data[i:n]
                realdata.append(pickle.loads(data[i:n]))
                i += length       
        else:
            realdata = None
        return realdata

    def reduce( self, message, function, root=0 ):
        """
        result = comm.reduce( value(s), function(operation), root(defaults to 0) )

        i.e.:
          global_ave = comm.reduce( local_ave, mpi.MPI_SUM )
        """
        data = self.gather( message, root )
        #realdata = [ pickle.loads(x) for x in data ]
        # apply function to realdata:
        rank = core.comm_rank( self.id )
        if(rank == root):
            #print data
            return function(data)
        else:
            return None
        
    def barrier( self ):
        """
        """
        return core.barrier( self.id )

    def comm_split(self, color, key = 0 ):
        """
        """
        return Communicator(self.split(color,key))

    def comm_dup(self):
        """
        """
        return Communicator(self.dup())

    def comm_create(self, group ):
        """
        """
        return Communicator(self.create(group))

    def comm_rank(self):
        return core.comm_rank( self.id )

    def comm_size(self):
        return core.comm_size( self.id )

# Request Objects
from request import Request

# Overloaded MPI_COMM_WORLD
WORLD=Communicator( COMM_WORLD )
# Overloaded METHODS:
def comm_split( color, key=0 ):
    return WORLD.comm_split(color,key)

def comm_dup():
    return WORLD.comm_dup()

def comm_create( group ):
    return WORLD.comm_create(group)

def comm_rank( ):
    return WORLD.comm_rank()

def comm_size( ):
    return WORLD.comm_size()


#comm_create = communicator.comm_create
#comm_dup = communicator.comm_dup
#comm_split = communicator.comm_split

# New PyMPI-style methods:
def barrier():
    return WORLD.barrier()

def send( message, destination, tag=0 ):
    """
    send( message, destination[, tag(defaults to 0)])
    # Identical to:
    WORLD.send( ... )
    
    Sends message to destination with tag (default tag is 0).
    
    This method will serialize message and send it as an array of characters.
    This method trades efficency for generality: i.e. It takes extra time and bandwidth
    to serialize and transmit the serialized object.  However, any Python object
    that can be Pickled can be sent.
    
    Currently this method uses the python pickle module(rather then cPickle).
    """
    return WORLD.send( message, destination, tag )

def isend( message, destination, tag=0 ):
    return WORLD.isend( message, destination, tag )


def recv( source=ANY_SOURCE, tag=ANY_TAG):
    """
    message = recv( [destination(defaults to ANY_SOURCE), tag(defaults to ANY_TAG)])
    # Identical to:
    WORLD.recv( ... )
    
    Receives a message from any source and tag by default, or from specified source
    and tag.
    
    This method receives messages as arrays of characters.
    This method trades efficency for generality: i.e. It takes extra time and bandwidth
    to serialize and transmit the serialized object.  However, any Python object
    that can be Pickled can be received.
        
    Currently this method uses the python pickle module(rather then cPickle).
    """
    return WORLD.recv( source, tag )

def irecv( source=ANY_SOURCE, tag=ANY_TAG ):
    return WORLD.irecv( source, tag )

def bcast( message, root=0 ):
    return WORLD.bcast( message, root )

def gather( message, root=0 ):
    return WORLD.gather( message, root )



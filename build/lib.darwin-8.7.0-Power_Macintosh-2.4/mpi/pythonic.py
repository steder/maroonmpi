"""
MMPI - MPI Array Interface for Python
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

import core
import array
import serialobject as sobj

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

import types
__single__=[types.BooleanType, types.FloatType, types.IntType, types.LongType,
            types.NoneType]
__sequence__=[types.ListType, types.SliceType,
              #types.StringType, types.StringTypes,
              types.TupleType]

SINGLE=0
SEQUENCE=1
ARRAY=2
OBJECT=3
def getMessageType( obj, error="Unsure how to send object of type:"):
    tobj = type(obj)
    if type(message) in __single__: #single elements (integers, characters)
        messageType = SINGLE
    elif type(message) in __sequence__: #non-array sequences
        try:
            dataType = getSequenceType( message )
            messageType = SEQUENCE
        except TypeError:
            # If it's a funky sequence (like a list of lists)
            # simply serialize and send.
            messageType = OBJECT
    elif array.isArray(message): #Array Case
        messageType = ARRAY
    else: #object case
        messageType = OBJECT
        
def getSingleType( obj,error="Unsure how to send object of type:" ):
    tobj = type(obj)
    if  ( tobj == types.NoneType or tobj == types.BooleanType or
          tobj == types.IntType ):
        return core.MPI_INT
    elif( tobj == types.LongType ):
        return core.MPI_LONG
    elif( tobj == types.FloatType):
        return core.MPI_DOUBLE
    #elif( tobj == types.StringType):
    #    return core.MPI_CHAR
    else:
        raise TypeError,"%s %s ... aborting!"%(error, tobj)
    return

def getSequenceElementType( obj,error="Unsure how to send object of type:" ):
    tobj = type(obj)
    if  ( tobj == types.NoneType or tobj == types.BooleanType or
          tobj == types.IntType ):
        return core.MPI_INT
    elif( tobj == types.LongType ):
        return core.MPI_LONG
    elif( tobj == types.FloatType):
        return core.MPI_DOUBLE
    #elif( tobj == types.StringType):
    #    return core.MPI_CHAR
    else:
        raise TypeError,"%s %s ... aborting!"%(error, tobj)
    return

def getSequenceType( obj ):
    if(len(obj)>0):
        objType = getSequenceElementType(obj[0],
                                error="Unable to send %s of"%(type(obj) ))
    else:
        raise TypeError,"Message is empty sequence, nothing to send!"
    return objType

def formatReturnValue( obj, typestring ):
    if(typestring == "single"):
        return obj[0]
    elif(typestring == "sequence"):
        return obj
    elif(typestring == "array"):
        return obj
    elif(typestring == "object"):
        return obj
    else:
        raise "Unknown return type!"

### "pythonic" MPI functions:
def send(message, destination, tag=0, comm=core.MPI_COMM_WORLD):
    """
    mpi.send( message, destination[, tag(defaults to 0), comm(default is mpi.COMM_WORLD)]))
    
    Sends message to destination with tag (default tag is 0).
    """
    messageType = getMessageType( message )
    core.send( messageType, 1, core.MPI_INT, destination, tag, comm )
    if messageType == SINGLE: #single elements (integers, characters)
        print "Single Element Case:"
        dataType = getSingleType( message )
        core.send( dataType, 1, core.MPI_INT, destination, tag+1, comm )
        returnvalue = core.send( message, 1, dataType, destination, tag+2, comm )
    elif messageType == SEQUENCE: #non-array sequences
        print "Sequence Case:"
        dataType = getSequenceType( message )
        dataType = int(core.send( dataType, 1, core.MPI_INT, destination, tag+1, comm ))
        length = int(core.send( len(message), 1, core.MPI_INT, destination,tag+2, comm))
        returnvalue = core.send(  message, length, dataType, destination, tag+3, comm )
    elif messageType == ARRAY:
        print "Array Case:"
        returnvalue = array.send(message, destination, tag+1, comm )
    else: #object case
        print "Generic Object Case:"
        returnvalue = sobj.send( message, destinaion, tag+1, comm )# (2) are the same
    return returnvalue


def isend(self, message, destination, tag=0):
    """
    request = comm.isend( message, destination[, tag(defaults to 0)])
    
    Sends message to destination with tag (default tag is 0).
    
    This is a NON-Blocking send, meaning this process will not wait for the data if it is not
    yet ready.  The call will immediately return a request object.
    """
    raise NotImplementedError


def recv( source=ANY_SOURCE, tag=ANY_TAG, comm=core.MPI_COMM_WORLD ):
    """
    message = comm.recv( [destination(defaults to ANY_SOURCE), tag(defaults to ANY_TAG)])
    
    Receives a message from any source and tag by default, or from specified source
    and tag.
    """
    messageType = int(core.recv( 1, core.MPI_INT, source, tag, comm ))
    if messageType == SINGLE: #single elements (integers, characters)
        print "Single Element Case:"
        dataType = int(core.recv( 1, core.MPI_INT, source, tag+1, comm ))
        returnvalue = core.recv( message, 1, dataType, source, tag+2, comm )
        returnvalue = formatReturnValue( returnvalue, "single" )
    elif messageType == SEQUENCE: #non-array sequences
        print "Sequence Case:"
        dataType = int(core.recv( 1, core.MPI_INT, source, tag+1, comm ))
        length = int(core.recv( 1, core.MPI_INT, source,tag+2, comm))
        returnvalue = core.recv( length, dataType, source, tag+3, comm )
        returnvalue = formatReturnValue( returnvalue, "single" )
    elif messageType == ARRAY: #Array Case
        print "Array Case:"
        returnvalue = array.send(message, source, tag+1, comm )
    else: #object case
        print "Generic Object Case:"
        returnvalue = sobj.send( message, destinaion, tag+1, comm )# (2) are the same
    return returnvalue

def irecv( self, source=ANY_SOURCE, tag=ANY_TAG ):
    """
    message,request = comm.recv( [source(defaults to ANY_SOURCE), tag(defaults to ANY_TAG)])
    if( test(request) ):
        print 'Received message:', message
    
    Receives a message from any source and tag by default, or from specified source
    and tag.
    
    This is a NON-Blocking receive, meaning this process will not wait for the data if it is not
    yet ready.  The call will return immediately and you will want to call wait or test on
    the request object before actually using the 'message' object returned by this call.
    
    core.probe( source, tag, WORLD )
    count = core.get_count( core.MPI_CHAR )
    """
    raise NotImplementedError
    
def bcast( message, root=0, comm=core.MPI_COMM_WORLD ):
    """
    value = bcast( rootvalue[, root=0, communicator=mpi.COMM_WORLD] )

    Broadcast:  A collective operation that communicates the value on processor 'root' of
    of communicator mpi.COMM_WORLD to all processors in communicator mpi.COMM_WORLD

    rootvalue's value is ignored on non-root processors.

    Example of use:

    # generate / read data:
    if (mpi.COMM_WORLD.comm_rank()==0):
        mydata = somefile.read()
    else:
        mydata = 0
    # broadcast my data from root to all processors:
    mydata = mpi.bcast( mydata )
    # Or equivalently:
    mydata = mpi.bcast( mydata, 0, mpi.COMM_WORLD )
    # Or even:
    mydata = mpi.COMM_WORLD.bcast( mydata )
    # Yet another:
    mydata = mpi.COMM_WORLD.bcast( mydata, 0 )
    # Finally: do something with mydata
    # on all processors.
    """
    if type(message) in __single__: #single elements (integers, characters)
        print "Single Element Case:"
        dataType = getSingleType( message )
        dataType = int(core.bcast( dataType, 1, core.MPI_INT, root, comm ))
        returnvalue = core.bcast( message, 1, dataType, root, comm )
        returnvalue = formatReturnValue( returnvalue, "single" )
    elif type(message) in __sequence__: #non-array sequences
        try:
            print "Sequence Case:"
            dataType = getSequenceType( message )
            dataType = int(core.bcast( dataType, 1, core.MPI_INT, root, comm ))
            length = int(core.bcast( len(message), 1, core.MPI_INT, root, comm))
            returnvalue = core.bcast( message, length, dataType, root, comm )
            returnvalue = formatReturnValue( returnvalue, "sequence" )
        except TypeError:
            print "Complex Sequence Case:"
            # If it's a funky sequence (like a list of lists)
            # simply serialize and send.
            returnvalue = sobj.bcast( message, root, comm ) # (1) and (2)
            returnvalue = formatReturnValue( returnvalue, "object" )
    elif array.isArray(message): #Array Case
        print "Array Case:"
        returnvalue = array.bcast(message, root, comm )
        returnvalue = formatReturnValue( returnvalue, "array" )
    else: #object case
        print "Generic Object Case:"
        returnvalue = sobj.bcast( message, root, comm )# (2) are the same
        returnvalue = formatReturnValue( returnvalue, "object" )
    return returnvalue

def gather( self, message, root = 0 ):
    """
    """
    raise NotImplementedError

def reduce( self, message, function, root=0 ):
    """
    result = comm.reduce( value(s), function(operation), root(defaults to 0) )
    
    i.e.:
        global_ave = comm.reduce( local_ave, mpi.MPI_SUM )
    """
    raise NotImplementedError

# Object Oriented Interface to Pythonic
# Use Communicator Objects
# Overwrites a few (comm_split, comm_dup) functions in core.
import communicator
import request
class Communicator(communicator.Communicator):
    def __init__(self,id):
        communicator.Communicator.__init__(self,int(id))
        self.size = -1
        self.rank = -1
        
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
        """
        raise NotImplementedError

    def isend(self, message, destination, tag=0):
        """
        request = comm.isend( message, destination[, tag(defaults to 0)])

        Sends message to destination with tag (default tag is 0).

        This is a NON-Blocking send, meaning this process will not wait for the data if it is not
        yet ready.  The call will immediately return a request object.
        """
        raise NotImplementedError
    

    def recv(self, source=ANY_SOURCE, tag=ANY_TAG ):
        """
        message = comm.recv( [destination(defaults to ANY_SOURCE), tag(defaults to ANY_TAG)])

        Receives a message from any source and tag by default, or from specified source
        and tag.
        """
        raise NotImplementedError

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

                core.probe( source, tag, WORLD )
                count = core.get_count( core.MPI_CHAR )
        """
        raise NotImplementedError

    def bcast( self, message, root=0 ):
        """
        value = bcast( rootvalue[, root=0, communicator=mpi.COMM_WORLD] )
        
        Broadcast:  A collective operation that communicates the value on processor 'root' of
        of communicator mpi.COMM_WORLD to all processors in communicator mpi.COMM_WORLD
        
        rootvalue's value is ignored on non-root processors.
        
        Example of use:
        
        # generate / read data:
        if (mpi.COMM_WORLD.comm_rank()==0):
            mydata = somefile.read()
        else:
            mydata = 0
        # broadcast my data from root to all processors:
        mydata = mpi.bcast( mydata )
        # Or equivalently:
        mydata = mpi.bcast( mydata, 0, mpi.COMM_WORLD )
        # Or even:
        mydata = mpi.COMM_WORLD.bcast( mydata )
        # Yet another:
        mydata = mpi.COMM_WORLD.bcast( mydata, 0 )
        # Finally: do something with mydata
        # on all processors.
        """
        return bcast( message, root, self.id )

    def gather( self, message, root = 0 ):
        """
        """
        raise NotImplementedError

    def reduce( self, message, function, root=0 ):
        """
        result = comm.reduce( value(s), function(operation), root(defaults to 0) )

        i.e.:
          global_ave = comm.reduce( local_ave, mpi.MPI_SUM )
        """
        raise NotImplementedError
        
    def barrier( self ):
        """
        """
        return core.barrier( self.id )

# Request Objects
from request import Request

# Overloaded MPI_COMM_WORLD
COMM_WORLD=Communicator( COMM_WORLD )



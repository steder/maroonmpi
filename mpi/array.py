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

"""
array.py

Defines a series of specialized methods for handling arrays
while preserving their shape and type.
"""

import core
__arraylib__=[]
try:
    import Numeric
    nm = Numeric
    __arraylib__.append("numeric")
except ImportError:
    pass

try:
    import numpy
    nm = numpy
    __arraylib__.append("numpy")
except ImportError:
    pass

if(len(__arraylib__)==0):
    raise ImportError,"Unable to import either Numeric or Numpy array libraries!\nEither Numeric or Numpy is required for these MPI Array methods."


__types__=["Integer","UnsignedInteger","Float","Character"]
__inverse_typecodes__={}
for label in __types__:
    if "numeric" in __arraylib__:
        for code in Numeric.typecodes[label]:
            __inverse_typecodes__[code] = label
    if "numpy" in __arraylib__:
        for code in numpy.typecodes[label]:
            __inverse_typecodes__[code] = label

def isArray( obj ):
    if "numeric" in __arraylib__:
        if(type(obj) == Numeric.ArrayType):
            return True
    if "numpy" in __arraylib__:
        if(type(obj) == numpy.ArrayType):
            return True
    return False

def getPythonTypeFromNumeric(array):
    return array.typecode()

def getPythonTypeFromNumpy(array):
    return array.dtype

def getMpiType(array):
    try:
        numpytype = getPythonTypeFromNumpy(array)
    except:
        numpytype = None
        
    try:
        numerictype = getPythonTypeFromNumeric(array)
    except:
        numerictype = None
        
    #print numpytype
    #print numerictype

    if( numpytype == None and numerictype == None ):
        raise TypeError,"Unable to determine type of array!"
    elif( numpytype != None and numerictype == None ):
        pytype = numpytype
    elif( numpytype == None and numerictype != None ):
        pytype = numerictype
    else:
        raise TypeError,"Unable to determine type of array!"

    typestring = None
    for c in str(pytype):
        try:
            typestring = __inverse_typecodes__[c]
        except KeyError:
            pass

    if (not typestring):
        raise TypeError,"Unable to find an equivalent MPI type for typecode:%s"%(pytype)
        
    if(typestring == "Integer"):
        return core.MPI_INT
    elif(typestring == "UnsignedInteger"):
        return core.MPI_INT
    elif(typestring == "Float"):
        return core.MPI_DOUBLE
    elif(typestring == "Character"):
        return core.MPI_CHAR
    else:
        raise TypeError,"Unable to find an equivalent MPI type for typecode:%d"%(pytype)

"""
Common Methods       - Numeric          -  numpy  
-----------------------------------------------------------
*size(in elements,   - Numeric.size(A)  -  numpy.size(A)
 ignores 1d,2d,Nd)

*shape               - Numeric.shape(A) - numpy.shape(A)

*rank (len of shape) - Numeric.rank(A)  - numpy.rank(A)

___________________________________________________________

Typecodes            - Numeric          - numpy
------------------------------------------------------------
"""

def allgather( array, comm ):
    myid = core.comm_rank(comm)
    nprocs = core.comm_size(comm)
    if( myid==root ):
        print nm.size(array)
        datatype = getMpiType(array)
        size = nm.size(array)
        shape = nm.shape(array)
        rank = nm.rank(array)
    else:
        datatype = 0
        size = 0
        shape = 0
        rank = 0
    datatype = core.bcast( datatype, 1, core.MPI_INT, root, comm )
    rank = core.bcast( rank, 1, core.MPI_INT, root, comm )
    shape = core.bcast( shape, rank, core.MPI_INT, root, comm )
    size = core.bcast( size, 1, core.MPI_INT, root, comm )
    data = core.allgather( array, size, datatype,
                        size, datatype,
                        root, comm )
    
    print shape
    
    shape[0] = shape[0] * nprocs
        
    print shape
    array = nm.asarray(data)
    print nm.size(array)
    array.shape = shape
    return array

def allgatherv( array, comm ):
    raise NotImplementedError

def allreduce( **args ):
    """
    """
    data = allgather( array, root, comm )
    rank = core.comm_rank( comm )
    return function(data)

def alltoall(**args):
    """
    """
    raise NotImplementedError

def alltoallv(**args):
    """
    """
    raise NotImplementedError

def bcast( array, root, comm ):
    """
    """
    myid = core.comm_rank(comm)
    if(myid == root):
        datatype = getMpiType(array)
        size = nm.size( array )
        shape = nm.shape( array )
        rank = nm.rank( array )
    else:
        datatype = 0
        size = 0
        shape = 0
        rank = 0
    datatype = core.bcast( datatype, 1, core.MPI_INT, root, comm )
    rank = core.bcast( rank, 1, core.MPI_INT, root, comm )
    shape = core.bcast( shape, rank, core.MPI_INT, root, comm )
    size = core.bcast( size, 1, core.MPI_INT, root, comm )
    data = core.bcast( array, size, datatype, root, comm )
    array = nm.asarray(data)
    array.shape = shape
    return array

def gather( array, root, comm ):
    """
    """
    myid = core.comm_rank(comm)
    nprocs = core.comm_size(comm)
    if( myid==root ):
        print nm.size(array)
        datatype = getMpiType(array)
        size = nm.size(array)
        shape = nm.shape(array)
        rank = nm.rank(array)
    else:
        datatype = 0
        size = 0
        shape = 0
        rank = 0
    datatype = core.bcast( datatype, 1, core.MPI_INT, root, comm )
    rank = core.bcast( rank, 1, core.MPI_INT, root, comm )
    shape = core.bcast( shape, rank, core.MPI_INT, root, comm )
    size = core.bcast( size, 1, core.MPI_INT, root, comm )
    data = core.gather( array, size, datatype,
                        size, datatype,
                        root, comm )
    if(myid == root):
        print shape
        
        shape[0] = shape[0] * nprocs
        
        print shape
        array = nm.asarray(data)
        print nm.size(array)
        array.shape = shape
        return array
    else:
        return None

def gatherv( array, root, comm ):
    raise NotImplementedError

def isend( array, destination, tag, communicator ):
    datatype = getMpiType(array)
    size = nm.size( array )
    shape = nm.shape( array )
    rank = nm.rank( array )
    request = core.isend( datatype, 1, core.MPI_INT, destination, tag, communicator )
    request = core.isend( rank, 1, core.MPI_INT, destination, tag+1, communicator )
    request = core.isend( shape, rank, core.MPI_INT, destination, tag+2, communicator )
    request = core.isend( size, 1, core.MPI_INT, destination, tag+3, communicator )
    return core.send( array, size, datatype, destination, tag+4, communicator )

def irecv( source, tag, communicator ):
    datatype = core.irecv( 1, core.MPI_INT, source, tag, communicator )
    rank = core.irecv( 1, core.MPI_INT, source, tag+1, communicator )
    shape = core.irecv( rank, core.MPI_INT, source, tag+2, communicator )
    size = core.irecv( 1, core.MPI_INT, source, tag+3, communicator )
    request,data = core.irecv( size, datatype, source, tag+4, communicator )
    array = nm.asarray(data)
    array.shape = shape
    return request,array

def recv( source, tag, communicator ):
    datatype = core.recv( 1, core.MPI_INT, source, tag, communicator )
    rank = core.recv( 1, core.MPI_INT, source, tag+1, communicator )
    shape = core.recv( rank, core.MPI_INT, source, tag+2, communicator )
    size = core.recv( 1, core.MPI_INT, source, tag+3, communicator )
    data = core.recv( size, datatype, source, tag+4, communicator )
    array = nm.asarray(data)
    array.shape = shape
    return array

def reduce( array, function, root=0, comm=core.MPI_COMM_WORLD ):
    """
    """
    data = gather( array, root, comm )
    rank = core.comm_rank( comm )
    if( rank == root ):
        return function(data)
    else:
        return None

def scan( array, function, comm ):
    data = allgather( array, root, comm )
    rank = core.comm_rank( comm )
    return function(data[0:rank+1])

def scatter( array, root, comm ):
    raise NotImplementedError

def scatterv( array, root, comm ):
    raise NotImplementedError

def send( array, destination, tag, communicator ):
    """
    Specialized array send:

    array.send( myarray, destination, tag, communicator )

    example:
      import mpi
      mpi.array.send( Numeric.ones(100,Numeric.Int32), 0, 7, mpi.MPI_COMM_WORLD )
    """
    datatype = getMpiType(array)
    size = nm.size( array )
    shape = nm.shape( array )
    rank = nm.rank( array )
    
    core.send( datatype, 1, core.MPI_INT, destination, tag, communicator )
    core.send( rank, 1, core.MPI_INT, destination, tag+1, communicator )
    core.send( shape, rank, core.MPI_INT, destination, tag+2, communicator )
    core.send( size, 1, core.MPI_INT, destination, tag+3, communicator )
    return core.send( array, size, datatype, destination, tag+4, communicator )


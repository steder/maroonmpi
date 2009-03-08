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

import core
import pickle

def allgather( message, root=0, comm=core.MPI_COMM_WORLD ):
    """
    """
    return allgatherv( message, root, comm )

def allgatherv( message, root = 0,comm=core.MPI_COMM_WORLD ):
    rank = core.comm_rank( comm )
    size = core.comm_size( comm )
    
    s = pickle.dumps(message)
    
    recvlengths = core.allgather(len(s),1,core.MPI_INT,
                              1, core.MPI_INT,
                              root, comm)
            
    displacements = [0]
    displ = 0
    for rl in recvlengths[:-1]:
        displacements.append( displ+rl )
        displ += rl
        
    #if(rank==root):
    #    print "displacements:",displacements
        
    data = core.allgatherv(s, len(s), core.MPI_CHAR,
                        recvlengths, displacements, core.MPI_CHAR,
                        root, comm)
    
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
    return realdata

def allreduce( message, function, root=0, comm=core.MPI_COMM_WORLD ):
    """
    result = comm.reduce( value(s), function(operation), root(defaults to 0) )
    
    i.e.:
    global_ave = comm.reduce( local_ave, mpi.MPI_SUM )
    """
    data = allgather( message, root, comm )
    #realdata = [ pickle.loads(x) for x in data ]
    # apply function to realdata:
    rank = core.comm_rank( comm )    
    return function(data)

def alltoall(buffer, comm):
    """
    """
    #return
    raise NotImplementedError

def alltoallv(buffer, comm):
    """
    """
    #return
    raise NotImplementedError

def bcast(  message, root=0,comm=core.MPI_COMM_WORLD ):
    s = pickle.dumps( message )
    length = int(core.bcast(len(s),1,core.MPI_INT,root,comm))
    data = core.bcast( s, length, core.MPI_CHAR, root, comm )
    newmessage = pickle.loads(data)
    return newmessage

def gather( message, root=0, comm=core.MPI_COMM_WORLD ):
    """
    implemented by gatherv because
    objects will rarely have the same size.
    """
    return gatherv( message, root, comm )

def gatherv(  message, root = 0,comm=core.MPI_COMM_WORLD ):
    rank = core.comm_rank( comm )
    size = core.comm_size( comm )
    #raise NotImplementedError
    s = pickle.dumps(message)
    
    recvlengths = core.gather(len(s),1,core.MPI_INT,
                              1, core.MPI_INT,
                              root, comm)
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
                        root, comm)
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

def irecv(  source=core.MPI_ANY_SOURCE,
            tag=core.MPI_ANY_TAG,
            comm=core.MPI_COMM_WORLD ):
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
    req, data = request.irecv( count, core.MPI_CHAR, source, tag, comm )
    message = pickle.loads( data )
    return message,req

def isend(message, destination, tag=0, comm=core.MPI_COMM_WORLD):
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
    return request.isend( s, len(s), core.MPI_CHAR, destination, tag, comm )

def recv( source=core.MPI_ANY_SOURCE,
          tag=core.MPI_ANY_TAG,
          comm=core.MPI_COMM_WORLD ):
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
    data = core.recv( count, core.MPI_CHAR, source, tag, comm )
    message = pickle.loads( data )
    return message

def reduce(  message, function, root=0,comm=core.MPI_COMM_WORLD ):
    """
    result = comm.reduce( value(s), function(operation), root(defaults to 0) )
    
    i.e.:
    global_ave = comm.reduce( local_ave, mpi.MPI_SUM )
    """
    data = gather( message, root, comm  )
    #realdata = [ pickle.loads(x) for x in data ]
    # apply function to realdata:
    rank = core.comm_rank( comm )
    if(rank == root):
        #print data
        return function(data)
    else:
        return None

def scan( buffer, function, comm=core.MPI_COMM_WORLD):
    """
    """
    data = allgather( buffer, 0, comm )
    rank = core.comm_rank( comm )
    return function( data[0:rank+1] )

def scatter(buffer, root=0, comm=core.MPI_COMM_WORLD):
    """
    """
    return scatterv( buffer, root, comm )

def scatterv(buffer, root=0, comm=core.MPI_COMM_WORLD):
    """
    Input Parameters
      sendbuf: address of send buffer (choice, significant only at root)
      sendcounts: integer array (of length group size) specifying the number of elements to send to each processor
      displs: integer array (of length group size). Entry i specifies the displacement (relative to sendbuf from which to take the outgoing data to process i
      sendtype: data type of send buffer elements (handle)
      recvcount: number of elements in receive buffer (integer)
      recvtype: data type of receive buffer elements (handle)
      root: rank of sending process (integer)
      comm: communicator (handle)

    Output Parameter
      recvbuf: address of receive buffer (choice)
    """
    size = core.comm_size( comm )
    rank = core.comm_rank( comm )

    length = len(buffer)
    sendbuffer = []
    displacements = []
    sendcounts = []
    charbuffer = ""
    if( rank == root ):
        for b in buffer:
            sendbuffer.append( pickle.dumps( b ) )
        if( length % size == 0 ):
            for x in xrange( size ):
                start = x * size
                end = start + size
                elements = sendbuffer[start:end]
                es = pickle.dumps(elements)
                s = 0
                d = 0
                s = len(es)
                sendcounts.append(s)
                displacements.append(d)
                d += s
                charbuffer += es
        else:
            remainder = length % size
            for x in xrange( size ):
                if( x == 0 ):
                    start = 0
                    end = size + remainder
                else:
                    start = remainder + (x * size)
                    end = start + size
            elements = sendbuffer[start:end]
            es = pickle.dumps(elements)
            s = 0
            d = 0
            s = len(es)
            sendcounts.append(s)
            displacements.append(d)
            d+=s
            charbuffer+=es
        # SEND:
    recvbuffer = core.scatterv( charbuffer, sendcounts, displacements, core.MPI_CHAR,
                   sendcounts[rank], core.MPI_CHAR, root, comm )

    data = pickle.loads(recvbuffer)
    return data

def send(message, destination, tag=0, comm=core.MPI_COMM_WORLD):
    """
    comm.send( message, destination[, tag(defaults to 0)])
    
    Sends message to destination with tag (default tag is 0).
    
    This method will serialize message and send it as an array of characters.
    This method trades efficency for generality: i.e. It takes extra time and bandwidth
    to serialize and transmit the serialized object.  However, any Python object
    that can be Pickled can be sent.
    
v    Currently this method uses the python pickle module(rather then cPickle).
    """
    s = pickle.dumps( message )
    errorcode = core.send( s, len(s), core.MPI_CHAR, destination, tag, comm )
    return None    






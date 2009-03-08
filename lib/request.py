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
request.py

Defines a Request object and overloads asynchronous I/O
methods that normally return integer request handles to
instead return Request objects.

Request objects have a __int__ method to automatically
convert them back to integer handles for use with
_mpi functions.
"""

import core

def test( request ):
    """
    ready = test( request )

    if ( test( request )):
        print 'Non-blocking send or receive operation is complete!'

    Note that the request object is no longer valid after this call
    returns successfully and the operation is complete.
    """
    #raise NotImplementedError,"test has not yet been implemented"
    
    # Invalid Request ID's (ID's for Sends/Recvs that have completed)
    # will cause a crash if they are passed directly to core.mpi_test.
    return request.test()

def wait( request ):
    """
    result = wait( mpi_request )

    request,buffer = mpi.irecv( ... )
    # Do other work:
    # ...
    # wait for the receive to complete so I can use buffer:
    wait(request)
    print 'Received:',buffer
    """
    #raise NotImplementedError,"wait has not yet been implemented"

    # Invalid Request ID's (ID's for Sends/Recvs that have completed)
    # will cause a crash if they are passed directly to core.mpi_test.
    return request.wait()
    
def isend( buffer, count, datatype, destination, tag, comm ):
    """
    request = isend(buffer, count, datatype, destination, tag, communicator)

    Send 'buffer', which consists of 'count' elements of type 'datatype',
    to the processor in 'comm' that has rank 'destination' and is waiting
    for a message with tag == 'tag'.

    Buffer:  Can be a single numeric value or a numeric array.
    Count:  Number of elements in an array, or 1 for scalar data.
    Datatype:  One of a few type constants defined in the mpi module.
    Destination:  Rank in the specified communicator to send this message to.
    Tag:  An arbitrary value used to route messages more precisely.
          Tags are often ignored (especially in simpler programs).  If
          you don't care what the tag is use:  MPI_ANY_TAG
    Comm:  The communicator that contains 'destination'

    Request:  Request is an integer that represents this nonblocking
    send operation.  You use this handle to check on the status of this
    isend by calling functions like test() and wait().

    Example:

    request = send( Numeric.ones(10), 10, MPI_INT, 1, 7, MPI_COMM_WORLD )
    if ( test( request ) ):
        print 'Send complete!'

    # Wait for the send to complete before proceeding:
    wait( request )

    """
    #raise NotImplementedError,"Non-Blocking I/O does not work(yet)"    
    id = core.isend( buffer, count, datatype, destination, tag, comm )
    request = Request( "send", id, buffer, count, datatype, destination, tag, comm )
    return request

def irecv( count, datatype, source, tag, comm ):
    """
    request_id, buffer = irecv( count, datatype, source, tag, communicator )

    irecv and recv have the same argument list but differ in return values.

    receive 'buffer', which consists of 'count' elements of type 'datatype',
    from the processor in 'comm' that has rank 'source' and is waiting
    for a message with tag == 'tag'.

    Request_Id:  This is an integer that provides a handle to pass
    to the functions 'test' and 'wait'.  
    Buffer:  Can be a single numeric value or a numeric array.
    Count:  Number of elements in an array, or 1 for scalar data.
    Datatype:  One of a few type constants defined in the mpi module.
    Source:  Rank in the specified communicator to receive this message from.
    Tag:  An arbitrary value used to route messages more precisely.
          Tags are often ignored (especially in simpler programs).  If
          you don't care what the tag is use:  MPI_ANY_TAG
    Comm:  The communicator that contains 'destination'
    --------------
    Example:

    # Start a recv for a 10 element array:
    >>> request,buffer = mpi.irecv( 10, mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )
    >>> print 'Request #: %s'%(request)
    Request #: 134985008    
    >>> print 'buffer: %s'%(buffer)
    buffer: [0 0 0 0 0 0 0 0 0 0]
    >>> A = Numeric.array([1,2,3,4,5,6,7,8,9,10],Numeric.Int32)
    >>> send_request = mpi.isend( A, 10, mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )
    >>> print 'Sending Request: %s'%(send_request)
    Sending Request: -1409286143
    >>> mpi.wait( request )
    >>> print 'buffer(after send): %s'%(buffer)
    buffer(after send): [ 1  2  3  4  5  6  7  8  9 10]

    --------------

    It's important to note that the initial value of 'buffer' is essentially
    undefined.  The values in 'buffer' can not be trusted until the irecv
    operation is complete.

    We can either use test() or wait() to determine that the irecv has
    finished.

    The wait() call blocks while test() returns immediately.

    After the call to wait() buffer is guaranteed to be set.
    """
    #raise NotImplementedError,"Non-Blocking I/O does not work(yet)"
    id,buffer = core.irecv( count, datatype, source, tag, comm )
    request = Request( "recv", id, buffer, count, datatype, source, tag, comm )
    return request,buffer

class Request:
    """
    Request objects encapsulate request ID's along with the
    buffers they are associated with and the count, type, source
    tag, and comm information.

    This allows the user to examine the types of pending(and completed)
    requests they have going on.  Also, these objects can and will check
    their own state.  You can determine the status and even get the data
    by simply calling the appropriate method on the request object.

    Important methods are:

      test() - returns true (the send/recv has completed) or false.
      wait() - does not return until the data is available.
      status() - prints a description of this request and tests to see if it is complete.
    """
    def __init__(self, type, id, buffer, count, datatype, source_or_destination, tag, comm ):
        """
        Creates a request object.  This is used internally by the MPI
        module.  You should never have to manually create a request object.
        
        my_request = Request( type('send' or 'recv'), request_id, buffer, count, type, source_or_destination, tag, comm )
        """
        self.type = type
        self.id = id
        self.buffer = buffer
        self.count = count
        self.datatype = datatype
        self.target = source_or_destination
        self.tag = tag
        self.comm = comm
        self.valid = True
        self.status = None

    def __int__(self):
        return self.id

    def test(self):
        """
        ready = request.test()

        if ( request.test() ):
            print 'Nonblocking Send/Recv Operation completed!'
        """
        # It's important to note that requests are only valid
        # until the communication operation that they represent
        # completes.
        # A call to the C test() routine with an invalid
        # request ID will crash.
        if( self.valid ):
            if( core.test( self.id ) ):
                self.valid = False
                return True
            else:
                return False
        else:
            return True

    def wait(self):
        # See the note above on Request.test()
        if (self.valid):
            self.status = core.wait( self.id )
            return self.status
        else:
            return self.status

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if ( self.valid ):
            valid="valid"
        else:
            valid="invalid"
        if ( self.type == 'send'):
            target = "destination"
        else:
            target = "source"
        s = "< %s %s request#: %s, count: %s, datatype: %s, %s: %s, tag: %s, comm: %s >" % ( valid, self.type, self.id, self.count, self.datatype, target, self.target, self.tag, self.comm )
        return s

    


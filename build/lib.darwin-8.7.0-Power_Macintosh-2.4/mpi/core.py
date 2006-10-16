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
core.py

Defines 'core' functions.  These functions are just simple wrappers
around the C Extension functions contained in '_mpi.so'.

These functions attempt to deal with the user calling them
before calling MPI_Init with a quick check.  Each of these
functions calls MPI_Initialized and throws an Exception
if MPI_Init has not been called.  This is preferable to an
interpreter crash (the alternative thanks to MPI error handling).
"""

import _mpi

# Hack:  this pulls all the MPI_ constants from _mpi and puts
# them in this namespace.
from definitions import *


"""
Documented definitions of all the functions in _mpi

Some of these functions have additional wrapping.
For instance, the non-blocking I/O operations that return
request ID's are now wrapped to take Request objects as arguments
and to return Request objects as results.

Functions:

  init( argc, argv )
  comm_rank( comm )
  comm_size( comm )
  test( request )
  wait( request )
  isend( buffer, count, datatype, destination, tag, comm )
  send( buffer, count, datatype, destination, tag, comm )
  irecv( count, datatype, source, tag, comm )
  recv( count, datatype, source, tag, comm )
  group_rank( group )
  group_incl( group, n, ranks )
  comm_group( comm )
  comm_dup( comm )
  comm_create( comm, group )
  barrier( comm )
  status( )
  error()
  error_string()
  abort()
  comm_split( incomm, color, key=0 )
  probe( source, tag, comm )
  iprobe( source, tag, comm )
  get_count( datatype )
  bcast( input, count, datatype, source, comm )
  scatterv( sendbuffer, send_count, displacements,
  gatherv( sendbuffer, sendcount, sendtype, recvcount,
  gather( sendbuffer, sendcount, sendtype, recvcount,
  scatter( sendbuffer, send_count, send_type, 
  reduce( send_buff, count, datatype, op, root, comm )
  allreduce( send_buff, count, datatype, op, comm )
  finalize(  )
  alltoall( **args )
  alltoallv( **args )
  wtick()
  wtime()

"""

# Definitions Begin:

def abort( comm, errorcode=None ):
    """
    errorcode = abort(comm [, errorcode ] )

    i.e.:
    ier = send( ... )
    if ( ier ):
       abort( MPI_COMM_WORLD, ier )
       #OR
       abort( MPI_COMM_WORLD )

    Terminates the MPI Execution environment
    """
    if( _mpi.mpi_initialized() ):
        if (errorcode):
            return _mpi.mpi_abort(comm, errorcode)
        else:
            return _mpi.mpi_abort( comm )
    else:
        raise mpiException,"Attempt to call %s before mpi.init!"%("mpi.abort")

def allgather( sendbuffer, sendcount, sendtype, recvcount,
            recvtype, comm ):
    """
    receive_buffer = allgather( sendbuffer,
                             sendcount, # number of elements sent by this processor
                             sendtype,  # datatype
                             recvcount, # number of elements being received from a single processor
                             recvtype,  # datatype
                             comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_allgather( sendbuffer, sendcount, sendtype, recvcount, recvtype, root, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.allgather")

def allgatherv( sendbuffer, sendcount, sendtype,
                recvcount, displacements, recvtype, comm ):
    """
    receive_buffer = allgather( sendbuffer,
                             sendcount, # number of elements sent by this processor
                             sendtype,  # datatype
                             recvcount, # number of elements being received from a single processor
                             recvtype,  # datatype
                             comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_allgatherv( sendbuffer, sendcount, sendtype, recvcount, displacements, recvtype, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.allgatherv")

def allreduce( send_buff, count, datatype, op, comm ):
    """
    result = allreduce( send_buff, count, datatype, op, comm )

    Example:
      sum = allreduce( partial_result, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD )

    'sum' on all processors of MPI_COMM_WORLD will contain the sum
    of all the 'partial_results' of all the processors in MPI_COMM_WORLD.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_allreduce( send_buff, count, datatype, op, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.allreduce")

def alltoall( **args ):
    """
    """
    raise NotImplementedError,"alltoall has not yet been implemented"
    return

def alltoallv( **args ):
    """
    """
    raise NotImplementedError,"alltoallv has not yet been implemented"
    return

def barrier( comm ):
    """
    error_code = barrier( mycomm )

    Causes all processors in 'mycomm'
    to synchronize at the call to 'barrier' before proceeding.

    Barrier is normally used to ensure synchronization between
    processors.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_barrier( comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.barrier")

def bcast( input, count, datatype, source, comm ):
    """
    answer = bcast( 42, 1, MPI_INT, 0, MPI_COMM_WORLD )

    This sends 'count' numbers (in this case just 42) from 'source'
    to every other processor in 'comm'.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_bcast( input, count, datatype, source, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.bcast")

def comm_create( comm, group ):
    """
    newcomm = comm_create( comm, group )

    Creates a new communicator from a current communicator and processor group.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_comm_create( comm, group )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.comm_create")

def comm_dup( comm ):
    """
    copy_of_comm = comm_dup( comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_comm_dup( comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.comm_dup")

def comm_group( comm ):
    """
    group = comm_group( comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_comm_group( comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.comm_group")

def comm_rank( comm ):
    """
    my_rank_in_comm = mpi.comm_rank( comm )

    Returns the rank of this MPI Processor in the communicator 'comm'.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_comm_rank( comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.comm_rank")

def comm_size( comm ):
    """
    size_of_comm = mpi.comm_size( comm )

    Returns the number of MPI Processors in the communicator 'comm'.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_comm_size( comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.comm_size")

def comm_split( incomm, color, key=0 ):
    """
    Creates a new communicator from all the processors in the
    communicator 'incomm'.

    All processors that call 'comm_split' with the same 'color' value
    (an integer >= 0) will be placed in the same communicator.

    'key' determines how the new communicators are sorted.  Unless
    you know you need to change this value the default should be fine.

    Example:
      evenodd_comm = comm_split( MPI_COMM_WORLD, myrank % 2 )

    This divides all your processors into 'even' and 'odd' processors
    depending on their rank and places them into seperate
    'even' and 'odd' communicators.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_comm_split( incomm, color, key )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.comm_split")

def error():
    """
    ierr = error()
    
    Returns most recent MPI calls return value/error code.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_error( )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.error")

def error_string():
    """
    s = error_code()

    Returns the description that corresponds to the current error / status code.
    """
    if( _mpi.mpi_initialized() ):
        return _mpi.mpi_error_string()
    else:
        raise mpiException,"Attempt to call %s before mpi.init!"%("mpi.error_string")

def finalize(  ):
    """
    mpi.finalize() # shutdown MPI

    You should either call this function when you are done making
    MPI calls or before your program exits.
    """
    # print "Entering finalize..."
    if ( _mpi.mpi_initialized() ):
        # print "Calling _mpi.mpi_finalize()..."
        return _mpi.mpi_finalize()
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.finalize")

def gather( sendbuffer, sendcount, sendtype, recvcount,
            recvtype, root, comm ):
    """
    receive_buffer = gather( sendbuffer,
                             sendcount, # number of elements sent by this processor
                             sendtype,  # datatype
                             recvcount, # number of elements being received from a single processor
                             recvtype,  # datatype
                             root,
                             comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_gather( sendbuffer, sendcount, sendtype, recvcount, recvtype, root, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.gather")

def gatherv( sendbuffer, sendcount, sendtype, recvcount,
             displacements, recvtype, root, comm ):
    """
    receive_buffer = gather( sendbuffer, sendcount, sendtype,
                             recvcount, displacements, recvtype,
                             root, comm)

    Gatherv is a special case of gather that allows you to specify
    how the data is distributed by passing a displacements array.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_gatherv( sendbuffer, sendcount, sendtype,
                                 recvcount, displacements, recvtype,
                                 root, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.gatherv")

def get_count( datatype ):
    """
    count = get_count( datatype )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_get_count( datatype )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.get_count")

def get_processor_name():
    """
    result = iprobe( source, tag, comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_get_processor_name()
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.get_processor_name")

def get_version():
    """
    result = iprobe( source, tag, comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_get_version()
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.get_version")

def group_incl( group, n, ranks ):
    """
    group_out = group_incl( group, n, ranks )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_group_incl( group, n, ranks )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.group_incl")

def group_rank( group ):
    """
    rank = group_rank( group, rank )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_group_rank( group )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.group_rank")

def initialized( ):
    """
    init_status = mpi.initialized()
    
    Returns 0 if MPI_Init has not been called.
    Returns Non-Zero if MPI_Init has been called.

    if ( mpi.initialized() ):
      print 'MPI_Init has been called!'
    """
    return _mpi.mpi_initialized( )

def init( argc=None, argv=None ):
    """
    myrank, numprocs = mpi.init( Integer argc, List[String] argv )

    myrank = MPI_Rank of the current process
    numprocs = The number of processors in mpi.MPI_COMM_WORLD
    
    Typically argc and argv are defined as:
      import sys
      argc = len(sys.argv)
      argv = sys.argv 
    """
    if (_mpi.mpi_initialized()):
        raise mpiException, "mpi.init has already been called!"
    if ( (not argc) or (not argv) ):
        import sys
        result = _mpi.mpi_init( len(sys.argv), sys.argv )
    else:
        result = _mpi.mpi_init( argc, argv )
    return result

def iprobe( source, tag, comm ):
    """
    result = iprobe( source, tag, comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_iprobe( source, tag, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.iprobe")

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
    if ( _mpi.mpi_initialized() ):
        id,buffer = _mpi.mpi_irecv( count, datatype, source, tag, comm )
        return id,buffer
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.irecv")

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
    if ( _mpi.mpi_initialized() ):
        id = _mpi.mpi_isend( buffer, count, datatype, destination, tag, comm )
        return id
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.isend")

def probe( source, tag, comm ):
    """
    result = probe( source, tag, comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_probe( source, tag, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.probe")

def recv( count, datatype, source, tag, comm ):
    """
    buffer = recv( count, datatype, source, tag, comm )

    receive 'buffer', which consists of 'count' elements of type 'datatype',
    from the processor in 'comm' that has rank 'source' and is waiting
    for a message with tag == 'tag'.

    Buffer:  Can be a single numeric value or a numeric array.
    Count:  Number of elements in an array, or 1 for scalar data.
    Datatype:  One of a few type constants defined in the mpi module.
    Source:  Rank in the specified communicator to receive this message from.
    Tag:  An arbitrary value used to route messages more precisely.
          Tags are often ignored (especially in simpler programs).  If
          you don't care what the tag is use:  MPI_ANY_TAG
    Comm:  The communicator that contains 'destination'

    Example:

    # This is the complement to the 'send' example above 
    all_ones = recv( 10, MPI_INT, 0, 7, MPI_COMM_WORLD )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_recv( count, datatype, source, tag, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.recv")
    
def reduce( send_buff, count, datatype, op, root, comm ):
    """
    result = reduce( send_buff, count, datatype, op, root, comm )

    Example:

      if ( rank = 0 ):
        sum = reduce( partial_result, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD )
      else:
        reduce( partial_result, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD )
    
    'sum' on processor 0 of MPI_COMM_WORLD will contain the sum
    of all the 'partial_results' of all the processors in MPI_COMM_WORLD.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_reduce( send_buff, count, datatype, op, root, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.reduce")

def scan( send_buff, count, datatype, op, comm ):
    """
    result = scan( send_buff, count, datatype, op, comm )

    Example:

      if ( rank = 0 ):
    
      else:
    
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_scan( send_buff, count, datatype, op, root, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.scan")

def scatter( sendbuffer, send_count, send_type,
             receive_count, receive_type, root, comm ):
    """
    receive_buffer = scatter( sendbuffer, send_count, send_type,
                              receive_count, receive_type, root, comm )
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_scatter( sendbuffer, send_count, send_type, receive_count, receive_type, root, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.scatter")

def scatterv( sendbuffer, send_count, displacements,
              send_type, receive_count, receive_type,
              root, comm ):
    """
    receive_buffer = scatterv( sendbuffer, send_count, displacements,
                       send_type, receive_count, receive_type,
                       root, comm )

    Scatterv is a special case of Scatter that allows you to
    specify displacements.

    displacements : an array of displacements describing
                    what part of sendbuffer to copy to each
                    processor in comm.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_scatterv( sendbuffer, send_count, displacements,
                                  send_type, receive_count, receive_type,
                                  root, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.scatterv")

def send( buffer, count, datatype, destination, tag, comm ):
    """
    error_code = send( buffer, count, datatype, destination, tag, comm )

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

    Example:

    ierr = send( Numeric.ones(10), 10, MPI_INT, 1, 7, MPI_COMM_WORLD )
    if( ierr ):
        print 'unable to send message to node 1'
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_send( buffer, count, datatype, destination, tag, comm )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.send")

def status( ):
    """
    ( source, tag, error ) = status()

    This function returns 3 mpi status bits describing the
    source, tag, and error.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_status()
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.status")

def test( request ):
    """
    ready = test( request_id )

    if ( test( request_id )):
        print 'Non-blocking send or receive operation is complete!'

    Note that the request ID is no longer valid after this call
    returns successfully and the operation is complete.
    """
    #raise NotImplementedError,"test has not yet been implemented"
    
    # Invalid Request ID's (ID's for Sends/Recvs that have completed)
    # will cause a crash if they are passed directly to _mpi.mpi_test.
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_test( request )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.test")

def wait( request ):
    """
    request_id = wait( request_id )

    request_id,buffer = mpi.irecv( ... )
    # Do other work:
    # ...
    # wait for the receive to complete so I can use buffer:
    wait(request_id)
    print 'Received:',buffer

    Invalid Request ID's (ID's for Sends/Recvs that have completed)
    will cause a crash if they are passed directly to _mpi.mpi_wait.
    """
    #raise NotImplementedError,"wait has not yet been implemented"
    
    # Invalid Request ID's (ID's for Sends/Recvs that have completed)
    # will cause a crash if they are passed directly to _mpi.mpi_wait.
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_wait( request )
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.wait")

def wtick():
    """
    resolution = wtick()

    Returns the resolution of wtime.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_wtick()
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.wtick")
    
def wtime():
    """
    time = wtime()

    Returns elapsed time on the calling processor.
    """
    if ( _mpi.mpi_initialized() ):
        return _mpi.mpi_wtime()
    else:
        raise mpiException, "Attempt to call %s before mpi.init!"%("mpi.wtime")



#####################################

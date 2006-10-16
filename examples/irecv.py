import sys
import Numeric
import mpi

try:
    rank,size = mpi.init( len(sys.argv), sys.argv )

    request,buffer = mpi.irecv( 10, mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )

    print "Request #: %s"%(request)
    print "buffer: %s"%(buffer)

    A = Numeric.array([1,2,3,4,5,6,7,8,9,10],Numeric.Int32)
    send_request = mpi.isend( A, 10, mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )
    print "Sending Request: %s"%(send_request)
    status = mpi.wait( request )
    status = mpi.wait( send_request )
    print "buffer(after send): %s"%(buffer)
    print "status:",status
    mpi.finalize()
except:
    mpi.finalize()
    raise

import mpi
import sys, Numeric

print "Creating Data Array..."
data = Numeric.array( [1,2,3,4], Numeric.Int32 )

print "Initializing MPI: (%s,%s)"%(len(sys.argv),sys.argv)
rank, size = mpi.init( len(sys.argv), sys.argv )
print "(%s,%s): initialized..." %(rank,size)

if( rank == 0 ):
    print "(%s,%s): sending: %s" %( rank, size, data )
    request = mpi.isend( data, 4, mpi.MPI_INT, 1, 0, mpi.MPI_COMM_WORLD )
    print "(%s,%s): request#: %s" %( rank, size, request )
    data2 = Numeric.array([ -1, -1, -1, -1 ], Numeric.Int32 )
elif(rank == 1):
    print "(%s,%s): receiving..." %(rank,size)
    data2 = mpi.recv( 4, mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )
else:
    pass

print "(%s,%s): received: %s" % ( rank, size, data2 )

mpi.finalize()

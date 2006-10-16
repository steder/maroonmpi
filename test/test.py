import mpi
import sys, Numeric

print "Creating Data Array..."
data = Numeric.array( [1,2,3,4], Numeric.Int32 )

rank, size = mpi.init( len(sys.argv), sys.argv )
assert size == 2
print "(%s,%s): initialized..." %(rank,size)

if( rank == 0 ):
    print "(%s,%s): sending: %s" %( rank, size, data )
    mpi.send( data, 4, mpi.MPI_INT, 1, 0, mpi.MPI_COMM_WORLD )
    data2 = Numeric.array([ -1, -1, -1, -1 ], Numeric.Int32 )
else:
    print "(%s,%s): receiving..." %(rank,size)
    data2 = mpi.recv( 4, mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )
    print "(%s,%s): received: %s" %(rank, size, data2)

print "(%s,%s): received: %s" % ( rank, size, data2 )

mpi.finalize()

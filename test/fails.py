import mpi
import sys, Numeric
import os

print "Creating Data Array..."
data = Numeric.array( [1,2,3,4], Numeric.Int32 )

rank, size = mpi.init( len(sys.argv), sys.argv )
print "(%s,%s): initialized..." %(rank,size)

returnCode = 1

if ( rank == 0 ):
    print "(%s,%s): sending: %s" %( rank, size, data )
    request = mpi.isend( data, 4, mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )
    print "(%s,%s): request#: %s" %( rank, size, request )
    print "(%s,%s): receiving..." %(rank,size)
    data2 = mpi.recv( 4, mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )
    print "(%s,%s): received: %s" %(rank, size, data2)

    file = open("fails.py.out","a")
    file.write( "My return code is %s\n"%returnCode )
    file.close()
    mpi.barrier(mpi.MPI_COMM_WORLD)
    
    mpi.abort(mpi.MPI_COMM_WORLD, returnCode)
else:
    mpi.barrier(mpi.MPI_COMM_WORLD)
    

mpi.finalize()

"""
Shape is not retained between sender and receiver.

This really should be fixed.
"""
import Numeric
import mpi
A = Numeric.ones( (3,4), 'i' )
rank,size = mpi.init()
if (rank == 0:
    mpi.isend( A, (3*4), mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )
    #[ valid send request#: -1409286144, count: 12, datatype: 1275069445, destination: 0, tag: 0, comm: [communicator#:1140850688,size:1] ]
    B = mpi.recv( (3*4), mpi.MPI_INT, 0, 0, mpi.MPI_COMM_WORLD )
    # array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],'i')
else:
    pass

mpi.finalize()

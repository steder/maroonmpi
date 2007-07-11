import mpi
import Numeric as nm

import mpi.pythonic
test = mpi.pythonic.bcast( 0 )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( 1.0 )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( "a" )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( 'b' )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( "hello" )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( (1,2,3) )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( [1,2,3,4,5,6,7,8,9,10] )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( [1.0,2.0,3.0,4.0,5.0] )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( nm.array([1,2,3,4,5],nm.Int32) )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( nm.array([[1,2,3,4,5],[6,7,8,9,0]],nm.Int32) )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( ["hello","mpi","world"] )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
test = mpi.pythonic.bcast( mpi.comm_rank )
mpi.barrier(mpi.MPI_COMM_WORLD)
print test
print test(mpi.MPI_COMM_WORLD)

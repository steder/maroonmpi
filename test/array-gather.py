import Numeric as nm
#import numpy as nm
import mpi
import mpi.array
rank,size = mpi.init()

assert size >= 2

if(rank == 0):
    mydata = nm.ones((3,3,3),nm.Int32)
else:
    mydata = nm.zeros((3,3,3),nm.Int32)

result = mpi.array.gather( mydata, 0, mpi.MPI_COMM_WORLD )

for i in range(size):
    if (rank == i):
        print result
    mpi.barrier(mpi.MPI_COMM_WORLD)

mpi.finalize()

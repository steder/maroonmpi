#import Numeric as nm
import numpy as nm
import mpi
import mpi.array
rank,size = mpi.init()

assert size >= 2

if(rank == 0):
    mydata = nm.ones((3,3,3),nm.Int32)
    mpi.array.send( mydata, 1, 7, mpi.MPI_COMM_WORLD )
elif(rank==1):
    data = mpi.array.recv( 0, 7, mpi.MPI_COMM_WORLD )
    print data
else:
    pass
mpi.finalize()

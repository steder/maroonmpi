import mpi
rank,size = mpi.init()

import simplempi as sm

rank = sm.getrank()
size = sm.getsize()

rank = sm.getrankfromcomm( mpi.MPI_COMM_WORLD )
size = sm.getsizefromcomm( mpi.MPI_COMM_WORLD )

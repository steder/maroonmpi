"""
gather.py

Quick test of how the 'gather' function works
"""
import mpi
rank,size=mpi.init()

recvlen = mpi.reduce( len(str(rank)),1,mpi.MPI_INT,
                      mpi.MPI_SUM,0,mpi.MPI_COMM_WORLD )
data = mpi.gather( str(rank),len(str(rank)), mpi.MPI_CHAR,
                   recvlen, mpi.MPI_CHAR,
                   0, mpi.MPI_COMM_WORLD )


print type(data)
print data

mpi.finalize()

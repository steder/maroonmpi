"""
allgather.py

Quick test of how the 'allgather' function works
"""
import mpi
rank,size=mpi.init()

data = mpi.allgather( rank, 1, mpi.MPI_INT,
                   1, mpi.MPI_INT, mpi.MPI_COMM_WORLD )


print type(data)
print data

mpi.finalize()

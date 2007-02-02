"""
allgather.py

Quick test of how the 'allgather' function works
"""
import mpi
rank,size=mpi.init()

data = mpi.gather( rank, 1, mpi.MPI_INT,
                   1, mpi.MPI_INT, 0, mpi.MPI_COMM_WORLD )

print type(data)
print data

mpi.finalize()

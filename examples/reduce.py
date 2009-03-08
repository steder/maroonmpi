import sys,mpi
rank,size = mpi.init(len(sys.argv),sys.argv)
sigma = mpi.reduce( 7, 1, mpi.MPI_INT, mpi.MPI_SUM, 0, mpi.MPI_COMM_WORLD )
print "Sum:",sigma 
print "MPI_INT:", mpi.MPI_INT
print "MPI_SUM:", mpi.MPI_SUM
print "MPI_COMM_WORLD:", mpi.MPI_COMM_WORLD
mpi.finalize()

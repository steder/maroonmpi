from mpi import core as mpi

rank,size = mpi.init()

assert size > 1

data = [rank+1]
result = mpi.scan( data, 1, mpi.MPI_INT, mpi.MPI_SUM, mpi.MPI_COMM_WORLD )
print "single element:",result

data = [rank+1] * size
result = mpi.scan( data, size, mpi.MPI_INT, mpi.MPI_SUM, mpi.MPI_COMM_WORLD )
print "sequence:",result

#data = [rank+1] * (rank+1)
#result = mpi.scan( data, rank, mpi.MPI_INT, mpi.MPI_SUM, mpi.MPI_COMM_WORLD )
#print "sequence*rank:",result

mpi.finalize()
